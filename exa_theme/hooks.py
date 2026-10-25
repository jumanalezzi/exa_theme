app_name = "exa_theme"
app_title = "Exa Theme"
app_publisher = "juman alezzi"
app_description = "Exa ERP UI theme. Product name and logos come from exa_app (exa_app/branding.py)."
app_email = "jumanalezzi@gmail.com"
app_license = "mit"
# 1. تحديد الصفحة الرئيسية للتطبيق برمجياً
home_page = "madar"

# 2. إجبار النظام على التوجه لمدار بعد نجاح تسجيل الدخول
login_redirect_url = "/madar"

# 3. إجبار النظام على التوجه لمدار بعد تسجيل الخروج 
# (ومنه سيتم سحبه للوجن لأن الجلسة انتهت)
#logout_redirect_url = "/madar"
# Apps
# ------------------

# exa_app owns the branding (name, logos) that this theme displays
required_apps = ["exa_app"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "admin",
# 		"logo": "/assets/exa_theme/logo.png",
# 		"title": "Madar",
# 		"route": "/admin",
# 		"has_permission": "exa_theme.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/exa_theme/css/admin.css"

# include js, css files in header of web template
# web_include_css = "/assets/exa_theme/css/admin.css"
# web_include_js = "/assets/exa_theme/js/admin.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "admin/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
# page_js = {"pos-awesome": "public/js/madar_pos_override.js"}


# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "admin/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "exa_theme.utils.jinja_methods",
# 	"filters": "exa_theme.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "exa_theme.install.before_install"
# after_install = "exa_theme.install.after_install"
after_install = [
    "exa_theme.setup_themes.initialize_themes",
    "exa_theme.setup_fonts.initialize_fonts",
    "exa_theme.setup_settings.initialize_madar_settings",
    "exa_theme.setup_system.run_setup"
]
# Uninstallation
# ------------

# before_uninstall = "exa_theme.uninstall.before_uninstall"
# after_uninstall = "exa_theme.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "exa_theme.utils.before_app_install"
# after_app_install = "exa_theme.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "exa_theme.utils.before_app_uninstall"
# after_app_uninstall = "exa_theme.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "exa_theme.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"GL Entry": {
		"after_insert": "exa_theme.dashboard_api.notify_dashboard_update",
		"on_trash": "exa_theme.dashboard_api.notify_dashboard_update",
        "on_update": "exa_theme.dashboard_api.notify_dashboard_update"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"exa_theme.tasks.all"
# 	],
# 	"daily": [
# 		"exa_theme.tasks.daily"
# 	],
# 	"hourly": [
# 		"exa_theme.tasks.hourly"
# 	],
# 	"weekly": [
# 		"exa_theme.tasks.weekly"
# 	],
# 	"monthly": [
# 		"exa_theme.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "exa_theme.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "exa_theme.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "exa_theme.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["exa_theme.utils.before_request"]
# after_request = ["exa_theme.utils.after_request"]

# Job Events
# ----------
# before_job = ["exa_theme.utils.before_job"]
# after_job = ["exa_theme.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"exa_theme.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
		"exa_theme.utils.get_zatca_qr_code"
	]
}

# Installation
# ------------

# before_install = "exa_theme.install.before_install"
# after_install = "exa_theme.install.after_install"
after_install = [
    "exa_theme.setup_themes.initialize_themes",
    "exa_theme.setup_fonts.initialize_fonts",
    "exa_theme.setup_settings.initialize_madar_settings",
    "exa_theme.setup_system.run_setup"
]
# Uninstallation
# ------------

# before_uninstall = "exa_theme.uninstall.before_uninstall"
# after_uninstall = "exa_theme.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "exa_theme.utils.before_app_install"
# after_app_install = "exa_theme.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "exa_theme.utils.before_app_uninstall"
# after_app_uninstall = "exa_theme.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "exa_theme.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"GL Entry": {
		"after_insert": "exa_theme.dashboard_api.notify_dashboard_update",
		"on_trash": "exa_theme.dashboard_api.notify_dashboard_update",
        "on_update": "exa_theme.dashboard_api.notify_dashboard_update"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"exa_theme.tasks.all"
# 	],
# 	"daily": [
# 		"exa_theme.tasks.daily"
# 	],
# 	"hourly": [
# 		"exa_theme.tasks.hourly"
# 	],
# 	"weekly": [
# 		"exa_theme.tasks.weekly"
# 	],
# 	"monthly": [
# 		"exa_theme.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "exa_theme.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "exa_theme.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "exa_theme.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["exa_theme.license_core.verify_app_license"]
# after_request = ["exa_theme.utils.after_request"]

# Job Events
# ----------
# before_job = ["exa_theme.utils.before_job"]
# after_job = ["exa_theme.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"exa_theme.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []



after_migrate = [
    "exa_theme.setup_system.run_setup"
]

app_include_js = ["/assets/exa_theme/js/madar_pos_cards_script.js"]
app_include_css = ["/assets/exa_theme/css/madar_pos_cards_theme.css"]

# page_css = {"pos-awesome": "public/css/madar_pos_theme.css"}
