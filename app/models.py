import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


def gen_uuid():
    return str(uuid.uuid4())


# ──────────────────────────────── User (Auth) ────────────────────────────────

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active_user,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# ──────────────────────────────── Brand ──────────────────────────────────────

class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(255), default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='brand', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# ──────────────────────────────── Variant ────────────────────────────────────

class Variant(db.Model):
    __tablename__ = 'variants'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(50), unique=True, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)

    products = db.relationship('Product', backref='variant', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'weight_kg': self.weight_kg,
        }


# ──────────────────────────────── Size ───────────────────────────────────────

class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    size_inches = db.Column(db.Float, unique=True, nullable=False)

    products = db.relationship('Product', backref='size', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'size_inches': self.size_inches,
        }


# ──────────────────────────────── Product ────────────────────────────────────

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(200), nullable=False)
    brand_id = db.Column(db.String(36), db.ForeignKey('brands.id'), nullable=False)
    variant_id = db.Column(db.String(36), db.ForeignKey('variants.id'), nullable=False)
    size_id = db.Column(db.String(36), db.ForeignKey('sizes.id'), nullable=False)
    hsn_code = db.Column(db.String(20), default='3917')
    unit = db.Column(db.String(20), default='Nos')
    price = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    inventory = db.relationship('Inventory', backref='product', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand_id': self.brand_id,
            'variant_id': self.variant_id,
            'size_id': self.size_id,
            'brand': self.brand.to_dict() if self.brand else None,
            'variant': self.variant.to_dict() if self.variant else None,
            'size': self.size.to_dict() if self.size else None,
            'hsn_code': self.hsn_code,
            'unit': self.unit,
            'price': self.price,
            'is_active': self.is_active,
            'inventory': self.inventory.to_dict() if self.inventory else None,
        }


# ──────────────────────────────── Inventory ──────────────────────────────────

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'reorder_level': self.reorder_level,
        }


# ──────────────────────────────── Customer ───────────────────────────────────

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(200), nullable=False)
    gstin = db.Column(db.String(20), default='')
    phone = db.Column(db.String(20), default='')
    email = db.Column(db.String(120), default='')
    address = db.Column(db.Text, default='')
    city = db.Column(db.String(100), default='')
    state = db.Column(db.String(100), default='')
    pincode = db.Column(db.String(10), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    invoices = db.relationship('Invoice', backref='customer', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gstin': self.gstin,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# ──────────────────────────────── Invoice ────────────────────────────────────

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.String(36), db.ForeignKey('customers.id'), nullable=False)
    invoice_date = db.Column(db.DateTime, default=datetime.utcnow)
    subtotal = db.Column(db.Float, default=0.0)
    cgst_total = db.Column(db.Float, default=0.0)
    sgst_total = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='draft')  # draft, sent, paid, cancelled
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_id': self.customer_id,
            'customer': self.customer.to_dict() if self.customer else None,
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'subtotal': self.subtotal,
            'cgst_total': self.cgst_total,
            'sgst_total': self.sgst_total,
            'grand_total': self.grand_total,
            'status': self.status,
            'notes': self.notes,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# ──────────────────────────────── InvoiceItem ────────────────────────────────

class InvoiceItem(db.Model):
    __tablename__ = 'invoice_items'

    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    invoice_id = db.Column(db.String(36), db.ForeignKey('invoices.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200), default='')
    hsn_code = db.Column(db.String(20), default='3917')
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, default=0.0)
    discount_percent = db.Column(db.Float, default=0.0)
    taxable_amount = db.Column(db.Float, default=0.0)
    cgst_amount = db.Column(db.Float, default=0.0)
    sgst_amount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)

    product = db.relationship('Product', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'hsn_code': self.hsn_code,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'discount_percent': self.discount_percent,
            'taxable_amount': self.taxable_amount,
            'cgst_amount': self.cgst_amount,
            'sgst_amount': self.sgst_amount,
            'total': self.total,
        }
