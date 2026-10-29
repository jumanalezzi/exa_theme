import frappe
from urllib.parse import quote

def redirect_top_level_app(context=None):
    """
    Hook called during website context generation (including /app, /app/*, and /madar).
    Redirects top-level browser requests:
    - /app, /app/home -> /exa
    - /app/<route> -> /exa?route=app/<route>
    - /madar, /madar/<route> -> /exa / /exa?route=...
    Leaves requests coming from within the Exa iframe untouched.
    """
    if not hasattr(frappe, "request") or not frappe.request:
        return

    path = (frappe.request.path or "").strip()

    # 1. تحويل مسارات /madar إلى /exa
    if path == "/madar" or path.startswith("/madar/"):
        query = frappe.request.query_string.decode("utf-8", errors="ignore") if frappe.request.query_string else ""
        sub = path[6:].lstrip("/")
        if sub:
            target = f"/exa?route={quote(sub)}"
            if query:
                target += f"&{query}"
        else:
            target = "/exa"
            if query:
                target += f"?{query}"
        frappe.local.flags.redirect_location = target
        raise frappe.Redirect(301)

    if not (path == "/app" or path.startswith("/app/")):
        return

    # Check if request is originating inside the Exa iframe:
    referer = frappe.request.headers.get("Referer") or ""
    sec_dest = frappe.request.headers.get("Sec-Fetch-Dest") or ""
    in_exa_param = frappe.request.args.get("in_exa") or frappe.request.args.get("in_madar")

    is_iframe = (
        in_exa_param == "1"
        or sec_dest == "iframe"
        or ("/exa" in referer and "/app" in path)
        or ("/madar" in referer and "/app" in path)
    )
    if is_iframe:
        return

    # Direct top-level request:
    if path in ("/app", "/app/", "/app/home", "/app/home/"):
        frappe.local.flags.redirect_location = "/exa"
        raise frappe.Redirect(302)

    # Any sub-route like /app/item or /app/hghjghj:
    route = path.lstrip("/")
    query = frappe.request.query_string.decode("utf-8", errors="ignore") if frappe.request.query_string else ""
    target = f"/exa?route={quote(route)}"
    if query:
        target += f"&{query}"

    frappe.local.flags.redirect_location = target
    raise frappe.Redirect(302)
