import frappe
from admin.license_core import verify_app_license

# ==========================================
# 1. مصفوفة الخطوط الافتراضية
# ==========================================
DEFAULT_FONTS = [
    {
        "font_name": "Cairo",
        "font_name_ar": "كايرو (القاهرة)",
        "font_name_en": "Cairo",
        "font_family": "'Cairo', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap",
        "is_default": 1
    },
    {
        "font_name": "Tajawal",
        "font_name_ar": "تجوال (رسمي)",
        "font_name_en": "Tajawal",
        "font_family": "'Tajawal', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap",
        "is_default": 0
    },
    {
        "font_name": "Almarai",
        "font_name_ar": "المراعي (عصري)",
        "font_name_en": "Almarai",
        "font_family": "'Almarai', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Almarai:wght@400;700&display=swap",
        "is_default": 0
    }
]

# ==========================================
# 2. كود التحقق والإنشاء (Setup Engine)
# ==========================================
@frappe.whitelist()
def initialize_fonts():
    # verify_app_license() # <-- الصافرة هنا
    doctype_name = "Madar Font"
    
    # 1. التحقق من وجود الـ DocType، وإذا لم يكن موجوداً نقوم بإنشائه
    if not frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": doctype_name,
            "module": "Madar",  # مطابق لتطبيقك
            "custom": 1,
            "autoname": "field:font_name",
            "fields": [
                {"fieldname": "font_name", "label": "Font ID", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "font_name_ar", "label": "Font Name (AR)", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "font_name_en", "label": "Font Name (EN)", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "font_family", "label": "CSS Font Family", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "font_url", "label": "Google Font URL", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "is_default", "label": "Is Default", "fieldtype": "Check", "default": 0}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "All", "read": 1, "write": 0, "create": 0, "delete": 0}
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"تم إنشاء DocType: {doctype_name} بنجاح.")

    # 2. التحقق من وجود الخطوط الافتراضية وحفظها
    for font in DEFAULT_FONTS:
        if not frappe.db.exists(doctype_name, font.get("font_name")):
            new_font = frappe.get_doc({
                "doctype": doctype_name,
                "font_name": font.get("font_name"),
                "font_name_ar": font.get("font_name_ar"),
                "font_name_en": font.get("font_name_en"),
                "font_family": font.get("font_family"),
                "font_url": font.get("font_url"),
                "is_default": font.get("is_default")
            })
            new_font.insert(ignore_permissions=True)
            print(f"تمت إضافة الخط الافتراضي: {font.get('font_name')}")
    
    frappe.db.commit()
    return "Fonts initialization completed successfully."