// الكائن الرئيسي لمحرك التوجيه (Router Engine)
const MadarRouter = {
    // 🚨 [إضافة جديدة]: مخزن الكاش لتسريع الصفحات المخصصة فوراً بعد أول تحميل
    pageCache: {},

    isPosRoute: function(route) {
        if (!route) return false;
        const r = route.toLowerCase().replace(/^\/+/, '');
        return r === 'app/posapp' || r === 'posapp' ||
               r === 'app/pos-awesome' || r === 'pos-awesome' ||
               r === 'app/point-of-sale' || r === 'point-of-sale' ||
               r.startsWith('app/posapp') || r.startsWith('posapp') ||
               r.startsWith('app/pos-awesome') || r.startsWith('pos-awesome') ||
               r.startsWith('app/point-of-sale') || r.startsWith('point-of-sale');
    },

    updatePosMode: function(route) {
        const isPos = this.isPosRoute(route);
        const wrapper = document.querySelector('.madar-wrapper');
        if (isPos) {
            document.documentElement.classList.add('madar-pos-mode');
            document.body.classList.add('madar-pos-mode');
            if (wrapper) wrapper.classList.add('pos-fullscreen-mode');
            console.log("🖥️ تم تفعيل وضع ملء الشاشة لنقطة البيع (POS Mode)");
        } else {
            document.documentElement.classList.remove('madar-pos-mode');
            document.body.classList.remove('madar-pos-mode');
            if (wrapper) wrapper.classList.remove('pos-fullscreen-mode');
        }
    },
    
    // الدالة الأولى: الفحص الأولي
    checkInitialRoute: function() {
        const currentPath = window.location.pathname.replace(/^\/+/,'');
        const urlParams = new URLSearchParams(window.location.search);
        const hasRouteParam = urlParams.has('route');
        let initialRoute = urlParams.get('route') || 'app/home';
        if (initialRoute === 'app/pos-awesome' || initialRoute === 'pos-awesome') {
            initialRoute = 'app/posapp';
        }

        this.updatePosMode(initialRoute);

        if ((currentPath === "madar" || currentPath === "") && !hasRouteParam) {
            //if (frappe.session.user !== "Guest") {
                const defaultRoute = "app/home";
                const newUrl = `${window.location.origin}/madar?route=${encodeURIComponent(defaultRoute)}`;
                
                window.history.replaceState({ route: defaultRoute }, "", newUrl);
                console.log("🚀 تم رصد دخول صافي، وتحويل المسار برمجياً إلى الرئيسية:", defaultRoute);
           // }
        }
        
        // 1. تفعيل مستمع أزرار المتصفح (الخلف والأمام)
        this.initRouterListener();
        
        // 2. تفعيل الحماية ومنع التحديث لنقرات السايدبار
        this.bindMenuClickEvents();

        // 🚨 [إضافة جديدة]: تفعيل مستمع الفريم الذكي لمزامنة الروابط علوياً وعكسياً
        this.bindIframeInternalNavigation();

        // 3. شحن المحتوى الفعلي بناءً على الرابط الحالي
        this.handleCurrentRoute();
    },

    // الدالة الثانية: قراءة الرابط وشحن المحتوى بالتبديل الذكي
    handleCurrentRoute: function() {
        const urlParams = new URLSearchParams(window.location.search);
        let currentRoute = urlParams.get('route');

        if (currentRoute === 'app/pos-awesome' || currentRoute === 'pos-awesome') {
            currentRoute = 'app/posapp';
            const newUrl = `${window.location.origin}/madar?route=app%2Fposapp`;
            window.history.replaceState({ route: 'app/posapp' }, '', newUrl);
        }

        this.updatePosMode(currentRoute);

        if (!currentRoute) return;

        const menuItems1 = window.user_pref_context?.custom_menu_json || [];
        
        // مسارات الإعدادات الثابتة الخاصة بمدار
        const fixedRoutes = [
            { "route": "app/madar-theme-settings", "path": "/appearance-settings/madar-theme-settings.html", "view_type": "file" },
            { "route": "app/madar-font-settings", "path": "/appearance-settings/madar-font-settings.html", "view_type": "file" },
            { "route": "app/madar-system-settings", "path": "/appearance-settings/madar-system-settings.html", "view_type": "file" },
            { "route": "app/madar-menu-settings", "path": "/appearance-settings/madar-menu-settings.html", "view_type": "file" }
        ];
        
        // دمج المصفوفات الذكي الخاص بك
        const menuItems = [...fixedRoutes, ...menuItems1];
        
        const findRouteRecursive = (items, routeToFind) => {
            const normalizedFind = (routeToFind === 'app/pos-awesome' || routeToFind === 'pos-awesome') ? 'app/posapp' : routeToFind;
            for (let item of items) {
                const itemRouteNorm = (item.route === 'app/pos-awesome' || item.route === 'pos-awesome') ? 'app/posapp' : item.route;
                if (item.route === routeToFind || itemRouteNorm === normalizedFind) return item;
                if (item.children && item.children.length > 0) {
                    const found = findRouteRecursive(item.children, routeToFind);
                    if (found) return found;
                }
            }
            return null;
        };

        const matchedRoute = findRouteRecursive(menuItems, currentRoute);
        const iframeElement = document.getElementById('systemFrame');
        const customContainer = document.getElementById('customContentContainer');

        if (matchedRoute && (matchedRoute.view_type === 'file' || matchedRoute.path)) {
            // إذا كنا نتجه لصفحة مخصصة (مثل لوحة التحكم app/home) وكان الفريم في الخلفية على نقطة البيع، نعيد تهيئة الفريم إلى /app
            if (iframeElement) {
                try {
                    const isPos = (iframeElement.src && iframeElement.src.includes('pos')) || 
                                  (iframeElement.contentWindow && iframeElement.contentWindow.document.body && iframeElement.contentWindow.document.body.classList.contains('madar-pos-skin'));
                    if (isPos) {
                        iframeElement.src = `${window.location.origin}/app`;
                    }
                } catch(e) {}
            }

            if (customContainer) {
                const filePath = matchedRoute.path.startsWith('/') ? matchedRoute.path : '/' + matchedRoute.path;
                
                // 🚨 [تعديل ذكي]: إذا كانت الصفحة محفوظة في الكاش مسبقاً، اشحنها برمشة عين وبدون طلب شبكة
                const injectHTMLAndRunScripts = (html) => {
                    customContainer.innerHTML = html;
                    const scripts = customContainer.querySelectorAll('script');
                    scripts.forEach(oldScript => {
                        const newScript = document.createElement('script');
                        Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                        oldScript.parentNode.replaceChild(newScript, oldScript);
                    });
                };

                if (this.pageCache[filePath]) {
                    this.switchView('custom');
                    injectHTMLAndRunScripts(this.pageCache[filePath]);
                    console.log("⚡ تم شحن الصفحة المخصصة فوراً من الكاش السريع:", filePath);
                } else {
                    // إظهار اللودر أثناء سحب الملف لأول مرة فقط
                    this.switchView('loader');
                    // إضافة cache buster لمنع المتصفح من كاش الملفات الثابتة
                    const fetchPath = filePath + '?v=' + new Date().getTime();
                    fetch(fetchPath)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(filePath + " غير موجود في المسار المحدد. تأكد من أن الملف موجود في مجلد public وأن المسار صحيح.");
                            }
                            return response.text(); 
                        })
                        .then(htmlContent => {
                            this.pageCache[filePath] = htmlContent; // حفظ في الكاش للمرات القادمة
                            this.switchView('custom');
                            injectHTMLAndRunScripts(htmlContent);
                            console.log("📂 تم شحن وتحديث الصفحة المخصصة بنجاح عبر الـ Fetch:", filePath);
                        })
                        .catch(error => {
                            console.error(error);
                            this.switchView('custom');
                            customContainer.innerHTML = `<div style="color:red; padding:20px;">❌ خطأ في تحميل الصفحة: المسار غير صحيح أو الملف مفقود. <br><small>${error.message}</small></div>`;
                        });
                }
            }
        } else {
            // توجيه المسار إلى الفريم الأصلي لفرابي
            this.switchView('iframe');
            if (iframeElement) {
                const targetPath = '/' + currentRoute;
                const iframeTargetUrl = `${window.location.origin}${targetPath}`;
                const frappeRoute = currentRoute.replace(/^app\//, '');
                
                // فحص ما إذا كان الفريم حالياً في وضع شاشة نقطة البيع أو صفحة عادية
                let isInsidePos = false;
                try {
                    if (iframeElement.contentWindow) {
                        const win = iframeElement.contentWindow;
                        const doc = win.document;
                        const currentIframePath = win.location.pathname;
                        if (currentIframePath.includes('posapp') || currentIframePath.includes('pos-awesome') || currentIframePath.includes('point-of-sale') || (doc.body && doc.body.classList.contains('madar-pos-skin'))) {
                            isInsidePos = true;
                        }
                    }
                } catch(e) {}

                const targetIsPos = MadarRouter.isPosRoute(currentRoute);

                // إذا كنا ننتقل من أو إلى نقطة البيع، يجب إعادة تحميل الفريم لضمان نظافة DOM فرابي
                if (isInsidePos || targetIsPos || !iframeElement.src || !iframeElement.contentWindow || !iframeElement.contentWindow.frappe) {
                    if (iframeElement.src !== iframeTargetUrl) {
                        iframeElement.src = iframeTargetUrl;
                        console.log("🔄 تم إعادة شحن الفريم بالرابط الكامل:", iframeTargetUrl);
                    }
                } else {
                    // كلا المسارين صفحات ديسك عادية: استخدام frappe.set_route للتنقل السريع
                    try {
                        if (iframeElement.contentWindow.frappe && typeof iframeElement.contentWindow.frappe.set_route === 'function') {
                            iframeElement.contentWindow.frappe.set_route(frappeRoute);
                            console.log("⚡ تم توجيه فرابي داخلياً عبر set_route إلى:", frappeRoute);
                        } else {
                            iframeElement.src = iframeTargetUrl;
                        }
                    } catch(e) {
                        console.warn("تعذر التوجيه الداخلي، سيتم إعادة تحميل الفريم:", e);
                        iframeElement.src = iframeTargetUrl;
                    }
                }
            }
        }
    },

    // دالة الخداع البصري وإدارة الحاوية (محدثة لمنع الـ Crash)
    switchView: function(viewName) {
        const loader = document.getElementById('madarLoader');
        const iframe = document.getElementById('systemFrame');
        const custom = document.getElementById('customContentContainer');

        if (loader) loader.style.display = 'none';
        if (custom) custom.style.display = 'none';
        this.currentView = viewName;
        
        // 🚨 [الحل الجذري]: منع display:none للفريم لأنها تدمر EditorJS
        if (iframe) {
            iframe.style.display = 'block'; // يجب أن يكون block دائماً
            iframe.style.position = 'absolute';
            iframe.style.top = '0';
            iframe.style.left = '0';
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.zIndex = '1';
            iframe.style.opacity = '0';
            iframe.style.pointerEvents = 'none';
        }
        
        if (viewName === 'loader' && loader) {
            loader.style.display = 'flex';
        } else if (viewName === 'iframe' && iframe) {
            iframe.style.position = 'relative'; // عودة لوضعه الطبيعي
            iframe.style.opacity = '1';
            iframe.style.pointerEvents = 'auto';
            iframe.style.zIndex = '2';
        } else if (viewName === 'custom' && custom) {
            custom.style.display = 'block';
            custom.style.position = 'relative';
            custom.style.zIndex = '3';
        }
    },

    bindMenuClickEvents: function() {
        const me = this;
        const menuLinks = document.querySelectorAll('.menu-link');
        
        menuLinks.forEach(link => {
            // 🚨 حارس منع التكرار لحماية أحداث النقر من اللخبطة
            if (link.dataset.bound === "true") return;
            link.dataset.bound = "true";

            link.addEventListener('click', function(e) {
                e.preventDefault(); 
                let targetRoute = this.getAttribute('data-route');
                if (!targetRoute) return;
                if (targetRoute === 'app/pos-awesome' || targetRoute === 'pos-awesome') {
                    targetRoute = 'app/posapp';
                }

                const newUrl = `${window.location.origin}/madar?route=${encodeURIComponent(targetRoute)}`;
                window.history.pushState({ route: targetRoute }, "", newUrl);
                
                document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
                this.classList.add('active');

                me.handleCurrentRoute();
                
                // Close sidebar on mobile after clicking a link
                if (window.innerWidth < 992) {
                    const sidebar = document.getElementById('mainSidebar');
                    if (sidebar && sidebar.classList.contains('collapsed')) {
                        sidebar.classList.remove('collapsed');
                    }
                }
            });
        });
    },

    // 🚨 [إضافة جديدة]: دالة لقط تنقلات الفريم الداخلية ومزامنتها مع المتصفح العلوي والسايدبار عكسياً
    bindIframeInternalNavigation: function() {
        const iframeElement = document.getElementById('systemFrame');
        if (!iframeElement) return;

        iframeElement.addEventListener('load', () => {
            if (!iframeElement.contentWindow) return;

            // 🚨 حقن أكواد CSS ذكية لإظهار مسار الصفحة (Breadcrumbs) فقط مع إخفاء باقي عناصر الهيدر
            try {
                const doc = iframeElement.contentDocument || iframeElement.contentWindow.document;
                let style = doc.getElementById('madar-iframe-custom-css');
                if (!style) {
                    style = doc.createElement('style');
                    style.id = 'madar-iframe-custom-css';
                    doc.head.appendChild(style);
                }
                
                style.textContent = `
                    /* تثبيت شريط الهيدر المدمج لمسار الصفحة */
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
                        background-color: var(--card-bg, #ffffff) !important;
                        border-bottom: 1px solid var(--border-color, #e2e8f0) !important;
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

                    /* إخفاء الشعار، وحقل البحث، والإشعارات، وزر المساعدة، وشعار المستخدم */
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

                    /* تنسيق وإظهار مسار الصفحة (مسار الصفحة - Breadcrumbs) */
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
                        color: var(--text-muted, #64748b) !important;
                        text-decoration: none !important;
                        font-size: 13px !important;
                        font-weight: 500 !important;
                        transition: color 0.15s ease !important;
                    }

                    #navbar-breadcrumbs li:last-child a,
                    #navbar-breadcrumbs li:last-child span,
                    #navbar-breadcrumbs li:last-child {
                        color: var(--text-color, #1e293b) !important;
                        font-weight: 600 !important;
                    }

                    #navbar-breadcrumbs a:hover {
                        color: var(--primary, #0d6efd) !important;
                    }

                    /* ضبط ارتفاع الهيدر وموقع رأس الصفحة */
                    :root {
                        --navbar-height: 38px !important;
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
            } catch (e) {
                console.warn("إشعار: تعذر حقن CSS في الفريم لتخصيص الهيدر.");
            }

            const syncUrlToParent = () => {
                try {
                    // إذا كان المستخدم يشاهد صفحة مخصصة حالياً (مثل الداشبورد app/home أو الإعدادات)، نمنع الفريم في الخلفية من تغيير الرابط
                    if (MadarRouter.currentView !== 'iframe') {
                        return;
                    }

                    let internalRoute = iframeElement.contentWindow.location.pathname.replace(/^\/+/,'');
                    if (internalRoute === 'app' || internalRoute === '' || internalRoute === 'desk') {
                        internalRoute = 'app/home';
                    }

                    // إذا كان المسار الداخلي يطابق الصفحة الرئيسية (app/home)، نرجع لتوجيه مدار وعرض الداشبورد المخصص
                    if (internalRoute === 'app/home') {
                        const newUrl = `${window.location.origin}/madar?route=app%2Fhome`;
                        window.history.replaceState({ route: 'app/home' }, "", newUrl);
                        MadarRouter.updatePosMode('app/home');
                        MadarRouter.handleCurrentRoute();
                        return;
                    }

                    if (internalRoute.startsWith('app/')) {
                        const newUrl = `${window.location.origin}/madar?route=${encodeURIComponent(internalRoute)}`;
                        
                        // تحديث شريط المتصفح الرئيسي صامتاً ليتطابق مع مكان المستخدم الحالي داخل فرابي
                        window.history.replaceState({ route: internalRoute }, "", newUrl);
                        
                        // تحديث وضع ملء الشاشة لشاشات نقاط البيع فوراً
                        MadarRouter.updatePosMode(internalRoute);

                        // تحديث حالة Active للزر المطابق في القائمة الجانبية تلقائياً
                        document.querySelectorAll('.menu-link').forEach(link => {
                            if (link.getAttribute('data-route') === internalRoute) {
                                link.classList.add('active');
                            } else {
                                link.classList.remove('active');
                            }
                        });
                    }
                } catch (e) {
                    // أمان إضافي لتفادي قيود المتصفحات في الأصول المختلفة
                    console.warn("إشعار: تم منع مزامنة الرابط بسبب حماية النطاق الخارجي المتصل بالفريم.");
                }
            };

            try {
                // اعتراض دوال التنقل القياسية لفرابي داخل الفريم للمزامنة الفورية
                const originalPushState = iframeElement.contentWindow.history.pushState;
                iframeElement.contentWindow.history.pushState = function() {
                    originalPushState.apply(this, arguments);
                    syncUrlToParent();
                };

                const originalReplaceState = iframeElement.contentWindow.history.replaceState;
                iframeElement.contentWindow.history.replaceState = function() {
                    originalReplaceState.apply(this, arguments);
                    syncUrlToParent();
                };

                // الاستماع لأزرار التنقل الخلفي والأمامي داخل الفريم
                iframeElement.contentWindow.addEventListener('popstate', syncUrlToParent);

                // الاستماع لروتر فرابي الداخلي إن وجد
                if (iframeElement.contentWindow.frappe && iframeElement.contentWindow.frappe.router) {
                    iframeElement.contentWindow.frappe.router.on('change', () => {
                        setTimeout(syncUrlToParent, 50);
                    });
                }
            } catch (e) {
                console.warn("تعذر الوصول لـ History الخاص بالفريم بسبب قيود الأمان للمتصفح.");
            }
        });
    },

    initRouterListener: function() {
        const me = this;
        window.addEventListener('popstate', function(event) {
            me.handleCurrentRoute();
        });
    }
};

// تشغيل محرك التوجيه
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function() {
        MadarRouter.checkInitialRoute();
    });
} else {
    MadarRouter.checkInitialRoute();
}

// Expose router globally
window.MadarRouter = MadarRouter;