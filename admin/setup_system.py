import frappe
import json
from admin.license_core import verify_app_license

def create_madar_system_doctype():
    if frappe.db.exists("DocType", "Madar System"):
        doc = frappe.get_doc("DocType", "Madar System")
        has_field = any(f.fieldname == "dashboard_menu" for f in doc.fields)
        if not has_field:
            doc.append("fields", {
                "fieldname": "dashboard_menu",
                "label": "مفضلة الداشبورد (JSON)",
                "fieldtype": "Code",
                "options": "JSON"
            })
            doc.save(ignore_permissions=True)
            
        needs_save = False
        for f in doc.fields:
            if f.fieldname in ["is_default", "is_mandatory"]:
                if not f.read_only:
                    f.read_only = 1
                    needs_save = True
        if needs_save:
            doc.save(ignore_permissions=True)
        return

    # تعريف الدوكتايب الأساسي
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Madar System",
        "module": "Madar",  # استبدله بالموديول الخاص بك
        "custom": 0,
        "autoname": "field:system_name_en",
        "naming_rule": "By fieldname",
        "fields": [
            # قسم المعلومات الأساسية
            {"fieldname": "section_main", "fieldtype": "Section Break", "label": "المعلومات الأساسية"},
            {"fieldname": "system_name_ar", "label": "اسم النظام (عربي)", "fieldtype": "Data", "reqd": 1},
            {"fieldname": "system_name_en", "label": "اسم النظام (إنجليزي)", "fieldtype": "Data", "reqd": 1, "unique": 1},
            {"fieldname": "col_break_1", "fieldtype": "Column Break"},
            {"fieldname": "is_default", "label": "نظام افتراضي", "fieldtype": "Check", "default": "0", "read_only": 1},
            {"fieldname": "is_mandatory", "label": "إلزامي", "fieldtype": "Check", "default": "0", "read_only": 1},

            # قسم الأوصاف
            {"fieldname": "section_desc", "fieldtype": "Section Break", "label": "الأوصاف"},
            {"fieldname": "short_description_ar", "label": "وصف قصير (عربي)", "fieldtype": "Small Text"},
            {"fieldname": "short_description_en", "label": "وصف قصير (إنجليزي)", "fieldtype": "Small Text"},
            {"fieldname": "col_break_2", "fieldtype": "Column Break"},
            {"fieldname": "long_description_ar", "label": "وصف مطول (عربي)", "fieldtype": "Text Editor"},
            {"fieldname": "long_description_en", "label": "وصف مطول (إنجليزي)", "fieldtype": "Text Editor"},

            # قسم القائمة البرمجية (JSON)
            {"fieldname": "section_config", "fieldtype": "Section Break", "label": "إعدادات القائمة"},
            {"fieldname": "default_menu_json", "label": "مصفوفة القائمة (JSON)", "fieldtype": "Code", "options": "JSON"},
            {"fieldname": "dashboard_menu", "label": "قائمة المفضلة للداشبورد (JSON)", "fieldtype": "Code", "options": "JSON"}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
            {"role": "All", "read": 1}
        ]
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()


def setup_madar_systems():
    systems_data = [
       {
    "name_ar": "نظام مدار الافتراضي",
    "name_en": "Madar Default",
    "is_default": 1,
    "is_mandatory": 1,
    "menu": [
        {"label_ar": "الرئيسية", "label_en": "Home", "type": "link", "route": "app/home", "view_type": "file", "path": "/systems/madar/home/home.html", "icon": "fa fa-home", "favorites": "0"},
        {"label_ar": "نقاط البيع", "label_en": "POS Awesome", "type": "link", "route": "app/posapp", "view_type": "frame", "path": "", "icon": "fa fa-cash-register", "favorites": "1"},
        {
            "label_ar": "الحسابات", "label_en": "Accounts", "type": "folder", "icon": "fa fa-calculator",
            "children": [
                {
                    "label_ar": "البيانات الأساسية", "label_en": "Basic Data", "type": "folder", "icon": "fa fa-folder-open",
                    "children": [
                        {"label_ar": "بيانات شركة", "label_en": "Company Info", "type": "link", "route": "app/company", "view_type": "frame", "path": "", "icon": "fa fa-building", "favorites": "0"},
                        {"label_ar": "الدليل المحاسبي", "label_en": "Chart of Accounts", "type": "link", "route": "app/account", "view_type": "frame", "path": "", "icon": "fa fa-sitemap", "favorites": "0"},
                        {"label_ar": "إعدادات الحسابات", "label_en": "Accounts Settings", "type": "link", "route": "app/accounts-settings", "view_type": "frame", "path": "", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "السنة المالية", "label_en": "Fiscal Year", "type": "link", "route": "app/fiscal-year", "view_type": "frame", "path": "", "icon": "fa fa-calendar-alt", "favorites": "0"},
                        {"label_ar": "الابعاد المحاسبية", "label_en": "Accounting Dimension", "type": "link", "route": "app/accounting-dimension", "view_type": "frame", "path": "", "icon": "fa fa-cube", "favorites": "0"},
                        {"label_ar": "دفتر الحسابات", "label_en": "Finance Book", "type": "link", "route": "app/finance-book", "view_type": "frame", "path": "", "icon": "fa fa-book", "favorites": "0"},
                        {"label_ar": "الفترات المحاسبية", "label_en": "Accounting Period", "type": "link", "route": "app/accounting-period", "view_type": "frame", "path": "", "icon": "fa fa-business-time", "favorites": "0"},
                        {"label_ar": "شروط الدفع", "label_en": "Payment Terms", "type": "link", "route": "app/terms-and-conditions", "view_type": "frame", "path": "", "icon": "fa fa-handshake", "favorites": "0"},
                        {"label_ar": "العملة", "label_en": "Currency", "type": "link", "route": "app/currency", "view_type": "frame", "path": "", "icon": "fa fa-money-bill-wave", "favorites": "0"},
                        {"label_ar": "صرف العملات", "label_en": "Currency Exchange", "type": "link", "route": "app/currency-exchange", "view_type": "frame", "path": "", "icon": "fa fa-exchange-alt", "favorites": "0"},
                        {"label_ar": "إعادة تقييم سعر الصرف", "label_en": "Exchange Rate Revaluation", "type": "link", "route": "app/exchange-rate-revaluation", "view_type": "frame", "path": "", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "مراكز التكلفة", "label_en": "Cost Centers", "type": "link", "route": "app/cost-center", "view_type": "frame", "path": "", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                        {"label_ar": "الميزانية", "label_en": "Budget", "type": "link", "route": "app/budget", "view_type": "frame", "path": "", "icon": "fa fa-wallet", "favorites": "0"},
                        {"label_ar": "البنوك", "label_en": "Banks", "type": "link", "route": "app/bank-clearance", "view_type": "frame", "path": "", "icon": "fa fa-university", "favorites": "0"},
                        {"label_ar": "حساب بنكي", "label_en": "Bank Account", "type": "link", "route": "app/bank-account", "view_type": "frame", "path": "", "icon": "fa fa-credit-card", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-cogs",
                    "children": [
                        {"label_ar": "قيود يوميه", "label_en": "Journal Entries", "type": "link", "route": "app/journal-entry", "view_type": "frame", "path": "", "icon": "fa fa-pen-square", "favorites": "0"},
                        {"label_ar": "سندات القبض و الصرف", "label_en": "Payment Entries", "type": "link", "route": "app/payment-entry", "view_type": "frame", "path": "", "icon": "fa fa-receipt", "favorites": "0"},
                        {"label_ar": "قالب قيود اليومية", "label_en": "Journal Entry Template", "type": "link", "route": "app/journal-entry-template", "view_type": "frame", "path": "", "icon": "fa fa-paste", "favorites": "0"},
                        {"label_ar": "الشروط والأحكام", "label_en": "Terms and Conditions", "type": "link", "route": "app/terms-and-conditions", "view_type": "frame", "path": "", "icon": "fa fa-file-contract", "favorites": "0"},
                        {"label_ar": "طريقة الدفع", "label_en": "Mode of Payment", "type": "link", "route": "app/mode-of-payment", "view_type": "frame", "path": "", "icon": "fa fa-money-check", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "الضرائب", "label_en": "Taxes", "type": "folder", "icon": "fa fa-percent",
                    "children": [
                        {"label_ar": "قالب الضرائب والرسوم على المبيعات", "label_en": "Sales Taxes Template", "type": "link", "route": "app/sales-taxes-and-charges-template", "view_type": "frame", "path": "", "icon": "fa fa-file-invoice-dollar", "favorites": "0"},
                        {"label_ar": "قالب الضرائب والرسوم على المشتريات", "label_en": "Purchase Taxes Template", "type": "link", "route": "app/purchase-taxes-and-charges-template", "view_type": "frame", "path": "", "icon": "fa fa-file-invoice-dollar", "favorites": "0"},
                        {"label_ar": "قالب ضريبة السلعه", "label_en": "Item Tax Template", "type": "link", "route": "app/item-tax-template", "view_type": "frame", "path": "", "icon": "fa fa-tag", "favorites": "0"},
                        {"label_ar": "الفئة الضريبية", "label_en": "Tax Category", "type": "link", "route": "app/tax-category", "view_type": "frame", "path": "", "icon": "fa fa-folder", "favorites": "0"},
                        {"label_ar": "القاعدة الضريبية", "label_en": "Tax Rule", "type": "link", "route": "app/tax-rule", "view_type": "frame", "path": "", "icon": "fa fa-gavel", "favorites": "0"},
                        {"label_ar": "فئة حجب الضرائب", "label_en": "Tax Withholding Category", "type": "link", "route": "app/tax-withholding-category", "view_type": "frame", "path": "", "icon": "fa fa-shield-alt", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير الماليه", "label_en": "Financial Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "الأستاذ العام", "label_en": "General Ledger", "type": "link", "route": "app/query-report/General%20Ledger", "view_type": "frame", "path": "", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "ميزان مراجعه", "label_en": "Trial Balance", "type": "link", "route": "app/query-report/Trial%20Balance", "view_type": "frame", "path": "", "icon": "fa fa-balance-scale", "favorites": "0"},
                        {"label_ar": "قائمة الدخل", "label_en": "Profit and Loss Statement", "type": "link", "route": "app/query-report/Profit%20and%20Loss%20Statement", "view_type": "frame", "path": "", "icon": "fa fa-chart-pie", "favorites": "0"},
                        {"label_ar": "الأرباح والخسائر", "label_en": "Gross and Net Profit Report", "type": "link", "route": "app/query-report/Gross%20and%20Net%20Profit%20Report", "view_type": "frame", "path": "", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تقرير إنحرافات الموازنة", "label_en": "Budget Variance Report", "type": "link", "route": "app/query-report/Budget%20Variance%20Report", "view_type": "frame", "path": "", "icon": "fa fa-exclamation-triangle", "favorites": "0"},
                        {"label_ar": "الميزانية العمومية", "label_en": "Balance Sheet", "type": "link", "route": "app/query-report/Balance%20Sheet", "view_type": "frame", "path": "", "icon": "fa fa-table", "favorites": "0"}
                    ]
                }
            ]
        },
        {
            "label_ar": "نظام المخازن", "label_en": "Stock System", "type": "folder", "icon": "fa fa-cubes",
            "children": [
                {
                    "label_ar": "مدخلات المخزون", "label_en": "Stock Inputs", "type": "folder", "icon": "fa fa-folder-open",
                    "children": [
                        {"label_ar": "الأصناف", "label_en": "Items", "type": "link", "route": "app/item", "view_type": "frame", "path": "", "icon": "fa fa-box", "favorites": "0"},
                        {"label_ar": "مجموعة الأصناف", "label_en": "Item Groups", "type": "link", "route": "app/item-group", "view_type": "frame", "path": "", "icon": "fa fa-boxes", "favorites": "0"},
                        {"label_ar": "الصنف البديل", "label_en": "Alternative Item", "type": "link", "route": "app/item-alternative", "view_type": "frame", "path": "", "icon": "fa fa-sync", "favorites": "0"},
                        {"label_ar": "إعدادات المخزون", "label_en": "Stock Settings", "type": "link", "route": "app/stock-settings", "view_type": "frame", "path": "", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "المخازن", "label_en": "Warehouses", "type": "link", "route": "app/warehouse", "view_type": "frame", "path": "", "icon": "fa fa-warehouse", "favorites": "0"},
                        {"label_ar": "وحدة القياس", "label_en": "UOM", "type": "link", "route": "app/uom", "view_type": "frame", "path": "", "icon": "fa fa-weight", "favorites": "0"},
                        {"label_ar": "العلامة التجارية", "label_en": "Brand", "type": "link", "route": "app/brand", "view_type": "frame", "path": "", "icon": "fa fa-trademark", "favorites": "0"},
                        {"label_ar": "عامل تحويل وحدة القياس", "label_en": "UOM Conversion Factor", "type": "link", "route": "app/uom-conversion-factor", "view_type": "frame", "path": "", "icon": "fa fa-calculator", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "عمليات المخزون", "label_en": "Stock Operations", "type": "folder", "icon": "fa fa-dolly",
                    "children": [
                        {"label_ar": "طلب مواد", "label_en": "Material Requests", "type": "link", "route": "app/material-request", "view_type": "frame", "path": "", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "مدخلات المخزون", "label_en": "Stock Entries", "type": "link", "route": "app/stock-entry", "view_type": "frame", "path": "", "icon": "fa fa-truck-loading", "favorites": "0"},
                        {"label_ar": "استلام مشتريات", "label_en": "Purchase Receipts", "type": "link", "route": "app/purchase-receipt", "view_type": "frame", "path": "", "icon": "fa fa-file-download", "favorites": "0"},
                        {"label_ar": "فحص الجودة", "label_en": "Quality Inspection", "type": "link", "route": "app/quality-inspection", "view_type": "frame", "path": "", "icon": "fa fa-check-double", "favorites": "0"},
                        {"label_ar": "قالب فحص الجودة", "label_en": "Quality Inspection Template", "type": "link", "route": "app/quality-inspection-template", "view_type": "frame", "path": "", "icon": "fa fa-clipboard-check", "favorites": "0"},
                        {"label_ar": "جرد المخزون", "label_en": "Stock Reconciliation", "type": "link", "route": "app/stock-reconciliation", "view_type": "frame", "path": "", "icon": "fa fa-tasks", "favorites": "0"},
                        {"label_ar": "الرقم التسلسلي", "label_en": "Serial No", "type": "link", "route": "app/serial-no", "view_type": "frame", "path": "", "icon": "fa fa-barcode", "favorites": "0"},
                        {"label_ar": "الدفعات", "label_en": "Batches", "type": "link", "route": "app/batch", "view_type": "frame", "path": "", "icon": "fa fa-layer-group", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-line",
                    "children": [
                        {"label_ar": "تحليلات المخازن", "label_en": "Stock Analytics", "type": "link", "route": "app/query-report/Stock%20Analytics", "view_type": "frame", "path": "", "icon": "fa fa-chart-bar", "favorites": "0"},
                        {"label_ar": "تحليل أوامر المبيعات", "label_en": "Sales Order Analysis", "type": "link", "route": "app/query-report/Sales%20Order%20Analysis", "view_type": "frame", "path": "", "icon": "fa fa-analytics", "favorites": "0"},
                        {"label_ar": "تحليل أوامر الشراء", "label_en": "Purchase Order Analysis", "type": "link", "route": "app/query-report/Purchase%20Order%20Analysis", "view_type": "frame", "path": "", "icon": "fa fa-analytics", "favorites": "0"},
                        {"label_ar": "تقرير نقص الصنف", "label_en": "Item Shortage Report", "type": "link", "route": "app/query-report/Item%20Shortage%20Report", "view_type": "frame", "path": "", "icon": "fa fa-minus-circle", "favorites": "0"},
                        {"label_ar": "أسعار الصنف", "label_en": "Item Prices", "type": "link", "route": "app/query-report/Item%20Prices", "view_type": "frame", "path": "", "icon": "fa fa-tags", "favorites": "0"},
                        {"label_ar": "سجل المخزن", "label_en": "Stock Ledger", "type": "link", "route": "app/query-report/Stock%20Ledger", "view_type": "frame", "path": "", "icon": "fa fa-history", "favorites": "0"},
                        {"label_ar": "رصيد المخزون", "label_en": "Stock Balance", "type": "link", "route": "app/query-report/Stock%20Balance", "view_type": "frame", "path": "", "icon": "fa fa-cubes", "favorites": "0"}
                    ]
                }
            ]
        },
        {
            "label_ar": "نظام المشتريات والموردين", "label_en": "Buying System", "type": "folder", "icon": "fa fa-shopping-bag",
            "children": [
                {
                    "label_ar": "البيانات الأساسية", "label_en": "Basic Data", "type": "folder", "icon": "fa fa-folder-open",
                    "children": [
                        {"label_ar": "بيانات الموردين", "label_en": "Suppliers", "type": "link", "route": "app/supplier", "view_type": "frame", "path": "", "icon": "fa fa-truck", "favorites": "0"},
                        {"label_ar": "مجموعة الموردين", "label_en": "Supplier Groups", "type": "link", "route": "app/supplier-group", "view_type": "frame", "path": "", "icon": "fa fa-users-cog", "favorites": "0"},
                        {"label_ar": "معلومات الاتصال بالموردين", "label_en": "Contacts", "type": "link", "route": "app/contact", "view_type": "frame", "path": "", "icon": "fa fa-id-card", "favorites": "0"},
                        {"label_ar": "عناوين الموردين", "label_en": "Addresses", "type": "link", "route": "app/address", "view_type": "frame", "path": "", "icon": "fa fa-map-marked-alt", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-exchange-alt",
                    "children": [
                        {"label_ar": "طلب مواد", "label_en": "Material Requests", "type": "link", "route": "app/material-request", "view_type": "frame", "path": "", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "أمر الشراء", "label_en": "Purchase Orders", "type": "link", "route": "app/purchase-order", "view_type": "frame", "path": "", "icon": "fa fa-file-shopping-bag", "favorites": "0"},
                        {"label_ar": "فاتورة شراء", "label_en": "Purchase Invoices", "type": "link", "route": "app/purchase-invoice", "view_type": "frame", "path": "", "icon": "fa fa-file-invoice", "favorites": "0"},
                        {"label_ar": "طلب عرض سعر", "label_en": "Supplier Quotations", "type": "link", "route": "app/supplier-quotation", "view_type": "frame", "path": "", "icon": "fa fa-comment-dollar", "favorites": "0"},
                        {"label_ar": "عرض سعر المورد", "label_en": "Supplier Quotation Comparison", "type": "link", "route": "app/query-report/Supplier%20Quotation%20Comparison", "view_type": "frame", "path": "", "icon": "fa fa-balance-scale", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "تحليلات المشتريات", "label_en": "Purchase Analytics", "type": "link", "route": "app/query-report/Purchase%20Analytics", "view_type": "frame", "path": "", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تحليل أوامر الشراء", "label_en": "Purchase Order Analysis", "type": "link", "route": "app/query-report/Purchase%20Order%20Analysis", "view_type": "frame", "path": "", "icon": "fa fa-table", "favorites": "0"},
                        {"label_ar": "عناوين الموردين وجهات الاتصال", "label_en": "Addresses and Contacts", "type": "link", "route": "app/address", "view_type": "frame", "path": "", "icon": "fa fa-address-book", "favorites": "0"}
                    ]
                }
            ]
        },
        {
            "label_ar": "نظام المبيعات والعملاء", "label_en": "Selling System", "type": "folder", "icon": "fa fa-users",
            "children": [
                {
                    "label_ar": "البيانات الأساسية", "label_en": "Basic Data", "type": "folder", "icon": "fa fa-folder-open",
                    "children": [
                        {"label_ar": "العملاء", "label_en": "Customers", "type": "link", "route": "app/customer", "view_type": "frame", "path": "", "icon": "fa fa-user-tag", "favorites": "0"},
                        {"label_ar": "مجموعة العملاء", "label_en": "Customer Groups", "type": "link", "route": "app/customer-group", "view_type": "frame", "path": "", "icon": "fa fa-users-cog", "favorites": "0"},
                        {"label_ar": "اعدات المبيعات", "label_en": "Selling Settings", "type": "link", "route": "app/selling-settings", "view_type": "frame", "path": "", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "الأصناف", "label_en": "Items", "type": "link", "route": "app/item", "view_type": "frame", "path": "", "icon": "fa fa-box", "favorites": "0"},
                        {"label_ar": "مجموعة الأصناف", "label_en": "Item Groups", "type": "link", "route": "app/item-group", "view_type": "frame", "path": "", "icon": "fa fa-boxes", "favorites": "0"},
                        {"label_ar": "قائمة الأسعار", "label_en": "Price Lists", "type": "link", "route": "app/price-list", "view_type": "frame", "path": "", "icon": "fa fa-list-ol", "favorites": "0"},
                        {"label_ar": "سعر الأصناف", "label_en": "Item Prices", "type": "link", "route": "app/item-price", "view_type": "frame", "path": "", "icon": "fa fa-tags", "favorites": "0"},
                        {"label_ar": "جهات الاتصال", "label_en": "Contacts", "type": "link", "route": "app/contact", "view_type": "frame", "path": "", "icon": "fa fa-id-card", "favorites": "0"},
                        {"label_ar": "عناوين الموردين", "label_en": "Addresses", "type": "link", "route": "app/address", "view_type": "frame", "path": "", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                        {"label_ar": "الأقاليم", "label_en": "Territories", "type": "link", "route": "app/territory", "view_type": "frame", "path": "", "icon": "fa fa-globe-asia", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-hand-holding-usd",
                    "children": [
                        {"label_ar": "عرض سعر", "label_en": "Quotations", "type": "link", "route": "app/quotation", "view_type": "frame", "path": "", "icon": "fa fa-comment-dollar", "favorites": "0"},
                        {"label_ar": "امر بيع", "label_en": "Blanket Orders", "type": "link", "route": "app/blanket-order", "view_type": "frame", "path": "", "icon": "fa fa-file-contract", "favorites": "0"},
                        {"label_ar": "فاتورة مبيعات", "label_en": "Sales Invoice", "type": "link", "route": "app/sales-invoice/new-sales-invoice-1", "view_type": "frame", "path": "", "icon": "fa fa-file-invoice-dollar", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "إعدادات البيع", "label_en": "Selling Settings", "type": "folder", "icon": "fa fa-cog",
                    "children": [
                        {"label_ar": "قالب الشروط والأحكام", "label_en": "Terms and Conditions Template", "type": "link", "route": "app/terms-and-conditions", "view_type": "frame", "path": "", "icon": "fa fa-file-signature", "favorites": "0"},
                        {"label_ar": "قالب الضرائب والرسوم على المبيعات", "label_en": "Sales Taxes Template", "type": "link", "route": "app/sales-taxes-and-charges-template", "view_type": "frame", "path": "", "icon": "fa fa-percent", "favorites": "0"},
                        {"label_ar": "مصدر الزبون المحتمل", "label_en": "Lead Source", "type": "link", "route": "app/lead-source", "view_type": "frame", "path": "", "icon": "fa fa-search-location", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقاير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "تحليل المبيعات", "label_en": "Sales Analytics", "type": "link", "route": "app/query-report/Sales%20Analytics", "view_type": "frame", "path": "", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تحليل أوامر المبيعات", "label_en": "Sales Order Analysis", "type": "link", "route": "app/query-report/Sales%20Order%20Analysis", "view_type": "frame", "path": "", "icon": "fa fa-table", "favorites": "0"},
                        {"label_ar": "العملاء الغير النشطين", "label_en": "Inactive Customers", "type": "link", "route": "app/query-report/Inactive%20Customers", "view_type": "frame", "path": "", "icon": "fa fa-user-slash", "favorites": "0"},
                        {"label_ar": "ملخص المبيعات بناء على رجل المبيعات", "label_en": "Sales Person Transaction Summary", "type": "link", "route": "app/query-report/Sales%20Person-wise%20Transaction%20Summary", "view_type": "frame", "path": "", "icon": "fa fa-user-friends", "favorites": "0"},
                        {"label_ar": "الحركة التاريخية للمبيعات وفقاً للصنف", "label_en": "Item-wise Sales History", "type": "link", "route": "app/query-report/Item-wise%20Sales%20History", "view_type": "frame", "path": "", "icon": "fa fa-history", "favorites": "0"},
                        {"label_ar": "عناوين العملاء وجهات الإتصال", "label_en": "Address and Contacts", "type": "link", "route": "app/query-report/Address%20And%20Contacts", "view_type": "frame", "path": "", "icon": "fa fa-address-book", "favorites": "0"},
                        {"label_ar": "المخزون المتاج للأصناف المعبأة", "label_en": "Available Stock for Packing Items", "type": "link", "route": "app/query-report/Available%20Stock%20for%20Packing%20Items", "view_type": "frame", "path": "", "icon": "fa fa-box-open", "favorites": "0"},
                        {"label_ar": "اصناف كتيرة معلقة لطلب الشراء", "label_en": "Pending SO Items For Purchase Request", "type": "link", "route": "app/query-report/Pending%20SO%20Items%20For%20Purchase%20Request", "view_type": "frame", "path": "", "icon": "fa fa-hourglass-half", "favorites": "0"},
                        {"label_ar": "رصيد العميل", "label_en": "Customer Credit Balance", "type": "link", "route": "app/query-report/Customer%20Credit%20Balance", "view_type": "frame", "path": "", "icon": "fa fa-dollar-sign", "favorites": "0"}
                    ]
                }
            ]
        },
        {
            "label_ar": "الاصــــول", "label_en": "Assets", "type": "folder", "icon": "fa fa-boxes",
            "children": [
                {"label_ar": "بيانات الأصل", "label_en": "Asset Details", "type": "link", "route": "app/asset", "view_type": "frame", "path": "", "icon": "fa fa-barcode", "favorites": "0"},
                {"label_ar": "الموقع", "label_en": "Locations", "type": "link", "route": "app/location", "view_type": "frame", "path": "", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                {"label_ar": "تصنيف الأصول", "label_en": "Asset Category", "type": "link", "route": "app/asset-category", "view_type": "frame", "path": "", "icon": "fa fa-folder-open", "favorites": "0"},
                {"label_ar": "حركة الأصول", "label_en": "Asset Movement", "type": "link", "route": "app/asset-movement", "view_type": "frame", "path": "", "icon": "fa fa-dolly-flatbed", "favorites": "0"},
                {"label_ar": "فريق الصيانة", "label_en": "Asset Maintenance Team", "type": "link", "route": "app/asset-maintenance-team", "view_type": "frame", "path": "", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "صيانة الأصول", "label_en": "Asset Maintenance", "type": "link", "route": "app/asset-maintenance", "view_type": "frame", "path": "", "icon": "fa fa-tools", "favorites": "0"},
                {"label_ar": "سجل صيانة الأصول", "label_en": "Asset Maintenance Log", "type": "link", "route": "app/asset-maintenance-log", "view_type": "frame", "path": "", "icon": "fa fa-clipboard-list", "favorites": "0"},
                {"label_ar": "تعديل قيمة أصل", "label_en": "Asset Value Adjustment", "type": "link", "route": "app/asset-value-adjustment", "view_type": "frame", "path": "", "icon": "fa fa-adjust", "favorites": "0"},
                {"label_ar": "إصلاح الأصول", "label_en": "Asset Repair", "type": "link", "route": "app/asset-repair", "view_type": "frame", "path": "", "icon": "fa fa-wrench", "favorites": "0"},
                {"label_ar": "تقرير دفتر حسابات استهلاك الأصول", "label_en": "Asset Depreciation Ledger", "type": "link", "route": "app/query-report/Asset%20Depreciation%20Ledger?", "view_type": "frame", "path": "", "icon": "fa fa-book-open", "favorites": "0"},
                {"label_ar": "تقرير استهلاك الأصول والأرصدة", "label_en": "Asset Depreciations and Balances", "type": "link", "route": "app/query-report/Asset%20Depreciations%20and%20Balances?", "view_type": "frame", "path": "", "icon": "fa fa-calculator", "favorites": "0"}
            ]
        },
        {
            "label_ar": "المستخدمين", "label_en": "Users", "type": "folder", "icon": "fa fa-user-shield",
            "children": [
                {"label_ar": "المستخدمين", "label_en": "Users List", "type": "link", "route": "app/user", "view_type": "frame", "path": "", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "الأدوار و المهام", "label_en": "Roles and Permissions", "type": "link", "route": "app/role", "view_type": "frame", "path": "", "icon": "fa fa-user-tag", "favorites": "0"},
                {"label_ar": "مدير صلاحيات", "label_en": "Permission Manager", "type": "link", "route": "app/permission-manager", "view_type": "frame", "path": "", "icon": "fa fa-lock-open", "favorites": "0"}
            ]
        },
        {
            "label_ar": "الاعدادات", "label_en": "Settings", "type": "folder", "icon": "fa fa-cog",
            "children": [
                {"label_ar": "المستخدمين", "label_en": "System Settings", "type": "link", "route": "app/system-settings", "view_type": "frame", "path": "", "icon": "fa fa-sliders-h", "favorites": "0"},
                {"label_ar": "إعدادات الحسابات", "label_en": "Accounts Settings", "type": "link", "route": "app/accounts-settings", "view_type": "frame", "path": "", "icon": "fa fa-calculator", "favorites": "0"},
                {"label_ar": "إعدادات المخازن", "label_en": "Stock Settings", "type": "link", "route": "app/stock-settings", "view_type": "frame", "path": "", "icon": "fa fa-cubes", "favorites": "0"},
                {"label_ar": "إعدادات المبيعات", "label_en": "Selling Settings", "type": "link", "route": "app/selling-settings", "view_type": "frame", "path": "", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "إعدادات المشتريات", "label_en": "Buying Settings", "type": "link", "route": "app/buying-settings", "view_type": "frame", "path": "", "icon": "fa fa-shopping-bag", "favorites": "0"},
                {"label_ar": "الإعدادات العامة", "label_en": "Global Defaults", "type": "link", "route": "app/global-defaults", "view_type": "frame", "path": "", "icon": "fa fa-globe", "favorites": "0"}
            ]
        }
    ]
}
    ]
    for sys in systems_data:
        sys["dashboard_menu"] = [{"label_ar": "قيد محاسبي ", "label_en": "Journal Entries", "type": "link", "route": "app/journal-entry", "view_type": "file", "path": "/systems/madar/accounts/journal-entry.html", "icon": "fa fa-book", "favorites": "1"}, {"label_ar": " سند قبض/ صرف", "label_en": "Payment Entries", "type": "link", "route": "app/payment-entry", "view_type": "file", "path": "/systems/madar/accounts/payment-entry.html", "icon": "fa fa-money-check-alt", "favorites": "1"}, {"label_ar": "الدليل المحاسبي", "label_en": "Chart of Accounts", "type": "link", "route": "app/account", "view_type": "file", "path": "/systems/madar/accounts/chart-of-accounts.html", "icon": "fa fa-sitemap", "favorites": "1"}, {"label_ar": "فاتورة مشتريات ", "label_en": "Purchase Invoices", "type": "link", "route": "app/purchase-invoice", "view_type": "file", "path": "/systems/madar/buying/purchase-invoice.html", "icon": "fa fa-file-invoice", "favorites": "1"}, {"label_ar": "فاتورة مبيعات", "label_en": "Sales Invoice", "type": "link", "route": "app/sales-invoice", "view_type": "file", "path": "/systems/madar/selling/new-sales-invoice.html", "icon": "fa fa-file-invoice-dollar", "favorites": "1"}, {"label_ar": "عميل", "label_en": "Customers", "type": "link", "route": "app/customer", "view_type": "file", "path": "/systems/madar/selling/customers.html", "icon": "fa fa-users", "favorites": "1"}, {"label_ar": "مورد ", "label_en": "Suppliers", "type": "link", "route": "app/supplier", "view_type": "file", "path": "/systems/madar/buying/suppliers.html", "icon": "fa fa-truck-loading", "favorites": "1"}, {"label_ar": "الأصناف", "label_en": "Items", "type": "link", "route": "app/item", "view_type": "file", "path": "/systems/madar/selling/items.html", "icon": "fa fa-boxes", "favorites": "1"}, {"label_ar": "صرف العملات", "label_en": "Currency Exchange", "type": "link", "route": "app/currency-exchange", "view_type": "file", "path": "/systems/madar/accounts/currency-exchange.html", "icon": "fa fa-exchange-alt", "favorites": "1"}, {"label_ar": "الأستاذ العام", "label_en": "General Ledger", "type": "link", "route": "app/query-report/General%20Ledger", "view_type": "file", "path": "/systems/madar/accounts/reports/general-ledger.html", "icon": "fa fa-book-open", "favorites": "1"}, {"label_ar": "ميزان مراجعه", "label_en": "Trial Balance", "type": "link", "route": "app/query-report/Trial%20Balance", "view_type": "file", "path": "/systems/madar/accounts/reports/trial-balance.html", "icon": "fa fa-balance-scale", "favorites": "1"}, {"label_ar": "نقاط البيع", "label_en": "POS Awesome", "type": "link", "route": "app/posapp", "view_type": "frame", "path": "", "icon": "fa fa-cash-register", "favorites": "1"}]

        if not frappe.db.exists("Madar System", {"system_name_en": sys["name_en"]}):
            doc = frappe.get_doc({
                "doctype": "Madar System",
                "system_name_ar": sys.get("name_ar", "نظام مدار"),
                "system_name_en": sys["name_en"],
                "is_default": sys["is_default"],
                "is_mandatory": sys["is_mandatory"],
                "default_menu_json": json.dumps(sys["menu"], ensure_ascii=False),
                "dashboard_menu": json.dumps(sys["dashboard_menu"], ensure_ascii=False)
            })
            doc.insert(ignore_permissions=True)
        else:
            doc = frappe.get_doc("Madar System", {"system_name_en": sys["name_en"]})
            doc.default_menu_json = json.dumps(sys["menu"], ensure_ascii=False)
            doc.dashboard_menu = json.dumps(sys["dashboard_menu"], ensure_ascii=False)
            doc.is_default = sys.get("is_default", 0)
            doc.is_mandatory = sys.get("is_mandatory", 0)
            doc.save(ignore_permissions=True)
    
    frappe.db.commit()
    print("تم إنشاء نظام مدار الافتراضي بنجاح.")

def create_user_preference_doctype():
    doctype_name = "Madar User Preference"
    
    if frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc("DocType", doctype_name)
        has_field = any(f.fieldname == "dashboard_menu" for f in doc.fields)
        if not has_field:
            doc.append("fields", {
                "fieldname": "dashboard_menu",
                "label": "قائمة المفضلة للداشبورد (JSON)",
                "fieldtype": "Code",
                "options": "JSON"
            })
            doc.save(ignore_permissions=True)
        return

    if not frappe.db.exists("DocType", doctype_name):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": doctype_name,
            "module": "Madar",
            "custom": 1,
            "autoname": "field:user",
            "fields": [
                {
                    "fieldname": "user",
                    "label": "المستخدم",
                    "fieldtype": "Link",
                    "options": "User",
                    "unique": 1,
                    "reqd": 1
                },
                # النظام يحدد التخطيط (Layout) والقائمة الافتراضية
                {"fieldname": "current_system", "label": "النظام الحالي", "fieldtype": "Link", "options": "Madar System", "reqd": 1},
                
                # إذا وجد بيانات هنا، نعتمدها بدلاً من قائمة النظام
                {"fieldname": "custom_menu_json", "label": "القائمة المخصصة (JSON)", "fieldtype": "Code", "options": "JSON"},
                
                # مصفوفة المفضلة (JSON)
                {"fieldname": "dashboard_menu", "label": "قائمة المفضلة للداشبورد (JSON)", "fieldtype": "Code", "options": "JSON"},
                
                # إعدادات الواجهة الرسومية
                {"fieldname": "madar_theme", "label": "الثيم المفضل", "fieldtype": "Link", "options": "Madar Theme"},
                {"fieldname": "madar_font", "label": "الخط المفضل", "fieldtype": "Link", "options": "Madar Font"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "All", "read": 1, "write": 1, "create": 1}
            ]
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
def run_setup():
    # verify_app_license() # <-- الصافرة هنا
    print("بدء عملية التأسيس...")
    
    # 1. إنشاء الدوكتايب أولاً
    create_madar_system_doctype()
    
    # 2. إنشاء الأنظمة الافتراضية ثانياً
    setup_madar_systems()
    
    # 3. إنشاء دوكتايب تفضيلات المستخدم (الذي سنضيفه الآن)
    create_user_preference_doctype()
    
    print("اكتملت عملية التأسيس بنجاح!")