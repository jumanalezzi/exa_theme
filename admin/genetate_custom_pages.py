import os

# 1. مصفوفة الأنظمة الكاملة (تأكد من دمج مصفوفتي فوترة ورؤى بالكامل هنا)
systems_data = [
    {
    "name_ar": "نظام فوترة",
    "name_en": "Fotarh System",
    "is_default": 0,
    "is_mandatory": 0,
    "menu": [
        {"label_ar": "الرئيسية", "label_en": "Home", "type": "link", "route": "app/home", "view_type": "file", "path": "/systems/fotarh/home/home.html", "icon": "fa fa-home", "favorites": "0"},
        {
            "label_ar": "الحسابات", "label_en": "Accounts", "type": "folder", "icon": "fa fa-calculator",
            "children": [
                {
                    "label_ar": "البيانات الأساسية", "label_en": "Basic Data", "type": "folder", "icon": "fa fa-folder-open",
                    "children": [
                        {"label_ar": "بيانات شركة", "label_en": "Company Info", "type": "link", "route": "app/company", "view_type": "file", "path": "/systems/fotarh/accounts/company.html", "icon": "fa fa-building", "favorites": "0"},
                        {"label_ar": "الدليل المحاسبي", "label_en": "Chart of Accounts", "type": "link", "route": "app/account", "view_type": "file", "path": "/systems/fotarh/accounts/chart-of-accounts.html", "icon": "fa fa-sitemap", "favorites": "0"},
                        {"label_ar": "إعدادات الحسابات", "label_en": "Accounts Settings", "type": "link", "route": "app/accounts-settings", "view_type": "file", "path": "/systems/fotarh/accounts/accounts-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "السنة المالية", "label_en": "Fiscal Year", "type": "link", "route": "app/fiscal-year", "view_type": "file", "path": "/systems/fotarh/accounts/fiscal-year.html", "icon": "fa fa-calendar-alt", "favorites": "0"},
                        {"label_ar": "الابعاد المحاسبية", "label_en": "Accounting Dimension", "type": "link", "route": "app/accounting-dimension", "view_type": "file", "path": "/systems/fotarh/accounts/accounting-dimension.html", "icon": "fa fa-cube", "favorites": "0"},
                        {"label_ar": "دفتر الحسابات", "label_en": "Finance Book", "type": "link", "route": "app/finance-book", "view_type": "file", "path": "/systems/fotarh/accounts/finance-book.html", "icon": "fa fa-book", "favorites": "0"},
                        {"label_ar": "الفترات المحاسبية", "label_en": "Accounting Period", "type": "link", "route": "app/accounting-period", "view_type": "file", "path": "/systems/fotarh/accounts/accounting-period.html", "icon": "fa fa-business-time", "favorites": "0"},
                        {"label_ar": "شروط الدفع", "label_en": "Payment Terms", "type": "link", "route": "app/terms-and-conditions", "view_type": "file", "path": "/systems/fotarh/accounts/payment-terms.html", "icon": "fa fa-handshake", "favorites": "0"},
                        {"label_ar": "العملة", "label_en": "Currency", "type": "link", "route": "app/currency", "view_type": "file", "path": "/systems/fotarh/accounts/currency.html", "icon": "fa fa-money-bill-wave", "favorites": "0"},
                        {"label_ar": "صرف العملات", "label_en": "Currency Exchange", "type": "link", "route": "app/currency-exchange", "view_type": "file", "path": "/systems/fotarh/accounts/currency-exchange.html", "icon": "fa fa-exchange-alt", "favorites": "0"},
                        {"label_ar": "إعادة تقييم سعر الصرف", "label_en": "Exchange Rate Revaluation", "type": "link", "route": "app/exchange-rate-revaluation", "view_type": "file", "path": "/systems/fotarh/accounts/exchange-revaluation.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "مراكز التكلفة", "label_en": "Cost Centers", "type": "link", "route": "app/cost-center", "view_type": "file", "path": "/systems/fotarh/accounts/cost-center.html", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                        {"label_ar": "الميزانية", "label_en": "Budget", "type": "link", "route": "app/budget", "view_type": "file", "path": "/systems/fotarh/accounts/budget.html", "icon": "fa fa-wallet", "favorites": "0"},
                        {"label_ar": "البنوك", "label_en": "Banks", "type": "link", "route": "app/bank-clearance", "view_type": "file", "path": "/systems/fotarh/accounts/banks.html", "icon": "fa fa-university", "favorites": "0"},
                        {"label_ar": "حساب بنكي", "label_en": "Bank Account", "type": "link", "route": "app/bank-account", "view_type": "file", "path": "/systems/fotarh/accounts/bank-account.html", "icon": "fa fa-credit-card", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-cogs",
                    "children": [
                        {"label_ar": "قيود يوميه", "label_en": "Journal Entries", "type": "link", "route": "app/journal-entry", "view_type": "file", "path": "/systems/fotarh/accounts/journal-entry.html", "icon": "fa fa-pen-square", "favorites": "0"},
                        {"label_ar": "سندات القبض و الصرف", "label_en": "Payment Entries", "type": "link", "route": "app/payment-entry", "view_type": "file", "path": "/systems/fotarh/accounts/payment-entry.html", "icon": "fa fa-receipt", "favorites": "0"},
                        {"label_ar": "قالب قيود اليومية", "label_en": "Journal Entry Template", "type": "link", "route": "app/journal-entry-template", "view_type": "file", "path": "/systems/fotarh/accounts/journal-entry-template.html", "icon": "fa fa-paste", "favorites": "0"},
                        {"label_ar": "الشروط والأحكام", "label_en": "Terms and Conditions", "type": "link", "route": "app/terms-and-conditions", "view_type": "file", "path": "/systems/fotarh/accounts/terms-conditions.html", "icon": "fa fa-file-contract", "favorites": "0"},
                        {"label_ar": "طريقة الدفع", "label_en": "Mode of Payment", "type": "link", "route": "app/mode-of-payment", "view_type": "file", "path": "/systems/fotarh/accounts/mode-of-payment.html", "icon": "fa fa-money-check", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "الضرائب", "label_en": "Taxes", "type": "folder", "icon": "fa fa-percent",
                    "children": [
                        {"label_ar": "قالب الضرائب والرسوم على المبيعات", "label_en": "Sales Taxes Template", "type": "link", "route": "app/sales-taxes-and-charges-template", "view_type": "file", "path": "/systems/fotarh/accounts/sales-taxes-template.html", "icon": "fa fa-file-invoice-dollar", "favorites": "0"},
                        {"label_ar": "قالب الضرائب والرسوم على المشتريات", "label_en": "Purchase Taxes Template", "type": "link", "route": "app/purchase-taxes-and-charges-template", "view_type": "file", "path": "/systems/fotarh/accounts/purchase-taxes-template.html", "icon": "fa fa-file-invoice-dollar", "favorites": "0"},
                        {"label_ar": "قالب ضريبة السلعه", "label_en": "Item Tax Template", "type": "link", "route": "app/item-tax-template", "view_type": "file", "path": "/systems/fotarh/accounts/item-tax-template.html", "icon": "fa fa-tag", "favorites": "0"},
                        {"label_ar": "الفئة الضريبية", "label_en": "Tax Category", "type": "link", "route": "app/tax-category", "view_type": "file", "path": "/systems/fotarh/accounts/tax-category.html", "icon": "fa fa-folder", "favorites": "0"},
                        {"label_ar": "القاعدة الضريبية", "label_en": "Tax Rule", "type": "link", "route": "app/tax-rule", "view_type": "file", "path": "/systems/fotarh/accounts/tax-rule.html", "icon": "fa fa-gavel", "favorites": "0"},
                        {"label_ar": "فئة حجب الضرائب", "label_en": "Tax Withholding Category", "type": "link", "route": "app/tax-withholding-category", "view_type": "file", "path": "/systems/fotarh/accounts/tax-withholding.html", "icon": "fa fa-shield-alt", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير الماليه", "label_en": "Financial Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "الأستاذ العام", "label_en": "General Ledger", "type": "link", "route": "app/query-report/General%20Ledger", "view_type": "file", "path": "/systems/fotarh/accounts/reports/general-ledger.html", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "ميزان مراجعه", "label_en": "Trial Balance", "type": "link", "route": "app/query-report/Trial%20Balance", "view_type": "file", "path": "/systems/fotarh/accounts/reports/trial-balance.html", "icon": "fa fa-balance-scale", "favorites": "0"},
                        {"label_ar": "قائمة الدخل", "label_en": "Profit and Loss Statement", "type": "link", "route": "app/query-report/Profit%20and%20Loss%20Statement", "view_type": "file", "path": "/systems/fotarh/accounts/reports/profit-loss.html", "icon": "fa fa-chart-pie", "favorites": "0"},
                        {"label_ar": "الأرباح والخسائر", "label_en": "Gross and Net Profit Report", "type": "link", "route": "app/query-report/Gross%20and%20Net%20Profit%20Report", "view_type": "file", "path": "/systems/fotarh/accounts/reports/gross-and-net-profit.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تقرير إنحرافات الموازنة", "label_en": "Budget Variance Report", "type": "link", "route": "app/query-report/Budget%20Variance%20Report", "view_type": "file", "path": "/systems/fotarh/accounts/reports/budget-variance.html", "icon": "fa fa-exclamation-triangle", "favorites": "0"},
                        {"label_ar": "الميزانية العمومية", "label_en": "Balance Sheet", "type": "link", "route": "app/query-report/Balance%20Sheet", "view_type": "file", "path": "/systems/fotarh/accounts/reports/balance-sheet.html", "icon": "fa fa-table", "favorites": "0"}
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
                        {"label_ar": "الأصناف", "label_en": "Items", "type": "link", "route": "app/item", "view_type": "file", "path": "/systems/fotarh/stock/items.html", "icon": "fa fa-box", "favorites": "0"},
                        {"label_ar": "مجموعة الأصناف", "label_en": "Item Groups", "type": "link", "route": "app/item-group", "view_type": "file", "path": "/systems/fotarh/stock/item-groups.html", "icon": "fa fa-boxes", "favorites": "0"},
                        {"label_ar": "الصنف البديل", "label_en": "Alternative Item", "type": "link", "route": "app/item-alternative", "view_type": "file", "path": "/systems/fotarh/stock/item-alternative.html", "icon": "fa fa-sync", "favorites": "0"},
                        {"label_ar": "إعدادات المخزون", "label_en": "Stock Settings", "type": "link", "route": "app/stock-settings", "view_type": "file", "path": "/systems/fotarh/stock/stock-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "المخازن", "label_en": "Warehouses", "type": "link", "route": "app/warehouse", "view_type": "file", "path": "/systems/fotarh/stock/warehouses.html", "icon": "fa fa-warehouse", "favorites": "0"},
                        {"label_ar": "وحدة القياس", "label_en": "UOM", "type": "link", "route": "app/uom", "view_type": "file", "path": "/systems/fotarh/stock/uom.html", "icon": "fa fa-weight", "favorites": "0"},
                        {"label_ar": "العلامة التجارية", "label_en": "Brand", "type": "link", "route": "app/brand", "view_type": "file", "path": "/systems/fotarh/stock/brand.html", "icon": "fa fa-trademark", "favorites": "0"},
                        {"label_ar": "عامل تحويل وحدة القياس", "label_en": "UOM Conversion Factor", "type": "link", "route": "app/uom-conversion-factor", "view_type": "file", "path": "/systems/fotarh/stock/uom-conversion.html", "icon": "fa fa-calculator", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "عمليات المخزون", "label_en": "Stock Operations", "type": "folder", "icon": "fa fa-dolly",
                    "children": [
                        {"label_ar": "طلب مواد", "label_en": "Material Requests", "type": "link", "route": "app/material-request", "view_type": "file", "path": "/systems/fotarh/stock/material-request.html", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "مدخلات المخزون", "label_en": "Stock Entries", "type": "link", "route": "app/stock-entry", "view_type": "file", "path": "/systems/fotarh/stock/stock-entry.html", "icon": "fa fa-truck-loading", "favorites": "0"},
                        {"label_ar": "استلام مشتريات", "label_en": "Purchase Receipts", "type": "link", "route": "app/purchase-receipt", "view_type": "file", "path": "/systems/fotarh/stock/purchase-receipt.html", "icon": "fa fa-file-download", "favorites": "0"},
                        {"label_ar": "فحص الجودة", "label_en": "Quality Inspection", "type": "link", "route": "app/quality-inspection", "view_type": "file", "path": "/systems/fotarh/stock/quality-inspection.html", "icon": "fa fa-check-double", "favorites": "0"},
                        {"label_ar": "قالب فحص الجودة", "label_en": "Quality Inspection Template", "type": "link", "route": "app/quality-inspection-template", "view_type": "file", "path": "/systems/fotarh/stock/quality-template.html", "icon": "fa fa-clipboard-check", "favorites": "0"},
                        {"label_ar": "جرد المخزون", "label_en": "Stock Reconciliation", "type": "link", "route": "app/stock-reconciliation", "view_type": "file", "path": "/systems/fotarh/stock/stock-reconciliation.html", "icon": "fa fa-tasks", "favorites": "0"},
                        {"label_ar": "الرقم التسلسلي", "label_en": "Serial No", "type": "link", "route": "app/serial-no", "view_type": "file", "path": "/systems/fotarh/stock/serial-no.html", "icon": "fa fa-barcode", "favorites": "0"},
                        {"label_ar": "الدفعات", "label_en": "Batches", "type": "link", "route": "app/batch", "view_type": "file", "path": "/systems/fotarh/stock/batches.html", "icon": "fa fa-layer-group", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-line",
                    "children": [
                        {"label_ar": "تحليلات المخازن", "label_en": "Stock Analytics", "type": "link", "route": "app/query-report/Stock%20Analytics", "view_type": "file", "path": "/systems/fotarh/stock/reports/stock-analytics.html", "icon": "fa fa-chart-bar", "favorites": "0"},
                        {"label_ar": "تحليل أوامر المبيعات", "label_en": "Sales Order Analysis", "type": "link", "route": "app/query-report/Sales%20Order%20Analysis", "view_type": "file", "path": "/systems/fotarh/stock/reports/sales-order-analysis.html", "icon": "fa fa-analytics", "favorites": "0"},
                        {"label_ar": "تحليل أوامر الشراء", "label_en": "Purchase Order Analysis", "type": "link", "route": "app/query-report/Purchase%20Order%20Analysis", "view_type": "file", "path": "/systems/fotarh/stock/reports/purchase-order-analysis.html", "icon": "fa fa-analytics", "favorites": "0"},
                        {"label_ar": "تقرير نقص الصنف", "label_en": "Item Shortage Report", "type": "link", "route": "app/query-report/Item%20Shortage%20Report", "view_type": "file", "path": "/systems/fotarh/stock/reports/item-shortage.html", "icon": "fa fa-minus-circle", "favorites": "0"},
                        {"label_ar": "أسعار الصنف", "label_en": "Item Prices", "type": "link", "route": "app/query-report/Item%20Prices", "view_type": "file", "path": "/systems/fotarh/stock/reports/item-prices.html", "icon": "fa fa-tags", "favorites": "0"},
                        {"label_ar": "سجل المخزن", "label_en": "Stock Ledger", "type": "link", "route": "app/query-report/Stock%20Ledger", "view_type": "file", "path": "/systems/fotarh/stock/reports/stock-ledger.html", "icon": "fa fa-history", "favorites": "0"},
                        {"label_ar": "رصيد المخزون", "label_en": "Stock Balance", "type": "link", "route": "app/query-report/Stock%20Balance", "view_type": "file", "path": "/systems/fotarh/stock/reports/stock-balance.html", "icon": "fa fa-cubes", "favorites": "0"}
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
                        {"label_ar": "بيانات الموردين", "label_en": "Suppliers", "type": "link", "route": "app/supplier", "view_type": "file", "path": "/systems/fotarh/buying/suppliers.html", "icon": "fa fa-truck", "favorites": "0"},
                        {"label_ar": "مجموعة الموردين", "label_en": "Supplier Groups", "type": "link", "route": "app/supplier-group", "view_type": "file", "path": "/systems/fotarh/buying/supplier-groups.html", "icon": "fa fa-users-cog", "favorites": "0"},
                        {"label_ar": "معلومات الاتصال بالموردين", "label_en": "Contacts", "type": "link", "route": "app/contact", "view_type": "file", "path": "/systems/fotarh/buying/contacts.html", "icon": "fa fa-id-card", "favorites": "0"},
                        {"label_ar": "عناوين الموردين", "label_en": "Addresses", "type": "link", "route": "app/address", "view_type": "file", "path": "/systems/fotarh/buying/addresses.html", "icon": "fa fa-map-marked-alt", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-exchange-alt",
                    "children": [
                        {"label_ar": "طلب مواد", "label_en": "Material Requests", "type": "link", "route": "app/material-request", "view_type": "file", "path": "/systems/fotarh/buying/material-request.html", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "أمر الشراء", "label_en": "Purchase Orders", "type": "link", "route": "app/purchase-order", "view_type": "file", "path": "/systems/fotarh/buying/purchase-order.html", "icon": "fa fa-file-shopping-bag", "favorites": "0"},
                        {"label_ar": "فاتورة شراء", "label_en": "Purchase Invoices", "type": "link", "route": "app/purchase-invoice", "view_type": "file", "path": "/systems/fotarh/buying/purchase-invoice.html", "icon": "fa fa-file-invoice", "favorites": "0"},
                        {"label_ar": "طلب عرض سعر", "label_en": "Supplier Quotations", "type": "link", "route": "app/supplier-quotation", "view_type": "file", "path": "/systems/fotarh/buying/supplier-quotation.html", "icon": "fa fa-comment-dollar", "favorites": "0"},
                        {"label_ar": "عرض سعر المورد", "label_en": "Supplier Quotation Comparison", "type": "link", "route": "app/query-report/Supplier%20Quotation%20Comparison", "view_type": "file", "path": "/systems/fotarh/buying/quotation-comparison.html", "icon": "fa fa-balance-scale", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "تحليلات المشتريات", "label_en": "Purchase Analytics", "type": "link", "route": "app/query-report/Purchase%20Analytics", "view_type": "file", "path": "/systems/fotarh/buying/reports/purchase-analytics.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تحليل أوامر الشراء", "label_en": "Purchase Order Analysis", "type": "link", "route": "app/query-report/Purchase%20Order%20Analysis", "view_type": "file", "path": "/systems/fotarh/buying/reports/purchase-order-analysis.html", "icon": "fa fa-table", "favorites": "0"},
                        {"label_ar": "عناوين الموردين وجهات الاتصال", "label_en": "Addresses and Contacts", "type": "link", "route": "app/address", "view_type": "file", "path": "/systems/fotarh/buying/reports/addresses-contacts.html", "icon": "fa fa-address-book", "favorites": "0"}
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
                        {"label_ar": "العملاء", "label_en": "Customers", "type": "link", "route": "app/customer", "view_type": "file", "path": "/systems/fotarh/selling/customers.html", "icon": "fa fa-user-tag", "favorites": "0"},
                        {"label_ar": "مجموعة العملاء", "label_en": "Customer Groups", "type": "link", "route": "app/customer-group", "view_type": "file", "path": "/systems/fotarh/selling/customer-groups.html", "icon": "fa fa-users-cog", "favorites": "0"},
                        {"label_ar": "اعدات المبيعات", "label_en": "Selling Settings", "type": "link", "route": "app/selling-settings", "view_type": "file", "path": "/systems/fotarh/selling/selling-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "الأصناف", "label_en": "Items", "type": "link", "route": "app/item", "view_type": "file", "path": "/systems/fotarh/selling/items.html", "icon": "fa fa-box", "favorites": "0"},
                        {"label_ar": "مجموعة الأصناف", "label_en": "Item Groups", "type": "link", "route": "app/item-group", "view_type": "file", "path": "/systems/fotarh/selling/item-groups.html", "icon": "fa fa-boxes", "favorites": "0"},
                        {"label_ar": "قائمة الأسعار", "label_en": "Price Lists", "type": "link", "route": "app/price-list", "view_type": "file", "path": "/systems/fotarh/selling/price-lists.html", "icon": "fa fa-list-ol", "favorites": "0"},
                        {"label_ar": "سعر الأصناف", "label_en": "Item Prices", "type": "link", "route": "app/item-price", "view_type": "file", "path": "/systems/fotarh/selling/item-prices.html", "icon": "fa fa-tags", "favorites": "0"},
                        {"label_ar": "جهات الاتصال", "label_en": "Contacts", "type": "link", "route": "app/contact", "view_type": "file", "path": "/systems/fotarh/selling/contacts.html", "icon": "fa fa-id-card", "favorites": "0"},
                        {"label_ar": "عناوين الموردين", "label_en": "Addresses", "type": "link", "route": "app/address", "view_type": "file", "path": "/systems/fotarh/selling/addresses.html", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                        {"label_ar": "الأقاليم", "label_en": "Territories", "type": "link", "route": "app/territory", "view_type": "file", "path": "/systems/fotarh/selling/territories.html", "icon": "fa fa-globe-asia", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-hand-holding-usd",
                    "children": [
                        {"label_ar": "عرض سعر", "label_en": "Quotations", "type": "link", "route": "app/quotation", "view_type": "file", "path": "/systems/fotarh/selling/quotations.html", "icon": "fa fa-comment-dollar", "favorites": "0"},
                        {"label_ar": "امر بيع", "label_en": "Blanket Orders", "type": "link", "route": "app/blanket-order", "view_type": "file", "path": "/systems/fotarh/selling/blanket-order.html", "icon": "fa fa-file-contract", "favorites": "0"},
                        {"label_ar": "فاتورة مبيعات", "label_en": "Sales Invoice", "type": "link", "route": "app/sales-invoice/new-sales-invoice-1", "view_type": "file", "path": "/systems/fotarh/selling/new-sales-invoice.html", "icon": "fa fa-file-invoice-dollar", "favorites": "1"}
                    ]
                },
                {
                    "label_ar": "إعدادات البيع", "label_en": "Selling Settings", "type": "folder", "icon": "fa fa-cog",
                    "children": [
                        {"label_ar": "قالب الشروط والأحكام", "label_en": "Terms and Conditions Template", "type": "link", "route": "app/terms-and-conditions", "view_type": "file", "path": "/systems/fotarh/selling/terms-template.html", "icon": "fa fa-file-signature", "favorites": "0"},
                        {"label_ar": "قالب الضرائب والرسوم على المبيعات", "label_en": "Sales Taxes Template", "type": "link", "route": "app/sales-taxes-and-charges-template", "view_type": "file", "path": "/systems/fotarh/selling/taxes-template.html", "icon": "fa fa-percent", "favorites": "0"},
                        {"label_ar": "مصدر الزبون المحتمل", "label_en": "Lead Source", "type": "link", "route": "app/lead-source", "view_type": "file", "path": "/systems/fotarh/selling/lead-source.html", "icon": "fa fa-search-location", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقاير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "تحليل المبيعات", "label_en": "Sales Analytics", "type": "link", "route": "app/query-report/Sales%20Analytics", "view_type": "file", "path": "/systems/fotarh/selling/reports/sales-analytics.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تحليل أوامر المبيعات", "label_en": "Sales Order Analysis", "type": "link", "route": "app/query-report/Sales%20Order%20Analysis", "view_type": "file", "path": "/systems/fotarh/selling/reports/sales-order-analysis.html", "icon": "fa fa-table", "favorites": "0"},
                        {"label_ar": "العملاء الغير النشطين", "label_en": "Inactive Customers", "type": "link", "route": "app/query-report/Inactive%20Customers", "view_type": "file", "path": "/systems/fotarh/selling/reports/inactive-customers.html", "icon": "fa fa-user-slash", "favorites": "0"},
                        {"label_ar": "ملخص المبيعات بناء على رجل المبيعات", "label_en": "Sales Person Transaction Summary", "type": "link", "route": "app/query-report/Sales%20Person-wise%20Transaction%20Summary", "view_type": "file", "path": "/systems/fotarh/selling/reports/salesperson-summary.html", "icon": "fa fa-user-friends", "favorites": "0"},
                        {"label_ar": "الحركة التاريخية للمبيعات وفقاً للصنف", "label_en": "Item-wise Sales History", "type": "link", "route": "app/query-report/Item-wise%20Sales%20History", "view_type": "file", "path": "/systems/fotarh/selling/reports/item-sales-history.html", "icon": "fa fa-history", "favorites": "0"},
                        {"label_ar": "عناوين العملاء وجهات الإتصال", "label_en": "Address and Contacts", "type": "link", "route": "app/query-report/Address%20And%20Contacts", "view_type": "file", "path": "/systems/fotarh/selling/reports/customer-contacts.html", "icon": "fa fa-address-book", "favorites": "0"},
                        {"label_ar": "المخزون المتاج للأصناف المعبأة", "label_en": "Available Stock for Packing Items", "type": "link", "route": "app/query-report/Available%20Stock%20for%20Packing%20Items", "view_type": "file", "path": "/systems/fotarh/selling/reports/packing-stock.html", "icon": "fa fa-box-open", "favorites": "0"},
                        {"label_ar": "اصناف كتيرة معلقة لطلب الشراء", "label_en": "Pending SO Items For Purchase Request", "type": "link", "route": "app/query-report/Pending%20SO%20Items%20For%20Purchase%20Request", "view_type": "file", "path": "/systems/fotarh/selling/reports/pending-so.html", "icon": "fa fa-hourglass-half", "favorites": "0"},
                        {"label_ar": "رصيد العميل", "label_en": "Customer Credit Balance", "type": "link", "route": "app/query-report/Customer%20Credit%20Balance", "view_type": "file", "path": "/systems/fotarh/selling/reports/credit-balance.html", "icon": "fa fa-dollar-sign", "favorites": "0"}
                    ]
                }
            ]
        },
        {
            "label_ar": "الاصــــول", "label_en": "Assets", "type": "folder", "icon": "fa fa-boxes",
            "children": [
                {"label_ar": "بيانات الأصل", "label_en": "Asset Details", "type": "link", "route": "app/asset", "view_type": "file", "path": "/systems/fotarh/assets/asset-details.html", "icon": "fa fa-barcode", "favorites": "0"},
                {"label_ar": "الموقع", "label_en": "Locations", "type": "link", "route": "app/location", "view_type": "file", "path": "/systems/fotarh/assets/locations.html", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                {"label_ar": "تصنيف الأصول", "label_en": "Asset Category", "type": "link", "route": "app/asset-category", "view_type": "file", "path": "/systems/fotarh/assets/asset-category.html", "icon": "fa fa-folder-open", "favorites": "0"},
                {"label_ar": "حركة الأصول", "label_en": "Asset Movement", "type": "link", "route": "app/asset-movement", "view_type": "file", "path": "/systems/fotarh/assets/asset-movement.html", "icon": "fa fa-dolly-flatbed", "favorites": "0"},
                {"label_ar": "فريق الصيانة", "label_en": "Asset Maintenance Team", "type": "link", "route": "app/asset-maintenance-team", "view_type": "file", "path": "/systems/fotarh/assets/maintenance-team.html", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "صيانة الأصول", "label_en": "Asset Maintenance", "type": "link", "route": "app/asset-maintenance", "view_type": "file", "path": "/systems/fotarh/assets/asset-maintenance.html", "icon": "fa fa-tools", "favorites": "0"},
                {"label_ar": "سجل صيانة الأصول", "label_en": "Asset Maintenance Log", "type": "link", "route": "app/asset-maintenance-log", "view_type": "file", "path": "/systems/fotarh/assets/maintenance-log.html", "icon": "fa fa-clipboard-list", "favorites": "0"},
                {"label_ar": "تعديل قيمة أصل", "label_en": "Asset Value Adjustment", "type": "link", "route": "app/asset-value-adjustment", "view_type": "file", "path": "/systems/fotarh/assets/value-adjustment.html", "icon": "fa fa-adjust", "favorites": "0"},
                {"label_ar": "إصلاح الأصول", "label_en": "Asset Repair", "type": "link", "route": "app/asset-repair", "view_type": "file", "path": "/systems/fotarh/assets/asset-repair.html", "icon": "fa fa-wrench", "favorites": "0"},
                {"label_ar": "تقرير دفتر حسابات استهلاك الأصول", "label_en": "Asset Depreciation Ledger", "type": "link", "route": "app/query-report/Asset%20Depreciation%20Ledger?", "view_type": "file", "path": "/systems/fotarh/assets/reports/depreciation-ledger.html", "icon": "fa fa-book-open", "favorites": "0"},
                {"label_ar": "تقرير استهلاك الأصول والأرصدة", "label_en": "Asset Depreciations and Balances", "type": "link", "route": "app/query-report/Asset%20Depreciations%20and%20Balances?", "view_type": "file", "path": "/systems/fotarh/assets/reports/depreciations-balances.html", "icon": "fa fa-calculator", "favorites": "0"}
            ]
        },
        {
            "label_ar": "المستخدمين", "label_en": "Users", "type": "folder", "icon": "fa fa-user-shield",
            "children": [
                {"label_ar": "المستخدمين", "label_en": "Users List", "type": "link", "route": "app/user", "view_type": "file", "path": "/systems/fotarh/users/users-list.html", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "الأدوار و المهام", "label_en": "Roles and Permissions", "type": "link", "route": "app/role", "view_type": "file", "path": "/systems/fotarh/users/roles-permissions.html", "icon": "fa fa-user-tag", "favorites": "0"},
                {"label_ar": "مدير صلاحيات", "label_en": "Permission Manager", "type": "link", "route": "app/permission-manager", "view_type": "file", "path": "/systems/fotarh/users/permission-manager.html", "icon": "fa fa-lock-open", "favorites": "0"}
            ]
        },
        {
            "label_ar": "الاعدادات", "label_en": "Settings", "type": "folder", "icon": "fa fa-cog",
            "children": [
                {"label_ar": "إعدادات النظام", "label_en": "System Settings", "type": "link", "route": "app/system-settings", "view_type": "file", "path": "/systems/fotarh/settings/system-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                {"label_ar": "إعدادات الحسابات", "label_en": "Accounts Settings", "type": "link", "route": "app/accounts-settings", "view_type": "file", "path": "/systems/fotarh/settings/accounts-settings.html", "icon": "fa fa-calculator", "favorites": "0"},
                {"label_ar": "إعدادات المخازن", "label_en": "Stock Settings", "type": "link", "route": "app/stock-settings", "view_type": "file", "path": "/systems/fotarh/settings/stock-settings.html", "icon": "fa fa-cubes", "favorites": "0"},
                {"label_ar": "إعدادات المبيعات", "label_en": "Selling Settings", "type": "link", "route": "app/selling-settings", "view_type": "file", "path": "/systems/fotarh/settings/selling-settings.html", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "إعدادات المشتريات", "label_en": "Buying Settings", "type": "link", "route": "app/buying-settings", "view_type": "file", "path": "/systems/fotarh/settings/buying-settings.html", "icon": "fa fa-shopping-bag", "favorites": "0"},
                {"label_ar": "الإعدادات العامة", "label_en": "Global Defaults", "type": "link", "route": "app/global-defaults", "view_type": "file", "path": "/systems/fotarh/settings/global-defaults.html", "icon": "fa fa-globe", "favorites": "0"}
            ]
        }
    ]
},
       {
    "name_ar": "نظام رؤى",
    "name_en": "Roaya System",
    "is_default": 0,
    "is_mandatory": 0,
    "menu": 
    [
        {"label_ar": "الرئيسية", "label_en": "Home", "type": "link", "route": "app/home", "view_type": "file", "path": "/systems/roaya/home/home.html", "icon": "fa fa-home", "favorites": "0"},
        {
            "label_ar": "الحسابات", "label_en": "Accounts", "type": "folder", "icon": "fa fa-calculator",
            "children": [
                {
                    "label_ar": "البيانات الأساسية", "label_en": "Basic Data", "type": "folder", "icon": "fa fa-folder-open",
                    "children": [
                        {"label_ar": "بيانات شركة", "label_en": "Company Info", "type": "link", "route": "app/company", "view_type": "file", "path": "/systems/roaya/accounts/company.html", "icon": "fa fa-building", "favorites": "0"},
                        {"label_ar": "الدليل المحاسبي", "label_en": "Chart of Accounts", "type": "link", "route": "app/account", "view_type": "file", "path": "/systems/roaya/accounts/chart-of-accounts.html", "icon": "fa fa-sitemap", "favorites": "0"},
                        {"label_ar": "إعدادات الحسابات", "label_en": "Accounts Settings", "type": "link", "route": "app/accounts-settings", "view_type": "file", "path": "/systems/roaya/accounts/accounts-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "السنة المالية", "label_en": "Fiscal Year", "type": "link", "route": "app/fiscal-year", "view_type": "file", "path": "/systems/roaya/accounts/fiscal-year.html", "icon": "fa fa-calendar-alt", "favorites": "0"},
                        {"label_ar": "الابعاد المحاسبية", "label_en": "Accounting Dimension", "type": "link", "route": "app/accounting-dimension", "view_type": "file", "path": "/systems/roaya/accounts/accounting-dimension.html", "icon": "fa fa-cube", "favorites": "0"},
                        {"label_ar": "دفتر الحسابات", "label_en": "Finance Book", "type": "link", "route": "app/finance-book", "view_type": "file", "path": "/systems/roaya/accounts/finance-book.html", "icon": "fa fa-book", "favorites": "0"},
                        {"label_ar": "الفترات المحاسبية", "label_en": "Accounting Period", "type": "link", "route": "app/accounting-period", "view_type": "file", "path": "/systems/roaya/accounts/accounting-period.html", "icon": "fa fa-business-time", "favorites": "0"},
                        {"label_ar": "شروط الدفع", "label_en": "Payment Terms", "type": "link", "route": "app/terms-and-conditions", "view_type": "file", "path": "/systems/roaya/accounts/payment-terms.html", "icon": "fa fa-handshake", "favorites": "0"},
                        {"label_ar": "العملة", "label_en": "Currency", "type": "link", "route": "app/currency", "view_type": "file", "path": "/systems/roaya/accounts/currency.html", "icon": "fa fa-money-bill-wave", "favorites": "0"},
                        {"label_ar": "صرف العملات", "label_en": "Currency Exchange", "type": "link", "route": "app/currency-exchange", "view_type": "file", "path": "/systems/roaya/accounts/currency-exchange.html", "icon": "fa fa-exchange-alt", "favorites": "0"},
                        {"label_ar": "إعادة تقييم سعر الصرف", "label_en": "Exchange Rate Revaluation", "type": "link", "route": "app/exchange-rate-revaluation", "view_type": "file", "path": "/systems/roaya/accounts/exchange-revaluation.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "مراكز التكلفة", "label_en": "Cost Centers", "type": "link", "route": "app/cost-center", "view_type": "file", "path": "/systems/roaya/accounts/cost-center.html", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                        {"label_ar": "الميزانية", "label_en": "Budget", "type": "link", "route": "app/budget", "view_type": "file", "path": "/systems/roaya/accounts/budget.html", "icon": "fa fa-wallet", "favorites": "0"},
                        {"label_ar": "البنوك", "label_en": "Banks", "type": "link", "route": "app/bank-clearance", "view_type": "file", "path": "/systems/roaya/accounts/banks.html", "icon": "fa fa-university", "favorites": "0"},
                        {"label_ar": "حساب بنكي", "label_en": "Bank Account", "type": "link", "route": "app/bank-account", "view_type": "file", "path": "/systems/roaya/accounts/bank-account.html", "icon": "fa fa-credit-card", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-cogs",
                    "children": [
                        {"label_ar": "قيود يوميه", "label_en": "Journal Entries", "type": "link", "route": "app/journal-entry", "view_type": "file", "path": "/systems/roaya/accounts/journal-entry.html", "icon": "fa fa-pen-square", "favorites": "0"},
                        {"label_ar": "سندات القبض و الصرف", "label_en": "Payment Entries", "type": "link", "route": "app/payment-entry", "view_type": "file", "path": "/systems/roaya/accounts/payment-entry.html", "icon": "fa fa-receipt", "favorites": "0"},
                        {"label_ar": "قالب قيود اليومية", "label_en": "Journal Entry Template", "type": "link", "route": "app/journal-entry-template", "view_type": "file", "path": "/systems/roaya/accounts/journal-entry-template.html", "icon": "fa fa-paste", "favorites": "0"},
                        {"label_ar": "الشروط والأحكام", "label_en": "Terms and Conditions", "type": "link", "route": "app/terms-and-conditions", "view_type": "file", "path": "/systems/roaya/accounts/terms-conditions.html", "icon": "fa fa-file-contract", "favorites": "0"},
                        {"label_ar": "طريقة الدفع", "label_en": "Mode of Payment", "type": "link", "route": "app/mode-of-payment", "view_type": "file", "path": "/systems/roaya/accounts/mode-of-payment.html", "icon": "fa fa-money-check", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "الضرائب", "label_en": "Taxes", "type": "folder", "icon": "fa fa-percent",
                    "children": [
                        {"label_ar": "قالب الضرائب والرسوم على المبيعات", "label_en": "Sales Taxes Template", "type": "link", "route": "app/sales-taxes-and-charges-template", "view_type": "file", "path": "/systems/roaya/accounts/sales-taxes-template.html", "icon": "fa fa-file-invoice-dollar", "favorites": "0"},
                        {"label_ar": "قالب الضرائب والرسوم على المشتريات", "label_en": "Purchase Taxes Template", "type": "link", "route": "app/purchase-taxes-and-charges-template", "view_type": "file", "path": "/systems/roaya/accounts/purchase-taxes-template.html", "icon": "fa fa-file-invoice-dollar", "favorites": "0"},
                        {"label_ar": "قالب ضريبة السلعه", "label_en": "Item Tax Template", "type": "link", "route": "app/item-tax-template", "view_type": "file", "path": "/systems/roaya/accounts/item-tax-template.html", "icon": "fa fa-tag", "favorites": "0"},
                        {"label_ar": "الفئة الضريبية", "label_en": "Tax Category", "type": "link", "route": "app/tax-category", "view_type": "file", "path": "/systems/roaya/accounts/tax-category.html", "icon": "fa fa-folder", "favorites": "0"},
                        {"label_ar": "القاعدة الضريبية", "label_en": "Tax Rule", "type": "link", "route": "app/tax-rule", "view_type": "file", "path": "/systems/roaya/accounts/tax-rule.html", "icon": "fa fa-gavel", "favorites": "0"},
                        {"label_ar": "فئة حجب الضرائب", "label_en": "Tax Withholding Category", "type": "link", "route": "app/tax-withholding-category", "view_type": "file", "path": "/systems/roaya/accounts/tax-withholding.html", "icon": "fa fa-shield-alt", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير الماليه", "label_en": "Financial Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "الأستاذ العام", "label_en": "General Ledger", "type": "link", "route": "app/query-report/General%20Ledger", "view_type": "file", "path": "/systems/roaya/accounts/reports/general-ledger.html", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "ميزان مراجعه", "label_en": "Trial Balance", "type": "link", "route": "app/query-report/Trial%20Balance", "view_type": "file", "path": "/systems/roaya/accounts/reports/trial-balance.html", "icon": "fa fa-balance-scale", "favorites": "0"},
                        {"label_ar": "قائمة الدخل", "label_en": "Profit and Loss Statement", "type": "link", "route": "app/query-report/Profit%20and%20Loss%20Statement", "view_type": "file", "path": "/systems/roaya/accounts/reports/profit-loss.html", "icon": "fa fa-chart-pie", "favorites": "0"},
                        {"label_ar": "الأرباح والخسائر", "label_en": "Gross and Net Profit Report", "type": "link", "route": "app/query-report/Gross%20and%20Net%20Profit%20Report", "view_type": "file", "path": "/systems/roaya/accounts/reports/gross-and-net-profit.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تقرير إنحرافات الموازنة", "label_en": "Budget Variance Report", "type": "link", "route": "app/query-report/Budget%20Variance%20Report", "view_type": "file", "path": "/systems/roaya/accounts/reports/budget-variance.html", "icon": "fa fa-exclamation-triangle", "favorites": "0"},
                        {"label_ar": "الميزانية العمومية", "label_en": "Balance Sheet", "type": "link", "route": "app/query-report/Balance%20Sheet", "view_type": "file", "path": "/systems/roaya/accounts/reports/balance-sheet.html", "icon": "fa fa-table", "favorites": "0"}
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
                        {"label_ar": "الأصناف", "label_en": "Items", "type": "link", "route": "app/item", "view_type": "file", "path": "/systems/roaya/stock/items.html", "icon": "fa fa-box", "favorites": "0"},
                        {"label_ar": "مجموعة الأصناف", "label_en": "Item Groups", "type": "link", "route": "app/item-group", "view_type": "file", "path": "/systems/roaya/stock/item-groups.html", "icon": "fa fa-boxes", "favorites": "0"},
                        {"label_ar": "الصنف البديل", "label_en": "Alternative Item", "type": "link", "route": "app/item-alternative", "view_type": "file", "path": "/systems/roaya/stock/item-alternative.html", "icon": "fa fa-sync", "favorites": "0"},
                        {"label_ar": "إعدادات المخزون", "label_en": "Stock Settings", "type": "link", "route": "app/stock-settings", "view_type": "file", "path": "/systems/roaya/stock/stock-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "المخازن", "label_en": "Warehouses", "type": "link", "route": "app/warehouse", "view_type": "file", "path": "/systems/roaya/stock/warehouses.html", "icon": "fa fa-warehouse", "favorites": "0"},
                        {"label_ar": "وحدة القياس", "label_en": "UOM", "type": "link", "route": "app/uom", "view_type": "file", "path": "/systems/roaya/stock/uom.html", "icon": "fa fa-weight", "favorites": "0"},
                        {"label_ar": "العلامة التجارية", "label_en": "Brand", "type": "link", "route": "app/brand", "view_type": "file", "path": "/systems/roaya/stock/brand.html", "icon": "fa fa-trademark", "favorites": "0"},
                        {"label_ar": "عامل تحويل وحدة القياس", "label_en": "UOM Conversion Factor", "type": "link", "route": "app/uom-conversion-factor", "view_type": "file", "path": "/systems/roaya/stock/uom-conversion.html", "icon": "fa fa-calculator", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "عمليات المخزون", "label_en": "Stock Operations", "type": "folder", "icon": "fa fa-dolly",
                    "children": [
                        {"label_ar": "طلب مواد", "label_en": "Material Requests", "type": "link", "route": "app/material-request", "view_type": "file", "path": "/systems/roaya/stock/material-request.html", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "مدخلات المخزون", "label_en": "Stock Entries", "type": "link", "route": "app/stock-entry", "view_type": "file", "path": "/systems/roaya/stock/stock-entry.html", "icon": "fa fa-truck-loading", "favorites": "0"},
                        {"label_ar": "استلام مشتريات", "label_en": "Purchase Receipts", "type": "link", "route": "app/purchase-receipt", "view_type": "file", "path": "/systems/roaya/stock/purchase-receipt.html", "icon": "fa fa-file-download", "favorites": "0"},
                        {"label_ar": "فحص الجودة", "label_en": "Quality Inspection", "type": "link", "route": "app/quality-inspection", "view_type": "file", "path": "/systems/roaya/stock/quality-inspection.html", "icon": "fa fa-check-double", "favorites": "0"},
                        {"label_ar": "قالب فحص الجودة", "label_en": "Quality Inspection Template", "type": "link", "route": "app/quality-inspection-template", "view_type": "file", "path": "/systems/roaya/stock/quality-template.html", "icon": "fa fa-clipboard-check", "favorites": "0"},
                        {"label_ar": "جرد المخزون", "label_en": "Stock Reconciliation", "type": "link", "route": "app/stock-reconciliation", "view_type": "file", "path": "/systems/roaya/stock/stock-reconciliation.html", "icon": "fa fa-tasks", "favorites": "0"},
                        {"label_ar": "الرقم التسلسلي", "label_en": "Serial No", "type": "link", "route": "app/serial-no", "view_type": "file", "path": "/systems/roaya/stock/serial-no.html", "icon": "fa fa-barcode", "favorites": "0"},
                        {"label_ar": "الدفعات", "label_en": "Batches", "type": "link", "route": "app/batch", "view_type": "file", "path": "/systems/roaya/stock/batches.html", "icon": "fa fa-layer-group", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-line",
                    "children": [
                        {"label_ar": "تحليلات المخازن", "label_en": "Stock Analytics", "type": "link", "route": "app/query-report/Stock%20Analytics", "view_type": "file", "path": "/systems/roaya/stock/reports/stock-analytics.html", "icon": "fa fa-chart-bar", "favorites": "0"},
                        {"label_ar": "تحليل أوامر المبيعات", "label_en": "Sales Order Analysis", "type": "link", "route": "app/query-report/Sales%20Order%20Analysis", "view_type": "file", "path": "/systems/roaya/stock/reports/sales-order-analysis.html", "icon": "fa fa-analytics", "favorites": "0"},
                        {"label_ar": "تحليل أوامر الشراء", "label_en": "Purchase Order Analysis", "type": "link", "route": "app/query-report/Purchase%20Order%20Analysis", "view_type": "file", "path": "/systems/roaya/stock/reports/purchase-order-analysis.html", "icon": "fa fa-analytics", "favorites": "0"},
                        {"label_ar": "تقرير نقص الصنف", "label_en": "Item Shortage Report", "type": "link", "route": "app/query-report/Item%20Shortage%20Report", "view_type": "file", "path": "/systems/roaya/stock/reports/item-shortage.html", "icon": "fa fa-minus-circle", "favorites": "0"},
                        {"label_ar": "أسعار الصنف", "label_en": "Item Prices", "type": "link", "route": "app/query-report/Item%20Prices", "view_type": "file", "path": "/systems/roaya/stock/reports/item-prices.html", "icon": "fa fa-tags", "favorites": "0"},
                        {"label_ar": "سجل المخزن", "label_en": "Stock Ledger", "type": "link", "route": "app/query-report/Stock%20Ledger", "view_type": "file", "path": "/systems/roaya/stock/reports/stock-ledger.html", "icon": "fa fa-history", "favorites": "0"},
                        {"label_ar": "رصيد المخزون", "label_en": "Stock Balance", "type": "link", "route": "app/query-report/Stock%20Balance", "view_type": "file", "path": "/systems/roaya/stock/reports/stock-balance.html", "icon": "fa fa-cubes", "favorites": "0"}
                    ]
                }
            ]
        },
        {
            "label_ar": "نظام المشتريات والموردين", "label_en": "Buying System", "type": "folder", "icon": "fa fa-shopping-bag",
            "children": [
                {
                    "label_ar": "الالبيانات الأساسية", "label_en": "Basic Data", "type": "folder", "icon": "fa fa-folder-open",
                    "children": [
                        {"label_ar": "بيانات الموردين", "label_en": "Suppliers", "type": "link", "route": "app/supplier", "view_type": "file", "path": "/systems/roaya/buying/suppliers.html", "icon": "fa fa-truck", "favorites": "0"},
                        {"label_ar": "مجموعة الموردين", "label_en": "Supplier Groups", "type": "link", "route": "app/supplier-group", "view_type": "file", "path": "/systems/roaya/buying/supplier-groups.html", "icon": "fa fa-users-cog", "favorites": "0"},
                        {"label_ar": "معلومات الاتصال بالموردين", "label_en": "Contacts", "type": "link", "route": "app/contact", "view_type": "file", "path": "/systems/roaya/buying/contacts.html", "icon": "fa fa-id-card", "favorites": "0"},
                        {"label_ar": "عناوين الموردين", "label_en": "Addresses", "type": "link", "route": "app/address", "view_type": "file", "path": "/systems/roaya/buying/addresses.html", "icon": "fa fa-map-marked-alt", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-exchange-alt",
                    "children": [
                        {"label_ar": "طلب مواد", "label_en": "Material Requests", "type": "link", "route": "app/material-request", "view_type": "file", "path": "/systems/roaya/buying/material-request.html", "icon": "fa fa-file-alt", "favorites": "0"},
                        {"label_ar": "أمر الشراء", "label_en": "Purchase Orders", "type": "link", "route": "app/purchase-order", "view_type": "file", "path": "/systems/roaya/buying/purchase-order.html", "icon": "fa fa-file-shopping-bag", "favorites": "0"},
                        {"label_ar": "فاتورة شراء", "label_en": "Purchase Invoices", "type": "link", "route": "app/purchase-invoice", "view_type": "file", "path": "/systems/roaya/buying/purchase-invoice.html", "icon": "fa fa-file-invoice", "favorites": "0"},
                        {"label_ar": "طلب عرض سعر", "label_en": "Supplier Quotations", "type": "link", "route": "app/supplier-quotation", "view_type": "file", "path": "/systems/roaya/buying/supplier-quotation.html", "icon": "fa fa-comment-dollar", "favorites": "0"},
                        {"label_ar": "عرض سعر المورد", "label_en": "Supplier Quotation Comparison", "type": "link", "route": "app/query-report/Supplier%20Quotation%20Comparison", "view_type": "file", "path": "/systems/roaya/buying/quotation-comparison.html", "icon": "fa fa-balance-scale", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقارير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "تحليلات المشتريات", "label_en": "Purchase Analytics", "type": "link", "route": "app/query-report/Purchase%20Analytics", "view_type": "file", "path": "/systems/roaya/buying/reports/purchase-analytics.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تحليل أوامر الشراء", "label_en": "Purchase Order Analysis", "type": "link", "route": "app/query-report/Purchase%20Order%20Analysis", "view_type": "file", "path": "/systems/roaya/buying/reports/purchase-order-analysis.html", "icon": "fa fa-table", "favorites": "0"},
                        {"label_ar": "عناوين الموردين وجهات الاتصال", "label_en": "Addresses and Contacts", "type": "link", "route": "app/address", "view_type": "file", "path": "/systems/roaya/buying/reports/addresses-contacts.html", "icon": "fa fa-address-book", "favorites": "0"}
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
                        {"label_ar": "العملاء", "label_en": "Customers", "type": "link", "route": "app/customer", "view_type": "file", "path": "/systems/roaya/selling/customers.html", "icon": "fa fa-user-tag", "favorites": "0"},
                        {"label_ar": "مجموعة العملاء", "label_en": "Customer Groups", "type": "link", "route": "app/customer-group", "view_type": "file", "path": "/systems/roaya/selling/customer-groups.html", "icon": "fa fa-users-cog", "favorites": "0"},
                        {"label_ar": "اعدات المبيعات", "label_en": "Selling Settings", "type": "link", "route": "app/selling-settings", "view_type": "file", "path": "/systems/roaya/selling/selling-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                        {"label_ar": "الأصناف", "label_en": "Items", "type": "link", "route": "app/item", "view_type": "file", "path": "/systems/roaya/selling/items.html", "icon": "fa fa-box", "favorites": "0"},
                        {"label_ar": "مجموعة الأصناف", "label_en": "Item Groups", "type": "link", "route": "app/item-group", "view_type": "file", "path": "/systems/roaya/selling/item-groups.html", "icon": "fa fa-boxes", "favorites": "0"},
                        {"label_ar": "قائمة الأسعار", "label_en": "Price Lists", "type": "link", "route": "app/price-list", "view_type": "file", "path": "/systems/roaya/selling/price-lists.html", "icon": "fa fa-list-ol", "favorites": "0"},
                        {"label_ar": "سعر الأصناف", "label_en": "Item Prices", "type": "link", "route": "app/item-price", "view_type": "file", "path": "/systems/roaya/selling/item-prices.html", "icon": "fa fa-tags", "favorites": "0"},
                        {"label_ar": "جهات الاتصال", "label_en": "Contacts", "type": "link", "route": "app/contact", "view_type": "file", "path": "/systems/roaya/selling/contacts.html", "icon": "fa fa-id-card", "favorites": "0"},
                        {"label_ar": "عناوين الموردين", "label_en": "Addresses", "type": "link", "route": "app/address", "view_type": "file", "path": "/systems/roaya/selling/addresses.html", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                        {"label_ar": "الأقاليم", "label_en": "Territories", "type": "link", "route": "app/territory", "view_type": "file", "path": "/systems/roaya/selling/territories.html", "icon": "fa fa-globe-asia", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "العمليات", "label_en": "Operations", "type": "folder", "icon": "fa fa-hand-holding-usd",
                    "children": [
                        {"label_ar": "عرض سعر", "label_en": "Quotations", "type": "link", "route": "app/quotation", "view_type": "file", "path": "/systems/roaya/selling/quotations.html", "icon": "fa fa-comment-dollar", "favorites": "0"},
                        {"label_ar": "امر بيع", "label_en": "Blanket Orders", "type": "link", "route": "app/blanket-order", "view_type": "file", "path": "/systems/roaya/selling/blanket-order.html", "icon": "fa fa-file-contract", "favorites": "0"},
                        {"label_ar": "فاتورة مبيعات", "label_en": "Sales Invoice", "type": "link", "route": "app/sales-invoice/new-sales-invoice-1", "view_type": "file", "path": "/systems/roaya/selling/new-sales-invoice.html", "icon": "fa fa-file-invoice-dollar", "favorites": "1"}
                    ]
                },
                {
                    "label_ar": "إعدادات البيع", "label_en": "Selling Settings", "type": "folder", "icon": "fa fa-cog",
                    "children": [
                        {"label_ar": "قالب الشروط والأحكام", "label_en": "Terms and Conditions Template", "type": "link", "route": "app/terms-and-conditions", "view_type": "file", "path": "/systems/roaya/selling/terms-template.html", "icon": "fa fa-file-signature", "favorites": "0"},
                        {"label_ar": "قالب الضرائب والرسوم على المبيعات", "label_en": "Sales Taxes Template", "type": "link", "route": "app/sales-taxes-and-charges-template", "view_type": "file", "path": "/systems/roaya/selling/taxes-template.html", "icon": "fa fa-percent", "favorites": "0"},
                        {"label_ar": "مصدر الزبون المحتمل", "label_en": "Lead Source", "type": "link", "route": "app/lead-source", "view_type": "file", "path": "/systems/roaya/selling/lead-source.html", "icon": "fa fa-search-location", "favorites": "0"}
                    ]
                },
                {
                    "label_ar": "التقاير", "label_en": "Reports", "type": "folder", "icon": "fa fa-chart-bar",
                    "children": [
                        {"label_ar": "تحليل المبيعات", "label_en": "Sales Analytics", "type": "link", "route": "app/query-report/Sales%20Analytics", "view_type": "file", "path": "/systems/roaya/selling/reports/sales-analytics.html", "icon": "fa fa-chart-line", "favorites": "0"},
                        {"label_ar": "تحليل أوامر المبيعات", "label_en": "Sales Order Analysis", "type": "link", "route": "app/query-report/Sales%20Order%20Analysis", "view_type": "file", "path": "/systems/roaya/selling/reports/sales-order-analysis.html", "icon": "fa fa-table", "favorites": "0"},
                        {"label_ar": "العملاء الغير النشطين", "label_en": "Inactive Customers", "type": "link", "route": "app/query-report/Inactive%20Customers", "view_type": "file", "path": "/systems/roaya/selling/reports/inactive-customers.html", "icon": "fa fa-user-slash", "favorites": "0"},
                        {"label_ar": "ملخص المبيعات بناء على رجل المبيعات", "label_en": "Sales Person Transaction Summary", "type": "link", "route": "app/query-report/Sales%20Person-wise%20Transaction%20Summary", "view_type": "file", "path": "/systems/roaya/selling/reports/salesperson-summary.html", "icon": "fa fa-user-friends", "favorites": "0"},
                        {"label_ar": "الحركة التاريخية للمبيعات وفقاً للصنف", "label_en": "Item-wise Sales History", "type": "link", "route": "app/query-report/Item-wise%20Sales%20History", "view_type": "file", "path": "/systems/roaya/selling/reports/item-sales-history.html", "icon": "fa fa-history", "favorites": "0"},
                        {"label_ar": "عناوين العملاء وجهات الإتصال", "label_en": "Address and Contacts", "type": "link", "route": "app/query-report/Address%20And%20Contacts", "view_type": "file", "path": "/systems/roaya/selling/reports/customer-contacts.html", "icon": "fa fa-address-book", "favorites": "0"},
                        {"label_ar": "المخزون المتاج للأصناف المعبأة", "label_en": "Available Stock for Packing Items", "type": "link", "route": "app/query-report/Available%20Stock%20for%20Packing%20Items", "view_type": "file", "path": "/systems/roaya/selling/reports/packing-stock.html", "icon": "fa fa-box-open", "favorites": "0"},
                        {"label_ar": "اصناف كتيرة معلقة لطلب الشراء", "label_en": "Pending SO Items For Purchase Request", "type": "link", "route": "app/query-report/Pending%20SO%20Items%20For%20Purchase%20Request", "view_type": "file", "path": "/systems/roaya/selling/reports/pending-so.html", "icon": "fa fa-hourglass-half", "favorites": "0"},
                        {"label_ar": "رصيد العميل", "label_en": "Customer Credit Balance", "type": "link", "route": "app/query-report/Customer%20Credit%20Balance", "view_type": "file", "path": "/systems/roaya/selling/reports/credit-balance.html", "icon": "fa fa-dollar-sign", "favorites": "0"}
                    ]
                }
            ]
        },
        {
            "label_ar": "الاصــــول", "label_en": "Assets", "type": "folder", "icon": "fa fa-boxes",
            "children": [
                {"label_ar": "بيانات الأصل", "label_en": "Asset Details", "type": "link", "route": "app/asset", "view_type": "file", "path": "/systems/roaya/assets/asset-details.html", "icon": "fa fa-barcode", "favorites": "0"},
                {"label_ar": "الموقع", "label_en": "Locations", "type": "link", "route": "app/location", "view_type": "file", "path": "/systems/roaya/assets/locations.html", "icon": "fa fa-map-marker-alt", "favorites": "0"},
                {"label_ar": "تصنيف الأصول", "label_en": "Asset Category", "type": "link", "route": "app/asset-category", "view_type": "file", "path": "/systems/roaya/assets/asset-category.html", "icon": "fa fa-folder-open", "favorites": "0"},
                {"label_ar": "حركة الأصول", "label_en": "Asset Movement", "type": "link", "route": "app/asset-movement", "view_type": "file", "path": "/systems/roaya/assets/asset-movement.html", "icon": "fa fa-dolly-flatbed", "favorites": "0"},
                {"label_ar": "فريق الصيانة", "label_en": "Asset Maintenance Team", "type": "link", "route": "app/asset-maintenance-team", "view_type": "file", "path": "/systems/roaya/assets/maintenance-team.html", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "صيانة الأصول", "label_en": "Asset Maintenance", "type": "link", "route": "app/asset-maintenance", "view_type": "file", "path": "/systems/roaya/assets/asset-maintenance.html", "icon": "fa fa-tools", "favorites": "0"},
                {"label_ar": "سجل صيانة الأصول", "label_en": "Asset Maintenance Log", "type": "link", "route": "app/asset-maintenance-log", "view_type": "file", "path": "/systems/roaya/assets/maintenance-log.html", "icon": "fa fa-clipboard-list", "favorites": "0"},
                {"label_ar": "تعديل قيمة أصل", "label_en": "Asset Value Adjustment", "type": "link", "route": "app/asset-value-adjustment", "view_type": "file", "path": "/systems/roaya/assets/value-adjustment.html", "icon": "fa fa-adjust", "favorites": "0"},
                {"label_ar": "إصلاح الأصول", "label_en": "Asset Repair", "type": "link", "route": "app/asset-repair", "view_type": "file", "path": "/systems/roaya/assets/asset-repair.html", "icon": "fa fa-wrench", "favorites": "0"},
                {"label_ar": "تقرير دفتر حسابات استهلاك الأصول", "label_en": "Asset Depreciation Ledger", "type": "link", "route": "app/query-report/Asset%20Depreciation%20Ledger?", "view_type": "file", "path": "/systems/roaya/assets/reports/depreciation-ledger.html", "icon": "fa fa-book-open", "favorites": "0"},
                {"label_ar": "تقرير استهلاك الأصول والأرصدة", "label_en": "Asset Depreciations and Balances", "type": "link", "route": "app/query-report/Asset%20Depreciations%20and%20Balances?", "view_type": "file", "path": "/systems/roaya/assets/reports/depreciations-balances.html", "icon": "fa fa-calculator", "favorites": "0"}
            ]
        },
        {
            "label_ar": "المستخدمين", "label_en": "Users", "type": "folder", "icon": "fa fa-user-shield",
            "children": [
                {"label_ar": "المستخدمين", "label_en": "Users List", "type": "link", "route": "app/user", "view_type": "file", "path": "/systems/roaya/users/users-list.html", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "الأدوار و المهام", "label_en": "Roles and Permissions", "type": "link", "route": "app/role", "view_type": "file", "path": "/systems/roaya/users/roles-permissions.html", "icon": "fa fa-user-tag", "favorites": "0"},
                {"label_ar": "مدير صلاحيات", "label_en": "Permission Manager", "type": "link", "route": "app/permission-manager", "view_type": "file", "path": "/systems/roaya/users/permission-manager.html", "icon": "fa fa-lock-open", "favorites": "0"}
            ]
        },
        {
            "label_ar": "الاعدادات", "label_en": "Settings", "type": "folder", "icon": "fa fa-cog",
            "children": [
                {"label_ar": "إعدادات النظام", "label_en": "System Settings", "type": "link", "route": "app/system-settings", "view_type": "file", "path": "/systems/roaya/settings/system-settings.html", "icon": "fa fa-sliders-h", "favorites": "0"},
                {"label_ar": "إعدادات الحسابات", "label_en": "Accounts Settings", "type": "link", "route": "app/accounts-settings", "view_type": "file", "path": "/systems/roaya/settings/accounts-settings.html", "icon": "fa fa-calculator", "favorites": "0"},
                {"label_ar": "إعدادات المخازن", "label_en": "Stock Settings", "type": "link", "route": "app/stock-settings", "view_type": "file", "path": "/systems/roaya/settings/stock-settings.html", "icon": "fa fa-cubes", "favorites": "0"},
                {"label_ar": "إعدادات المبيعات", "label_en": "Selling Settings", "type": "link", "route": "app/selling-settings", "view_type": "file", "path": "/systems/roaya/settings/selling-settings.html", "icon": "fa fa-users", "favorites": "0"},
                {"label_ar": "إعدادات المشتريات", "label_en": "Buying Settings", "type": "link", "route": "app/buying-settings", "view_type": "file", "path": "/systems/roaya/settings/buying-settings.html", "icon": "fa fa-shopping-bag", "favorites": "0"},
                {"label_ar": "الإعدادات العامة", "label_en": "Global Defaults", "type": "link", "route": "app/global-defaults", "view_type": "file", "path": "/systems/roaya/settings/global-defaults.html", "icon": "fa fa-globe", "favorites": "0"}
            ]
        }
    ]
 }
]

# المسار الافتراضي لمجلد www داخل تطبيق الـ admin
BASE_WWW_PATH = os.path.expanduser("~/frappe-bench/apps/admin/admin/www")

# قالب النص المحدث بناءً على طلبك
DEFAULT_TEMPLATE = """{system_name}
{label_ar}
{label_en}
"""

def extract_paths_and_labels(menu_items):
    """دالة شجرية لاستخراج الروابط من كافة المستويات والمجلدات الداخلية"""
    pages = []
    for item in menu_items:
        if item.get("type") == "link" and item.get("view_type") == "file" and item.get("path"):
            pages.append({
                "path": item["path"].lstrip("/"),
                "label_ar": item["label_ar"],
                "label_en": item["label_en"]
            })
        if "children" in item and item["children"]:
            pages.extend(extract_paths_and_labels(item["children"]))
    return pages

def create_system_files():
    print("🚀 بدء إنشاء المجلدات والملفات بالهيكل المحدث...")
    
    for system in systems_data:
        print(f"\n📁 جاري العمل على: {system['name_ar']}...")
        all_pages = extract_paths_and_labels(system["menu"])
        
        created_dirs = 0
        created_files = 0
        
        for page in all_pages:
            full_file_path = os.path.join(BASE_WWW_PATH, page["path"])
            dir_path = os.path.dirname(full_file_path)
            
            # إنشاء المجلدات الفرعية إن لم تكن موجودة
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                created_dirs += 1
                
            # إنشاء الملف وكتابة البيانات المحددة بداخله (إذا لم يكن موجوداً مسبقاً)
            if not os.path.exists(full_file_path):
                with open(full_file_path, "w", encoding="utf-8") as f:
                    f.write(DEFAULT_TEMPLATE.format(
                        system_name=system["name_ar"],
                        label_ar=page["label_ar"],
                        label_en=page["label_en"]
                    ))
                created_files += 1
                
        print(f"✅ انتهى: تم إنشاء ({created_dirs}) مجلدات و ({created_files}) ملفات لـ {system['name_ar']}.")

if __name__ == "__main__":
    create_system_files()