import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


COMPANY = {
    'name': 'KVM ENTERPRISES',
    'address': '#6, Karumai Amman Kovil Street, Vadapalani, Chennai, Tamil Nadu 600026',
    'phone': '9884243950',
    'gstin': '33EFMPS7293G1ZT',
}


def generate_invoice_pdf(invoice):
    """Return a BytesIO buffer containing the invoice PDF."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=15 * mm, bottomMargin=15 * mm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Heading1'],
                                 alignment=TA_CENTER, fontSize=16, spaceAfter=2)
    subtitle_style = ParagraphStyle('sub', parent=styles['Normal'],
                                    alignment=TA_CENTER, fontSize=9, spaceAfter=4)
    normal = styles['Normal']
    bold = ParagraphStyle('bold', parent=normal, fontName='Helvetica-Bold')
    right = ParagraphStyle('right', parent=normal, alignment=TA_RIGHT)

    elements = []

    # ── Header ───────────────────────────────────────────────────────────
    elements.append(Paragraph(COMPANY['name'], title_style))
    elements.append(Paragraph(COMPANY['address'], subtitle_style))
    elements.append(Paragraph(f"Phone: {COMPANY['phone']}  |  GSTIN: {COMPANY['gstin']}", subtitle_style))
    elements.append(Spacer(1, 6 * mm))
    elements.append(Paragraph('<b>TAX INVOICE</b>', ParagraphStyle('inv', parent=styles['Heading2'], alignment=TA_CENTER)))
    elements.append(Spacer(1, 4 * mm))

    # ── Invoice info ─────────────────────────────────────────────────────
    customer = invoice.customer
    inv_date = invoice.invoice_date.strftime('%d-%m-%Y') if invoice.invoice_date else ''

    info_data = [
        [Paragraph(f"<b>Invoice #:</b> {invoice.invoice_number}", normal),
         Paragraph(f"<b>Date:</b> {inv_date}", right)],
        [Paragraph(f"<b>Bill To:</b> {customer.name if customer else ''}", normal),
         Paragraph(f"<b>Status:</b> {invoice.status.upper()}", right)],
    ]
    if customer:
        addr_parts = [p for p in [customer.address, customer.city, customer.state, customer.pincode] if p]
        info_data.append([Paragraph(', '.join(addr_parts), normal), Paragraph('', normal)])
        if customer.gstin:
            info_data.append([Paragraph(f"<b>GSTIN:</b> {customer.gstin}", normal), Paragraph('', normal)])
        if customer.phone:
            info_data.append([Paragraph(f"<b>Phone:</b> {customer.phone}", normal), Paragraph('', normal)])

    info_table = Table(info_data, colWidths=[doc.width * 0.6, doc.width * 0.4])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 6 * mm))

    # ── Items table ──────────────────────────────────────────────────────
    header = ['#', 'Product', 'HSN', 'Qty', 'Rate (₹)', 'Disc %', 'Taxable (₹)', 'CGST (₹)', 'SGST (₹)', 'Total (₹)']
    table_data = [header]

    for idx, item in enumerate(invoice.items, 1):
        table_data.append([
            str(idx),
            item.product_name or '',
            item.hsn_code or '',
            str(item.quantity),
            f"{item.unit_price:,.2f}",
            f"{item.discount_percent:.1f}",
            f"{item.taxable_amount:,.2f}",
            f"{item.cgst_amount:,.2f}",
            f"{item.sgst_amount:,.2f}",
            f"{item.total:,.2f}",
        ])

    col_widths = [doc.width * w for w in [0.04, 0.22, 0.07, 0.06, 0.1, 0.07, 0.11, 0.1, 0.1, 0.13]]
    items_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 6 * mm))

    # ── Totals ───────────────────────────────────────────────────────────
    totals_data = [
        ['', '', 'Subtotal:', f"₹ {invoice.subtotal:,.2f}"],
        ['', '', 'CGST (9%):', f"₹ {invoice.cgst_total:,.2f}"],
        ['', '', 'SGST (9%):', f"₹ {invoice.sgst_total:,.2f}"],
        ['', '', 'Grand Total:', f"₹ {invoice.grand_total:,.2f}"],
    ]
    totals_table = Table(totals_data,
                         colWidths=[doc.width * 0.35, doc.width * 0.25, doc.width * 0.2, doc.width * 0.2])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('LINEABOVE', (2, -1), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 10 * mm))

    # ── Notes ────────────────────────────────────────────────────────────
    if invoice.notes:
        elements.append(Paragraph(f"<b>Notes:</b> {invoice.notes}", normal))
        elements.append(Spacer(1, 4 * mm))

    # ── Terms ────────────────────────────────────────────────────────────
    elements.append(Paragraph('<b>Terms & Conditions:</b>', bold))
    terms = [
        '1. Goods once sold will not be taken back.',
        '2. Payment due within 30 days of invoice date.',
        '3. Subject to Chennai jurisdiction.',
    ]
    for t in terms:
        elements.append(Paragraph(t, ParagraphStyle('term', parent=normal, fontSize=8)))
    elements.append(Spacer(1, 12 * mm))

    # ── Signature ────────────────────────────────────────────────────────
    sig_data = [['', Paragraph('<b>For KVM ENTERPRISES</b>', right)],
                ['', ''],
                ['', Paragraph('Authorized Signatory', right)]]
    sig_table = Table(sig_data, colWidths=[doc.width * 0.6, doc.width * 0.4])
    elements.append(sig_table)

    doc.build(elements)
    buf.seek(0)
    return buf
