import frappe
from exa_theme.license_core import verify_app_license

import json



@frappe.whitelist()

def update_user_preference(field, value):
    # verify_app_license() # <-- الصافرة هنا

    user_id = frappe.session.user

    if field not in ['madar_theme', 'madar_font','custom_menu_json','current_system']:

        return {"status": "error", "message": "Invalid field"}



    if not frappe.db.exists("Madar User Preference", {"user": user_id}):

        doc = frappe.new_doc("Madar User Preference")

        doc.user = user_id

        doc.set(field, value)

        doc.insert(ignore_permissions=True)

    else:

        frappe.db.set_value("Madar User Preference", {"user": user_id}, field, value)



    frappe.db.commit()

    return {"status": "success", "message": f"{field} updated"}



@frappe.whitelist()

def get_user_preferences_api():
    # verify_app_license() # <-- الصافرة هنا

    user_id = frappe.session.user

    pref = frappe.get_all("Madar User Preference", filters={"user": user_id}, fields=["*"])

    if pref:

        pref = pref[0]

    else:

        pref = {}



    system_name = pref.get("current_system")

    system_doc = frappe.get_doc("Madar System", system_name) if system_name else None



    # Custom Menu

    raw_custom = pref.get("custom_menu_json")

    custom_list = json.loads(raw_custom) if raw_custom else []

    

    system_default_menu = system_doc.default_menu_json if system_doc and hasattr(system_doc, "default_menu_json") else "[]"

    system_default_menu_list = json.loads(system_default_menu) if system_default_menu else []

    

    if not custom_list:

        custom_list = system_default_menu_list



    filtered_menu = filter_menu_by_permissions(custom_list)



    # Dashboard Menu

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



def filter_menu_by_permissions(menu_list):

    filtered_list = []

    

    for item in menu_list:

        if item.get("type") == "folder":

            children = item.get("children", [])

            filtered_children = filter_menu_by_permissions(children)

            if filtered_children:

                item["children"] = filtered_children

                filtered_list.append(item)

        elif item.get("type") == "link":

            if has_route_permission(item):

                filtered_list.append(item)

                

    return filtered_list



def has_route_permission(item):

    view_type = item.get("view_type")

    route = item.get("route", "")

    

    if not route:

        return True

        

    if view_type == "file":

        return True

        

    elif view_type == "frame":

        if route.startswith("app/"):

            route = route[4:]

            

        parts = route.strip("/").split("/")

        if not parts or not parts[0]:

            return True

            

        first_part = parts[0]

        # Hide POS Awesome if app is not installed
        if first_part in ("pos-awesome", "posapp") and "posawesome" not in frappe.get_installed_apps():
            return False

        

        # 1. Workspaces

        if first_part.lower() in ("workspaces", "workspace") and len(parts) > 1:

            workspace_name = frappe.unscrub(parts[1])

            has_ws = frappe.get_list("Workspace", filters={"name": workspace_name}, limit=1)

            return bool(has_ws)

            

        # 2. List

        elif first_part.lower() == "list" and len(parts) > 1:

            doctype = frappe.unscrub(parts[1])

            if frappe.db.exists("DocType", doctype):

                return frappe.has_permission(doctype, ptype="read")

                

        # 3. Form/Page

        else:

            doctype = frappe.unscrub(first_part)

            if frappe.db.exists("DocType", doctype):

                return frappe.has_permission(doctype, ptype="read")

            

            if frappe.db.exists("Page", first_part):

                return True

                

        return True

        

    return True



@frappe.whitelist()

def update_dashboard_menu_for_system(system_name, menu_json):

    import json

    user_id = frappe.session.user

    

    try:

        frappe.log_error(title="update_dashboard_menu_for_system_debug", message=f"Received system: {system_name}\nPayload: {menu_json}")

        new_menu = json.loads(menu_json)

    except:

        return {"status": "error", "message": "Invalid JSON"}

        

    pref = frappe.db.get_value("Madar User Preference", {"user": user_id}, "dashboard_menu")

    

    parsed_dash = []

    if pref:

        try:

            parsed = json.loads(pref)

            if parsed and isinstance(parsed, list) and isinstance(parsed[0], dict) and "system" in parsed[0]:

                parsed_dash = parsed

        except:

            pass

            

    # Update or append

    found = False

    for sys_menu in parsed_dash:

        if sys_menu.get("system") == system_name:

            sys_menu["menu"] = new_menu

            found = True

            break

            

    if not found:

        parsed_dash.append({

            "system": system_name,

            "menu": new_menu

        })

        

    if not frappe.db.exists("Madar User Preference", {"user": user_id}):

        doc = frappe.new_doc("Madar User Preference")

        doc.user = user_id

        doc.dashboard_menu = json.dumps(parsed_dash, ensure_ascii=False)

        doc.insert(ignore_permissions=True)

    else:

        frappe.db.set_value("Madar User Preference", user_id, "dashboard_menu", json.dumps(parsed_dash, ensure_ascii=False))

        

    frappe.db.commit()

    

    return {"status": "success"}

@frappe.whitelist()

def get_pending_approvals():

    user = frappe.session.user

    approvals = frappe.get_all(

        'Workflow Action',

        filters={'user': user, 'status': 'Open'},

        fields=['name', 'reference_doctype', 'reference_name', 'workflow_state', 'creation'],

        limit_page_length=10,

        order_by='creation desc',

        ignore_permissions=True

    )

    return approvals



import requests

import re

import json



@frappe.whitelist()

def add_madar_font(font_name_ar, font_url):
    # verify_app_license() # <-- الصافرة هنا

    match = re.search(r"family=([^&:]+)", font_url)

    if not match:

        frappe.throw("رابط الخط غير صالح أو لا يحتوي على اسم العائلة (family).")

    

    font_name_en = match.group(1).replace("+", " ")

    font_family = f"'{font_name_en}', sans-serif"

    

    if frappe.db.exists("Madar Font", font_name_en):

        frappe.throw(f"الاسم الإنجليزي '{font_name_en}' موجود مسبقاً في النظام.")

    if frappe.db.exists("Madar Font", {"font_name_ar": font_name_ar}):

        frappe.throw(f"اسم الخط بالعربي '{font_name_ar}' موجود مسبقاً في النظام.")

        

    doc = frappe.get_doc({

        "doctype": "Madar Font",

        "font_name": font_name_en,

        "font_name_ar": font_name_ar,

        "font_name_en": font_name_en,

        "font_family": font_family,

        "font_url": font_url,

        "is_default": 0

    })

    doc.insert(ignore_permissions=True)

    return doc.name



@frappe.whitelist()

def edit_madar_font(font_name, font_name_ar):

    if not frappe.db.exists("Madar Font", font_name):

        frappe.throw("الخط غير موجود.")

        

    if frappe.db.exists("Madar Font", {"font_name_ar": font_name_ar, "name": ("!=", font_name)}):

        frappe.throw(f"اسم الخط بالعربي '{font_name_ar}' موجود مسبقاً في النظام لخط آخر.")

        

    doc = frappe.get_doc("Madar Font", font_name)

    doc.font_name_ar = font_name_ar

    doc.save(ignore_permissions=True)

    return "success"



@frappe.whitelist()

def delete_madar_font(font_name):

    used_in_pref = frappe.db.exists("Madar User Preference", {"madar_font": font_name})

    if used_in_pref:

        frappe.throw("لا يمكن حذف هذا الخط لأنه مستخدم من قبل مستخدمين آخرين في تفضيلاتهم.")

        

    doc = frappe.get_doc("Madar Font", font_name)

    if doc.is_default:

        frappe.throw("لا يمكن حذف الخط الافتراضي للنظام.")

        

    frappe.delete_doc("Madar Font", font_name, ignore_permissions=True)

    return "success"



@frappe.whitelist()

def suggest_madar_font_ai():
    import time
    settings = frappe.get_doc("Madar Settings", "Madar Settings")
    api_url = settings.get("ai_api_url")
    model_name = settings.get("ai_model_name")
    
    if not api_url or not model_name:
        frappe.throw("خدمة الذكاء الاصطناعي غير مفعلة في الإعدادات.")
        
    existing_fonts_en = frappe.get_all("Madar Font", pluck="font_name_en")
    existing_fonts_ar = frappe.get_all("Madar Font", pluck="font_name_ar")
    existing_fonts_en_lower = [f.lower().strip() for f in existing_fonts_en if f]
    existing_fonts_ar_lower = [f.lower().strip() for f in existing_fonts_ar if f]
    
    existing_fonts_str = ", ".join(existing_fonts_en + existing_fonts_ar)
    
    prompt = f"""You are an expert web developer. Suggest a highly popular Google Font that supports BOTH Arabic and English languages.
CRITICAL RULE 1: Do NOT suggest any font from this list: [{existing_fonts_str}].
CRITICAL RULE 2: font_name_ar MUST be written using Arabic letters ONLY (e.g. كايرو, تاجوال, المري).
Return ONLY a valid JSON object. The JSON MUST be formatted EXACTLY like this example:
{{"font_name_ar": "اسم الخط بالحروف العربية", "font_name_en": "English Name", "font_url": "https://fonts.googleapis.com/css2?family=Example:wght@400;500;700"}}"""

    gemini_key = settings.get_password("gemini_api_key")
    if gemini_key:
        gemini_key = gemini_key.strip()
        
    if not gemini_key:
        frappe.throw("الرجاء إضافة مفتاح Gemini API في إعدادات مدار.")
        
    if gemini_key:
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts":[{"text": prompt}]}]
        }
        models_to_try = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash-exp", "gemini-1.5-flash"]
        
        for attempt in range(3):
            success = False
            last_err = ""
            for m in models_to_try:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={gemini_key}"
                try:
                    response = requests.post(gemini_url, json=payload, headers=headers, timeout=60)
                    if response.status_code != 200:
                        raise Exception(f"Google API Error {response.status_code}: {response.text}")
                    success = True
                    break
                except Exception as ex:
                    last_err = str(ex)
                    continue
                    
            if not success:
                frappe.log_error(title="Gemini API Error All Models", message=last_err)
                frappe.throw(f"Gemini API Error: {last_err}")


            data = response.json()
            
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                try:
                    result = json.loads(json_str)
                except Exception as e:
                    frappe.log_error(title="Gemini JSON Error", message=f"{str(e)} - Content: {content}")
                    frappe.throw(f"Gemini JSON Error: {str(e)}")
                
                suggested_en = result.get("font_name_en", "").lower().strip()
                suggested_ar = result.get("font_name_ar", "").lower().strip()
                
                import re
                has_arabic = bool(re.search(r'[\u0600-\u06FF]', suggested_ar))
                
                if suggested_en and suggested_ar and has_arabic:
                    if suggested_en not in existing_fonts_en_lower and suggested_ar not in existing_fonts_ar_lower:
                        return result
                
                payload["contents"][0]["parts"].append({"text": f"You provided '{suggested_ar}'. Try another entirely different Arabic font and ensure it uses Arabic letters."})
            else:
                if attempt == 2:
                    frappe.throw("تعذر استخراج JSON من إجابة الذكاء الاصطناعي.")
        frappe.throw("فشل الذكاء الاصطناعي في توليد بيانات صحيحة بعد 3 محاولات.")
        
    else:
        if not api_url.endswith("/chat/completions"):
            api_url = api_url.rstrip("/") + "/chat/completions"
            
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
            "keep_alive": "24h",
            "options": {"num_predict": 1024}
        }
        
        # Try up to 3 times to get a unique font
        for attempt in range(3):
            response = requests.post(api_url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            data = response.json()
            
            content = data["choices"][0]["message"]["content"]
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                result = json.loads(json_str)
                
                # Check if the AI hallucinated an existing font
                suggested_en = result.get("font_name_en", "").lower().strip()
                suggested_ar = result.get("font_name_ar", "").lower().strip()
                
                # Check if it contains Arabic letters
                has_arabic = bool(re.search(r'[\u0600-\u06FF]', suggested_ar))
                
                if suggested_en and suggested_en not in existing_fonts_en_lower and suggested_ar not in existing_fonts_ar_lower and has_arabic:
                    return result
                
                # If duplicate or non-arabic, change the prompt slightly to force a new one
                payload["messages"].append({"role": "assistant", "content": json_str})
                if not has_arabic:
                    payload["messages"].append({"role": "user", "content": f"You provided '{suggested_ar}' for font_name_ar. This is English! You MUST write font_name_ar using ARABIC LETTERS."})
                else:
                    payload["messages"].append({"role": "user", "content": f"You suggested {suggested_en} or {suggested_ar} which is already in the forbidden list! Try another entirely different Arabic font."})
            else:
                if attempt == 2:
                    frappe.throw("تعذر فهم استجابة الذكاء الاصطناعي.")
        
        # If all 3 attempts fail or return duplicates, fallback to a hardcoded popular font
        fallbacks = [
            {"font_name_ar": "لمار", "font_name_en": "Lalezar", "font_url": "https://fonts.googleapis.com/css2?family=Lalezar&display=swap"},
            {"font_name_ar": "أميري", "font_name_en": "Amiri", "font_url": "https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"},
            {"font_name_ar": "شروق", "font_name_en": "Changa", "font_url": "https://fonts.googleapis.com/css2?family=Changa:wght@300;400;700&display=swap"}
        ]
        for fb in fallbacks:
            if fb["font_name_en"].lower() not in existing_fonts_en_lower and fb["font_name_ar"].lower() not in existing_fonts_ar_lower:
                return fb
                
        frappe.throw("استنفدنا محاولات العثور على خط جديد غير موجود.")
            



@frappe.whitelist()
def auto_detect_ai():
    import requests
    try:
        res = requests.get('http://127.0.0.1:11434/api/tags', timeout=2)
        if res.status_code == 200:
            models = res.json().get('models', [])
            if models:
                model_name = models[0]['name']
                doc = frappe.get_doc('Madar Settings', 'Madar Settings')
                doc.ai_api_url = 'http://127.0.0.1:11434/v1'
                doc.ai_model_name = model_name
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                return {'status': 'success', 'url': doc.ai_api_url, 'model': doc.ai_model_name}
    except Exception as e:
        pass
    return {'status': 'failed'}




@frappe.whitelist()
def suggest_madar_theme_ai(description=""):
    import requests, json
    
    settings = frappe.get_doc("Madar Settings", "Madar Settings")
    api_url = settings.get("ai_api_url")
    model_name = settings.get("ai_model_name")
    
    if not api_url or not model_name:
        frappe.throw("خدمة الذكاء الاصطناعي غير مفعلة في الإعدادات.")
        
    existing_themes_en = frappe.get_all("Madar Theme", pluck="theme_name_en")
    existing_themes_ar = frappe.get_all("Madar Theme", pluck="theme_name_ar")
    existing_themes_str = ", ".join([f for f in (existing_themes_en + existing_themes_ar) if f])
    
    base_prompt = f"""You are an expert UI/UX designer. Suggest a highly beautiful, modern, and coherent color theme for an admin dashboard.
CRITICAL RULE 1: Do NOT suggest any theme name from this list: [{existing_themes_str}].
CRITICAL RULE 2: theme_name_ar MUST be written using Arabic letters ONLY (e.g. نيون ليلي, خريفي دافئ).
CRITICAL RULE 3: theme_name_en MUST be written in English.
CRITICAL RULE 4: All color values MUST be valid HEX codes (e.g. #ff0000).
CRITICAL RULE 5 (The Contrast & Hierarchy Equation): 
You MUST mathematically ensure high contrast and proper hierarchical shading based on whether the theme is Light or Dark:
A) For Light Themes:
   - Text on light backgrounds MUST be dark (e.g. #212529 or #3e2723) to ensure > 4.5:1 contrast ratio.
   - Background Hierarchy: `content.surface_bg` should be pure white (#ffffff) or very light. `content.page_bg` should be slightly darker (e.g. #f4f6f9) to create depth.
   - Sidebar Hierarchy: Progress smoothly from lightest to slightly darker. Level 1 bg > Level 2 bg > Level 3 bg (e.g. L1: #ffffff, L2: #fafafa, L3: #f4f6f9).
B) For Dark Themes:
   - Text on dark backgrounds MUST be light (e.g. #ffffff or #f8fafc).
   - Background Hierarchy: `content.page_bg` should be very dark (e.g. #151521), and `content.surface_bg` should be slightly lighter (e.g. #1e1e2d) to lift elements.
   - Sidebar Hierarchy: Progress smoothly from lighter to darker. Level 1 bg > Level 2 bg > Level 3 bg (e.g. L1: #151521, L2: #11111a, L3: #0d0d14).
C) Interactive Elements:
   - `hover_bg` and `active_bg` MUST be subtle tints/shades of the primary color.
   - `hover_text` and `active_text` MUST strongly contrast with their backgrounds (usually the primary color itself or pure white/black).
   - Header text and buttons MUST contrast beautifully against the `header.bg`.

Return ONLY a valid JSON object matching the exact structure below. Do not include markdown or extra text.

{{
  "theme_name_ar": "اسم الثيم بالحروف العربية",
  "theme_name_en": "Theme Name in English",
  "colors": {{
    "palette": {{
      "primary": "#hex", "secondary": "#hex", "success": "#hex", "danger": "#hex", "warning": "#hex", "info": "#hex"
    }},
    "header": {{
      "bg": "#hex", "text": "#hex",
      "buttons": {{"bg": "transparent", "text": "#hex", "hover_bg": "#hex", "hover_text": "#hex"}}
    }},
    "sidebar": {{
      "level_1": {{"bg": "#hex", "text": "#hex", "hover_bg": "#hex", "hover_text": "#hex", "active_bg": "#hex", "active_text": "#hex"}},
      "level_2": {{"bg": "#hex", "text": "#hex", "hover_bg": "#hex", "hover_text": "#hex", "active_bg": "#hex", "active_text": "#hex"}},
      "level_3": {{"bg": "#hex", "text": "#hex", "hover_bg": "#hex", "hover_text": "#hex", "active_bg": "#hex", "active_text": "#hex"}}
    }},
    "footer": {{
      "bg": "#hex", "text": "#hex",
      "links": {{"text": "#hex", "hover_text": "#hex"}}
    }},
    "content": {{
      "page_bg": "#hex", "surface_bg": "#hex", "text_primary": "#hex", "text_muted": "#hex", "border_color": "#hex", "input_bg": "#hex"
    }}
  }}
}}
"""

    if description.strip():
        prompt = base_prompt + f"\n\nUSER REQUEST: The theme MUST perfectly match this description: '{description}'"
    else:
        prompt = base_prompt + "\n\nUSER REQUEST: Generate a random, unique, and extremely beautiful modern theme."

    gemini_key = settings.get_password("gemini_api_key")
    
    try:
        for attempt in range(3):
            if gemini_key:
                payload = {
                    "contents": [{"parts":[{"text": prompt}]}]
                }
                headers = {"Content-Type": "application/json"}
                
                models_to_try = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash-exp", "gemini-1.5-flash"]
                success = False
                last_err = ""
                
                for m in models_to_try:
                    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={gemini_key}"
                    try:
                        response = requests.post(gemini_url, json=payload, headers=headers, timeout=60)
                        response.raise_for_status()
                        success = True
                        break
                    except Exception as ex:
                        last_err = str(ex)
                        continue
                        
                if not success:
                    frappe.log_error(title="Gemini Theme Error All Models", message=last_err)
                    frappe.throw(f"Gemini API Error: {last_err}")
                data = response.json()
                
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    result = json.loads(json_str)
                    
                    suggested_en = result.get("theme_name_en", "").lower().strip()
                    suggested_ar = result.get("theme_name_ar", "").lower().strip()
                    
                    import re
                    has_arabic = bool(re.search(r'[\u0600-\u06FF]', suggested_ar))
                    
                    if suggested_en and suggested_ar and has_arabic:
                        existing_en_lower = [f.lower().strip() for f in existing_themes_en if f]
                        existing_ar_lower = [f.lower().strip() for f in existing_themes_ar if f]
                        if suggested_en not in existing_en_lower and suggested_ar not in existing_ar_lower:
                            return result
                    
                    payload["contents"][0]["parts"].append({"text": f"You provided '{suggested_ar}'. Try another entirely different Arabic theme name and ensure it uses Arabic letters."})
                else:
                    if attempt == 2:
                        frappe.throw("تعذر استخراج JSON من إجابة الذكاء الاصطناعي.")
            frappe.throw("فشل الذكاء الاصطناعي في توليد بيانات صحيحة بعد 3 محاولات.")
            
        else:
            if not api_url.endswith("/chat/completions"):
                api_url = api_url.rstrip("/") + "/chat/completions"
                
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.9,
                "keep_alive": "24h",
                "options": {"num_predict": 1024}
            }
            
            for attempt in range(3):
                response = requests.post(api_url, json=payload, headers=headers, timeout=300)
                response.raise_for_status()
                data = response.json()
                
                content = data["choices"][0]["message"]["content"]
        frappe.throw("استنفدنا محاولات توليد ثيم جديد.")
            
    except Exception as e:
        frappe.log_error(title="Gemini Theme Error", message=f"{str(e)}")
        frappe.throw(f"Gemini API Error: {str(e)}")

@frappe.whitelist()
def add_madar_theme(theme_name_ar, theme_name_en, theme_data):
    # verify_app_license() # <-- الصافرة هنا
    theme_id = theme_name_en.lower().replace(" ", "_")
    if frappe.db.exists("Madar Theme", {"theme_id": theme_id}):
        frappe.throw(f"الاسم الإنجليزي '{theme_name_en}' موجود مسبقاً في النظام.")
        
    if frappe.db.exists("Madar Theme", {"theme_name_ar": theme_name_ar}):
        frappe.throw(f"اسم الثيم بالعربي '{theme_name_ar}' موجود مسبقاً في النظام.")
        
    doc = frappe.get_doc({
        "doctype": "Madar Theme",
        "theme_id": theme_id,
        "theme_name_ar": theme_name_ar,
        "theme_name_en": theme_name_en,
        "theme_data": theme_data,
        "is_default": 0
    })
    
    doc.insert(ignore_permissions=True)
    return doc.name

@frappe.whitelist()
def edit_madar_theme(theme_name, theme_name_ar, theme_name_en, theme_data):
    if not frappe.db.exists("Madar Theme", theme_name):
        frappe.throw("الثيم غير موجود.")
        
    if frappe.db.exists("Madar Theme", {"theme_name_ar": theme_name_ar, "name": ("!=", theme_name)}):
        frappe.throw(f"اسم الثيم بالعربي '{theme_name_ar}' موجود مسبقاً في النظام لثيم آخر.")
        
    if frappe.db.exists("Madar Theme", {"theme_name_en": theme_name_en, "name": ("!=", theme_name)}):
        frappe.throw(f"اسم الثيم الإنجليزي '{theme_name_en}' موجود مسبقاً في النظام لثيم آخر.")
        
    doc = frappe.get_doc("Madar Theme", theme_name)
    doc.theme_name_ar = theme_name_ar
    doc.theme_name_en = theme_name_en
    doc.theme_data = theme_data
        
    doc.save(ignore_permissions=True)
    return "success"

@frappe.whitelist()
def delete_madar_theme(theme_name):
    # theme_id might be used in preferences
    doc = frappe.get_doc("Madar Theme", theme_name)
    used_in_pref = frappe.db.exists("Madar User Preference", {"madar_theme": doc.theme_id})
    if used_in_pref:
        frappe.throw("لا يمكن حذف هذا الثيم لأنه مستخدم من قبل مستخدمين آخرين في تفضيلاتهم.")
        
    if doc.is_default:
        frappe.throw("لا يمكن حذف الثيم الافتراضي للنظام.")
        
    frappe.delete_doc("Madar Theme", theme_name, ignore_permissions=True)
    return "success"


@frappe.whitelist()
def translate_menu_label_ai(label, target_lang):
    import requests
    import json
    settings = frappe.get_single("Madar Settings")
    gemini_key = settings.get_password("gemini_api_key")
    if not gemini_key:
        frappe.throw("Gemini API key is missing.")
        
    prompt = f"Translate the following short UI menu label strictly to {target_lang}. If the text consists of random or meaningless characters, return the exact string 'ERR_NO_TRANSLATION'. Return ONLY the translation or the error string, maximum 4 words. Text: {label}"
    payload = {
        "contents": [{"parts":[{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        return content
    except Exception as e:
        frappe.log_error(title="Menu AI Translation Error", message=str(e))
        frappe.throw(f"Translation failed: {str(e)}")

@frappe.whitelist()
def search_doctypes_for_menu(txt):
    doctypes = frappe.db.sql("""
        SELECT name, module 
        FROM `tabDocType` 
        WHERE istable = 0 AND custom = 0 
    """, as_dict=True)
    
    txt_lower = txt.lower()
    results = []
    for d in doctypes:
        translated = frappe._(d.name)
        d["translated_name"] = translated
        
        # Check english name
        if txt_lower in d.name.lower():
            results.append(d)
        else:
            # Check localized name
            if txt_lower in translated.lower():
                results.append(d)
                
        if len(results) >= 50:
            break
            
    return results

@frappe.whitelist()
def restore_default_menu():
    try:
        user = frappe.session.user
        pref_name = frappe.db.get_value("Madar User Preference", {"user": user}, "name")
        if pref_name:
            doc = frappe.get_doc("Madar User Preference", pref_name)
            doc.custom_menu_json = ""
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.clear_cache(user=user)
        return "success"
    except Exception as e:
        frappe.log_error("Madar Restore Menu Error", str(e))
        return "error"


@frappe.whitelist(allow_guest=True)
def check_route_exists(route):
    """
    Checks if a given /app route exists in ERPNext / Frappe.
    Returns: {"exists": True/False, "route": route}
    """
    if not route:
        return {"exists": False}

    r = str(route).strip('/').lower()
    if r.startswith('app/'):
        r = r[4:]
    elif r == 'app' or r == '':
        return {"exists": True}

    parts = r.split('/')
    first = parts[0]

    # 1. Fixed Madar routes
    if first in ['home', 'madar-theme-settings', 'madar-font-settings', 'madar-system-settings', 'madar-menu-settings']:
        return {"exists": True}

    # 2. Check Page doctype
    if frappe.db.exists("Page", {"name": first}) or frappe.db.exists("Page", {"page_name": first}):
        return {"exists": True}

    # 3. Check Workspace doctype
    if frappe.db.exists("Workspace", {"name": first}):
        return {"exists": True}
    workspaces = frappe.get_all("Workspace", fields=["name", "title"])
    for w in workspaces:
        if frappe.scrub(w.name).replace('_', '-') == first or frappe.scrub(w.title or '').replace('_', '-') == first:
            return {"exists": True}

    # 4. Check DocType (direct slug, or List/Form/Tree/Report prefix)
    doctype_candidate = None
    if first in ['list', 'form', 'report', 'tree'] and len(parts) > 1:
        doctype_candidate = parts[1]
    else:
        doctype_candidate = first

    if frappe.db.exists("DocType", {"name": doctype_candidate}):
        return {"exists": True}

    all_dt = frappe.get_all("DocType", fields=["name"])
    for d in all_dt:
        if frappe.scrub(d.name).replace('_', '-') == doctype_candidate or d.name.lower() == doctype_candidate.lower():
            return {"exists": True}

    # 5. Check Report doctype
    if first in ['query-report', 'report'] and len(parts) > 1:
        rep_candidate = parts[-1]
        if frappe.db.exists("Report", {"name": rep_candidate}):
            return {"exists": True}

    return {"exists": False}
