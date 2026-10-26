import frappe
from frappe import _
from frappe.utils import today, getdate, date_diff, add_days, flt, add_months, get_first_day, get_last_day

def resolve_company(company):
    """The dashboard sums ledger rows with raw SQL, which skips User Permissions, so keep it to the
    companies the user may see. Returns None (all companies) only for users without a restriction."""
    from frappe.core.doctype.user_permission.user_permission import get_permitted_documents

    permitted = get_permitted_documents("Company")
    if not permitted:
        return company or None
    if company:
        if company not in permitted:
            frappe.throw(_("You are not permitted to view the dashboard for company {0}").format(company), frappe.PermissionError)
        return company
    default = frappe.defaults.get_user_default("Company")
    return default if default in permitted else permitted[0]

def check_permission(doctype):
    try:
        return frappe.has_permission(doctype, "read")
    except Exception:
        return False

def get_date_ranges(filter_type, custom_from, custom_to):
    t = getdate(today())
    if filter_type == "today":
        c_start, c_end = t, t
        p_start, p_end = add_days(t, -1), add_days(t, -1)
        current_label = _("Today")
        label = _("vs yesterday")
    elif filter_type == "last_day":
        c_start, c_end = add_days(t, -1), add_days(t, -1)
        p_start, p_end = add_days(t, -2), add_days(t, -2)
        current_label = _("Yesterday")
        label = _("vs day before")
    elif filter_type == "this_week":
        w_start = add_days(t, -t.weekday())
        c_start, c_end = w_start, add_days(w_start, 6)
        p_start, p_end = add_days(w_start, -7), add_days(w_start, -1)
        current_label = _("This Week")
        label = _("vs last week")
    elif filter_type == "last_week":
        w_start = add_days(add_days(t, -t.weekday()), -7)
        c_start, c_end = w_start, add_days(w_start, 6)
        p_start, p_end = add_days(w_start, -7), add_days(w_start, -1)
        current_label = _("Last Week")
        label = _("vs week before")
    elif filter_type == "this_month":
        c_start, c_end = get_first_day(t), get_last_day(t)
        p_start, p_end = get_first_day(add_months(t, -1)), get_last_day(add_months(t, -1))
        current_label = _("This Month")
        label = _("vs last month")
    elif filter_type == "last_month":
        c_start, c_end = get_first_day(add_months(t, -1)), get_last_day(add_months(t, -1))
        p_start, p_end = get_first_day(add_months(t, -2)), get_last_day(add_months(t, -2))
        current_label = _("Last Month")
        label = _("vs month before")
    elif filter_type == "this_quarter":
        q = (t.month - 1) // 3
        c_start = getdate(f"{t.year}-{q*3 + 1}-01")
        c_end = get_last_day(add_months(c_start, 2))
        p_start = add_months(c_start, -3)
        p_end = get_last_day(add_months(p_start, 2))
        current_label = _("This Quarter")
        label = _("vs last quarter")
    elif filter_type == "last_quarter":
        q = (t.month - 1) // 3
        c_start = add_months(getdate(f"{t.year}-{q*3 + 1}-01"), -3)
        c_end = get_last_day(add_months(c_start, 2))
        p_start = add_months(c_start, -3)
        p_end = get_last_day(add_months(p_start, 2))
        current_label = _("Last Quarter")
        label = _("vs quarter before")
    elif filter_type == "this_half":
        h = 1 if t.month <= 6 else 2
        c_start = getdate(f"{t.year}-01-01") if h == 1 else getdate(f"{t.year}-07-01")
        c_end = getdate(f"{t.year}-06-30") if h == 1 else getdate(f"{t.year}-12-31")
        p_start = getdate(f"{t.year-1}-07-01") if h == 1 else getdate(f"{t.year}-01-01")
        p_end = getdate(f"{t.year-1}-12-31") if h == 1 else getdate(f"{t.year}-06-30")
        current_label = _("This Half")
        label = _("vs last half")
    elif filter_type == "last_half":
        h = 1 if t.month <= 6 else 2
        c_start = getdate(f"{t.year-1}-07-01") if h == 1 else getdate(f"{t.year}-01-01")
        c_end = getdate(f"{t.year-1}-12-31") if h == 1 else getdate(f"{t.year}-06-30")
        p_start = getdate(f"{t.year-1}-01-01") if h == 1 else getdate(f"{t.year-1}-07-01")
        p_end = getdate(f"{t.year-1}-06-30") if h == 1 else getdate(f"{t.year-1}-12-31")
        current_label = _("Last Half")
        label = _("vs half before")
    elif filter_type == "this_year":
        c_start, c_end = getdate(f"{t.year}-01-01"), getdate(f"{t.year}-12-31")
        p_start, p_end = getdate(f"{t.year-1}-01-01"), getdate(f"{t.year-1}-12-31")
        current_label = _("This Year")
        label = _("vs last year")
    elif filter_type == "last_year":
        c_start, c_end = getdate(f"{t.year-1}-01-01"), getdate(f"{t.year-1}-12-31")
        p_start, p_end = getdate(f"{t.year-2}-01-01"), getdate(f"{t.year-2}-12-31")
        current_label = _("Last Year")
        label = _("vs year before")
    elif filter_type == "custom":
        if custom_from and custom_to:
            c_start, c_end = getdate(custom_from), getdate(custom_to)
            diff = date_diff(c_end, c_start)
            p_start, p_end = add_days(c_start, -(diff + 1)), add_days(c_end, -(diff + 1))
            current_label = _("Custom Range")
            label = _("vs previous period")
        else:
            c_start, c_end = getdate("2020-01-01"), t
            p_start, p_end = getdate("2010-01-01"), getdate("2019-12-31")
            current_label = _("All Time")
            label = _("vs previous years")
    else: # Default if empty -> This Month
        c_start, c_end = get_first_day(t), get_last_day(t)
        p_start, p_end = get_first_day(add_months(t, -1)), get_last_day(add_months(t, -1))
        current_label = _("This Month")
        label = _("vs last month")
    
    return (c_start, c_end), (p_start, p_end), current_label, label

def get_percentage_change(current, previous):
    if previous == 0:
        return 100.0 if current > 0 else (0.0 if current == 0 else -100.0)
    change = ((current - previous) / abs(previous)) * 100.0
    return round(change, 1)

@frappe.whitelist()
def get_dashboard_data(company=None, filter_type=None, from_date=None, to_date=None):
    company = resolve_company(company)

    # إذا كانت company فارغة، نعتبرها (جميع الشركات)
    # لحساب التواريخ
    (c_start, c_end), (p_start, p_end), current_label, comparison_label = get_date_ranges(filter_type, from_date, to_date)

    data = {}
    data["comparison_label"] = comparison_label
    data["current_filter_label"] = current_label
    
    if check_permission("GL Entry") and check_permission("Account"):
        # Current Period
        c_rev = get_total_revenue(company, c_start, c_end)
        c_exp = get_total_expenses(company, c_start, c_end)
        c_prof = c_rev - c_exp
        c_cash = get_cash_flow(company, c_start, c_end)
        
        # Previous Period
        p_rev = get_total_revenue(company, p_start, p_end)
        p_exp = get_total_expenses(company, p_start, p_end)
        p_prof = p_rev - p_exp
        p_cash = get_cash_flow(company, p_start, p_end)

        data["financials"] = {
            "total_revenue": c_rev,
            "total_expenses": c_exp,
            "net_profit": c_prof,
            "cash_flow": c_cash,
            
            "comparisons": {
                "revenue": get_percentage_change(c_rev, p_rev),
                "expenses": get_percentage_change(c_exp, p_exp),
                "profit": get_percentage_change(c_prof, p_prof),
                "cash_flow": get_percentage_change(c_cash, p_cash)
            },
            
            "trend_data": get_trend_data(company, c_start, c_end),
            "expenses_breakdown": get_expense_breakdown(company, c_start, c_end)
        }
    else:
        data["financials"] = None

    data["pending_approvals"] = get_pending_approvals()

    if check_permission("Sales Order") and check_permission("Sales Invoice"):
        sales_data = get_sales_trend_data(company, c_start, c_end)
        top_items = get_top_selling_items(company, c_start, c_end)
        
        data["sales"] = {
            "trend_data": sales_data,
            "top_items": top_items
        }
    else:
        data["sales"] = None

    if check_permission("Purchase Order") and check_permission("Purchase Receipt") and check_permission("Purchase Invoice"):
        transactions = get_purchase_transactions_summary(company, c_start, c_end)
        trend = get_purchase_trend_data(company, c_start, c_end)
        invoices = get_supplier_invoices_summary(company, c_start, c_end)
        
        data["purchasing"] = {
            "transactions": transactions,
            "trend": trend,
            "invoices": invoices
        }
    else:
        data["purchasing"] = None

    if check_permission("Bin") and check_permission("Item"):
        data["inventory"] = get_inventory_health(company, c_start, c_end)
    else:
        data["inventory"] = None

    data["currency"] = frappe.defaults.get_user_default("currency") or frappe.defaults.get_global_default("currency") or "SAR"
    return data

def get_total_revenue(company, from_date, to_date):
    if company:
        cond = "AND company = %s AND account IN (SELECT name FROM `tabAccount` WHERE root_type = 'Income' AND company = %s)"
        args = [from_date, to_date, company, company]
    else:
        cond = "AND account IN (SELECT name FROM `tabAccount` WHERE root_type = 'Income')"
        args = [from_date, to_date]
        
    query = f"SELECT SUM(credit) - SUM(debit) as balance FROM `tabGL Entry` WHERE posting_date BETWEEN %s AND %s {cond} AND is_cancelled = 0"
    result = frappe.db.sql(query, tuple(args), as_dict=True)
    return flt(result[0].balance) if result and result[0].balance else 0.0

def get_total_expenses(company, from_date, to_date):
    if company:
        cond = "AND company = %s AND account IN (SELECT name FROM `tabAccount` WHERE root_type = 'Expense' AND company = %s)"
        args = [from_date, to_date, company, company]
    else:
        cond = "AND account IN (SELECT name FROM `tabAccount` WHERE root_type = 'Expense')"
        args = [from_date, to_date]
        
    query = f"SELECT SUM(debit) - SUM(credit) as balance FROM `tabGL Entry` WHERE posting_date BETWEEN %s AND %s {cond} AND is_cancelled = 0"
    result = frappe.db.sql(query, tuple(args), as_dict=True)
    return flt(result[0].balance) if result and result[0].balance else 0.0

def get_expense_breakdown(company, from_date, to_date):
    if company:
        cond = "AND company = %s AND account IN (SELECT name FROM `tabAccount` WHERE root_type = 'Expense' AND company = %s)"
        args = [from_date, to_date, company, company]
    else:
        cond = "AND account IN (SELECT name FROM `tabAccount` WHERE root_type = 'Expense')"
        args = [from_date, to_date]
        
    query = f"SELECT account, SUM(debit) - SUM(credit) as balance FROM `tabGL Entry` WHERE posting_date BETWEEN %s AND %s {cond} AND is_cancelled = 0 GROUP BY account ORDER BY balance DESC LIMIT 4"
    result = frappe.db.sql(query, tuple(args), as_dict=True)
    
    labels = []
    series = []
    for r in result:
        acc_name = frappe.get_cached_value("Account", r.account, "account_name") or r.account
        labels.append(_(acc_name))
        series.append(flt(r.balance))
    return {"labels": labels, "series": series}

def get_cash_flow(company, from_date, to_date):
    if company:
        cond = "AND company = %s AND account IN (SELECT name FROM `tabAccount` WHERE account_type IN ('Bank', 'Cash') AND company = %s)"
        args = [from_date, to_date, company, company]
    else:
        cond = "AND account IN (SELECT name FROM `tabAccount` WHERE account_type IN ('Bank', 'Cash'))"
        args = [from_date, to_date]
        
    query = f"SELECT SUM(debit) - SUM(credit) as balance FROM `tabGL Entry` WHERE posting_date BETWEEN %s AND %s {cond} AND is_cancelled = 0"
    result = frappe.db.sql(query, tuple(args), as_dict=True)
    return flt(result[0].balance) if result and result[0].balance else 0.0

def get_pending_approvals():
    if not check_permission("Workflow Action"): return {"count": 0, "items": []}
    actions = frappe.get_all("Workflow Action", filters={"user": frappe.session.user, "status": "Open"}, fields=["reference_doctype", "reference_name"], limit=5)
    return {"count": len(actions), "items": actions}

def get_stock_value_by_warehouse(company, to_date):
    if company:
        cond = "AND company = %s"
        args = [to_date, company]
    else:
        cond = ""
        args = [to_date]
        
    query = f"""
        SELECT warehouse, SUM(stock_value_difference) as stock_value
        FROM `tabStock Ledger Entry`
        WHERE posting_date <= %s AND is_cancelled = 0 {cond}
        GROUP BY warehouse
        HAVING SUM(stock_value_difference) > 0
        ORDER BY stock_value DESC
    """
    return frappe.db.sql(query, tuple(args), as_dict=True)

def get_low_stock_items(company, to_date):
    if company:
        cond = "AND company = %s"
        args = [to_date, company]
    else:
        cond = ""
        args = [to_date]
        
    query = f"""
        SELECT item_code, SUM(actual_qty) as actual_qty
        FROM `tabStock Ledger Entry`
        WHERE posting_date <= %s AND is_cancelled = 0 {cond}
        GROUP BY item_code
    """
    balances = frappe.db.sql(query, tuple(args), as_dict=True)
    
    ir_cond = ""
    ir_args = []
    if company:
        ir_cond = "AND (warehouse IS NULL OR warehouse IN (SELECT name FROM `tabWarehouse` WHERE company = %s))"
        ir_args = [company]
        
    ir_query = f"""
        SELECT parent as item_code, SUM(warehouse_reorder_level) as re_order_level
        FROM `tabItem Reorder`
        WHERE 1=1 {ir_cond}
        GROUP BY parent
    """
    reorder_levels_result = frappe.db.sql(ir_query, tuple(ir_args), as_dict=True)
    reorder_map = {r.item_code: flt(r.re_order_level) for r in reorder_levels_result}
    
    low_stock = []
    for b in balances:
        qty = flt(b.actual_qty)
        re_order = reorder_map.get(b.item_code, 0)
        if not re_order:
            re_order = 5.0
            
        if qty <= re_order:
            item_name = frappe.db.get_value("Item", b.item_code, "item_name") or b.item_code
            low_stock.append({
                "item_code": b.item_code,
                "item_name": item_name,
                "actual_qty": qty,
                "re_order_level": re_order,
                "ratio": (qty / re_order) if re_order > 0 else 0
            })
            
    low_stock.sort(key=lambda x: x["ratio"])
    return low_stock[:5]

def get_inventory_health(company, c_start, c_end):
    return {
        "stock_value_by_warehouse": get_stock_value_by_warehouse(company, c_end),
        "low_stock_items": get_low_stock_items(company, c_end)
    }

def get_trend_data(company, from_date, to_date):
    d1 = getdate(from_date)
    d2 = getdate(to_date)
    diff = date_diff(d2, d1)
    
    max_bins = 7
    if diff <= max_bins:
        interval_days = 1
        num_bins = diff + 1
    else:
        interval_days = max(1, diff // max_bins)
        num_bins = max_bins
        
    labels, revenues, expenses, profits, cash_flows = [], [], [], [], []
    current_start = d1
    
    for i in range(num_bins):
        current_end = add_days(current_start, interval_days - 1)
        if i == num_bins - 1 or current_end > d2: current_end = d2
            
        if interval_days > 1:
            m1 = _(current_start.strftime('%b'))
            m2 = _(current_end.strftime('%b'))
            label = f"{m1} {current_start.strftime('%d')} - {m2} {current_end.strftime('%d')}"
        else:
            m1 = _(current_start.strftime('%b'))
            label = f"{m1} {current_start.strftime('%d')}"
            
        labels.append(label)
        rev = get_total_revenue(company, current_start, current_end)
        exp = get_total_expenses(company, current_start, current_end)
        csh = get_cash_flow(company, current_start, current_end)
        revenues.append(rev)
        expenses.append(exp)
        profits.append(rev - exp)
        cash_flows.append(csh)
        
        current_start = add_days(current_end, 1)
        if current_start > d2: break
            
    # Do NOT reverse to keep it chronological
    return {
        "labels": labels,
        "revenue_data": revenues,
        "expense_data": expenses,
        "profit_data": profits,
        "cash_flow_data": cash_flows
    }

def get_total_sales_orders(company, from_date, to_date):
    if company:
        cond = "AND company = %s"
        args = [from_date, to_date, company]
    else:
        cond = ""
        args = [from_date, to_date]
        
    query = f"SELECT SUM(base_grand_total) as total FROM `tabSales Order` WHERE transaction_date BETWEEN %s AND %s AND docstatus = 1 {cond}"
    result = frappe.db.sql(query, tuple(args), as_dict=True)
    return flt(result[0].total) if result and result[0].total else 0.0

def get_total_sales_invoices(company, from_date, to_date):
    if company:
        cond = "AND company = %s"
        args = [from_date, to_date, company]
    else:
        cond = ""
        args = [from_date, to_date]
        
    query = f"SELECT SUM(base_grand_total) as total FROM `tabSales Invoice` WHERE posting_date BETWEEN %s AND %s AND docstatus = 1 AND is_return = 0 {cond}"
    result = frappe.db.sql(query, tuple(args), as_dict=True)
    return flt(result[0].total) if result and result[0].total else 0.0

def get_sales_trend_data(company, from_date, to_date):
    d1 = getdate(from_date)
    d2 = getdate(to_date)
    diff = date_diff(d2, d1)
    
    max_bins = 7
    if diff <= max_bins:
        interval_days = 1
        num_bins = diff + 1
    else:
        interval_days = max(1, diff // max_bins)
        num_bins = max_bins
        
    labels, sales_orders, invoices = [], [], []
    current_start = d1
    
    for i in range(num_bins):
        current_end = add_days(current_start, interval_days - 1)
        if i == num_bins - 1 or current_end > d2: current_end = d2
            
        if interval_days > 1:
            m1 = _(current_start.strftime('%b'))
            m2 = _(current_end.strftime('%b'))
            label = f"{m1} {current_start.strftime('%d')} - {m2} {current_end.strftime('%d')}"
        else:
            m1 = _(current_start.strftime('%b'))
            label = f"{m1} {current_start.strftime('%d')}"
            
        labels.append(label)
        so_total = get_total_sales_orders(company, current_start, current_end)
        si_total = get_total_sales_invoices(company, current_start, current_end)
        
        sales_orders.append(so_total)
        invoices.append(si_total)
        
        current_start = add_days(current_end, 1)
        if current_start > d2: break
            
    return {
        "labels": labels,
        "sales_orders_data": sales_orders,
        "invoices_data": invoices
    }

def get_top_selling_items(company, from_date, to_date):
    if company:
        cond = "AND si.company = %s"
        args = [from_date, to_date, company]
    else:
        cond = ""
        args = [from_date, to_date]
        
    query = f"""
        SELECT 
            sii.item_name, 
            SUM(sii.base_net_amount) as total_sales
        FROM 
            `tabSales Invoice Item` sii
        JOIN 
            `tabSales Invoice` si ON sii.parent = si.name
        WHERE 
            si.posting_date BETWEEN %s AND %s 
            AND si.docstatus = 1 
            AND si.is_return = 0
            {cond}
        GROUP BY 
            sii.item_code, sii.item_name
        ORDER BY 
            total_sales DESC
        LIMIT 5
    """
    result = frappe.db.sql(query, tuple(args), as_dict=True)
    
    labels = []
    series = []
    for r in result:
        labels.append(_(r.item_name))
        series.append(flt(r.total_sales))
        
    return {
        "labels": labels,
        "series": series
    }

def get_purchase_transactions_summary(company, from_date, to_date):
    cond = "AND company = %s" if company else ""
    args = [from_date, to_date]
    if company: args.append(company)
    
    query = f"""
        SELECT status, COUNT(name) as count
        FROM `tabPurchase Order`
        WHERE transaction_date BETWEEN %s AND %s
        AND docstatus < 2
        {cond}
        GROUP BY status
    """
    res = frappe.db.sql(query, tuple(args), as_dict=True)
    
    total = 0
    pending = 0
    completed = 0
    
    pending_statuses = ['To Receive and Bill', 'To Bill', 'To Receive', 'Draft']
    completed_statuses = ['Completed', 'Closed']
    
    for row in res:
        total += row.count
        if row.status in pending_statuses:
            pending += row.count
        elif row.status in completed_statuses:
            completed += row.count
            
    return {
        "total": total,
        "pending": pending,
        "completed": completed
    }

def get_purchase_trend_data(company, from_date, to_date):
    d1 = getdate(from_date)
    d2 = getdate(to_date)
    diff = date_diff(d2, d1)
    
    max_bins = 7
    if diff <= max_bins:
        interval_days = 1
        num_bins = diff + 1
    else:
        interval_days = max(1, diff // max_bins)
        num_bins = max_bins
        
    labels, count_data, value_data = [], [], []
    current_start = d1
    
    for i in range(num_bins):
        current_end = add_days(current_start, interval_days - 1)
        if i == num_bins - 1 or current_end > d2: current_end = d2
            
        if interval_days > 1:
            m1 = _(current_start.strftime('%b'))
            m2 = _(current_end.strftime('%b'))
            label = f"{m1} {current_start.strftime('%d')} - {m2} {current_end.strftime('%d')}"
        else:
            m1 = _(current_start.strftime('%b'))
            label = f"{m1} {current_start.strftime('%d')}"
            
        labels.append(label)
        
        cond = "AND company = %s" if company else ""
        args = [current_start, current_end]
        if company: args.append(company)
        
        query = f"SELECT COUNT(name) as count, SUM(base_grand_total) as total FROM `tabPurchase Order` WHERE transaction_date BETWEEN %s AND %s AND docstatus = 1 {cond}"
        res = frappe.db.sql(query, tuple(args), as_dict=True)
        count = res[0].count if res and res[0].count else 0
        value = flt(res[0].total) if res and res[0].total else 0.0
        
        count_data.append(count)
        value_data.append(value)
        
        current_start = add_days(current_end, 1)
        if current_start > d2: break
            
    return {
        "labels": labels,
        "count_data": count_data,
        "value_data": value_data
    }

def get_supplier_invoices_summary(company, from_date, to_date):
    cond = "AND company = %s" if company else ""
    args = [from_date, to_date]
    if company: args.append(company)
    
    query = f"""
        SELECT status, COUNT(name) as count, SUM(base_grand_total) as total
        FROM `tabPurchase Invoice`
        WHERE posting_date BETWEEN %s AND %s
        AND docstatus = 1
        {cond}
        GROUP BY status
    """
    res = frappe.db.sql(query, tuple(args), as_dict=True)
    
    paid_count, paid_amount = 0, 0.0
    unpaid_count, unpaid_amount = 0, 0.0
    overdue_count, overdue_amount = 0, 0.0
    
    for row in res:
        if row.status == 'Paid':
            paid_count += row.count
            paid_amount += flt(row.total)
        elif row.status == 'Unpaid':
            unpaid_count += row.count
            unpaid_amount += flt(row.total)
        elif row.status == 'Overdue':
            overdue_count += row.count
            overdue_amount += flt(row.total)
            
    total_count = paid_count + unpaid_count + overdue_count
    total_amount = paid_amount + unpaid_amount + overdue_amount
            
    return {
        "paid": {"count": paid_count, "amount": paid_amount},
        "unpaid": {"count": unpaid_count, "amount": unpaid_amount},
        "overdue": {"count": overdue_count, "amount": overdue_amount},
        "total": {"count": total_count, "amount": total_amount}
    }

@frappe.whitelist()
def notify_dashboard_update(doc, method):
    """
    Called via doc_events hook when a GL Entry is inserted, updated, or trashed.
    Broadcasts a realtime event so the frontend dashboard can silently refresh.
    """
    frappe.publish_realtime(
        "madar_dashboard_update", 
        {"company": doc.company}, 
        after_commit=True
    )

@frappe.whitelist()
def check_dashboard_updates():
    """
    Lightweight polling endpoint. Returns the latest modification time of any GL Entry.
    If this changes, the frontend knows it needs to fetch new dashboard data.
    """
    try:
        # Get the latest modified timestamp from GL Entry
        result = frappe.db.sql("SELECT MAX(modified) as last_mod FROM `tabGL Entry`", as_dict=True)
        if result and result[0].last_mod:
            return str(result[0].last_mod)
        return "none"
    except Exception:
        return "error"

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
