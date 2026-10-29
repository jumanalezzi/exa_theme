import frappe

def get_context(context):
    query = frappe.request.query_string.decode("utf-8", errors="ignore") if hasattr(frappe, "request") and frappe.request and frappe.request.query_string else ""
    target = "/exa"
    if query:
        target += f"?{query}"
    frappe.local.flags.redirect_location = target
    raise frappe.Redirect(301)
