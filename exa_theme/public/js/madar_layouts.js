const MADAR_LAYOUTS = [
    {
        "id": "distribution_system",
        "render_mode": "iframe", 
        "base_folder": "distribution",
        "title": "DIST_SYS_TITLE", // مفتاح ترجمة: "نظام التوزيع والمبيعات"
        "description": "DIST_SYS_DESC", // مفتاح ترجمة: "نظام متكامل لإدارة المناديب، الفواتير، والمخزون مع دعم نقاط البيع."
        
        "default_menu": [
            {
                "id": "sales_dept",
                "title": "SALES_DEPT_LABEL",
                "description": "SALES_DEPT_DESC", // وصف للقسم الرئيسي
                "icon": "fa-store",
                "type": "folder",
                "level": 1,
                "children": [
                    {
                        "id": "inv_mgnt",
                        "title": "INV_MGNT_LABEL",
                        "icon": "fa-file-invoice-dollar",
                        "type": "folder", // المستوى الثاني (مجلد)
                        "level": 2,
                        "children": [
                            {
                                "title": "NEW_INVOICE",
                                "type": "link", // المستوى الثالث (رابط)
                                "level": 3,
                                "route": "/app/sales-invoice/new"
                            },
                            {
                                "title": "INVOICE_LIST",
                                "type": "link",
                                "level": 3,
                                "route": "/app/sales-invoice"
                            }
                        ]
                    },
                    {
                        "id": "cust_direct",
                        "title": "CUSTOMERS_LABEL",
                        "icon": "fa-users",
                        "type": "link", // المستوى الثاني (رابط مباشر - خليط)
                        "level": 2,
                        "route": "/app/customer"
                    }
                ]
            }
        ]
    }
];