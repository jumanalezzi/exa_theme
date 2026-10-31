
// محرك المزامنة للمفضلات
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
                        if (i.route && i.route !== '' && i.route !== 'app/home' && !seenRoutes.has(i.route)) {
                            seenRoutes.add(i.route);
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
            
            // حفظ القائمة المفضلة بشكل تلقائي إذا كانت هذه هي القائمة الافتراضية للنظام
            if (ctx.is_default_dashboard) {
                setTimeout(() => {
                    this.saveToServer(false); // true/false for showing alert
                }, 1000);
            }
        },
        saveToServer: function(showAlert = true) {
            const systemName = window.user_pref_context ? window.user_pref_context.current_system : "";
            $.ajax({
                url: '/api/method/exa_theme.api.update_dashboard_menu_for_system',
                type: 'POST',
                data: {
                    system_name: systemName,
                    menu_json: JSON.stringify(this.localArray)
                },
                headers: { 'X-Frappe-CSRF-Token': frappe.csrf_token },
                success: function(r) {
                    if (r.message && r.message.status === 'success') {
                        if (window.user_pref_context) {
                            window.user_pref_context.dashboard_menu = window.MadarFavoritesSync.localArray;
                        }
                        if (showAlert && frappe.show_alert) {
                            frappe.show_alert({
                                message: __('تم حفظ التفضيلات بنجاح'),
                                indicator: 'green'
                            });
                        }
                    }
                }
            });
        },
        syncAll: function() {
            document.querySelectorAll('.sidebar-fav-checkbox').forEach(cb => {
                const route = cb.getAttribute('data-route');
                const item = this.localArray.find(i => i.route === route);
                cb.checked = item ? (item.favorites === "1" || item.favorites == 1) : false;
            });
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
            
            this.saveToServer(true);
        }
    };
}


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
                    const cleanItemRoute = decodeURI(item.route || '');
                    const portalLink = `/exa?route=${encodeURIComponent(cleanItemRoute)}`;
                    let isFav = '';
                    let checkboxHtml = '';
                    
                    if (item.route !== 'app/home') {
                        if (window.MadarFavoritesSync && window.MadarFavoritesSync.localArray) {
                            const itemInLocal = window.MadarFavoritesSync.localArray.find(f => f.route === item.route);
                            if (itemInLocal && (itemInLocal.favorites == 1 || itemInLocal.favorites === "1")) {
                                isFav = 'checked';
                            }
                        }
                        checkboxHtml = `<input type="checkbox" class="sidebar-fav-checkbox form-check-input flex-shrink-0 ms-2 me-2" style="cursor: pointer; z-index: 2; width: 15px; height: 15px; border-color: #adb5bd;" data-route="${item.route}" ${isFav} title="إضافة/إزالة من المفضلة">`;
                    }
                    
                    html += `
                        <li class="menu-item link-item level-${currentLevel}">
                            <a href="${portalLink}" data-path="${item.path}" class="menu-link" data-route="${item.route}" data-view="${item.view_type}" >
                                <i class="${iconClass} menu-icon"></i>
                                <span class="menu-label">${label}</span>
                                ${checkboxHtml}
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

                const sidebar = document.getElementById('mainSidebar');
                const isDesktop = window.innerWidth >= 992;
                if (sidebar && sidebar.classList.contains('collapsed') && isDesktop) {
                    e.stopPropagation();
                    if (typeof MadarSidebar.showFlyoutMenu === 'function') {
                        MadarSidebar.showFlyoutMenu(this, childrenContainer);
                    }
                    return; // Stop normal accordion logic
                }

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

        // تفعيل أحداث المفضلات
        const favCheckboxes = document.querySelectorAll('.sidebar-fav-checkbox');
        favCheckboxes.forEach(cb => {
            cb.addEventListener('click', function(e) {
                e.stopPropagation(); // منع النقر من فتح الرابط
            });
            cb.addEventListener('change', function(e) {
                const route = e.target.getAttribute('data-route');
                const isChecked = e.target.checked;
                if (window.MadarFavoritesSync) {
                    window.MadarFavoritesSync.toggleFavorite(route, isChecked);
                }
            });
        });

        // Tooltips for collapsed state
        const level1Items = document.querySelectorAll('.level-1 > .folder-toggle, .level-1 > .menu-link');
        let tooltipEl = null;

        level1Items.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const sidebar = document.getElementById('mainSidebar');
                const isDesktop = window.innerWidth >= 992;
                if (sidebar && sidebar.classList.contains('collapsed') && isDesktop) {
                    if (tooltipEl) tooltipEl.remove();
                    tooltipEl = document.createElement('div');
                    tooltipEl.className = 'madar-sidebar-tooltip';
                    const label = this.querySelector('.menu-label');
                    if (label) {
                        tooltipEl.textContent = label.textContent;
                        document.body.appendChild(tooltipEl);
                        const rect = this.getBoundingClientRect();
                        const isRtl = document.documentElement.dir === "rtl" || document.body.style.direction === "rtl";
                        tooltipEl.style.top = (rect.top + (rect.height - tooltipEl.offsetHeight) / 2) + 'px';
                        if (isRtl) {
                            tooltipEl.style.right = (window.innerWidth - rect.left) + 'px';
                        } else {
                            tooltipEl.style.left = rect.right + 'px';
                        }
                    }
                }
            });
            item.addEventListener('mouseleave', function() {
                if (tooltipEl) {
                    tooltipEl.remove();
                    tooltipEl = null;
                }
            });
        });

    },
    // دالة إنشاء القائمة المنبثقة
    showFlyoutMenu: function(toggleElement, childrenContainer) {
        document.querySelectorAll('.madar-sidebar-flyout').forEach(el => el.remove());
        if (!childrenContainer) return;
        
        if (toggleElement.classList.contains('flyout-active')) {
            toggleElement.classList.remove('flyout-active');
            return;
        }
        document.querySelectorAll('.flyout-active').forEach(el => el.classList.remove('flyout-active'));
        toggleElement.classList.add('flyout-active');

        const flyout = document.createElement('div');
        flyout.className = 'madar-sidebar-flyout';
        
        flyout.innerHTML = childrenContainer.innerHTML;
        document.body.appendChild(flyout);
        
        // إزالة الحماية من التكرار من العناصر المنسوخة حتى يقبل الراوتر ربطها مجدداً
        flyout.querySelectorAll('.menu-link').forEach(link => {
            delete link.dataset.bound;
        });

        // إعادة ربط أحداث النقر للروابط داخل القائمة المنبثقة لتعمل داخل الـ iframe
        if (typeof window.MadarRouter !== 'undefined' && typeof window.MadarRouter.bindMenuClickEvents === 'function') {
            window.MadarRouter.bindMenuClickEvents();
        }
        
        const rect = toggleElement.getBoundingClientRect();
        const isRtl = document.documentElement.dir === "rtl" || document.body.style.direction === "rtl";
        
        flyout.style.top = rect.top + 'px';
        if (isRtl) {
            flyout.style.right = (window.innerWidth - rect.left) + 'px';
        } else {
            flyout.style.left = rect.right + 'px';
        }

        const flyoutToggles = flyout.querySelectorAll('.folder-toggle');
        flyoutToggles.forEach(ft => {
            ft.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                const parent = this.parentElement;
                const child = parent.querySelector('.folder-children');
                const arrow = this.querySelector('.arrow-icon');
                if (child) {
                    if (child.style.display === 'none' || child.style.display === '') {
                        child.style.display = 'block';
                        parent.classList.add('is-open');
                        if (arrow) arrow.style.transform = isRtl ? 'rotate(-90deg)' : 'rotate(90deg)';
                    } else {
                        child.style.display = 'none';
                        parent.classList.remove('is-open');
                        if (arrow) arrow.style.transform = 'rotate(0deg)';
                    }
                }
            });
        });

        const closeFlyout = (e) => {
            if (!flyout.contains(e.target) && !toggleElement.contains(e.target)) {
                flyout.remove();
                toggleElement.classList.remove('flyout-active');
                document.removeEventListener('click', closeFlyout);
            }
        };
        document.addEventListener('click', closeFlyout);

        const flyoutLinks = flyout.querySelectorAll('.menu-link');
        flyoutLinks.forEach(link => {
            link.addEventListener('click', function() {
                flyout.remove();
                toggleElement.classList.remove('flyout-active');
                document.removeEventListener('click', closeFlyout);
            });
        });
    }
};

// نقطة الانطلاق
document.addEventListener("DOMContentLoaded", function() {

    if (window.user_pref_context) {
        window.MadarFavoritesSync.init(window.user_pref_context);
    }

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