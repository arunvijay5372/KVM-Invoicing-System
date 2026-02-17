from flask import Blueprint, render_template
from flask_login import login_required

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
@login_required
def index():
    return render_template('index.html')


@web_bp.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html')


@web_bp.route('/invoices')
@login_required
def invoices():
    return render_template('invoices.html')


@web_bp.route('/invoices/new')
@login_required
def new_invoice():
    return render_template('new_invoice.html')


@web_bp.route('/invoices/<invoice_id>')
@login_required
def view_invoice(invoice_id):
    return render_template('view_invoice.html', invoice_id=invoice_id)


@web_bp.route('/brands')
@login_required
def brands():
    return render_template('brands.html')


@web_bp.route('/customers')
@login_required
def customers():
    return render_template('customers.html')
