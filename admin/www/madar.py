import frappe
from frappe import _
import json
from admin.license_core import verify_app_license

def get_context(context):
    # verify_app_license() # <-- الصافرة هنا
    set_lang = frappe.form_dict.get('set_lang')
    if set_lang and set_lang in ['ar', 'en']:
        # 1. تحديث قاعدة البيانات
        frappe.db.set_value("User", frappe.session.user, "language", set_lang)
        frappe.clear_cache(user=frappe.session.user)
        frappe.db.commit()
        
        # 2. بناء رابط العودة النظيف
        # نأخذ المسار الحالي (مثلاً /madar)
        path = frappe.request.path 
        
        # نجهز قائمة المعاملات الأخرى (مثل الفلاتر أو أرقام الصفحات) 
        # مع استبعاد أي شيء يخص اللغة القديمة
        params = []
        for key, value in frappe.form_dict.items():
            if key not in ['set_lang', 'lang']:
                params.append(f"{key}={value}")
        
        # إضافة معامل اللغة الجديد والوحيد
        params.append(f"lang={set_lang}")
        
        # دمج الرابط
        clean_url = f"{path}?{'&'.join(params)}"
        
        # 3. إعادة توجيه قاطعة
        frappe.local.flags.redirect_location = clean_url
        raise frappe.Redirect

    # 1. التأكد من تسجيل الدخول
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/madar"
        raise frappe.Redirect

    # 2. معالجة اللغة والاتجاه
    user_lang = frappe.db.get_value("User", frappe.session.user, "language") or frappe.local.lang
    context.lang = user_lang
    
    # تحديد الاتجاه بناءً على اللغة المكتشفة
    # نتحقق إذا كانت اللغة تنتمي للغات التي تكتب من اليمين لليسان
    context.layout_direction = "rtl" if frappe.local.lang in ["ar", "he", "fa", "ps", "ur"] else "ltr"
    context.user_pref = get_user_preferences()
    # 3. التأكد من وجود مستند الإعدادات وفحص البيانات
    settings = ensure_settings_exists()
    is_ready = (settings.app_name_ar or settings.app_name_en) and (settings.light_logo or settings.dark_logo)
    # 4. تحديد القالب وتمرير البيانات
    if is_ready:
        context.settings = settings
      
        # ملاحظة: محرك Frappe سيبحث عن madar.html كقالب أساسي، 
        # ويمكننا استخدام التبديل داخل الملف نفسه أو عبر الشرط هنا
        context.show_main_interface = True
    else:
        context.show_main_interface = False
        if "System Manager" in frappe.get_roles(frappe.session.user):
            context.setup_status = "admin_needed"
        else:
            context.setup_status = "user_wait"
    context.installed_apps = frappe.get_installed_apps()
    context.system_theme = frappe.conf.get("system_theme", "madar")
    context.no_cache = 1
    return context

def ensure_settings_exists():
    """تتأكد من وجود مستند Single وإنشاؤه إن لم يوجد"""
    if not frappe.db.exists("Madar Settings", "Madar Settings"):
        doc = frappe.get_doc({
            "doctype": "Madar Settings",
            "app_name_ar": "إتقان",
             "app_name_en": "Etqan"
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
    return frappe.get_doc("Madar Settings")

def get_user_preferences():
    user = frappe.session.user
    
    # 1. محاولة جلب التفضيلات الحالية
    pref = frappe.db.get_value("Madar User Preference", {"user": user}, 
        ["current_system", "custom_menu_json", "madar_theme", "madar_font", "dashboard_menu"], as_dict=True)
    
    # 2. إذا كان المستخدم جديداً، نقوم بتجهيز "الباقة الافتراضية" له
    if not pref:
        # جلب النظام الافتراضي
        default_system = frappe.db.get_value("Madar System", {"is_default": 1}, "name")
        
        # جلب الثيم والخط الذي حدده المدير كافتراضي
        default_theme = frappe.db.get_value("Madar Theme", {"is_default": 1}, "name")
        default_font = frappe.db.get_value("Madar Font", {"is_default": 1}, "name")
        
        if not default_system:
            return {"error": "لا يوجد نظام افتراضي معرف في Madar System"}
            
        # إنشاء السجل الجديد بالقيم الافتراضية المحددة من المدير
        new_pref = frappe.get_doc({
            "doctype": "Madar User Preference",
            "user": user,
            "current_system": default_system,
            "madar_theme": default_theme, # سيتم تعيينه تلقائياً مما حدده المدير
            "madar_font": default_font    # سيتم تعيينه تلقائياً مما حدده المدير
        })
        new_pref.insert(ignore_permissions=True)
        frappe.db.commit()
        pref = new_pref

    # 3. جلب بيانات النظام (System Data)
    # لاحظ أننا نستخدم pref كـ dict سواء كان قديماً أو تم إنشاؤه للتو
    system_name = pref.get("current_system")
    system_doc = frappe.get_doc("Madar System", system_name)
    
    # تحديد القائمة النهائية (الأولوية للمخصصة ثم قائمة النظام)
    raw_menu = pref.get("custom_menu_json") if pref.get("custom_menu_json") else system_doc.default_menu_json
    menu_list = json.loads(raw_menu) if raw_menu else []
    
    # 7. فلترة القائمة برمجياً بناءً على الصلاحيات قبل إرجاعها
    filtered_menu = filter_menu_by_permissions(menu_list)
    
        # 8. Dashboard Menu
    raw_dashboard = pref.get("dashboard_menu")
    dashboard_list = []
    
    system_default_dashboard = system_doc.dashboard_menu if system_doc and hasattr(system_doc, "dashboard_menu") else "[]"
    system_default_list = json.loads(system_default_dashboard) if system_default_dashboard else []
    
    is_default_dashboard = False
    
    if raw_dashboard:
        try:
            parsed_dash = json.loads(raw_dashboard)
            if parsed_dash and isinstance(parsed_dash, list) and isinstance(parsed_dash[0], dict) and "system" in parsed_dash[0]:
                found = False
                for sys_menu in parsed_dash:
                    if sys_menu.get("system") == system_name:
                        dashboard_list = sys_menu.get("menu", [])
                        found = True
                        break
                if not found:
                    dashboard_list = system_default_list
                    is_default_dashboard = True
            else:
                dashboard_list = parsed_dash
        except:
            dashboard_list = system_default_list
            is_default_dashboard = True
    else:
        dashboard_list = system_default_list
        is_default_dashboard = True

    filtered_dashboard = filter_menu_by_permissions(dashboard_list)
    filtered_full_dashboard = filter_menu_by_permissions(system_default_list)
    
    return {
        "current_system": system_name,
        "custom_menu_json": filtered_menu,
        "dashboard_menu": filtered_dashboard,
        "is_default_dashboard": is_default_dashboard,
        "full_system_dashboard_menu": filtered_full_dashboard,
        "madar_theme": pref.get("madar_theme"),
        "madar_font": pref.get("madar_font"),
        "is_admin": "System Manager" in frappe.get_roles(frappe.session.user),
        "system_info": {
            "name_ar": system_doc.system_name_ar if system_doc else "",
            "name_en": system_doc.system_name_en if system_doc else ""
        }
    }

@frappe.whitelist()
def update_user_language(new_lang):
    if not new_lang:
        frappe.throw("الرجاء اختيار لغة صحيحة")
    
    # 1. تحديث حقل اللغة للمستخدم الحالي
    frappe.db.set_value("User", frappe.session.user, "language", new_lang)
    
    # 2. خطوة جوهرية: مسح الكاش الخاص بالمستخدم
    # بدون هذا السطر، سيظل النظام يخدم ملفات الترجمة القديمة المخزنة في الذاكرة
    frappe.clear_cache(user=frappe.session.user)
    
    # 3. حفظ التغييرات نهائياً
    frappe.db.commit()
    
    return {"status": "success", "message": "تم تحديث اللغة بنجاح"}

def filter_menu_by_permissions(menu_list):
    filtered_list = []
    
    for item in menu_list:
        if item.get("type") == "folder":
            # تفحص الأبناء بشكل متكرر
            children = item.get("children", [])
            filtered_children = filter_menu_by_permissions(children)
            
            # نضيف المجلد فقط إذا كان لديه أبناء بعد الفلترة (حذف المجلدات الفارغة)
            if filtered_children:
                item["children"] = filtered_children
                filtered_list.append(item)
                
        elif item.get("type") == "link":
            # التحقق من الصلاحية بناء على نوع العرض والمسار
            if has_route_permission(item):
                filtered_list.append(item)
                
    return filtered_list

def has_route_permission(item):
    view_type = item.get("view_type")
    route = item.get("route", "")
    
    if not route:
        return True
        
    if view_type == "file":
        # نفترض أن الصفحات المخصصة متاحة، أو يمكن فحص أدوار محددة لاحقاً
        return True
        
    elif view_type == "frame":
        # معالجة مسارات فرابي القياسية مثل app/sales-invoice
        if route.startswith("app/"):
            route = route[4:]
            
        parts = route.strip("/").split("/")
        if not parts or not parts[0]:
            return True
            
        first_part = parts[0]

        # Hide POS Awesome if app is not installed
        if first_part in ("pos-awesome", "posapp") and "posawesome" not in frappe.get_installed_apps():
            return False
        
        # 1. فحص صلاحية مساحات العمل (Workspaces)
        if first_part.lower() in ("workspaces", "workspace") and len(parts) > 1:
            workspace_name = frappe.unscrub(parts[1])
            has_ws = frappe.get_list("Workspace", filters={"name": workspace_name}, limit=1)
            return bool(has_ws)
            
        # 2. فحص صلاحية القوائم (List)
        elif first_part.lower() == "list" and len(parts) > 1:
            doctype = frappe.unscrub(parts[1])
            if frappe.db.exists("DocType", doctype):
                return frappe.has_permission(doctype, ptype="read")
                
        # 3. فحص صلاحية الدوكتايب المباشر (مثل sales-invoice)
        else:
            doctype = frappe.unscrub(first_part)
            if frappe.db.exists("DocType", doctype):
                return frappe.has_permission(doctype, ptype="read")
            
            # إذا كانت صفحة Page عادية
            if frappe.db.exists("Page", first_part):
                return True
                
        return True
        
    return True