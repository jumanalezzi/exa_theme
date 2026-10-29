// madar-search.js - Native Bootstrap Modal Search Implementation
document.addEventListener('DOMContentLoaded', () => {
    const searchModal = document.getElementById('madarSearchModal');
    
    // نقل النافذة إلى الـ body لحل مشكلة تعتيم الخلفية (Z-index/Stacking Context)
    if (searchModal) {
        document.body.appendChild(searchModal);
    }

    const searchInput = document.getElementById('madar-search-input');
    const searchResults = document.getElementById('madar-search-results');
    let debounceTimer;

    // Capture Ctrl+G shortcut to open search modal
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && (e.key === 'g' || e.key === 'G')) {
            e.preventDefault();
            if (searchModal && typeof bootstrap !== 'undefined') {
                const bsModal = bootstrap.Modal.getInstance(searchModal) || new bootstrap.Modal(searchModal);
                bsModal.show();
            }
        }
    });

    if (searchModal && searchInput) {
        // Focus input when modal opens
        searchModal.addEventListener('shown.bs.modal', () => {
            searchInput.focus();
            if (searchInput.value.trim().length > 0) {
                searchInput.dispatchEvent(new Event('input'));
            }
        });

        // Handle search typing
        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            const query = e.target.value.trim();
            
            if (query.length < 1) {
                searchResults.innerHTML = `
                    <div class="text-center p-5 text-muted">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3 text-secondary"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                        <h6 class="fw-bold text-dark">جاهز للبحث</h6>
                        <p class="small mb-0">اكتب ما تبحث عنه للبدء...</p>
                    </div>
                `;
                return;
            }

            searchResults.innerHTML = '<div class="text-center p-5 text-muted" style="margin-top: 20px;"><i class="fas fa-spinner fa-spin fa-2x mb-3"></i><br>جاري البحث...</div>';

            debounceTimer = setTimeout(() => {
                const encodedQuery = encodeURIComponent(query);
                const iframe = document.getElementById('systemFrame');
                let frappeNavResults = [];
                
                // 1. جلب نتائج Awesomebar من محرك فرابي الداخلي مباشرة
                if (iframe && iframe.contentWindow && iframe.contentWindow.frappe && iframe.contentWindow.frappe.search && iframe.contentWindow.frappe.search.utils) {
                    try {
                        const utils = iframe.contentWindow.frappe.search.utils;
                        const navSections = (typeof utils.get_nav_results === 'function' ? utils.get_nav_results(query) : []) || [];
                        
                        // معالجة أقسام النتائج وتفكيكها بدقة
                        if (Array.isArray(navSections)) {
                            navSections.forEach(section => {
                                if (section && Array.isArray(section.results)) {
                                    section.results.forEach(item => {
                                        if (item) {
                                            let labelText = '';
                                            if (typeof item.value === 'string' && item.value.trim()) {
                                                labelText = item.value.trim();
                                            } else if (typeof item.label === 'string' && item.label.trim()) {
                                                labelText = item.label.replace(/<[^>]*>?/gm, '').trim();
                                            } else if (typeof item.match === 'string' && item.match.trim()) {
                                                labelText = item.match.trim();
                                            }
                                            
                                            if (labelText) {
                                                frappeNavResults.push({
                                                    label: labelText,
                                                    type: item.type || section.title || 'صفحة',
                                                    route: item.route,
                                                    match: item.match
                                                });
                                            }
                                        }
                                    });
                                }
                            });
                        }
                        
                        // Fallback مباشر إذا كانت المصفوفة فارغة
                        if (frappeNavResults.length === 0) {
                            const doctypes = (typeof utils.get_doctypes === 'function' ? utils.get_doctypes(query) : []) || [];
                            const reports = (typeof utils.get_reports === 'function' ? utils.get_reports(query) : []) || [];
                            const pages = (typeof utils.get_pages === 'function' ? utils.get_pages(query) : []) || [];
                            const workspaces = (typeof utils.get_workspaces === 'function' ? utils.get_workspaces(query) : []) || [];
                            
                            [...doctypes, ...reports, ...pages, ...workspaces].forEach(item => {
                                let labelText = item.value || (typeof item.label === 'string' ? item.label.replace(/<[^>]*>?/gm, '') : '') || item.match || '';
                                if (labelText) {
                                    frappeNavResults.push({
                                        label: labelText,
                                        type: item.type || 'الصفحات',
                                        route: item.route,
                                        match: item.match
                                    });
                                }
                            });
                        }
                    } catch (err) {
                        console.error("Error fetching native frappe results:", err);
                    }
                }
                
                // إزالة التكرار من نتائج فرابي
                const seenNav = new Set();
                const uniqueNavResults = [];
                frappeNavResults.forEach(item => {
                    const key = (item.label + '|' + JSON.stringify(item.route)).toLowerCase();
                    if (!seenNav.has(key)) {
                        seenNav.add(key);
                        uniqueNavResults.push(item);
                    }
                });
                
                // 2. البحث في القائمة الجانبية لتطبيق مدار
                const menuResults = [];
                const customMenu = window.user_pref_context?.custom_menu_json || [];
                const currentLang = document.documentElement.lang === 'ar' ? 'ar' : 'en';

                function searchMenuRecursive(items) {
                    if (!items || !Array.isArray(items)) return;
                    items.forEach(item => {
                        const titleAr = item.title_ar || item.label_ar || item.label || item.title || '';
                        const titleEn = item.title_en || item.label_en || item.label || item.title || '';
                        const route = item.route || item.path || '';
                        const qLower = query.toLowerCase();
                        
                        if (titleAr.toLowerCase().includes(qLower) || titleEn.toLowerCase().includes(qLower)) {
                            if (route) {
                                const displayTitle = currentLang === 'ar' ? (titleAr || titleEn) : (titleEn || titleAr);
                                menuResults.push({
                                    label: displayTitle,
                                    type: 'القائمة الجانبية',
                                    route: route,
                                    isMenuRoute: true
                                });
                            }
                        }
                        if (item.children && Array.isArray(item.children)) {
                            searchMenuRecursive(item.children);
                        }
                    });
                }
                searchMenuRecursive(customMenu);

                // 3. البحث في السجلات بقاعدة البيانات (البحث الشامل)
                fetch(`/api/method/frappe.utils.global_search.search?text=${encodedQuery}&limit=10`, {
                    headers: { 'Accept': 'application/json' }
                }).then(r => r.json()).catch(() => ({}))
                .then(resData => {
                    const records = (resData && resData.message) ? resData.message : [];
                    
                    const hasNav = uniqueNavResults.length > 0;
                    const hasMenu = menuResults.length > 0;
                    const hasRecords = records.length > 0;
                    
                    if (hasNav || hasMenu || hasRecords) {
                        let html = '';
                        
                        // عرض نتائج Awesomebar (Doctypes, Pages, Reports, Workspaces)
                        if (hasNav) {
                            html += '<div class="px-3 py-2 bg-light fw-bold text-muted border-bottom d-flex justify-content-between align-items-center" style="font-size: 0.85rem;"><span><i class="fas fa-layer-group me-2"></i> قوائم، تقارير وإعدادات</span><span class="badge bg-secondary">' + uniqueNavResults.length + '</span></div>';
                            uniqueNavResults.slice(0, 30).forEach(res => {
                                const labelText = escapeHtml(res.label);
                                const routeStr = res.route ? encodeURIComponent(JSON.stringify(res.route)) : '';
                                
                                html += `
                                    <a href="#" onclick="handleSearchRoute(event, '${routeStr}', false)" 
                                       class="list-group-item list-group-item-action p-3 border-bottom">
                                        <div class="d-flex w-100 justify-content-between align-items-center">
                                            <h6 class="mb-1 fw-bold text-primary" style="font-size: 0.95rem;">${labelText}</h6>
                                            <small class="badge bg-light text-dark border">${res.type}</small>
                                        </div>
                                    </a>
                                `;
                            });
                        }

                        // عرض نتائج القائمة الجانبية لمدار
                        if (hasMenu) {
                            html += '<div class="px-3 py-2 bg-light fw-bold text-muted border-bottom d-flex justify-content-between align-items-center" style="font-size: 0.85rem;"><span><i class="fas fa-bars me-2"></i> عناصر القائمة الجانبية</span><span class="badge bg-secondary">' + menuResults.length + '</span></div>';
                            menuResults.forEach(res => {
                                const labelText = escapeHtml(res.label);
                                const routeStr = encodeURIComponent(res.route);
                                
                                html += `
                                    <a href="#" onclick="handleSearchRoute(event, '${routeStr}', true)" 
                                       class="list-group-item list-group-item-action p-3 border-bottom">
                                        <div class="d-flex w-100 justify-content-between align-items-center">
                                            <h6 class="mb-1 fw-bold text-success" style="font-size: 0.95rem;">${labelText}</h6>
                                            <small class="badge bg-success bg-opacity-10 text-success border border-success">${res.type}</small>
                                        </div>
                                    </a>
                                `;
                            });
                        }

                        // عرض السجلات المتطابقة
                        if (hasRecords) {
                            html += '<div class="px-3 py-2 bg-light fw-bold text-muted border-bottom d-flex justify-content-between align-items-center" style="font-size: 0.85rem;"><span><i class="fas fa-database me-2"></i> سجلات متطابقة</span><span class="badge bg-secondary">' + records.length + '</span></div>';
                            records.forEach(res => {
                                const title = escapeHtml(res.content || res.name || res.title || '');
                                const docName = escapeHtml(res.name || '');
                                const docType = escapeHtml(res.doctype || '');
                                const routeStr = encodeURIComponent(JSON.stringify(['Form', res.doctype, res.name]));
                                html += `
                                    <a href="#" onclick="handleSearchRoute(event, '${routeStr}', false)" 
                                       class="list-group-item list-group-item-action p-3 border-bottom">
                                        <div class="d-flex w-100 justify-content-between align-items-center">
                                            <h6 class="mb-1 fw-bold text-dark text-truncate" style="max-width: 75%; font-size: 0.95rem;">${title}</h6>
                                            <small class="badge bg-light text-dark border">${docType}</small>
                                        </div>
                                        <small class="text-muted d-block mt-1">${docName}</small>
                                    </a>
                                `;
                            });
                        }
                        
                        searchResults.innerHTML = html;
                    } else {
                        searchResults.innerHTML = `
                            <div class="text-center p-5 text-muted">
                                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3 text-secondary"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                                <h6 class="fw-bold text-dark">لا توجد نتائج</h6>
                                <p class="small mb-0">لم نتمكن من العثور على ما يطابق "${escapeHtml(query)}"</p>
                            </div>
                        `;
                    }
                })
                .catch(err => {
                    console.error('Search error:', err);
                    searchResults.innerHTML = `
                        <div class="text-center p-5 text-danger">
                            <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                            <h6 class="fw-bold mb-1">خطأ في التحميل</h6>
                            <p class="small mb-0">حدث خطأ أثناء البحث. يرجى المحاولة لاحقاً.</p>
                        </div>
                    `;
                });
            }, 250);
        });
    }
});

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// دالة لمعالجة النقر على نتائج البحث وتوجيه الفريم الداخلي بدقة
window.handleSearchRoute = function(event, routeStr, isMenuRoute) {
    if (event) event.preventDefault();
    
    if (routeStr) {
        try {
            const decodedRoute = decodeURIComponent(routeStr);
            const iframe = document.getElementById('systemFrame');
            
            if (isMenuRoute) {
                if (window.MadarRouter && typeof window.MadarRouter.handleCurrentRoute === 'function') {
                    const newUrl = `${window.location.origin}/exa?route=${encodeURIComponent(decodedRoute)}`;
                    window.history.pushState({ route: decodedRoute }, "", newUrl);
                    window.MadarRouter.handleCurrentRoute();
                } else {
                    window.location.href = `/exa?route=${encodeURIComponent(decodedRoute)}`;
                }
            } else {
                let routeArray;
                try {
                    routeArray = JSON.parse(decodedRoute);
                } catch(e) {
                    routeArray = [decodedRoute];
                }
                
                if (iframe && iframe.contentWindow && iframe.contentWindow.frappe) {
                    if (Array.isArray(routeArray)) {
                        iframe.contentWindow.frappe.set_route.apply(iframe.contentWindow.frappe, routeArray);
                    } else {
                        iframe.contentWindow.frappe.set_route(routeArray);
                    }
                    
                    if (window.MadarRouter && typeof window.MadarRouter.switchView === 'function') {
                        window.MadarRouter.switchView('iframe');
                    }
                } else {
                    if (Array.isArray(routeArray) && routeArray.length > 0) {
                        window.location.hash = '#app/' + routeArray.join('/').toLowerCase().replace(/ /g, '-');
                    }
                }
            }
        } catch (e) {
            console.error("Routing error:", e);
        }
    }
    
    // إغلاق النافذة
    if (typeof bootstrap !== 'undefined') {
        const modalEl = document.getElementById('madarSearchModal');
        if (modalEl) {
            const modalInstance = bootstrap.Modal.getInstance(modalEl);
            if (modalInstance) modalInstance.hide();
        }
    }
};
