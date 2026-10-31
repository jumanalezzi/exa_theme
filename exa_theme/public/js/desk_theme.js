// Exa ERP theme for the standard desk (/app).
// Applies the user's Madar theme and font, opens pages full width, collapses the list "Filter By"
// sidebar by default and adds an "Appearance" item to the user menu.
// Inside the /madar frame, theme_engine.js styles the desk instead, so this script stays idle there.
(function () {
	const in_madar_frame = (() => {
		try {
			if (window.self !== window.top) return true;
			const p = window.parent && window.parent.location.pathname; return window.parent !== window && p && (p.startsWith("/exa") || p.startsWith("/madar"));
		} catch (e) {
			return true;
		}
	})();

	if (in_madar_frame) {
		// داخل الفريم: منع أي رسائل أو نوافذ منبثقة 404 وتوجيهها لشاشة مدار المصممة
		function install404Interceptor() {
			if (!window.frappe) return;

			// 1. اعتراض frappe.show_not_found
			const orig_show_not_found = frappe.show_not_found;
			frappe.show_not_found = function(page_name) {
				try {
					if (window.parent && (window.parent.ExaRouter || window.parent.MadarRouter) && typeof (window.parent.ExaRouter || window.parent.MadarRouter).show404 === 'function') {
						const route = page_name || (frappe.get_route_str ? frappe.get_route_str() : window.location.pathname);
						(window.parent.ExaRouter || window.parent.MadarRouter).show404(route);
						return;
					}
				} catch (e) {}
				if (orig_show_not_found) orig_show_not_found.apply(this, arguments);
			};

			// 2. اعتراض frappe.msgprint لمنع النافذة المنبثقة "لم يتم العثور على"
			const orig_msgprint = frappe.msgprint;
			frappe.msgprint = function(msg, title) {
				let msg_str = '';
				let title_str = '';
				if (typeof msg === 'string') {
					msg_str = msg;
				} else if (msg && typeof msg === 'object') {
					msg_str = msg.message || '';
					title_str = msg.title || '';
				}
				if (typeof title === 'string') title_str = title;

				const is_not_found = 
					(msg_str.includes('The resource you are looking for is not available') || msg_str.includes('المصدر الذي تبحث عنه غير متاح')) ||
					(title_str.includes('Not found') || title_str.includes('لم يتم العثور على')) ||
					(msg_str.includes('Workspace') && (msg_str.includes('does not exist') || msg_str.includes('غير موجود')));

				if (is_not_found) {
					try {
						if (window.parent && (window.parent.ExaRouter || window.parent.MadarRouter) && typeof (window.parent.ExaRouter || window.parent.MadarRouter).show404 === 'function') {
							const route = (frappe.get_route_str ? frappe.get_route_str() : '') || window.location.pathname;
							(window.parent.ExaRouter || window.parent.MadarRouter).show404(route);
							return null;
						}
					} catch (e) {}
				}
				return orig_msgprint ? orig_msgprint.apply(this, arguments) : null;
			};
		}

		if (window.frappe) install404Interceptor();
		$(document).ready(install404Interceptor);
		return;
	}

	// ---------- خارج الفريم: إعادة توجيه /app وكل صفحاتها تلقائياً إلى /madar ----------
	const pathname = window.location.pathname;
	if (/^\/app(\/home)?\/?$/i.test(pathname)) {
		window.location.replace("/exa");
		return;
	}

	if (pathname.startsWith("/app/")) {
		const route = pathname.replace(/^\/+/, "");
		const search = window.location.search || "";
		const hash = window.location.hash || "";
		const targetUrl = "/exa?route=" + encodeURIComponent(route) + (search ? (search.startsWith("?") ? "&" + search.substring(1) : search) : "") + hash;
		window.location.replace(targetUrl);
		return;
	}

	function is_home_route(route) {
		if (!route || !route.length) return true; // /app
		return route[0] === "Workspaces" && (!route[1] || String(route[1]).toLowerCase() === "home");
	}

	function leave_default_home() {
		if (window.frappe && frappe.get_route && is_home_route(frappe.get_route())) {
			window.location.replace("/exa");
		}
	}

	const SIDEBAR_KEY = "exa_list_sidebar_open";
	// Only Google Fonts stylesheets may be loaded; a font URL is stored by users, so anything else is ignored
	const FONT_URL = /^https:\/\/fonts\.googleapis\.com\//;

	let themes = {};
	let fonts = {};

	// ---------- full width ----------
	function default_full_width() {
		if (localStorage.container_fullwidth === undefined) {
			// Frappe's own "Toggle Full Width" setting; users can still switch it off from the user menu
			localStorage.container_fullwidth = "true";
		}
		frappe.ui.toolbar?.set_fullwidth_if_enabled?.();
	}

	// ---------- list sidebar ----------
	function apply_sidebar_state() {
		document.body.classList.toggle("exa-list-sidebar-open", localStorage.getItem(SIDEBAR_KEY) === "1");
	}

	function on_sidebar_toggle(e) {
		const btn = e.target.closest(".sidebar-toggle-btn");
		if (!btn || window.innerWidth < 992) return; // small screens keep Frappe's slide-out sidebar
		const page = btn.closest(".page-container");
		const route = (page && page.getAttribute("data-page-route")) || "";
		if (!/^(List|Report)\//.test(route)) return;
		// Frappe's own handler would toggle an inline display that fights the default-collapsed CSS
		e.stopImmediatePropagation();
		e.preventDefault();
		localStorage.setItem(SIDEBAR_KEY, localStorage.getItem(SIDEBAR_KEY) === "1" ? "0" : "1");
		apply_sidebar_state();
	}

	// ---------- theme ----------
	function hex_to_rgb(hex) {
		hex = (hex || "").replace("#", "").trim();
		if (hex.length === 3) hex = hex.split("").map((c) => c + c).join("");
		const num = parseInt(hex, 16);
		return isNaN(num) ? "13, 110, 253" : `${(num >> 16) & 255}, ${(num >> 8) & 255}, ${num & 255}`;
	}

	function theme_css(data) {
		const dark = (data.theme_mode || "light").toLowerCase() === "dark";
		const c = (data.colors && data.colors.content) || {};
		const primary = (data.colors && data.colors.palette && data.colors.palette.primary) || "#0d6efd";
		const rgb = hex_to_rgb(primary);
		const page_bg = c.page_bg || (dark ? "#151521" : "#f4f6f9");
		const surface = c.surface_bg || (dark ? "#1e1e2d" : "#ffffff");
		const input_bg = c.input_bg || (dark ? "#2b2b40" : "#ffffff");
		const text = c.text_primary || (dark ? "#ffffff" : "#212529");
		const muted = c.text_muted || (dark ? "#a1a5b7" : "#6c757d");
		const border = c.border_color || (dark ? "#323248" : "#dee2e6");
		const control_border = dark ? "rgba(255, 255, 255, 0.22)" : "#cbd5e1";
		const disabled_bg = dark ? "rgba(255, 255, 255, 0.04)" : "#f8fafc";
		const disabled_border = dark ? "rgba(255, 255, 255, 0.12)" : "#e2e8f0";
		const card_border = dark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.08)";
		const colors = data.colors || {};
		const header = colors.header || {};
		const header_btn = header.buttons || {};
		const side = (colors.sidebar && colors.sidebar.level_1) || {};
		const nav_bg = header.bg || surface;
		// A coloured header (e.g. Ocean Blue's dark blue) needs a light tint for the search box
		const [r, g, b] = hex_to_rgb(nav_bg).split(",").map(Number);
		const nav_is_dark = 0.299 * r + 0.587 * g + 0.114 * b < 140;
		const nav_text = header.text || text;
		const nav_icon = header_btn.text || muted;
		const nav_hover_bg = header_btn.hover_bg || `rgba(${rgb}, 0.08)`;
		const nav_hover_text = header_btn.hover_text || primary;
		const side_bg = side.bg || "transparent";
		const side_text = side.text || text;
		const side_hover_bg = side.hover_bg || `rgba(${rgb}, 0.08)`;
		const side_hover_text = side.hover_text || primary;
		const side_active_bg = side.active_bg || `rgba(${rgb}, 0.12)`;
		const side_active_text = side.active_text || primary;

		return `
			/* ---- top navbar: theme "header" colours ---- */
			:root { --navbar-bg: ${nav_bg}; }
			.navbar, header.navbar {
				background-color: ${nav_bg} !important;
				border-bottom: 1px solid ${border} !important;
			}
			.navbar .navbar-brand, .navbar #navbar-breadcrumbs a, .navbar #navbar-breadcrumbs span {
				color: ${nav_text} !important;
			}
			.navbar .nav-link, .navbar .navbar-nav .icon, .navbar .btn-reset {
				color: ${nav_icon} !important;
				--icon-stroke: ${nav_icon};
			}
			.navbar .nav-link:hover, .navbar .btn-reset:hover {
				background-color: ${nav_hover_bg} !important;
				color: ${nav_hover_text} !important;
			}
			.navbar .search-bar .form-control, .navbar #navbar-search {
				background-color: ${nav_is_dark ? "rgba(255, 255, 255, 0.14)" : "rgba(0, 0, 0, 0.04)"} !important;
				color: ${nav_text} !important;
				border-color: transparent !important;
			}
			.navbar #navbar-search::placeholder { color: ${nav_text} !important; opacity: 0.7; }

			/* ---- workspace sidebar: theme "sidebar level 1" colours ---- */
			.desk-sidebar, .layout-side-section .list-sidebar {
				background-color: ${side_bg} !important;
				border-radius: 10px;
			}
			.desk-sidebar .standard-sidebar-item, .desk-sidebar .sidebar-item-label,
			.desk-sidebar .standard-sidebar-item .item-anchor, .list-sidebar .sidebar-label,
			.list-sidebar .group-by-dropdown .dropdown-toggle {
				color: ${side_text} !important;
				--icon-stroke: ${side_text};
			}
			.desk-sidebar .standard-sidebar-item:hover, .desk-sidebar .standard-sidebar-item:hover .item-anchor {
				background-color: ${side_hover_bg} !important;
				color: ${side_hover_text} !important;
				--icon-stroke: ${side_hover_text};
			}
			.desk-sidebar .standard-sidebar-item.selected, .desk-sidebar .standard-sidebar-item.selected .item-anchor,
			.desk-sidebar .standard-sidebar-item.selected .sidebar-item-label {
				background-color: ${side_active_bg} !important;
				color: ${side_active_text} !important;
				font-weight: 600;
				--icon-stroke: ${side_active_text};
			}

			/* ---- page head, headings, list and table headers ---- */
			.page-head { background-color: var(--bg-color) !important; }
			.page-head .title-text, h1, h2, h3, h4, h5, .widget-title, .head-title { color: ${text} !important; }
			.list-row-head, .datatable .dt-header .dt-cell, .grid-heading-row, .report-wrapper .dt-header {
				background-color: ${dark ? "rgba(255, 255, 255, 0.04)" : `rgba(${rgb}, 0.06)`} !important;
				color: ${text} !important;
			}
			.list-row:hover, .list-row-container:hover .list-row, .datatable .dt-row:hover .dt-cell {
				background-color: rgba(${rgb}, ${dark ? "0.10" : "0.05"}) !important;
			}
			a.list-row-col.bold, .list-subject a, .form-link, .control-value a { color: ${primary} !important; }
			input[type="checkbox"]:checked { background-color: ${primary} !important; border-color: ${primary} !important; }

			/* ---- colour variables used across the desk ---- */
			:root, [data-theme="light"], [data-theme="dark"] {
				--page-bg: ${page_bg}; --bg-color: ${page_bg}; --bg-light: ${page_bg}; --bg-dark: ${surface};
				--fg-color: ${surface}; --card-bg: ${surface}; --modal-bg: ${surface}; --navbar-bg: ${surface};
				--text-color: ${text}; --text-muted: ${muted};
				--border-color: ${border}; --control-border: ${control_border}; --control-border-color: ${control_border};
				--primary: ${primary}; --primary-color: ${primary};
				--control-bg: ${input_bg}; --control-bg-on-gray: ${input_bg}; --disabled-control-bg: ${disabled_bg};
			}
			.form-control, .input-with-feedback, .frappe-control input, .frappe-control select,
			.frappe-control textarea, .awesomplete > input {
				background-color: var(--control-bg) !important;
				color: var(--text-color) !important;
				border: 1px solid var(--control-border) !important;
				border-radius: 6px !important;
				box-shadow: none !important;
			}
			.form-control:focus, .input-with-feedback:focus, .frappe-control input:focus,
			.frappe-control select:focus, .frappe-control textarea:focus, .awesomplete > input:focus {
				border-color: var(--primary) !important;
				box-shadow: 0 0 0 3px rgba(${rgb}, 0.22) !important;
			}
			.frappe-control .like-disabled-input, .form-control:disabled, .form-control[readonly], .like-disabled-input {
				background-color: ${disabled_bg} !important;
				border: 1px solid ${disabled_border} !important;
				color: var(--text-muted) !important;
			}
			.awesomplete > ul { background-color: var(--fg-color) !important; border: 1px solid var(--control-border) !important; }
			.awesomplete > ul > li:hover, .awesomplete > ul > li[aria-selected="true"] {
				background-color: rgba(${rgb}, ${dark ? "0.25" : "0.12"}) !important;
				color: var(--primary) !important;
			}
			.btn-primary, .primary-action, .show > .btn-primary.dropdown-toggle {
				background-color: var(--primary) !important;
				border-color: var(--primary) !important;
				color: #ffffff !important;
			}
			.btn-primary:hover, .primary-action:hover { filter: brightness(0.92); }
			.form-page, .form-section, .frappe-card, .layout-main-section {
				background-color: var(--fg-color) !important;
				border-color: ${card_border} !important;
			}
		`;
	}

	function style_tag(id) {
		let tag = document.getElementById(id);
		if (!tag) {
			tag = document.createElement("style");
			tag.id = id;
			document.head.appendChild(tag);
		}
		return tag;
	}

	function apply_theme(theme_id) {
		const data = themes[theme_id];
		if (!data) return;
		document.documentElement.setAttribute("data-theme", (data.theme_mode || "light").toLowerCase());
		style_tag("exa-desk-theme").textContent = theme_css(data);
		if (!localStorage.getItem("user_madar_font")) apply_font_data(data.typography);
	}

	function apply_font_data(font) {
		if (!font || !font.font_family) return;
		if (font.font_url && FONT_URL.test(font.font_url)) {
			let link = document.getElementById("exa-desk-font");
			if (!link) {
				link = document.createElement("link");
				link.id = "exa-desk-font";
				link.rel = "stylesheet";
				document.head.appendChild(link);
			}
			link.href = font.font_url;
		}
		// font_family is user-supplied; keep it to a plain font list before putting it into CSS
		const family = String(font.font_family).replace(/[^\w\s,'"-]/g, "");
		style_tag("exa-desk-font-style").textContent = `
			:root { --font-stack: ${family}; }
			body, .frappe-control, .form-control, button, input, select, textarea { font-family: ${family} !important; }
		`;
	}

	function apply_font(font_name) {
		if (fonts[font_name]) apply_font_data(fonts[font_name]);
	}

	async function load_and_apply() {
		const [theme_rows, font_rows, pref] = await Promise.all([
			frappe.db.get_list("Madar Theme", {
				fields: ["theme_id", "theme_name_ar", "theme_name_en", "theme_data", "is_default"],
				limit: 0,
			}),
			frappe.db.get_list("Madar Font", {
				fields: ["font_name", "font_name_ar", "font_name_en", "font_family", "font_url"],
				limit: 0,
			}),
			frappe.db.get_value("Madar User Preference", { user: frappe.session.user }, [
				"madar_theme",
				"madar_font",
			]),
		]);

		themes = {};
		let default_theme = null;
		(theme_rows || []).forEach((row) => {
			try {
				const data = JSON.parse(row.theme_data || "{}");
				data.theme_name_ar = row.theme_name_ar;
				data.theme_name_en = row.theme_name_en;
				themes[row.theme_id] = data;
				if (row.is_default) default_theme = row.theme_id;
			} catch (e) {
				// skip a theme whose data is not valid JSON
			}
		});
		fonts = {};
		(font_rows || []).forEach((row) => (fonts[row.font_name] = row));

		const saved = (pref && pref.message) || {};
		// Users who never picked a theme get the one marked as default
		const theme_id = themes[saved.madar_theme] ? saved.madar_theme : default_theme;
		if (theme_id) apply_theme(theme_id);
		if (saved.madar_font) apply_font(saved.madar_font);
		return saved;
	}

	// ---------- "Appearance" in the user menu ----------
	function label(row, en_field, ar_field, fallback) {
		return (frappe.boot.lang === "ar" ? row[ar_field] : row[en_field]) || row[fallback];
	}

	function open_appearance_dialog(saved) {
		const d = new frappe.ui.Dialog({
			title: __("Appearance"),
			fields: [
				{
					fieldname: "theme",
					fieldtype: "Select",
					label: __("Theme"),
					options: Object.keys(themes).map((id) => ({
						value: id,
						label: label(themes[id], "theme_name_en", "theme_name_ar", "theme_name_en"),
					})),
					default: saved.madar_theme,
				},
				{
					fieldname: "font",
					fieldtype: "Select",
					label: __("Font"),
					options: Object.keys(fonts).map((name) => ({
						value: name,
						label: label(fonts[name], "font_name_en", "font_name_ar", "font_name"),
					})),
					default: saved.madar_font,
				},
			],
			primary_action_label: __("Save"),
			primary_action: async (values) => {
				const save = (field, value) =>
					frappe.call("exa_theme.api.update_user_preference", { field, value });
				if (values.theme) {
					await save("madar_theme", values.theme);
					apply_theme(values.theme);
					saved.madar_theme = values.theme;
				}
				if (values.font) {
					await save("madar_font", values.font);
					localStorage.setItem("user_madar_font", values.font);
					apply_font(values.font);
					saved.madar_font = values.font;
				}
				d.hide();
			},
		});
		d.show();
	}

	function add_appearance_menu_item(saved) {
		const menu = document.querySelector("#toolbar-user") || document.querySelector(".dropdown-navbar-user .dropdown-menu");
		if (!menu || menu.querySelector(".exa-appearance-item")) return;
		const item = document.createElement("a");
		item.className = "dropdown-item exa-appearance-item";
		item.href = "#";
		item.textContent = __("Appearance");
		item.addEventListener("click", (e) => {
			e.preventDefault();
			open_appearance_dialog(saved);
		});
		menu.prepend(item);
	}

	// ---------- start ----------
	document.addEventListener("click", on_sidebar_toggle, true);

	$(document).ready(() => {
		if (!window.frappe || !frappe.boot || frappe.session.user === "Guest") return;
		// Clicking Home or the logo inside the desk changes the route without a page load
		frappe.router?.on("change", leave_default_home);
		default_full_width();
		apply_sidebar_state();
		load_and_apply()
			.then((saved) => add_appearance_menu_item(saved))
			.catch((e) => console.warn("Exa theme: could not load theme settings", e));
	});
})();
