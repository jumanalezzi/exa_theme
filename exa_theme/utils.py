import io
import base64
import frappe

def get_tlv(tag, value):
    tag_bytes = bytes([tag])
    val_bytes = str(value or '').encode('utf-8')
    len_bytes = bytes([len(val_bytes)])
    return tag_bytes + len_bytes + val_bytes

def get_zatca_qr_code(doc):
    """Generate ZATCA compliant Phase 1 & 2 TLV QR Code as a base64 PNG data URI"""
    try:
        # Imported here: this module is loaded as a jinja hook for every web page,
        # so a missing qrcode package must only blank the QR code, not break the site
        import qrcode

        company_name = getattr(doc, 'company', '') or frappe.defaults.get_user_default("Company") or ""
        company_tax_id = frappe.db.get_value('Company', company_name, 'tax_id') or getattr(doc, 'company_tax_id', '') or ''
        
        # Build ISO timestamp (YYYY-MM-DDTHH:MM:SSZ)
        date_str = str(getattr(doc, 'posting_date', '') or '')
        time_str = str(getattr(doc, 'posting_time', '') or '')
        if time_str and len(time_str.split('.')) > 1:
            time_str = time_str.split('.')[0]
        timestamp = f"{date_str}T{time_str}Z" if date_str and time_str else (f"{date_str}T00:00:00Z" if date_str else "")
        
        total = float(getattr(doc, 'rounded_total', 0) or getattr(doc, 'grand_total', 0) or 0)
        tax = float(getattr(doc, 'total_taxes_and_charges', 0) or 0)

        tlv = (
            get_tlv(1, company_name) +
            get_tlv(2, company_tax_id) +
            get_tlv(3, timestamp) +
            get_tlv(4, f"{total:.2f}") +
            get_tlv(5, f"{tax:.2f}")
        )
        b64_tlv = base64.b64encode(tlv).decode('utf-8')
        
        qr = qrcode.QRCode(version=1, box_size=3, border=1)
        qr.add_data(b64_tlv)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        img_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_b64}"
    except Exception as e:
        return ""
