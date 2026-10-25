import frappe

frappe.init(site="all")
frappe.connect()

try:
    companies = frappe.get_all("Company", fields=["name"])
    print("Companies in DB:")
    for c in companies:
        c_name = c['name']
        print(f"\n--- Company: '{c_name}' ---")
        
        # Test This Month
        res1 = frappe.get_attr("admin.dashboard_api.get_dashboard_data")(company=c_name, filter_type="this_month")
        print(f"This Month Revenue: {res1.get('financials', {}).get('total_revenue')}")
        
        # Test This Quarter
        res2 = frappe.get_attr("admin.dashboard_api.get_dashboard_data")(company=c_name, filter_type="this_quarter")
        print(f"This Quarter Revenue: {res2.get('financials', {}).get('total_revenue')}")
        
except Exception as e:
    import traceback
    traceback.print_exc()
