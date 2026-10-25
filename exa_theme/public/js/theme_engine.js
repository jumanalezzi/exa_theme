let availableThemes = {};
let availableFonts = {};
let availableSystems = {};
let currentThemeData = null;

// اكتشاف لغة الصفحة الحالية (غالباً Frappe يضعها في وسم html)
const currentLang = document.documentElement.lang === 'ar' ? 'ar' : 'en';

// Preview Mode Logic
const urlParams = new URLSearchParams(window.location.search);
const isPreviewMode = urlParams.get('preview_theme') === 'true';

function initThemeEngine() {
    loadThemes();
    loadFonts();
    loadSystems(); // أعدنا التفعيل ليقوم بفرض النظام الافتراضي في الخلفية
}

// 0. جلب الأنظمة ومعالجة الأنظمة الإلزامية
function loadSystems() {
    console.log("جاري جلب الأنظمة...");
    const url = `/api/method/frappe.client.get_list?doctype=Madar%20System&fields=["name","system_name_ar","system_name_en","is_mandatory"]`;

    fetch(url)
        .then(response => response.json())
        .then(r => {
            if (r.message && r.message.length > 0) {
                const systemList = document.getElementById('system-dropdown-list');
                const systemSelectorContainer = document.getElementById('system-selector-container');
                if (systemList) systemList.innerHTML = ''; 

                let mandatorySystem = null;
                
                // البحث عن النظام الإلزامي
                r.message.forEach(sys => {
                    availableSystems[sys.name] = sys;
                    if (sys.is_mandatory == 1) {
                        mandatorySystem = sys;
                    }
                });

                const currentSystemName = window.user_pref_context?.current_system;

                if (mandatorySystem) {
                    // إخفاء عنصر القائمة إن وُجد
                    if (systemSelectorContainer) {
                        systemSelectorContainer.classList.remove('d-lg-block');
                        systemSelectorContainer.style.display = 'none';
                    }

                    // فرض اختيار النظام الإلزامي
                    if (currentSystemName !== mandatorySystem.name) {
                        console.log("تغيير النظام إجبارياً للنظام الإلزامي...");
                        changeSystem(mandatorySystem.name, true);
                    } else {
                        // تحديث الاسم فقط إن كنا فعلاً على النظام الإلزامي
                        updateSystemHeaderName(mandatorySystem);
                    }
                } else {
                    // إذا لم يكن هناك نظام إلزامي، نقوم بتحديث الاسم الحالي فقط بدون إنشاء القائمة (تم الإخفاء بناء على طلب العميل)
                    if (availableSystems[currentSystemName]) {
                        updateSystemHeaderName(availableSystems[currentSystemName]);
                    }
                }
            } else {
                console.warn("لم يتم العثور على أي أنظمة.");
            }
        })
        .catch(err => console.error("خطأ في الاتصال بالسيرفر لجلب الأنظمة:", err));
}

function updateSystemHeaderName(sys) {
    const sysDisplayName = currentLang === 'ar' ? sys.system_name_ar : sys.system_name_en;
    const sysNameElement = document.getElementById('current-system-name');
    if (sysNameElement) sysNameElement.innerText = sysDisplayName;
}

function changeSystem(systemName, isForced = false) {
    if (!systemName) return;
    
    // 1. تحديث اسم النظام في الهيدر فوراً للشعور بالاستجابة
    if (availableSystems[systemName]) {
        updateSystemHeaderName(availableSystems[systemName]);
    }

    // 2. تحديث التفضيلات في قاعدة البيانات
    if (window.$ || window.jQuery) {
        $.ajax({
            url: '/api/method/exa_theme.api.update_user_preference',
            type: 'POST',
            dataType: 'json',
            data: { field: 'current_system', value: systemName },
            headers: { 'X-Frappe-CSRF-Token': frappe.csrf_token },
            success: function(response) {
                console.log("تم تغيير النظام بنجاح:", systemName);
                
                // 3. جلب التفضيلات الجديدة (شاملة القائمة الجانبية) لتحديث السايدبار
                $.ajax({
                    url: '/api/method/exa_theme.api.get_user_preferences_api',
                    type: 'GET',
                    headers: { 'X-Frappe-CSRF-Token': frappe.csrf_token },
                    success: function(prefResponse) {
                        if (prefResponse.message) {
                            // تحديث الكائن العام
                            window.user_pref_context = prefResponse.message;
                            
                            // 4. إعادة بناء السايدبار بالكامل
                            if (typeof MadarSidebar !== 'undefined' && typeof MadarSidebar.buildTreeHtml === 'function') {
                                MadarSidebar.buildTreeHtml();
                                
                                // 5. تحديث الشاشة الحالية لتتناسب مع النظام الجديد 
                                // بناءً على طلبك: نقوم بتحديث الصفحة الحالية فقط بدون توجيه للصفحة الرئيسية
                                if (typeof MadarRouter !== 'undefined') {
                                    // تشغيل مستمع الراوتر ليجلب الصفحة الحالية مجدداً بناءً على الرابط الحالي
                                    MadarRouter.handleCurrentRoute();
                                    
                                    // تحديث الأزرار النشطة في القائمة الجديدة
                                    if (typeof MadarSidebar.setActivePage === 'function') {
                                        MadarSidebar.setActivePage();
                                    }
                                }
                            } else {
                                console.error("⚠️ لم يتم العثور على MadarSidebar في البيئة العامة.");
                            }
                        }
                    },
                    error: function(xhr) { console.error("خطأ في جلب تفضيلات النظام الجديد:", xhr); }
                });
            },
            error: function(xhr) { console.error("خطأ أثناء تغيير النظام:", xhr.responseText); }
        });
    }
}

// 1. جلب الثيمات باستخدام واجهة fetch الأصلية
function loadThemes() {
    console.log("جاري جلب الثيمات...");
    
    if (isPreviewMode) {
        // إخفاء القائمة المنسدلة بأمان باستخدام CSS
        const themeSelectors = document.querySelectorAll('.theme-selector');
        themeSelectors.forEach(selector => {
            selector.style.setProperty('display', 'none', 'important');
        });
        
        const previewThemeJson = localStorage.getItem('madar_preview_theme');
        if (previewThemeJson) {
            try {
                const previewTheme = JSON.parse(previewThemeJson);
                // إعطاء المعاينة اسماً خاصاً
                previewTheme.theme_name_ar = previewTheme.theme_name_ar || 'معاينة الثيم';
                previewTheme.theme_name_en = previewTheme.theme_name_en || 'Theme Preview';
                
                availableThemes['preview_theme'] = previewTheme;
                applyTheme('preview_theme', false, true); // true for isPreviewModeLocal
            } catch(e) {
                console.error("Invalid preview theme data:", e);
            }
        }
        return; // خروج فوراً لعدم جلب الثيمات من قاعدة البيانات
    }

    // تحديث الأعمدة المطلوبة لتشمل اللغتين
    const url = `/api/method/frappe.client.get_list?doctype=Madar%20Theme&fields=["theme_id","theme_name_ar","theme_name_en","theme_data"]`;

    fetch(url)
        .then(response => response.json())
        .then(r => {
            if (r.message && r.message.length > 0) {
                const themeList = document.getElementById('theme-dropdown-list');
                themeList.innerHTML = ''; 

                r.message.forEach(theme => {
                    // دمج بيانات الثيم مع أسماء اللغات لسهولة الوصول إليها لاحقاً
                    let themeData = JSON.parse(theme.theme_data);
                    themeData.theme_name_ar = theme.theme_name_ar;
                    themeData.theme_name_en = theme.theme_name_en;
                    
                    availableThemes[theme.theme_id] = themeData;
                    
                    // تحديد الاسم المناسب حسب لغة المستخدم
                    const themeDisplayName = currentLang === 'ar' ? theme.theme_name_ar : theme.theme_name_en;

                    const li = document.createElement('li');
                    li.innerHTML = `<a class="dropdown-item" href="#" onclick="applyTheme('${theme.theme_id}',false)">
                                        ${themeDisplayName}
                                    </a>`;
                    themeList.appendChild(li);
                });

                let savedTheme = localStorage.getItem('user_madar_theme') || 'default_light';
                if (window.user_pref_context && window.user_pref_context.madar_theme) {
                    savedTheme = window.user_pref_context.madar_theme;
                    localStorage.setItem('user_madar_theme', savedTheme);
                }
                
                if(availableThemes[savedTheme]) {
                    applyTheme(savedTheme, false);
                }
            } else {
                console.warn("تم الاتصال ولكن لم يتم العثور على أي ثيمات (تأكد من صلاحيات القراءة للـ DocType)");
            }
        })
        .catch(err => console.error("خطأ في الاتصال بالسيرفر لجلب الثيمات:", err));
}

// 2. جلب الخطوط باستخدام واجهة fetch الأصلية
function loadFonts() {
    console.log("جاري جلب الخطوط...");
    // تحديث الأعمدة لتشمل اللغتين
    const url = `/api/method/frappe.client.get_list?doctype=Madar%20Font&fields=["font_name","font_name_ar","font_name_en","font_family","font_url"]`;

    fetch(url)
        .then(response => response.json())
        .then(r => {
            if (r.message && r.message.length > 0) {
                const fontList = document.getElementById('font-dropdown-list');
                fontList.innerHTML = ''; 

                r.message.forEach(font => {
                    availableFonts[font.font_name] = font;
                    
                    // تحديد الاسم المناسب حسب لغة المستخدم
                    const fontDisplayName = currentLang === 'ar' ? font.font_name_ar : font.font_name_en;

                    const li = document.createElement('li');
                    li.innerHTML = `<a class="dropdown-item" href="#" onclick="changeTypography('${font.font_name}')">
                                        ${fontDisplayName}
                                    </a>`;
                    fontList.appendChild(li);
                });
                
                let savedFont = localStorage.getItem('user_madar_font');
                if (window.user_pref_context && window.user_pref_context.madar_font) {
                    savedFont = window.user_pref_context.madar_font;
                    localStorage.setItem('user_madar_font', savedFont);
                }
                
                if(savedFont && availableFonts[savedFont]) {
                    setTimeout(() => changeTypography(savedFont), 100);
                }
            } else {
                 console.warn("تم الاتصال ولكن لم يتم العثور على أي خطوط");
            }
        })
        .catch(err => console.error("خطأ في الاتصال بالسيرفر لجلب الخطوط:", err));
}

function applyTheme(themeId, overrideFont = true, isPreviewModeLocal = false) {
    const theme = availableThemes[themeId];
    if (!theme) return;
    
    currentThemeData = JSON.parse(JSON.stringify(theme));

    flattenAndApplyCSS(currentThemeData.colors, '');
    
    // Apply common aliases to the main document :root
    document.documentElement.style.setProperty('--bg-color', currentThemeData.colors.content.page_bg);
    document.documentElement.style.setProperty('--fg-color', currentThemeData.colors.content.surface_bg);
    document.documentElement.style.setProperty('--text-color', currentThemeData.colors.content.text_primary);
    document.documentElement.style.setProperty('--text-muted', currentThemeData.colors.content.text_muted);
    document.documentElement.style.setProperty('--border-color', currentThemeData.colors.content.border_color);
    document.documentElement.style.setProperty('--primary', currentThemeData.colors.palette.primary);
    document.documentElement.style.setProperty('--control-bg', currentThemeData.colors.content.input_bg);

    if(overrideFont && !localStorage.getItem('user_madar_font')) {
        applyTypography(currentThemeData.typography);
     
    } else if (!overrideFont && localStorage.getItem('user_madar_font')) {
       
        const savedFont = localStorage.getItem('user_madar_font');
        if(availableFonts[savedFont]) applyTypography(availableFonts[savedFont]);
    } else {
      
        applyTypography(currentThemeData.typography);
    }
    
// داخل دالة applyTheme
const logoElement = document.getElementById('main-logo'); 
//const  madarLoader = document.getElementById('madarLoader');
if (logoElement && window.madarSettings) {
    const lightLogo = window.madarSettings.logoLight;
    const darkLogo = window.madarSettings.logoDark;
    const mode = (theme.theme_mode || 'light').toLowerCase();

    console.log("Current Mode:", mode); // للتدقيق
    console.log("Logos available:", { lightLogo, darkLogo }); // للتدقيق

    let selectedLogo = "";
    if (mode.toLowerCase() === 'dark') {
        selectedLogo = lightLogo || darkLogo; 
    } else {
        selectedLogo = darkLogo || lightLogo ;
    }

    if (selectedLogo) {
        logoElement.src = selectedLogo;
       // madarLoader.src = selectedLogo; // تحديث شعار اللودر أيضاً   
        console.log("Logo updated to:", selectedLogo);
    } else {
        console.warn("No logo path found in settings!");
    }
    

}
    if (!isPreviewModeLocal) {
        localStorage.setItem('user_madar_theme', themeId);
    }
    
    // تحديث اسم الثيم الحالي في الهيدر باللغة المناسبة
    const currentThemeName = currentLang === 'ar' ? theme.theme_name_ar : theme.theme_name_en;
    const themeNameElement = document.getElementById('current-theme-name');
    if (themeNameElement) themeNameElement.innerText = currentThemeName;
    
    if (!isPreviewModeLocal) {
        saveUserPreference('madar_theme', themeId);
    }
    
    syncThemeToIframe(currentThemeData);
    
    // Dispatch event to notify charts and other components
    document.dispatchEvent(new CustomEvent('madarThemeApplied', { detail: { themeId } }));
}

function applyTypography(fontData) {
    if (!fontData) return;
    
    importFont(fontData.font_url);
    document.documentElement.style.setProperty('--main-font', fontData.font_family);
    
    // تحديث اسم الخط الحالي في الهيدر باللغة المناسبة
    const fontDisplayName = currentLang === 'ar' ? (fontData.font_name_ar || fontData.font_name) : (fontData.font_name_en || fontData.font_name);
    const fontNameElement = document.getElementById('current-font-name');
    if (fontNameElement) fontNameElement.innerText = fontDisplayName;
    
    if(fontData.font_url) { 
        currentThemeData.typography = fontData;
    }
    saveUserPreference('madar_font', fontData.font_name);
}

function changeTypography(fontName) {
    if (!currentThemeData || !availableFonts[fontName]) return;

    const fontData = availableFonts[fontName];
    applyTypography(fontData);
    localStorage.setItem('user_madar_font', fontName);
    
    syncThemeToIframe(currentThemeData);
}

function flattenAndApplyCSS(obj, prefix) {
    for (let key in obj) {
        if (typeof obj[key] === 'object' && obj[key] !== null) {
            flattenAndApplyCSS(obj[key], `${prefix}${key}-`);
        } else {
            let val = obj[key];
            if (val === true) val = "solid";
            if (val === false) val = "none";
            const cssVar = `--${prefix}${key.replace(/_/g, '-')}`;
            document.documentElement.style.setProperty(cssVar, val);
        }
    }
}

function importFont(url) {
    if (!document.querySelector(`link[href="${url}"]`)) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = url;
        document.head.appendChild(link);
    }
}

function hexToRgbString(hex) {
    if (!hex) return '13, 110, 253';
    hex = hex.replace('#', '').trim();
    if (hex.length === 3) {
        hex = hex.split('').map(c => c + c).join('');
    }
    const num = parseInt(hex, 16);
    if (isNaN(num)) return '13, 110, 253';
    return `${(num >> 16) & 255}, ${(num >> 8) & 255}, ${num & 255}`;
}

function syncThemeToIframe(themeData) {
    if (!themeData) return;
    const iframe = document.getElementById('systemFrame');
    if (!iframe) return;

    try {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        if (!iframeDoc) return;
        
        let styleTag = iframeDoc.getElementById('madar-iframe-theme');
        if (!styleTag) {
            styleTag = iframeDoc.createElement('style');
            styleTag.id = 'madar-iframe-theme';
            if (iframeDoc.head) {
                iframeDoc.head.appendChild(styleTag);
            } else {
                return; // head not ready
            }
        }
        
        const themeMode = (themeData.theme_mode || 'light').toLowerCase();
        const isDark = themeMode === 'dark';
        iframeDoc.documentElement.setAttribute('data-theme', themeMode);

        const primaryColor = (themeData.colors && themeData.colors.palette && themeData.colors.palette.primary) || '#0d6efd';
        const primaryRgb = hexToRgbString(primaryColor);

        const pageBg = (themeData.colors && themeData.colors.content && themeData.colors.content.page_bg) || (isDark ? '#151521' : '#f4f6f9');
        const surfaceBg = (themeData.colors && themeData.colors.content && themeData.colors.content.surface_bg) || (isDark ? '#1e1e2d' : '#ffffff');
        const inputBg = (themeData.colors && themeData.colors.content && themeData.colors.content.input_bg) || (isDark ? '#2b2b40' : '#ffffff');
        const textPrimary = (themeData.colors && themeData.colors.content && themeData.colors.content.text_primary) || (isDark ? '#ffffff' : '#212529');
        const textMuted = (themeData.colors && themeData.colors.content && themeData.colors.content.text_muted) || (isDark ? '#a1a5b7' : '#6c757d');
        const themeBorder = (themeData.colors && themeData.colors.content && themeData.colors.content.border_color) || (isDark ? '#323248' : '#dee2e6');

        // Control border with guaranteed high visibility and crisp contrast
        const controlBorder = isDark ? 'rgba(255, 255, 255, 0.22)' : '#cbd5e1';
        const controlBorderHover = primaryColor;
        const disabledControlBg = isDark ? 'rgba(255, 255, 255, 0.04)' : '#f8fafc';
        const disabledControlBorder = isDark ? 'rgba(255, 255, 255, 0.12)' : '#e2e8f0';
        const cardBorder = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)';
        
        const cssOverrides = `
            :root, [data-theme="light"], [data-theme="dark"] {
                --page-bg: ${pageBg} !important;
                --bg-color: ${pageBg} !important;
                --bg-light: ${pageBg} !important;
                --bg-dark: ${surfaceBg} !important;
                --fg-color: ${surfaceBg} !important;
                --card-bg: ${surfaceBg} !important;
                --modal-bg: ${surfaceBg} !important;
                --text-color: ${textPrimary} !important;
                --text-muted: ${textMuted} !important;
                --border-color: ${themeBorder} !important;
                --control-border: ${controlBorder} !important;
                --control-border-color: ${controlBorder} !important;
                --border-subtle: ${isDark ? 'rgba(255, 255, 255, 0.1)' : '#e2e8f0'} !important;
                --primary: ${primaryColor} !important;
                --primary-color: ${primaryColor} !important;
                --control-bg: ${inputBg} !important;
                --control-bg-on-gray: ${inputBg} !important;
                --disabled-control-bg: ${disabledControlBg} !important;
                --font-stack: ${(themeData.typography && themeData.typography.font_family) || 'inherit'} !important;
            }
            
            /* =========================================================
               Form Controls & Inputs Visibility (Customer, Company, Links, etc.)
               ========================================================= */
            
            /* All Input, Select, Textarea, Link, and Data fields */
            .form-control,
            .input-with-feedback,
            .frappe-control input,
            .frappe-control select,
            .frappe-control textarea,
            .frappe-control[data-fieldtype="Link"] .input-with-feedback,
            .frappe-control[data-fieldtype="Dynamic Link"] .input-with-feedback,
            .frappe-control[data-fieldtype="Select"] select,
            .frappe-control[data-fieldtype="Date"] input,
            .frappe-control[data-fieldtype="Datetime"] input,
            .frappe-control[data-fieldtype="Data"] input,
            .frappe-control[data-fieldtype="Currency"] input,
            .frappe-control[data-fieldtype="Int"] input,
            .frappe-control[data-fieldtype="Float"] input,
            .input-group .form-control,
            .awesomplete > input,
            .grid-row .form-control,
            .grid-body .form-control,
            .form-grid .form-control,
            .filter-field .form-control,
            .search-bar .form-control {
                background-color: var(--control-bg) !important;
                color: var(--text-color) !important;
                border: 1px solid var(--control-border) !important;
                border-radius: 6px !important;
                box-shadow: none !important;
                font-family: inherit !important;
                transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, background-color 0.15s ease-in-out !important;
            }
            
            /* Input Placeholder */
            .form-control::placeholder,
            .input-with-feedback::placeholder,
            .frappe-control input::placeholder {
                color: var(--text-muted) !important;
                opacity: 0.65 !important;
            }
            
            /* Hover State */
            .form-control:hover:not(:disabled):not([readonly]),
            .input-with-feedback:hover:not(:disabled):not([readonly]),
            .frappe-control input:hover:not(:disabled):not([readonly]),
            .frappe-control select:hover:not(:disabled):not([readonly]),
            .frappe-control textarea:hover:not(:disabled):not([readonly]) {
                border-color: ${controlBorderHover} !important;
            }
            
            /* Focus State */
            .form-control:focus,
            .input-with-feedback:focus,
            .frappe-control input:focus,
            .frappe-control select:focus,
            .frappe-control textarea:focus,
            .awesomplete > input:focus {
                background-color: var(--control-bg) !important;
                color: var(--text-color) !important;
                border-color: var(--primary) !important;
                box-shadow: 0 0 0 3px rgba(${primaryRgb}, 0.22) !important;
                outline: none !important;
            }
            
            /* Readonly and Disabled Form Inputs */
            .frappe-control .like-disabled-input,
            .form-control:disabled,
            .form-control[readonly],
            .like-disabled-input {
                background-color: ${disabledControlBg} !important;
                border: 1px solid ${disabledControlBorder} !important;
                color: var(--text-muted) !important;
                border-radius: 6px !important;
                opacity: 0.88 !important;
            }
            
            /* Link Field and Dynamic Link buttons */
            .frappe-control[data-fieldtype="Link"] .link-btn,
            .frappe-control[data-fieldtype="Dynamic Link"] .link-btn {
                color: var(--text-muted) !important;
            }
            .frappe-control[data-fieldtype="Link"] .link-btn:hover,
            .frappe-control[data-fieldtype="Dynamic Link"] .link-btn:hover {
                color: var(--primary) !important;
            }
            
            /* Form Control Labels & Section Headers */
            .frappe-control .control-label,
            .form-section .section-head,
            .grid-heading-row {
                color: var(--text-color) !important;
                font-weight: 600 !important;
            }
            
            .frappe-control .help-box {
                color: var(--text-muted) !important;
            }
            
            /* Fix for browser autofill turning white */
            input:-webkit-autofill,
            input:-webkit-autofill:hover, 
            input:-webkit-autofill:focus, 
            input:-webkit-autofill:active {
                -webkit-box-shadow: 0 0 0 30px var(--control-bg) inset !important;
                -webkit-text-fill-color: var(--text-color) !important;
                transition: background-color 5000s ease-in-out 0s;
            }
            
            /* Awesomplete Autocomplete Dropdown List */
            .awesomplete > ul {
                background-color: var(--fg-color) !important;
                color: var(--text-color) !important;
                border: 1px solid var(--control-border) !important;
                border-radius: 8px !important;
                box-shadow: 0 10px 25px rgba(0, 0, 0, ${isDark ? '0.4' : '0.12'}) !important;
                padding: 6px !important;
                z-index: 9999 !important;
            }
            .awesomplete > ul > li {
                border-radius: 5px !important;
                padding: 7px 12px !important;
                color: var(--text-color) !important;
                font-size: 13px !important;
            }
            .awesomplete > ul > li:hover,
            .awesomplete > ul > li[aria-selected="true"] {
                background-color: rgba(${primaryRgb}, ${isDark ? '0.25' : '0.12'}) !important;
                color: var(--primary) !important;
                font-weight: 600 !important;
            }
            .awesomplete mark {
                background-color: transparent !important;
                color: var(--primary) !important;
                font-weight: 700 !important;
                text-decoration: underline !important;
            }
            
            /* Buttons */
            .btn-primary, .primary-action,
            .btn-primary:not(:disabled):not(.disabled):active,
            .btn-primary:not(:disabled):not(.disabled).active,
            .show > .btn-primary.dropdown-toggle {
                background-color: var(--primary) !important;
                border-color: var(--primary) !important;
                color: #ffffff !important;
            }
            .btn-primary:hover, .primary-action:hover {
                filter: brightness(0.92);
                background-color: var(--primary) !important;
                border-color: var(--primary) !important;
                color: #ffffff !important;
            }
            
            /* Form Layout Cards & Grid Structure */
            .form-page, .form-section, .frappe-card {
                background-color: var(--fg-color) !important;
                border-color: ${cardBorder} !important;
            }
            .grid-row.grid-row-open {
                background-color: var(--fg-color) !important;
                border: 1px solid var(--control-border) !important;
            }
            
            /* =========================================================
               Compact Breadcrumbs Navbar (مسار الصفحة فقط)
               ========================================================= */
            :root {
                --navbar-height: 38px !important;
                --navbar-bg: ${surfaceBg} !important;
            }

            .sticky-top {
                position: sticky !important;
                top: 0 !important;
                z-index: 1000 !important;
            }

            header.navbar {
                display: flex !important;
                visibility: visible !important;
                pointer-events: auto !important;
                position: sticky !important;
                top: 0 !important;
                left: 0 !important;
                right: 0 !important;
                width: 100% !important;
                height: 38px !important;
                min-height: 38px !important;
                max-height: 38px !important;
                background-color: ${surfaceBg} !important;
                border-bottom: 1px solid ${themeBorder} !important;
                padding: 0 16px !important;
                margin: 0 !important;
                z-index: 1000 !important;
            }

            header.navbar .container,
            header.navbar .container-fluid {
                display: flex !important;
                visibility: visible !important;
                pointer-events: auto !important;
                align-items: center !important;
                justify-content: flex-start !important;
                width: 100% !important;
                max-width: 100% !important;
                height: 100% !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            /* إخفاء باقي عناصر الهيدر */
            header.navbar .navbar-brand,
            header.navbar .navbar-home,
            header.navbar .app-logo,
            header.navbar .collapse.navbar-collapse,
            header.navbar form[role="search"],
            header.navbar .search-bar,
            header.navbar .navbar-nav:not(#navbar-breadcrumbs),
            header.navbar .dropdown-notifications,
            header.navbar .dropdown-message,
            header.navbar .dropdown-help,
            header.navbar .dropdown-navbar-user,
            header.navbar .vertical-bar,
            .announcement-widget {
                display: none !important;
                visibility: hidden !important;
                width: 0 !important;
                height: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
                pointer-events: none !important;
            }

            #navbar-breadcrumbs,
            header.navbar #navbar-breadcrumbs {
                display: flex !important;
                visibility: visible !important;
                pointer-events: auto !important;
                align-items: center !important;
                list-style: none !important;
                margin: 0 !important;
                padding: 0 !important;
                font-size: 13px !important;
                line-height: 1 !important;
            }

            #navbar-breadcrumbs li {
                display: inline-flex !important;
                align-items: center !important;
                font-size: 13px !important;
            }

            #navbar-breadcrumbs a,
            #navbar-breadcrumbs span {
                color: ${textMuted} !important;
                text-decoration: none !important;
                font-size: 13px !important;
                font-weight: 500 !important;
                transition: color 0.15s ease !important;
            }

            #navbar-breadcrumbs li:last-child a,
            #navbar-breadcrumbs li:last-child span,
            #navbar-breadcrumbs li:last-child {
                color: ${textPrimary} !important;
                font-weight: 600 !important;
            }

            #navbar-breadcrumbs a:hover {
                color: ${primaryColor} !important;
            }

            .page-head {
                top: 38px !important;
            }

            .page-container {
                padding-top: 0 !important;
            }

            .layout-main {
                margin-top: 0 !important;
            }

            /* إخفاء الهيدر ومسار الصفحة بالكامل في شاشة نقطة البيع داخل الفريم */
            body.madar-pos-skin header.navbar,
            body.madar-pos-skin .sticky-top {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                min-height: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            body.madar-pos-skin .page-head {
                top: 0 !important;
            }
        `;
        
        styleTag.innerHTML = cssOverrides;
        
        if (themeData.typography && themeData.typography.font_url) {
            let fontLink = iframeDoc.getElementById('madar-iframe-font');
            if (!fontLink) {
                fontLink = iframeDoc.createElement('link');
                fontLink.id = 'madar-iframe-font';
                fontLink.rel = 'stylesheet';
                iframeDoc.head.appendChild(fontLink);
            }
            fontLink.href = themeData.typography.font_url;
        }

    } catch (e) {
        console.warn('Could not sync theme to iframe (might be cross-origin or loading):', e);
    }
}

window.syncIframeThemeOnLoad = function() {
    if (currentThemeData) {
        syncThemeToIframe(currentThemeData);
    }
};

// 1. الدالة التي تتواصل مع السيرفر
function saveUserPreference(field, value) {
    // نتحقق من وجود jQuery أولاً
    if (window.$ || window.jQuery) {
        $.ajax({
            url: '/api/method/exa_theme.api.update_user_preference',
            type: 'POST',
            dataType: 'json',
            data: {
                field: field,
                value: value
            },
            headers: {
                'X-Frappe-CSRF-Token': frappe.csrf_token
            },
            success: function(response) {
                console.log("تم حفظ التفضيلات بنجاح:", field, value);
            },
            error: function(xhr) {
                console.error("خطأ أثناء حفظ التفضيلات:", xhr.responseText);
            }
        });
    } else {
        console.error("jQuery is not loaded!");
    }
}
document.addEventListener('DOMContentLoaded', initThemeEngine);