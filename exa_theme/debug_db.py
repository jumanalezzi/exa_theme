import frappe
import json

def run():
    frappe.init(site="all")
    frappe.connect()
    users = frappe.get_all("Madar User Preference", fields=["name", "dashboard_menu"])
    for u in users:
        print("User:", u.name)
        print("Dashboard Menu:")
        print(u.dashboard_menu)
        print("---")
