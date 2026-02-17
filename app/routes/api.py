import csv
import io
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required
from app import db
from app.models import (
    Brand, Variant, Size, Product, Inventory,
    Customer, Invoice, InvoiceItem,
)
from app.utils.pdf_generator import generate_invoice_pdf

api_bp = Blueprint('api', __name__)


# ─────────────────────────── Brands ──────────────────────────────────────────

@api_bp.route('/brands', methods=['GET'])
@login_required
def get_brands():
    brands = Brand.query.all()
    return jsonify([b.to_dict() for b in brands])


@api_bp.route('/brands', methods=['POST'])
@login_required
def create_brand():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('code'):
        return jsonify({'error': 'Name and code are required'}), 400

    if Brand.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Brand already exists'}), 409

    brand = Brand(
        name=data['name'],
        code=data['code'].upper(),
        description=data.get('description', ''),
    )
    db.session.add(brand)
    db.session.commit()

    # Auto-create products for this brand
    _auto_create_products(brand)

    return jsonify(brand.to_dict()), 201


@api_bp.route('/brands/<brand_id>', methods=['GET'])
@login_required
def get_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    return jsonify(brand.to_dict())


@api_bp.route('/brands/<brand_id>', methods=['PUT'])
@login_required
def update_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    data = request.get_json()
    if data.get('name'):
        brand.name = data['name']
    if data.get('code'):
        brand.code = data['code'].upper()
    if 'description' in data:
        brand.description = data['description']
    if 'is_active' in data:
        brand.is_active = data['is_active']
    db.session.commit()
    return jsonify(brand.to_dict())


@api_bp.route('/brands/<brand_id>', methods=['DELETE'])
@login_required
def delete_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    db.session.delete(brand)
    db.session.commit()
    return jsonify({'message': 'Brand deleted'})


# ─────────────────────────── Products ────────────────────────────────────────

@api_bp.route('/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.filter_by(is_active=True).all()
    return jsonify([p.to_dict() for p in products])


@api_bp.route('/products', methods=['POST'])
@login_required
def create_product():
    data = request.get_json()
    required = ['name', 'brand_id', 'variant_id', 'size_id']
    if not data or not all(data.get(k) for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    product = Product(
        name=data['name'],
        brand_id=data['brand_id'],
        variant_id=data['variant_id'],
        size_id=data['size_id'],
        hsn_code=data.get('hsn_code', '3917'),
        unit=data.get('unit', 'Nos'),
        price=float(data.get('price', 0)),
    )
    db.session.add(product)
    db.session.flush()

    inv = Inventory(product_id=product.id, quantity=0, reorder_level=10)
    db.session.add(inv)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@api_bp.route('/products/<product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@api_bp.route('/products/<product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    for key in ('name', 'hsn_code', 'unit', 'is_active'):
        if key in data:
            setattr(product, key, data[key])
    if 'price' in data:
        product.price = float(data['price'])
    db.session.commit()
    return jsonify(product.to_dict())


# ─────────────────────────── Inventory ───────────────────────────────────────

@api_bp.route('/inventory', methods=['GET'])
@login_required
def get_inventory():
    items = db.session.query(Inventory, Product).join(Product).all()
    result = []
    for inv, prod in items:
        d = inv.to_dict()
        d['product'] = prod.to_dict()
        result.append(d)
    return jsonify(result)


@api_bp.route('/inventory/<product_id>', methods=['GET'])
@login_required
def get_inventory_item(product_id):
    inv = Inventory.query.filter_by(product_id=product_id).first_or_404()
    return jsonify(inv.to_dict())


@api_bp.route('/inventory/<product_id>', methods=['PUT'])
@login_required
def update_inventory(product_id):
    try:
        inv = Inventory.query.filter_by(product_id=product_id).first()
        if not inv:
            inv = Inventory(product_id=product_id, quantity=0)
            db.session.add(inv)

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        if 'quantity' in data:
            inv.quantity = int(data['quantity'])
        if 'reorder_level' in data:
            inv.reorder_level = int(data['reorder_level'])
        db.session.commit()
        return jsonify(inv.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/inventory/upload', methods=['POST'])
@login_required
def upload_inventory():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are accepted'}), 400

    try:
        stream = io.StringIO(file.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        updated = 0
        for row in reader:
            pid = row.get('product_id', '').strip()
            qty = row.get('quantity', '0').strip()
            if not pid:
                continue
            inv = Inventory.query.filter_by(product_id=pid).first()
            if inv:
                inv.quantity = int(qty)
                updated += 1
        db.session.commit()
        return jsonify({'message': f'{updated} items updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ─────────────────────────── Customers ───────────────────────────────────────

@api_bp.route('/customers', methods=['GET'])
@login_required
def get_customers():
    custs = Customer.query.order_by(Customer.name).all()
    return jsonify([c.to_dict() for c in custs])


@api_bp.route('/customers', methods=['POST'])
@login_required
def create_customer():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Customer name is required'}), 400

    customer = Customer(
        name=data['name'],
        gstin=data.get('gstin', ''),
        phone=data.get('phone', ''),
        email=data.get('email', ''),
        address=data.get('address', ''),
        city=data.get('city', ''),
        state=data.get('state', ''),
        pincode=data.get('pincode', ''),
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


@api_bp.route('/customers/<customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    for key in ('name', 'gstin', 'phone', 'email', 'address', 'city', 'state', 'pincode'):
        if key in data:
            setattr(customer, key, data[key])
    db.session.commit()
    return jsonify(customer.to_dict())


@api_bp.route('/customers/<customer_id>', methods=['DELETE'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'})


# ─────────────────────────── Invoices ────────────────────────────────────────

@api_bp.route('/invoices', methods=['GET'])
@login_required
def get_invoices():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return jsonify([inv.to_dict() for inv in invoices])


@api_bp.route('/invoices', methods=['POST'])
@login_required
def create_invoice():
    data = request.get_json()
    if not data or not data.get('customer_id') or not data.get('items'):
        return jsonify({'error': 'Customer and items are required'}), 400

    # Generate invoice number
    count = Invoice.query.count() + 1
    inv_number = f"KVM-{datetime.utcnow().strftime('%Y%m%d')}-{count:04d}"

    invoice = Invoice(
        invoice_number=inv_number,
        customer_id=data['customer_id'],
        invoice_date=datetime.utcnow(),
        notes=data.get('notes', ''),
        status='draft',
    )
    db.session.add(invoice)
    db.session.flush()

    subtotal = 0
    cgst_total = 0
    sgst_total = 0

    for item_data in data['items']:
        qty = int(item_data.get('quantity', 1))
        price = float(item_data.get('unit_price', 0))
        discount_pct = float(item_data.get('discount_percent', 0))

        line_subtotal = qty * price
        discount_amt = line_subtotal * discount_pct / 100
        taxable = line_subtotal - discount_amt
        cgst = round(taxable * 9 / 100, 2)
        sgst = round(taxable * 9 / 100, 2)
        total = round(taxable + cgst + sgst, 2)

        product = Product.query.get(item_data['product_id'])
        product_name = product.name if product else item_data.get('product_name', '')

        item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item_data['product_id'],
            product_name=product_name,
            hsn_code=item_data.get('hsn_code', '3917'),
            quantity=qty,
            unit_price=price,
            discount_percent=discount_pct,
            taxable_amount=round(taxable, 2),
            cgst_amount=cgst,
            sgst_amount=sgst,
            total=total,
        )
        db.session.add(item)

        subtotal += round(taxable, 2)
        cgst_total += cgst
        sgst_total += sgst

    invoice.subtotal = round(subtotal, 2)
    invoice.cgst_total = round(cgst_total, 2)
    invoice.sgst_total = round(sgst_total, 2)
    invoice.grand_total = round(subtotal + cgst_total + sgst_total, 2)

    db.session.commit()
    return jsonify(invoice.to_dict()), 201


@api_bp.route('/invoices/<invoice_id>', methods=['GET'])
@login_required
def get_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return jsonify(invoice.to_dict())


@api_bp.route('/invoices/<invoice_id>/pdf', methods=['GET'])
@login_required
def get_invoice_pdf(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    pdf_buffer = generate_invoice_pdf(invoice)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'{invoice.invoice_number}.pdf',
    )


@api_bp.route('/invoices/<invoice_id>', methods=['PUT'])
@login_required
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json()
    if 'status' in data:
        invoice.status = data['status']
    if 'notes' in data:
        invoice.notes = data['notes']
    db.session.commit()
    return jsonify(invoice.to_dict())


# ─────────────────────────── Dashboard ───────────────────────────────────────

@api_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    total_products = Product.query.filter_by(is_active=True).count()
    active_brands = Brand.query.filter_by(is_active=True).count()

    # inventory value
    inv_items = db.session.query(Inventory, Product).join(Product).all()
    total_value = sum(i.quantity * p.price for i, p in inv_items)

    low_stock = Inventory.query.filter(Inventory.quantity <= Inventory.reorder_level).count()

    today = datetime.utcnow().date()
    today_invoices = Invoice.query.filter(
        db.func.date(Invoice.invoice_date) == today
    ).count()

    recent = Invoice.query.order_by(Invoice.created_at.desc()).limit(5).all()

    return jsonify({
        'total_products': total_products,
        'active_brands': active_brands,
        'total_inventory_value': round(total_value, 2),
        'low_stock_count': low_stock,
        'today_invoices': today_invoices,
        'recent_invoices': [r.to_dict() for r in recent],
    })


# ─────────────────────────── Helpers ─────────────────────────────────────────

def _auto_create_products(brand):
    """When a new brand is added, auto-create products for all variant+size combos."""
    variants = Variant.query.all()
    sizes = Size.query.all()
    for v in variants:
        for s in sizes:
            name = f"{brand.name} {v.name} {int(s.size_inches)}\" Pipe"
            p = Product(
                name=name,
                brand_id=brand.id,
                variant_id=v.id,
                size_id=s.id,
            )
            db.session.add(p)
            db.session.flush()
            inv = Inventory(product_id=p.id, quantity=0, reorder_level=10)
            db.session.add(inv)
    db.session.commit()
