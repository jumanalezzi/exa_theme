import frappe
from exa_theme.branding import get_madar_branding
from exa_theme.license_core import verify_app_license

@frappe.whitelist()
def initialize_madar_settings():
    # verify_app_license() # <-- الصافرة هنا
    doctype_name = "Madar Settings"
    
    # 1. إنشاء أو تحديث هيكل الـ DocType (الجدول في قاعدة البيانات)
    if frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc("DocType", doctype_name)
        needs_save = False
        existing_fields = [f.fieldname for f in doc.fields]
        
        if "ai_api_url" not in existing_fields:
            doc.append("fields", {
                "fieldname": "ai_api_url",
                "label": "رابط الذكاء الاصطناعي (AI API URL)",
                "fieldtype": "Data",
                "description": "مثال: http://localhost:11434/v1"
            })
            needs_save = True
            
        if "ai_model_name" not in existing_fields:
            doc.append("fields", {
                "fieldname": "ai_model_name",
                "label": "اسم نموذج الذكاء الاصطناعي (Model Name)",
                "fieldtype": "Data",
                "description": "مثال: llama3"
            })
            needs_save = True
            
        if "gemini_api_key" not in existing_fields:
            doc.append("fields", {
                "fieldname": "gemini_api_key",
                "label": "Gemini API Key",
                "fieldtype": "Password",
                "description": "إذا وضعت مفتاحاً هنا، سيتجاهل النظام الذكاء الاصطناعي المحلي ويستخدم Gemini للسرعة."
            })
            needs_save = True
            
        if needs_save:
            doc.save(ignore_permissions=True)
            
    if not frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": doctype_name,
            "module": "Madar",  # مطابقة اسم الموديول الفعلي
            "custom": 1,
            "issingle": 1,      # يجعله صفحة إعدادات واحدة فقط
            "fields": [
                {
                    "fieldname": "app_name_ar",
                    "label": "App Name (Arabic)",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "fieldname": "app_name_en",
                    "label": "App Name (English)",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "fieldname": "light_logo",
                    "label": "Logo (Light)",
                    "fieldtype": "Attach Image",
                    "description":"يستخدم مع الثيمات الداكنة (يجب أن يكون أبيض أو مفرغ PNG)",
                    "reqd": 1
                },
                {
                    "fieldname": "dark_logo",
                    "label": "Logo (Dark)",
                    "fieldtype": "Attach Image",
                    "description": "يستخدم مع الثيمات الفاتحة (يفضل أن يكون ملوناً أو غامقاً)" ,
                    "reqd": 1
                },
                {
                    "fieldname": "favicon",
                    "label": "Favicon",
                    "fieldtype": "Attach Image"
                },
                {
                    "fieldname": "ai_api_url",
                    "label": "رابط الذكاء الاصطناعي (AI API URL)",
                    "fieldtype": "Data",
                    "description": "مثال: http://localhost:11434/v1"
                },
                {
                    "fieldname": "ai_model_name",
                    "label": "اسم نموذج الذكاء الاصطناعي (Model Name)",
                    "fieldtype": "Data",
                    "description": "مثال: llama3"
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"تم إنشاء هيكل الـ DocType: {doctype_name}")

    # 2. إنشاء الإعدادات الافتراضية إذا لم تكن موجودة أو تعبئة الحقول الفارغة
    if not frappe.db.exists(doctype_name, doctype_name):
        settings_doc = frappe.get_doc({"doctype": doctype_name})
    else:
        settings_doc = frappe.get_doc(doctype_name, doctype_name)
        
    needs_update = False
    
    # الاسم والشعارات تأتي من exa_app (مصدر واحد للعلامة التجارية)
    for fieldname, value in get_madar_branding().items():
        if settings_doc.get(fieldname) != value:
            settings_doc.set(fieldname, value)
            needs_update = True

    if needs_update or settings_doc.is_new():
        settings_doc.flags.ignore_permissions = True
        if settings_doc.is_new():
            settings_doc.insert()
        else:
            settings_doc.save()
        frappe.db.commit()
        print("تم تحديث/إنشاء الإعدادات الافتراضية للنظام (الشعارات والأسماء).")

    return "Initialization completed successfully."
