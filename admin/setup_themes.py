import frappe
import json
from admin.license_core import verify_app_license

# ==========================================
# 1. مصفوفة الثيمات الافتراضية (الفاتح والداكن)
# ==========================================
       
DEFAULT_THEMES = [
    {
        "theme_id": "default_light",
        "theme_mode": "Light",
        "theme_name_ar": "الفاتح الافتراضي",
        "theme_name_en": "Default Light",
        "theme_desc_ar": "الثيم الفاتح الافتراضي للنظام",
        "theme_desc_en": "The default light theme for the system",
        "typography": {
            "font_name": "Cairo",
            "font_family": "'Cairo', sans-serif",
            "font_url": "https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap"
        },
        "colors": {
            "palette": {
                "primary": "#0d6efd",
                "secondary": "#6c757d",
                "success": "#198754",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#0dcaf0"
            },
            "header": {
                "bg": "#ffffff", "text": "#212529",
                "buttons": {"bg": "transparent", "text": "#6c757d", "hover_bg": "#f8f9fa", "hover_text": "#0d6efd"}
            },
            "sidebar": {
                "level_1": {"bg": "#ffffff", "text": "#495057", "hover_bg": "#f8f9fa", "hover_text": "#0d6efd", "active_bg": "#e9ecef", "active_text": "#0d6efd"},
                "level_2": {"bg": "#fafafa", "text": "#6c757d", "hover_bg": "#f1f3f5", "hover_text": "#0d6efd", "active_bg": "#e9ecef", "active_text": "#0d6efd"},
                "level_3": {"bg": "#f4f6f9", "text": "#868e96", "hover_bg": "#e9ecef", "hover_text": "#0d6efd", "active_bg": "#e9ecef", "active_text": "#0d6efd"}
            },
            "footer": {
                "bg": "#f8f9fa",
                "text": "#6c757d",
                "links": {"text": "#0d6efd", "hover_text": "#0a58ca"}
            },
            "content": {
                "page_bg": "#f4f6f9", 
                "surface_bg": "#ffffff",
                "text_primary": "#212529",
                "text_muted": "#6c757d", 
                "border_color": "#dee2e6",
                "input_bg": "#ffffff"
            }
        }
    },
    {
        "theme_id": "default_dark",
        "theme_mode": "Dark",
        "theme_name_ar": "الداكن الافتراضي",
        "theme_name_en": "Default Dark",
        "theme_desc_ar": "الثيم الداكن المريح للعين",
        "theme_desc_en": "The default eye-friendly dark theme",
        "typography": {
            "font_name": "Cairo",
            "font_family": "'Cairo', sans-serif",
            "font_url": "https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap"
        },
        "colors": {
            "palette": {
                "primary": "#009ef7",
                "secondary": "#a1a5b7",
                "success": "#50cd89",
                "danger": "#f1416c",
                "warning": "#ffc700",
                "info": "#7239ea"
            },
            "header": {
                "bg": "#151521", "text": "#ffffff",
                "buttons": {"bg": "transparent", "text": "#a1a5b7", "hover_bg": "#2b2b40", "hover_text": "#009ef7"}
            },
            "sidebar": {
                "level_1": {"bg": "#151521", "text": "#a1a5b7", "hover_bg": "#1e1e2d", "hover_text": "#009ef7", "active_bg": "#2b2b40", "active_text": "#009ef7"},
                "level_2": {"bg": "#11111a", "text": "#808290", "hover_bg": "#1e1e2d", "hover_text": "#009ef7", "active_bg": "#2b2b40", "active_text": "#009ef7"},
                "level_3": {"bg": "#0d0d14", "text": "#6c6e7a", "hover_bg": "#1e1e2d", "hover_text": "#009ef7", "active_bg": "#2b2b40", "active_text": "#009ef7"}
            },
            "footer": {
                "bg": "#151521",
                "text": "#a1a5b7",
                "links": {"text": "#009ef7", "hover_text": "#50cd89"}
            },
            "content": {
                "page_bg": "#151521", 
                "surface_bg": "#1e1e2d",
                "text_primary": "#ffffff",
                "text_muted": "#a1a5b7", 
                "border_color": "#323248",
                "input_bg": "#2b2b40"
            }
        }
    },
    {
        "theme_id": "ocean_blue",
        "theme_mode": "Light",
        "theme_name_ar": "المحيط الأزرق المنعش",
        "theme_name_en": "Ocean Blue",
        "theme_desc_ar": "ثيم فاتح ممتد من زرقة البحر الصافية",
        "theme_desc_en": "Fresh and vivid ocean blue light theme",
        "typography": {
            "font_name": "Tajawal",
            "font_family": "'Tajawal', sans-serif",
            "font_url": "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap"
        },
        "colors": {
            "palette": {
                "primary": "#1565c0",
                "secondary": "#546e7a",
                "success": "#2e7d32",
                "danger": "#c62828",
                "warning": "#f57f17",
                "info": "#0277bd"
            },
            "header": {
                "bg": "#0b3d91", "text": "#ffffff", 
                "buttons": {"bg": "transparent", "text": "#bbdefb", "hover_bg": "#1565c0", "hover_text": "#ffffff"}
            },
            "sidebar": {
                "level_1": {"bg": "#f0f6fc", "text": "#0b3d91", "hover_bg": "#e1edf8", "hover_text": "#1565c0", "active_bg": "#d2e3f4", "active_text": "#0b3d91"},
                "level_2": {"bg": "#e6eff9", "text": "#1565c0", "hover_bg": "#d2e3f4", "hover_text": "#0b3d91", "active_bg": "#cbdfea", "active_text": "#0b3d91"},
                "level_3": {"bg": "#dce8f5", "text": "#4a5568", "hover_bg": "#cbdfea", "hover_text": "#0b3d91", "active_bg": "#cbdfea", "active_text": "#0b3d91"}
            },
            "footer": {
                "bg": "#e1edf8",
                "text": "#546e7a",
                "links": {"text": "#1565c0", "hover_text": "#0b3d91"}
            },
            "content": {
                "page_bg": "#e1edf8", 
                "surface_bg": "#ffffff",
                "text_primary": "#0b3d91",
                "text_muted": "#546e7a", 
                "border_color": "#bbdefb",
                "input_bg": "#ffffff"
            }
        }
    },
    {
        "theme_id": "desert_gold",
        "theme_mode": "Light",
        "theme_name_ar": "الصحراء الدافئة الملوّن",
        "theme_name_en": "Desert Gold",
        "theme_desc_ar": "ثيم دافئ فاخر بألوان رمل الصحراء والكاكاو والنحاس",
        "theme_desc_en": "Luxury warm theme with sand, chocolate and copper accents",
        "typography": {
            "font_name": "Almarai",
            "font_family": "'Almarai', sans-serif",
            "font_url": "https://fonts.googleapis.com/css2?family=Almarai:wght@400;700&display=swap"
        },
        "colors": {
            "palette": {
                "primary": "#d84315",
                "secondary": "#795548",
                "success": "#2e7d32",
                "danger": "#c62828",
                "warning": "#ffb300",
                "info": "#00838f"
            },
            "header": {
                "bg": "#f5e6d3", "text": "#3e2723", 
                "buttons": {"bg": "transparent", "text": "#795548", "hover_bg": "#dfc3a3", "hover_text": "#d84315"}
            },
            "sidebar": {
                "level_1": {"bg": "#fff8f0", "text": "#3e2723", "hover_bg": "#fdf1e1", "hover_text": "#d84315", "active_bg": "#e8d1b5", "active_text": "#d84315"},
                "level_2": {"bg": "#fbf2e6", "text": "#5d4037", "hover_bg": "#e8d1b5", "hover_text": "#d84315", "active_bg": "#dfc3a3", "active_text": "#d84315"},
                "level_3": {"bg": "#f5e6d3", "text": "#795548", "hover_bg": "#dfc3a3", "hover_text": "#d84315", "active_bg": "#dfc3a3", "active_text": "#d84315"}
            },
            "footer": {
                "bg": "#fdf1e1",
                "text": "#795548",
                "links": {"text": "#d84315", "hover_text": "#ffb300"}
            },
            "content": {
                "page_bg": "#fbf2e6", 
                "surface_bg": "#ffffff",
                "text_primary": "#3e2723",
                "text_muted": "#795548", 
                "border_color": "#e8d1b5",
                "input_bg": "#ffffff"
            }
        }
    },
    {
        "theme_id": "fuchsia_blossom",
        "theme_mode": "Light",
        "theme_name_ar": "زهرة الفوشيا",
        "theme_name_en": "Fuchsia Blossom",
        "theme_desc_ar": "ثيم أنيق وجذاب يعتمد على تدرجات الفوشيا والوردي",
        "theme_desc_en": "Elegant and attractive theme based on fuchsia and pink gradients",
        "typography": {
            "font_name": "Cairo",
            "font_family": "'Cairo', sans-serif",
            "font_url": "https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap"
        },
        "colors": {
            "palette": {
                "primary": "#d81b60",
                "secondary": "#880e4f",
                "success": "#388e3c",
                "danger": "#d32f2f",
                "warning": "#fbc02d",
                "info": "#0288d1"
            },
            "header": {
                "bg": "#d81b60", "text": "#ffffff",
                "buttons": {"bg": "transparent", "text": "#f8bbd0", "hover_bg": "#ad1457", "hover_text": "#ffffff"}
            },
            "sidebar": {
                "level_1": {"bg": "#fff0f5", "text": "#880e4f", "hover_bg": "#fce4ec", "hover_text": "#d81b60", "active_bg": "#f8bbd0", "active_text": "#d81b60"},
                "level_2": {"bg": "#fcf5f8", "text": "#ad1457", "hover_bg": "#f8bbd0", "hover_text": "#d81b60", "active_bg": "#f48fb1", "active_text": "#880e4f"},
                "level_3": {"bg": "#fafafa", "text": "#c2185b", "hover_bg": "#f8bbd0", "hover_text": "#d81b60", "active_bg": "#f48fb1", "active_text": "#880e4f"}
            },
            "footer": {
                "bg": "#fce4ec",
                "text": "#880e4f",
                "links": {"text": "#d81b60", "hover_text": "#ad1457"}
            },
            "content": {
                "page_bg": "#fdf8fa", 
                "surface_bg": "#ffffff",
                "text_primary": "#4a148c",
                "text_muted": "#880e4f", 
                "border_color": "#f8bbd0",
                "input_bg": "#ffffff"
            }
        }
    },
    {
        "theme_id": "saudi_green",
        "theme_mode": "Light",
        "theme_name_ar": "الأخضر السعودي",
        "theme_name_en": "Saudi Green",
        "theme_desc_ar": "ثيم رسمي مستوحى من لون علم المملكة العربية السعودية",
        "theme_desc_en": "Official theme inspired by the Saudi Arabia flag color",
        "typography": {
            "font_name": "Tajawal",
            "font_family": "'Tajawal', sans-serif",
            "font_url": "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap"
        },
        "colors": {
            "palette": {
                "primary": "#006c35",
                "secondary": "#2e4036",
                "success": "#009c4d",
                "danger": "#c62828",
                "warning": "#f57f17",
                "info": "#0277bd"
            },
            "header": {
                "bg": "#006c35", "text": "#ffffff",
                "buttons": {"bg": "transparent", "text": "#a8e6cf", "hover_bg": "#004e26", "hover_text": "#ffffff"}
            },
            "sidebar": {
                "level_1": {"bg": "#f0f7f3", "text": "#004e26", "hover_bg": "#e1f0e8", "hover_text": "#006c35", "active_bg": "#c8e6d6", "active_text": "#004e26"},
                "level_2": {"bg": "#f8fbf9", "text": "#006c35", "hover_bg": "#dcf0e3", "hover_text": "#004e26", "active_bg": "#c8e6d6", "active_text": "#004e26"},
                "level_3": {"bg": "#ffffff", "text": "#2e4036", "hover_bg": "#dcf0e3", "hover_text": "#004e26", "active_bg": "#c8e6d6", "active_text": "#004e26"}
            },
            "footer": {
                "bg": "#e1f0e8",
                "text": "#2e4036",
                "links": {"text": "#006c35", "hover_text": "#004e26"}
            },
            "content": {
                "page_bg": "#f4f9f6", 
                "surface_bg": "#ffffff",
                "text_primary": "#1b2a22",
                "text_muted": "#2e4036", 
                "border_color": "#c8e6d6",
                "input_bg": "#ffffff"
            }
        }
    }
]


# ==========================================
# 2. كود التحقق والإنشاء (Setup Engine)
# ==========================================
@frappe.whitelist()
def initialize_themes():
    # verify_app_license() # <-- الصافرة هنا
    doctype_name = "Madar Theme"
    
    # 1. التحقق من وجود الـ DocType، وإذا لم يكن موجوداً نقوم بإنشائه
    if not frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": doctype_name,
            "module": "Madar",  # مطابق لتطبيقك
            "custom": 1,        
            "autoname": "field:theme_id",
            "fields": [
                {"fieldname": "theme_id", "label": "Theme ID", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "theme_name_ar", "label": "Theme Name (AR)", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "theme_name_en", "label": "Theme Name (EN)", "fieldtype": "Data", "reqd": 1},
                {
                    "fieldname": "theme_mode", 
                    "label": "Theme Mode", 
                    "fieldtype": "Select", 
                    "options": "Light\nDark", 
                    "reqd": 1, 
                    "default": "Light"
                },
                {"fieldname": "theme_desc_ar", "label": "Theme Description (AR)", "fieldtype": "Text"},
                {"fieldname": "theme_desc_en", "label": "Theme Description (EN)", "fieldtype": "Text"},
                {"fieldname": "is_default", "label": "Is Default Theme", "fieldtype": "Check", "default": 0},
                {"fieldname": "theme_data", "label": "Theme Data", "fieldtype": "Code", "options": "JSON", "reqd": 1}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "All", "read": 1, "write": 0, "create": 0, "delete": 0}
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"تم إنشاء DocType: {doctype_name} بنجاح.")

    # 2. التحقق من وجود الثيمات الافتراضية وحفظها (سنقوم بتحديثها إذا كانت موجودة)
    for theme in DEFAULT_THEMES:
        theme_id = theme.get("theme_id")
        
        theme_data_str = json.dumps(theme, ensure_ascii=False, indent=4)
        
        if not frappe.db.exists(doctype_name, theme_id):
            new_theme = frappe.get_doc({
                "doctype": doctype_name,
                "theme_id": theme_id,
                "theme_name_ar": theme.get("theme_name_ar"),
                "theme_name_en": theme.get("theme_name_en"),
                "theme_mode": theme.get("theme_mode"),
                "theme_desc_ar": theme.get("theme_desc_ar"),
                "theme_desc_en": theme.get("theme_desc_en"),
                "is_default": 1 if theme_id == "ocean_blue" else 0,
                "theme_data": theme_data_str
            })
            new_theme.insert(ignore_permissions=True)
            print(f"تم إضافة الثيم: {theme_id}")
        else:
            # Update existing theme
            existing_theme = frappe.get_doc(doctype_name, theme_id)
            existing_theme.theme_data = theme_data_str
            existing_theme.save(ignore_permissions=True)
            print(f"تم تحديث الثيم: {theme_id}")
            
    frappe.db.commit()
    return "Theme initialization completed successfully."