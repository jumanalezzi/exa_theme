// المحرك الرئيسي للسايدبار (Sidebar Engine)
/*document.addEventListener("DOMContentLoaded", function() {
    // ننتظر قليلاً أو نتأكد من تحميل الـ Router
    if (window.MadarRouter) {
        MadarSidebar.init();
    } else {
        // إذا لم يكن جاهزاً، ننتظر 50 ملي ثانية ونعيد المحاولة
        const checkRouter = setInterval(() => {
            if (window.MadarRouter) {
                clearInterval(checkRouter);
                MadarSidebar.init();
            }
        }, 50);
    }
});

const MadarSidebar = {
    userPref: null,
    currentLang: document.documentElement.lang || "ar",

    init: function() {
        // نأخذ البيانات التي تم حقنها في الـ context الخاص بـ Jinja في صفحة madar.html
        if (window.user_pref_context) {
            this.userPref = window.user_pref_context;
            this.startEngine();
        } else {
            this.fetchSettingsFromServer();
        }
    },

    // دالة جلب البيانات من ملف البايثون
    fetchSettingsFromServer: function() {
        const me = this;
        frappe.call({
            method: "admin.admin.www.madar.get_user_preferences", // عدل المسار حسب هيكلة تطبيقك
            callback: function(r) {
                if (r.message && !r.message.error) {
                    me.userPref = r.message;
                    me.startEngine();
                }
            }
        });
    },

    startEngine: function() {
        // تهيئة محرك المزامنة للمفضلات وبناء المصفوفة المحلية
        if (!window.MadarFavoritesSync) {
            window.MadarFavoritesSync = {
                localArray: [],
                init: function(contextObj) {
                    const ctx = contextObj || window.user_pref_context || {};
                    let allMenu = ctx.custom_menu_json || [];
                    if (typeof allMenu === 'string') {
                        try { allMenu = JSON.parse(allMenu); } catch(e) { allMenu = []; }
                    }
                    let savedFavs = ctx.dashboard_menu || [];
                    if (typeof savedFavs === 'string') {
                        try { savedFavs = JSON.parse(savedFavs); } catch(e) { savedFavs = []; }
                    }
                    
                    const extractedLinks = [];
                    const seenRoutes = new Set();
                    
                    const extract = (items) => {
                        if (!Array.isArray(items)) return;
                        items.forEach(i => {
                            if (i.type !== 'folder') {
                                // استثناء الرابط الفارغ وتجنب التكرار
                                if (i.route && i.route !== '' && !seenRoutes.has(i.route)) {
                                    seenRoutes.add(i.route);
                                    
                                    // التحقق من حالة المفضلة من السيرفر
                                    const savedItem = savedFavs.find(f => f.route === i.route);
                                    let isFav = "0";
                                    if (savedItem && (savedItem.favorites == 1 || savedItem.favorites === "1")) {
                                        isFav = "1";
                                    }
                                    
                                    extractedLinks.push({
                                        ...i,
                                        favorites: isFav
                                    });
                                }
                            } else if (i.children) {
                                extract(i.children);
                            }
                        });
                    };
                    extract(allMenu);
                    this.localArray = extractedLinks;
                    
                    if (extractedLinks.length === 0) {
                        setTimeout(() => {
                            let debugMsg = "Debug Info:\nallMenu isArray: " + Array.isArray(allMenu) + "\nlength: " + allMenu.length;
                            if (allMenu.length > 0) {
                                debugMsg += "\nFirst item type: " + allMenu[0].type + " route: " + allMenu[0].route;
                            }
                            alert(debugMsg);
                        }, 2000);
                    }
                },
                syncAll: function() {
                    // 1. تحديث كافة الـ checkboxes في السايدبار
                    document.querySelectorAll('.sidebar-fav-checkbox').forEach(cb => {
                        const route = cb.getAttribute('data-route');
                        const item = this.localArray.find(i => i.route === route);
                        cb.checked = item ? (item.favorites === "1" || item.favorites == 1) : false;
                    });
                    
                    // 2. تحديث الداشبورد
                    if (typeof window.renderMadarFavorites === 'function') window.renderMadarFavorites();
                    if (typeof window.renderFotarhFavorites === 'function') window.renderFotarhFavorites();
                    if (typeof window.renderRoayaFavorites === 'function') window.renderRoayaFavorites();
                },
                toggleFavorite: function(itemRoute, isChecked) {
                    const item = this.localArray.find(i => i.route === itemRoute);
                    if (item) {
                        item.favorites = isChecked ? "1" : "0";
                    }
                    
                    this.syncAll();
                    
                    // حفظ المصفوفة المحلية للسيرفر
                    const systemName = window.user_pref_context.current_system;
                    $.ajax({
                        url: '/api/method/admin.api.update_dashboard_menu_for_system',
                        type: 'POST',
                        data: {
                            system_name: systemName,
                            menu_json: JSON.stringify(this.localArray)
                        },
                        headers: { 'X-Frappe-CSRF-Token': frappe.csrf_token },
                        success: function(r) {
                            if (r.message && r.message.status === 'success') {
                                // Update window context just in case
                                window.user_pref_context.dashboard_menu = window.MadarFavoritesSync.localArray;
                                if (frappe.show_alert) {
                                    frappe.show_alert({
                                        message: isChecked ? __('تم الإضافة للمفضلة بنجاح') : __('تم الإزالة من المفضلة بنجاح'),
                                        indicator: 'green'
                                    });
                                }
                            } else {
                                if (frappe.show_alert) {
                                    frappe.show_alert({message: __('حدث خطأ أثناء حفظ المفضلة'), indicator: 'red'});
                                }
                            }
                        },
                        error: function() {
                            if (frappe.show_alert) {
                                frappe.show_alert({message: __('حدث خطأ أثناء الاتصال بالخادم'), indicator: 'red'});
                            }
                        }
                    });
                }
            };
        }
        
        // Ensure window context is set
        if (!window.user_pref_context && this.userPref) {
            window.user_pref_context = this.userPref;
        }
        
        // بناء المصفوفة
        window.MadarFavoritesSync.init(this.userPref);

        // 1. معالجة الصلاحيات للأزرار الثابتة أولاً
        this.handleAdminFeatures(this.userPref.is_admin);
        
        // 2. بناء القائمة الديناميكية شجرياً
        const dynamicContainer = document.getElementById("dynamicMenuContainer");
        if (dynamicContainer && this.userPref.custom_menu_json) {
            dynamicContainer.innerHTML = this.buildTreeHtml(this.userPref.custom_menu_json, 1);
        }

        // 🚨 التعديل الجوهري الأول: تمرير اسم النظام النشط حالياً إلى الـ Router لنجاح الـ Refresh والـ Direct Access
        if (window.MadarRouter) {
            const systemName = this.userPref.system_name || "نظام رؤى"; // تأكد من إرسال اسم النظام من السيرفر أو تخزينه
            window.MadarRouter.init(this.userPref.custom_menu_json || [], systemName);
            window.MadarRouter.handleCurrentLocation(); // معالجة الرابط الحالي فوراً بعد تهيئة الروتر
        }

        // 3. إظهار القائمة الثابتة بالكامل بعد انتهاء التحميل
        const fixedMenu = document.getElementById("fixedSettingsMenu");
        if (fixedMenu) fixedMenu.style.display = "block";

        // 4. تفعيل أحداث الضغط والفتح والإغلاق (Events)
        this.bindEvents();

        // 5. تحديد الصفحة الحالية (Set Active Element)
        this.setActivePage();
    },

    // دالة التحكم في إظهار أزرار الإدارة بناءً على صلاحية مدير النظام
    handleAdminFeatures: function(isAdmin) {
        if (isAdmin) {
            document.querySelectorAll(".admin-only").forEach(el => {
                el.style.display = "block";
            });
        }
    },

    // دالة البناء الشجري الذكي (المستويات الثلاثة)
    buildTreeHtml: function(items, currentLevel = 1) {
        if (!items || items.length === 0) return '';
        const me = this;
        let html = '<ul class="menu-list">';
        
        items.forEach(item => {
            const label = me.currentLang === 'ar' ? item.label_ar : item.label_en;
            const iconClass = item.icon ? item.icon : (item.type === 'folder' ? 'fas fa-folder' : 'fas fa-link');
            
            if (item.type === 'folder') {
                html += `
                    <li class="menu-item folder-item level-${currentLevel}">
                        <div class="folder-toggle">
                            <i class="${iconClass} menu-icon"></i>
                            <span class="menu-label">${label}</span>
                            <i class="fas fa-chevron-left arrow-icon"></i>
                        </div>
                        <div class="folder-children" style="display: none;">
                            ${me.buildTreeHtml(item.children, currentLevel + 1)}
                        </div>
                    </li>`;
            } else {
                let isFav = '';
                if (window.MadarFavoritesSync && window.MadarFavoritesSync.localArray) {
                    const itemInLocal = window.MadarFavoritesSync.localArray.find(f => f.route === item.route);
                    if (itemInLocal && (itemInLocal.favorites == 1 || itemInLocal.favorites === "1")) {
                        isFav = 'checked';
                    }
                }
                // 🚨 التعديل الجوهري الثاني: جعل الـ href يحمل سياقاً مرناً لمنع المتصفح من كسر الـ SPA وإرسال طلب صلب للسيرفر
                html += `
                    <li class="menu-item link-item level-${currentLevel} d-flex align-items-center">
                        <input type="checkbox" class="sidebar-fav-checkbox form-check-input ms-2 me-2" style="cursor: pointer; z-index: 2;" data-route="${item.route}" ${isFav} title="إضافة/إزالة من المفضلة">
                        <a href="#" class="menu-link flex-grow-1" data-route="${item.route}" data-view="${item.view_type}" data-path="${item.path}">
                            <i class="${iconClass} menu-icon"></i>
                            <span class="menu-label">${label}</span>
                        </a>
                    </li>`;
            }
        });
        
        html += '</ul>';
        return html;
    },

    // دالة معالجة نقرات السايدبار مفصولة بشكل مستقل لضمان نجاح الـ removeEventListener
    handleSidebarClick: function(e) {
        const targetLink = e.target.closest('[data-route]');
        
        if (targetLink) {
            e.preventDefault(); // إيقاف الريديركت الافتراضي للمتصفح فوراً
            
            const targetRoute = targetLink.getAttribute('data-route');
            console.log("تم التقاط الأكشن للرابط بنجاح:", targetRoute);
            
            if (window.MadarRouter) {
                window.MadarRouter.navigate(targetRoute);
            } else {
                console.error("المحرك الذكي MadarRouter غير موجود في الجلسة!");
            }
            
            if (window.innerWidth < 992) {
                const sidebar = document.getElementById('mainSidebar');
                if (sidebar && sidebar.classList.contains('collapsed')) {
                    sidebar.classList.remove('collapsed');
                }
            }
        }
    },

    // دالة تفعيل الأحداث وعمليات الفتح والإغلاق
    bindEvents: function() {
        const me = this;
        // 1. أحداث فتح وإغلاق المجلدات (كودك الأصلي تماماً دون تغيير)
        const toggles = document.querySelectorAll('.folder-toggle');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                const parent = this.parentElement;
                const children = parent.querySelector('.folder-children');
                const arrow = this.querySelector('.arrow-icon');
                const isRtl = document.documentElement.dir === "rtl";
                
                if (children.style.display === 'none') {
                    children.style.display = 'block';
                    parent.classList.add('is-open');
                    arrow.style.transform = isRtl ? 'rotate(-90deg)' : 'rotate(90deg)';
                } else {
                    children.style.display = 'none';
                    parent.classList.remove('is-open');
                    arrow.style.transform = 'rotate(0deg)';
                }
            });
        });

        // 2. 🚨 التعديل الجوهري الثالث: ربط دالة النقرات المحددة باسم تفاديًا للتكرار وضمان عزل الأحداث
        const sidebarContainer = document.getElementById('sidebarMenuContainer');
        if (sidebarContainer) {
            // الآن الـ remove تعمل بشكل حقيقي لأن الدالة أصبحت مسمّاة ولها كينونة ثابتة في الكائن
            sidebarContainer.removeEventListener('click', me.handleSidebarClick);
            sidebarContainer.addEventListener('click', me.handleSidebarClick);
            
            // إضافة مستمع للشيك بوكسات الخاصة بالمفضلة
            sidebarContainer.addEventListener('change', function(e) {
                if (e.target.classList.contains('sidebar-fav-checkbox')) {
                    const route = e.target.getAttribute('data-route');
                    const isChecked = e.target.checked;
                    if (window.MadarFavoritesSync) {
                        window.MadarFavoritesSync.toggleFavorite(route, isChecked);
                    }
                }
            });
        } else {
            console.warn("تعذر العثور على حاوية السايدبار sidebarMenuContainer لتفعيل الأكشن!");
        }
    },

    // دالة فحص وتحديد الرابط الحالي ليكون نشطاً (Active Link Highlight)
    setActivePage: function() {
        const currentRoute = window.location.pathname.replace(/^\/+/,'') || (window.frappe ? frappe.get_route_str() : "");
        
        const allLinks = document.querySelectorAll('.menu-link');
        allLinks.forEach(link => {
            const linkRoute = link.getAttribute('data-route');
            
            // مطابقة دقيقة أو جزئية للمسار لتمييز الزر
            if (linkRoute && currentRoute.includes(linkRoute) && linkRoute !== "") {
                link.classList.add('active');
                
                // ميزة ذكية: فتح المجلد الأب تلقائياً إذا كان الرابط النشط بداخله
                let parentFolder = link.closest('.folder-children');
                while (parentFolder) {
                    parentFolder.style.display = 'block';
                    const folderItem = parentFolder.closest('.folder-item');
                    if (folderItem) {
                        folderItem.classList.add('is-open');
                        const arrow = folderItem.querySelector('.arrow-icon');
                        if (arrow) {
                            const isRtl = document.documentElement.dir === "rtl";
                            arrow.style.transform = isRtl ? 'rotate(-90deg)' : 'rotate(90deg)';
                        }
                    }
                    parentFolder = folderItem ? folderItem.parentElement.closest('.folder-children') : null;
                }
            }
        });
    }
};*/
// الكائن الرئيسي للسايدبار
// الكائن الرئيسي للسايدبار
const MadarSidebar = {
    currentLang: document.documentElement.lang || "ar", // لغة الواجهة الحالية

    // دالة البناء الشجري للمجلدات والروابط داخل السايدبار
    buildTreeHtml: function() {
        const items = window.user_pref_context.custom_menu_json || [];
        
        // 🚨 هنا الحل: دالة داخلية صغيرة تستقبل الـ items والمستوى لتكرار نفسها بأمان
        const generateHtml = (menuItems, currentLevel = 1) => {
            if (!menuItems || menuItems.length === 0) return '';
            
            let html = '<ul class="menu-list">';
            
            menuItems.forEach(item => {
                const label = this.currentLang === 'ar' ? item.label_ar : item.label_en;
                const iconClass = item.icon ? item.icon : (item.type === 'folder' ? 'fas fa-folder' : 'fas fa-link');
                
                if (item.type === 'folder') {
                    // 1. إذا كان العنصر مجلداً: نستدعي الدالة الداخلية لتبني الأبناء
                    html += `
                        <li class="menu-item folder-item level-${currentLevel}">
                            <div class="folder-toggle" style="cursor: pointer;">
                                <i class="${iconClass} menu-icon"></i>
                                <span class="menu-label">${label}</span>
                                <i class="fas fa-chevron-left arrow-icon"></i>
                            </div>
                            <div class="folder-children" style="display: none;">
                                ${generateHtml(item.children, currentLevel + 1)}
                            </div>
                        </li>`;
                } else {
                    // 2. إذا كان العنصر رابطاً
                    const portalLink = `/madar?route=${encodeURIComponent(item.route)}`;
                    html += `
                        <li class="menu-item link-item level-${currentLevel}">
                            <a href="${portalLink}" data-path="${item.path}" class="menu-link" data-route="${item.route}" data-view="${item.view_type}" >
                                <i class="${iconClass} menu-icon"></i>
                                <span class="menu-label">${label}</span>
                            </a>
                        </li>`;
                }
            });
            
            html += '</ul>';
            return html;
        };

        // 🚨 عملية الحقن داخل الحاوية بعد توليد الـ HTML بالكامل
        const dynamicContainer = document.getElementById("dynamicMenuContainer");
        if (dynamicContainer) {
            if (items.length > 0) {
                dynamicContainer.innerHTML = generateHtml(items, 1);
                console.log("✅ تم بناء السايدبار وحقنه بنجاح!");
                this.bindEvents(); // تأكد من ربط الأحداث بعد الحقن 
            } else {
                dynamicContainer.innerHTML = '';
                console.log("⚠️ تم إفراغ السايدبار لعدم وجود عناصر.");
            }
        }
    },
    // ⚡ الدالة الثانية المحدثة: ربط أحداث النقر بنمط الأكورديون
    bindEvents: function() {
        const toggles = document.querySelectorAll('.folder-toggle');
        
        toggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                
                const parentListItem = this.parentElement; // li الحالي
                const childrenContainer = parentListItem.querySelector('.folder-children'); // ul الحالي
                const arrowIcon = this.querySelector('.arrow-icon');
                const isRtl = document.documentElement.dir === "rtl" || document.body.style.direction === "rtl";

                // 🚨 الحارس الذكي: التحقق مما إذا كان المجلد الحالي مغلقاً وسيتم فتحه الآن
                const isWillOpen = childrenContainer && (childrenContainer.style.display === 'none' || childrenContainer.style.display === '');

                if (isWillOpen) {
                    // 1. جلب كل المجلدات المفتوحة التي في نفس المستوى (Sibling Items)
                    const siblingListItems = parentListItem.parentElement.querySelectorAll(':scope > .folder-item');
                    
                    siblingListItems.forEach(sibling => {
                        // نتخطى المجلد الحالي الذي نقرنا عليه
                        if (sibling !== parentListItem) {
                            sibling.classList.remove('is-open');
                            
                            // إغلاق قائمة الأبناء بالكامل
                            const siblingChildren = sibling.querySelector('.folder-children');
                            if (siblingChildren) siblingChildren.style.display = 'none';
                            
                            // إرجاع السهم لوضعه الأصلي
                            const siblingArrow = sibling.querySelector('.arrow-icon');
                            if (siblingArrow) siblingArrow.style.transform = 'rotate(0deg)';

                            // 🔥 ميزة إضافية: إغلاق أي مجلد فرعي مفتوح داخل المجلدات الشقيقة لضمان التنظيف الشامل
                            const deepChildren = sibling.querySelectorAll('.folder-children');
                            deepChildren.forEach(child => child.style.display = 'none');
                            
                            const deepItems = sibling.querySelectorAll('.folder-item');
                            deepItems.forEach(item => item.classList.remove('is-open'));
                            
                            const deepArrows = sibling.querySelectorAll('.arrow-icon');
                            deepArrows.forEach(arrow => arrow.style.transform = 'rotate(0deg)');
                        }
                    });

                    // 2. الآن نفتح المجلد الحالي بأمان بعد تنظيف الساحة
                    childrenContainer.style.display = 'block';
                    parentListItem.classList.add('is-open');
                    if (arrowIcon) {
                        arrowIcon.style.transform = isRtl ? 'rotate(-90deg)' : 'rotate(90deg)';
                    }

                    // 🚨 الحل السحري لمشكلة السكرول وقفزة المنيو:
                    // نمنح المتصفح مهلة ميكرو-ثانية بسيطة حتى تنتهي حركة الإغلاق، ثم نثبت السكرول عليه
                    // setTimeout(() => {
                    //     parentListItem.scrollIntoView({
                    //         behavior: 'smooth',   // تحريك انسيابي ناعم بدون قفزة مفاجئة
                    //         block: 'nearest'      // يجلب العنصر لأقرب منطقة رؤية مرئية داخل السايدبار
                    //     });
                    // }, 50);
                } else {
                    // 3. إذا ضغط المستخدم على مجلد مفتوح أصلاً -> نقوم بإغلاقه
                    if (childrenContainer) {
                        childrenContainer.style.display = 'none';
                        parentListItem.classList.remove('is-open');
                        if (arrowIcon) {
                            arrowIcon.style.transform = 'rotate(0deg)';
                        }
                    }
                }
            });
        });
        console.log("✅ تم تفعيل نمط الأكورديون الذكي للمجلدات!");
    }
};

// نقطة الانطلاق
document.addEventListener("DOMContentLoaded", function() {
    if (window.user_pref_context && window.user_pref_context.custom_menu_json) {
        MadarSidebar.buildTreeHtml();
    } else {
        console.warn("بيانات القائمة الديناميكية custom_menu_json غير متوفرة هنا!");
    }
    
    // Ensure sidebar is closed on mobile by default
    if (window.innerWidth < 992) {
        const sidebar = document.getElementById('mainSidebar');
        if (sidebar && sidebar.classList.contains('collapsed')) {
            sidebar.classList.remove('collapsed');
        }
    }
});

window.MadarSidebar = MadarSidebar;