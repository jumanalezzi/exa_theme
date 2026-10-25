// madar_pos_cards_script.js

function setupMadarItemCardsObserver() {
    function tagItemCards() {
        try {
            const root = document.body;
            if (!root.classList.contains('madar-pos-skin')) return;
            
            const cards = root.querySelectorAll('.v-card, .card-item-card, .dynamic-item-card');
            
            cards.forEach(card => {
                let isDefiniteItem = card.classList.contains('card-item-card') || card.classList.contains('dynamic-item-card');
                
                if (!isDefiniteItem) {
                    if (card.querySelector('.v-card, .card-item-card, .dynamic-item-card')) {
                        card.classList.remove('madar-item-card');
                        return;
                    }
                    if (card.querySelector('input[placeholder*="البحث"]') || 
                        card.querySelector('input[placeholder*="Search"]') ||
                        card.querySelector('.v-data-table')) {
                        card.classList.remove('madar-item-card');
                        return;
                    }
                    const hasImage = card.querySelector('.v-image, .v-responsive, img, .card-item-image, .card-item-image-container');
                    if (!hasImage) {
                        card.classList.remove('madar-item-card');
                        return;
                    }
                }
                
                if (!card.classList.contains('madar-item-card')) {
                    card.classList.add('madar-item-card');
                }
                
                if (card.classList.contains('madar-item-card')) {
                    // Tag precisely by specific classes to avoid missing anything
                    const nameEl = card.querySelector('.card-item-name');
                    if (nameEl && !nameEl.classList.contains('madar-item-title')) nameEl.classList.add('madar-item-title');
                    
                    const priceEl = card.querySelector('.card-item-price');
                    if (priceEl && !priceEl.classList.contains('madar-price-sticker')) priceEl.classList.add('madar-price-sticker');
                    
                    const stockEl = card.querySelector('.card-item-stock');
                    if (stockEl && !stockEl.classList.contains('madar-item-unit')) stockEl.classList.add('madar-item-unit');
                }
            });
            
        } catch (e) {
            console.error("Madar POS Skin Error:", e);
        }
    }

    function injectCategoriesSidebar() {
        try {
            const root = document.body;
            if (!root.classList.contains('madar-pos-skin')) return;
            
            const mainRow = document.querySelector('.dynamic-main-row');
            if (!mainRow) return;

            const itemsCol = document.querySelector('.dynamic-col:first-child');
            if (!itemsCol) return;

            hideOriginalSelector();

            if (document.getElementById('madar-categories-sidebar')) return;

            const sidebar = document.createElement('div');
            sidebar.id = 'madar-categories-sidebar';
            sidebar.className = 'madar-categories-sidebar';
            
            sidebar.innerHTML = `
                <div class="madar-sidebar-inner" style="flex: 1; overflow-y: auto; padding: 10px; box-sizing: border-box; display: flex; flex-direction: column;">
                    <div id="madar-sidebar-categories-list" style="display: flex; flex-direction: column; gap: 10px;">
                        <div class="madar-category-loader" style="text-align:center; padding: 20px; color:#999;">جاري التحميل...</div>
                    </div>
                </div>
            `;

            itemsCol.style.display = 'flex';
            itemsCol.style.flexDirection = 'row';
            itemsCol.style.alignItems = 'flex-start';
            itemsCol.insertBefore(sidebar, itemsCol.firstChild);

            // Sync height pixel-perfectly using ResizeObserver and polling
            let heightAttempts = 0;
            const heightInterval = setInterval(() => {
                heightAttempts++;
                const itemsCard = document.querySelector('.pos-items-selector .cards');
                if (itemsCard) {
                    clearInterval(heightInterval);
                    const syncSidebarHeight = () => {
                        if (sidebar && itemsCard) {
                            const style = window.getComputedStyle(itemsCard);
                            sidebar.style.height = itemsCard.offsetHeight + 'px';
                            sidebar.style.maxHeight = itemsCard.offsetHeight + 'px';
                            sidebar.style.marginTop = style.marginTop;
                            sidebar.style.marginBottom = style.marginBottom;
                        }
                    };
                    syncSidebarHeight();
                    const resizeObserver = new ResizeObserver(syncSidebarHeight);
                    resizeObserver.observe(itemsCard);
                } else if (heightAttempts > 50) {
                    clearInterval(heightInterval); // stop trying after 25s
                }
            }, 500);

            loadCategoriesIntoSidebar();

        } catch (e) {
            console.error('Madar POS Cards: Error injecting categories sidebar', e);
        }
    }

    function loadCategoriesIntoSidebar() {
        frappe.db.get_list('Item Group', {
            fields: ['name', 'image', 'is_group'],
            limit: 0
        }).then(groups => {
            const listContainer = document.getElementById('madar-sidebar-categories-list');
            if (!listContainer) return;
            
            listContainer.innerHTML = ''; 
            
            // 1. Add "ALL" option
            const allLabel = frappe._("All") || "الكل";
            const allCat = createCategoryBox("ALL", allLabel, null, true);
            listContainer.appendChild(allCat);

            // 2. Add other groups
            groups.forEach(group => {
                if (group.name !== "All Item Groups" && group.name !== "ALL" && !group.is_group) {
                    const box = createCategoryBox(group.name, group.name, group.image, false);
                    listContainer.appendChild(box);
                }
            });
        });
    }

    function createCategoryBox(id, title, imageUrl, isAll) {
        const box = document.createElement('div');
        box.className = 'madar-category-box';
        box.dataset.category = id;
        box.style.cssText = `
            background: #fff;
            border-radius: 8px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
            min-height: 80px;
            border: 2px solid transparent;
            text-align: center;
            gap: 8px;
        `;
        
        const titleEl = document.createElement('div');
        titleEl.style.cssText = `
            font-size: 13px;
            font-weight: 600;
            color: #333;
            line-height: 1.2;
            width: 100%;
        `;
        titleEl.innerText = title;
        box.appendChild(titleEl);

        if (isAll) {
            const icon = document.createElement('div');
            icon.innerHTML = `<svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>`;
            icon.style.color = '#e91e63';
            box.appendChild(icon);
        } else if (imageUrl) {
            const img = document.createElement('img');
            img.src = imageUrl;
            img.style.cssText = `
                width: 40px;
                height: 40px;
                object-fit: contain;
                border-radius: 4px;
            `;
            box.appendChild(img);
        } else {
            const placeholder = document.createElement('div');
            placeholder.innerHTML = `<svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>`;
            placeholder.style.color = '#ccc';
            box.appendChild(placeholder);
        }

        box.addEventListener('click', () => {
            document.querySelectorAll('.madar-category-box').forEach(b => b.style.borderColor = 'transparent');
            box.style.borderColor = '#e91e63'; // Highlight selected
            selectPosCategory(id);
        });

        return box;
    }

    function movePriceListField() {
        const searchRow = document.querySelector('.sticky-header .v-row.items') || document.querySelector('.pos-items-selector .sticky-header .v-row');
        const labels = Array.from(document.querySelectorAll('label'));
        const priceListLabel = labels.find(l => l.textContent.includes('Price List') || l.textContent.includes('قائمة الأسعار') || l.textContent.includes('قائمة الاسعار'));
        
        if (searchRow && priceListLabel) {
            const priceListCol = priceListLabel.closest('[class*="v-col"]');
            if (priceListCol && priceListCol.parentElement !== searchRow) {
                // Adjust widths: make Price List take more columns to prevent text cut-off, remove pt-0 to match search row's vertical alignment
                priceListCol.className = 'v-col-sm-5 v-col-md-4 v-col-lg-3 v-col-12 pb-0 madar-price-list-col';
                priceListCol.classList.remove('mb-2'); // Remove bottom margin to match search row
                
                // Find Search column and adjust its width if it doesn't have an explicit one
                const searchLabel = labels.find(l => l.textContent.includes('Search Items') || l.textContent.includes('البحث عن الأصناف') || l.textContent.includes('بحث'));
                let searchCol = null;
                if (searchLabel) {
                    searchCol = searchLabel.closest('[class*="v-col"]');
                } else {
                    // Fallback to first column
                    searchCol = searchRow.firstElementChild;
                }
                
                if (searchCol) {
                    searchCol.classList.add('madar-search-col');
                }
                
                // Move Price List right after the Search column
                if (searchCol && searchCol.nextSibling) {
                    searchRow.insertBefore(priceListCol, searchCol.nextSibling);
                } else {
                    searchRow.appendChild(priceListCol);
                }
            }
        }
    }

    let isSimulatingClick = false;

    function hideOriginalSelector() {
        // Run continuously to ensure Vue re-renders don't make it visible again
        setInterval(() => {
            if (isSimulatingClick) return;
            const labels = Array.from(document.querySelectorAll('label'));
            const targetLabel = labels.find(l => l.textContent.includes('Items Group') || l.textContent.includes('مجموعة الأصناف') || l.textContent.includes('مجموعة الاصناف') || l.textContent.includes('Item Group'));
            if (targetLabel) {
                const selectContainer = targetLabel.closest('.v-input, .v-select') || targetLabel.closest('[class*="v-col"]');
                if (selectContainer) {
                    const wrapper = selectContainer.closest('[class*="v-col"]') || selectContainer;
                    if (wrapper && !wrapper.classList.contains('madar-hidden-select')) {
                        wrapper.classList.add('madar-hidden-select');
                    }
                }
            }
        }, 500);
    }

    function forceSetItemGroup(groupName) {
        const rootEl = document.querySelector('.pos-items-selector');
        if (!rootEl) return false;

        // Check all children to find the Vue component instance
        const elements = [rootEl, ...rootEl.querySelectorAll('*')];
        
        for (let el of elements) {
            // Vue 2
            if (el.__vue__ && 'item_group' in el.__vue__) {
                el.__vue__.item_group = groupName;
                if (typeof el.__vue__.get_items === 'function') el.__vue__.get_items(true);
                return true;
            }

            // Vue 3
            for (let key in el) {
                if (key.startsWith('__vueParentComponent') || key.startsWith('__vue_app__')) {
                    let comp = el[key];
                    while (comp) {
                        // Strictly verify it's the ItemsSelector component, NOT an item card
                        if (comp.proxy && 'item_group' in comp.proxy && 'get_items' in comp.proxy && 'loadItems' in comp.proxy) {
                            comp.proxy.item_group = groupName;
                            // Ensure Vue reactivity triggers by manually calling get_items if it exists
                            if (typeof comp.proxy.get_items === 'function') {
                                setTimeout(() => comp.proxy.get_items(true), 50);
                            }
                            return true;
                        }
                        comp = comp.parent;
                    }
                }
            }
        }
        return false;
    }

    function selectPosCategory(categoryName) {
        // Try the direct Vue internal modification first (100% robust if successful)
        if (forceSetItemGroup(categoryName)) {
            console.log("Madar POS: Successfully updated item group via Vue internals.");
            return;
        }

        console.log("Madar POS: Falling back to DOM click simulation for", categoryName);
        isSimulatingClick = true;

        // Fallback to DOM click simulation if Vue internals are inaccessible
        const labels = Array.from(document.querySelectorAll('label'));
        const targetLabel = labels.find(l => l.textContent.includes('Items Group') || l.textContent.includes('مجموعة الأصناف') || l.textContent.includes('مجموعة الاصناف') || l.textContent.includes('Item Group'));
        
        if (!targetLabel) {
            console.warn("Madar POS: Could not find label for Items Group dropdown");
            isSimulatingClick = false;
            return;
        }
        
        const selectContainer = targetLabel.closest('.v-input, .v-select') || targetLabel.closest('[class*="v-col"]');
        if (!selectContainer) {
            console.warn("Madar POS: Could not find selectContainer for fallback click");
            isSimulatingClick = false;
            return;
        }

        const wrapper = selectContainer.closest('[class*="v-col"]') || selectContainer;
        
        const clickTarget = selectContainer.querySelector('.v-field') || selectContainer.querySelector('.v-input__slot') || selectContainer;
        
        if (clickTarget) {
            console.log("Madar POS: Dispatching click to native dropdown activator");
            
            // Add temporary style to hide the overlay to prevent flickering
            let hideStyle = document.getElementById('madar-hide-dropdown-overlay');
            if (!hideStyle) {
                hideStyle = document.createElement('style');
                hideStyle.id = 'madar-hide-dropdown-overlay';
                hideStyle.innerHTML = `
                    .v-overlay-container, .v-overlay, .v-menu { 
                        opacity: 0 !important; 
                        z-index: -9999 !important; 
                        left: -9999px !important; 
                        top: -9999px !important;
                    }
                `;
                document.head.appendChild(hideStyle);
            }

            clickTarget.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
            clickTarget.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            clickTarget.click(); 
            clickTarget.dispatchEvent(new PointerEvent('pointerup', { bubbles: true }));
            clickTarget.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
            
            let attempts = 0;
            const checkInterval = setInterval(() => {
                attempts++;
                const listItems = document.querySelectorAll('.v-overlay-container .v-list-item, .v-menu__content .v-list-item');
                
                if (listItems.length > 0) {
                    console.log("Madar POS: Found overlay list items, looking for", categoryName);
                    clearInterval(checkInterval);
                    let found = false;
                    for (let item of listItems) {
                        const titleEl = item.querySelector('.v-list-item-title, .v-list-item__title');
                        const titleText = titleEl ? titleEl.textContent.trim() : item.textContent.trim();
                        
                        if (titleText === categoryName || titleText.includes(categoryName) || (categoryName === 'ALL' && titleText.includes('ALL'))) {
                            console.log("Madar POS: Found matching list item, clicking it!");
                            item.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
                            item.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                            item.click();
                            item.dispatchEvent(new PointerEvent('pointerup', { bubbles: true }));
                            item.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                            found = true;
                            break;
                        }
                    }
                    if (!found) console.warn("Madar POS: Did not find matching list item for", categoryName);
                    
                    setTimeout(() => {
                        isSimulatingClick = false;
                    }, 100);
                    
                    setTimeout(() => {
                        const styleNode = document.getElementById('madar-hide-dropdown-overlay');
                        if (styleNode) styleNode.remove();
                    }, 600);
                } else if (attempts > 20) {
                    console.warn("Madar POS: Timeout waiting for overlay list items");
                    clearInterval(checkInterval);
                    isSimulatingClick = false;
                    setTimeout(() => {
                        const styleNode = document.getElementById('madar-hide-dropdown-overlay');
                        if (styleNode) styleNode.remove();
                    }, 600);
                }
            }, 50);
        } else {
            console.warn("Madar POS: Could not find clickTarget");
            isSimulatingClick = false;
        }
    }

    let attempts = 0;
    const interval = setInterval(() => {
        if (!document.body.classList.contains('madar-pos-skin')) return;
        tagItemCards();
        injectCategoriesSidebar();
        movePriceListField();
        updatePosAwesomeTitleText();
        attempts++;
        if (attempts > 10) clearInterval(interval);
    }, 500);
    
    const observer = new MutationObserver((mutations) => {
        if (!document.body.classList.contains('madar-pos-skin')) return;
        
        let shouldTag = false;
        for (let m of mutations) {
            if (m.addedNodes.length > 0) {
                shouldTag = true;
                break;
            }
        }
        if (shouldTag) {
            clearTimeout(window.madarCardsTimer);
            window.madarCardsTimer = setTimeout(() => {
                if (!document.body.classList.contains('madar-pos-skin')) return;
                tagItemCards();
                injectCategoriesSidebar();
                movePriceListField();
                moveBottomActionButtons();
                updatePosAwesomeTitleText();
            }, 150);
        }
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
}

function moveBottomActionButtons() {
    const stickyHeader = document.querySelector('.sticky-header') || document.querySelector('.pos-items-selector .sticky-header');
    const toggleBtn = document.querySelector('.view-toggle-btn');
    if (toggleBtn && stickyHeader) {
        const buttonRow = toggleBtn.closest('.v-row');
        if (buttonRow && buttonRow.parentElement !== stickyHeader) {
            // Move the row inside stickyHeader
            stickyHeader.appendChild(buttonRow);
            
            // Removed extra top/bottom margin
            buttonRow.classList.remove('mt-2', 'mb-2');

            
            // Adjust the classes for responsive layout
            const toggleCol = toggleBtn.closest('[class*="v-col"]');
            const offersBtn = Array.from(buttonRow.querySelectorAll('.v-btn')).find(b => b.textContent.includes('Offers') || b.textContent.includes('عروض'));
            const offersCol = offersBtn ? offersBtn.closest('[class*="v-col"]') : null;
            const couponsBtn = Array.from(buttonRow.querySelectorAll('.v-btn')).find(b => b.textContent.includes('Coupons') || b.textContent.includes('كوبونات'));
            const couponsCol = couponsBtn ? couponsBtn.closest('[class*="v-col"]') : null;
            
            // Large screens (sm and up): all in 1 row (4 + 4 + 4 = 12 columns total).
            // Small screens (xs): Toggle takes 12 cols (1 row), Offers and Coupons take 6 cols each (1 row).
            if (toggleCol) toggleCol.className = 'v-col-12 v-col-sm-4 pb-0 pt-0 text-center dynamic-margin-xs';
            if (offersCol) offersCol.className = 'v-col-6 v-col-sm-4 pb-0 pt-0 text-center dynamic-margin-xs';
            if (couponsCol) couponsCol.className = 'v-col-6 v-col-sm-4 pb-0 pt-0 text-center dynamic-margin-xs';
            
            // Hide the old parent card visually without breaking interaction
            const parentCard = document.querySelector('.cards.mb-0.mt-3.resizable');
            if (parentCard && !parentCard.contains(buttonRow)) {
                parentCard.classList.add('madar-hidden-card');
            }
        }
    }
}

function applyMadarSkin() {
    document.body.classList.add('madar-pos-skin');
}

function checkPosAwesomeRoute() {
    const isMadar = window.location.pathname.startsWith('/madar') || 
                   (window.parent && window.parent.location.pathname.startsWith('/madar'));
                   
    if (!isMadar) {
        document.body.classList.remove('madar-pos-skin');
        return; 
    }

    if (window.frappe && frappe.get_route) {
        const route = frappe.get_route()[0];
        if (route === "pos-awesome" || route === "posapp") {
            applyMadarSkin();
        } else {
            document.body.classList.remove('madar-pos-skin');
        }
    }
}

function updatePosAwesomeTitleText() {
    try {
        const root = document.body;
        if (!root.classList.contains('madar-pos-skin')) return;

        const homeSvg = `<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle; flex-shrink: 0;"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>`;

        const titleElements = root.querySelectorAll('.v-toolbar__title, .v-toolbar-title, .v-app-bar-title');
        titleElements.forEach(el => {
            const txt = el.textContent ? el.textContent.trim() : '';
            if (txt.includes('نقاط البيع الرائع') || txt.includes('POS Awesome') || txt.includes('نقاط البيع') || (el.querySelector('.fas.fa-home') && !el.querySelector('svg'))) {
                const isArabic = document.documentElement.lang === 'ar' || document.documentElement.dir === 'rtl' || /[\u0600-\u06FF]/.test(txt);
                const newText = isArabic ? 'الرجوع للرئيسية' : 'Back to Home';
                
                el.innerHTML = `<span class="madar-pos-back-btn" style="cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-weight: 700; color: inherit; user-select: none; transition: opacity 0.15s ease;" title="${newText}">${homeSvg} <span>${newText}</span></span>`;
                el.classList.add('madar-back-to-home-link');
                el.style.cursor = 'pointer';
            }
        });
    } catch(e) {
        console.warn("Madar POS: Error updating title text", e);
    }
}

function setupPosAwesomeHomeNavigation() {
    document.addEventListener('click', function(e) {
        const target = e.target;
        if (!target) return;
        
        // البحث عن عنوان "الرجوع للرئيسية" أو "نقاط البيع الرائع" في الهيدر
        const backBtn = target.closest('.madar-pos-back-btn, .madar-back-to-home-link');
        const titleEl = target.closest('.v-toolbar__title, .v-toolbar-title, .v-app-bar-title') || 
                        (target.textContent && (target.textContent.trim().includes('الرجوع للرئيسية') || target.textContent.trim().includes('Back to Home') || target.textContent.trim().includes('نقاط البيع الرائع') || target.textContent.trim().includes('POS Awesome')) ? target : null);
        
        if (backBtn || (titleEl && (titleEl.textContent.includes('الرجوع للرئيسية') || titleEl.textContent.includes('Back to Home') || titleEl.textContent.includes('نقاط البيع الرائع') || titleEl.textContent.includes('POS Awesome')))) {
            // استثناء الأزرار والقوائم المجاورة (مثل الحساب أو قائمة الإعدادات)
            const parentBtn = target.closest('.v-btn, button, .v-menu, .v-list-item');
            if (parentBtn && !parentBtn.classList.contains('madar-pos-back-btn')) {
                const btnText = parentBtn.textContent || '';
                if (!btnText.includes('الرجوع للرئيسية') && !btnText.includes('Back to Home') && !btnText.includes('نقاط البيع الرائع') && !btnText.includes('POS Awesome')) {
                    return;
                }
            }
            
            e.preventDefault();
            e.stopPropagation();
            console.log("🚀 تم النقر على زر الرجوع للرئيسية، جاري العودة لصفحة مدار الرئيسية...");
            
            if (window.parent && window.parent !== window && window.parent.MadarRouter) {
                const newUrl = `${window.parent.location.origin}/madar?route=app%2Fhome`;
                window.parent.history.pushState({ route: 'app/home' }, '', newUrl);
                window.parent.MadarRouter.updatePosMode('app/home');
                window.parent.MadarRouter.handleCurrentRoute();
            } else if (window.frappe && frappe.set_route) {
                frappe.set_route('app/home');
            } else {
                window.location.href = '/madar?route=app%2Fhome';
            }
        }
    }, true);
}

if (window.frappe && frappe.router) {
    frappe.router.on('change', () => {
        checkPosAwesomeRoute();
    });
}

$(document).ready(function() {
    setTimeout(() => {
        checkPosAwesomeRoute();
        setupMadarItemCardsObserver();
        updatePosAwesomeTitleText();
        setupPosAwesomeHomeNavigation();
    }, 500);
});





function replaceTextInNode(element, searchStr, replaceStr) {
    if (!element) return;
    for (let node of element.childNodes) {
        if (node.nodeType === Node.TEXT_NODE) {
            if (node.nodeValue.includes(searchStr)) {
                node.nodeValue = node.nodeValue.replace(searchStr, replaceStr);
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            replaceTextInNode(node, searchStr, replaceStr);
        }
    }
}

function safeUpdateClasses(element, classesToAdd, classesToRemove) {
    classesToRemove.forEach(cls => {
        if (element.classList.contains(cls) && !classesToAdd.includes(cls)) {
            element.classList.remove(cls);
        }
    });
    classesToAdd.forEach(cls => {
        if (!element.classList.contains(cls)) {
            element.classList.add(cls);
        }
    });
}

function applyMadarCartLayoutFix() {
    const root = document.body;
    if (!root.classList.contains('madar-pos-skin')) return;

    const cartCol = document.querySelector('.dynamic-main-row > .dynamic-col:last-child');
    if (!cartCol) return;

    // Disconnect observer temporarily to prevent ANY infinite loops
    if (typeof madarCartObserver !== 'undefined' && madarCartObserver) {
        madarCartObserver.disconnect();
    }

    const allBtns = Array.from(cartCol.querySelectorAll('.v-btn')).filter(btn => !btn.closest('.v-input') && !btn.classList.contains('v-btn--icon'));
    const allFields = Array.from(cartCol.querySelectorAll('.v-text-field'));

    const allBtnClasses = ['madar-b1', 'madar-b2', 'madar-b3', 'madar-b4', 'madar-b5', 'madar-b6', 'madar-action-btn', 'madar-pay-btn'];
    const allFieldClasses = ['madar-f1', 'madar-f2', 'madar-f3', 'madar-f4', 'madar-f5', 'madar-f6', 'madar-cart-field'];

    const cancelPayBtn = allBtns.find(b => 
        b.textContent.includes('إلغاء الدفع') || 
        b.textContent.includes('Cancel Payment') ||
        b.textContent.includes('ترحيل') ||
        b.textContent.includes('إرسال وطباعة')
    );
    
    if (cancelPayBtn) {
        let current = cancelPayBtn;
        let paymentWrapper = null;
        while (current && current.parentElement) {
            if (current.parentElement === cartCol || current.parentElement.classList.contains('dynamic-col') || (current.parentElement.classList && current.parentElement.classList.contains('v-window-item'))) {
                paymentWrapper = current;
                break;
            }
            current = current.parentElement;
        }
        
        if (paymentWrapper && !paymentWrapper.classList.contains('madar-payment-popup')) {
            paymentWrapper.classList.add('madar-payment-popup');
        }
        if (!document.body.classList.contains('madar-checkout-active')) {
            document.body.classList.add('madar-checkout-active');
        }
    } else {
        if (document.body.classList.contains('madar-checkout-active')) {
            document.body.classList.remove('madar-checkout-active');
        }
        const oldPopup = document.querySelector('.madar-payment-popup');
        if (oldPopup) oldPopup.classList.remove('madar-payment-popup');
    }

    const filteredBtns = cancelPayBtn ? allBtns.filter(btn => {
        const popup = document.querySelector('.madar-payment-popup');
        return !popup || !popup.contains(btn);
    }) : allBtns;

    const filteredFields = cancelPayBtn ? allFields.filter(f => {
        const popup = document.querySelector('.madar-payment-popup');
        return !popup || !popup.contains(f);
    }) : allFields;

    const payBtn = filteredBtns.find(b => b.textContent.trim() === 'دفع' || b.textContent.includes('دفع') || b.textContent.includes('Pay'));
    
    const bottomField = allFields.find(f => 
        f.textContent.includes('خصم إضافي') || f.textContent.includes('Extra discount') ||
        f.textContent.includes('الكمية الإجمالية') || f.textContent.includes('Total qty') ||
        f.textContent.includes('خصومات الأصناف') || f.textContent.includes('Item discounts') ||
        f.textContent.includes('المجموع') || f.textContent.includes('Total')
    );

    if (payBtn && bottomField) {
        let commonAncestor = payBtn;
        while (commonAncestor && !commonAncestor.contains(bottomField)) {
            commonAncestor = commonAncestor.parentElement;
        }

        if (commonAncestor && !commonAncestor.querySelector('.v-data-table') && !commonAncestor.classList.contains('madar-bottom-section')) {
            commonAncestor.classList.add('madar-bottom-section');
        }
    }

    const dataTables = cartCol.querySelectorAll('.v-data-table');
    const lastTable = dataTables[dataTables.length - 1];

    let madarActionBtnIndex = 1;
    filteredBtns.forEach(btn => {
        let inBottomSection = false;
        if (lastTable) {
            const pos = lastTable.compareDocumentPosition(btn);
            if ((pos & Node.DOCUMENT_POSITION_FOLLOWING) && !(pos & Node.DOCUMENT_POSITION_CONTAINED_BY)) {
                inBottomSection = true;
            }
        } else if (bottomField) {
            if (btn.compareDocumentPosition(bottomField) & Node.DOCUMENT_POSITION_PRECEDING || bottomField.compareDocumentPosition(btn) & Node.DOCUMENT_POSITION_PRECEDING) {
                inBottomSection = true;
            }
        }

        if (inBottomSection) {
            if (btn === payBtn || btn.textContent.includes('دفع') || btn.textContent.includes('Pay')) {
                safeUpdateClasses(btn, ['madar-pay-btn'], allBtnClasses);
            } else {
                safeUpdateClasses(btn, ['madar-action-btn', `madar-b${madarActionBtnIndex}`], allBtnClasses);
                madarActionBtnIndex++;
                
                if (!btn.dataset.madarModified) {
                    replaceTextInNode(btn, 'حفظ ومسح', 'حفظ');
                    replaceTextInNode(btn, 'Save and Clear', 'Save');
                    replaceTextInNode(btn, 'تحميل المسودات', 'المسودات');
                    replaceTextInNode(btn, 'Load Drafts', 'Drafts');
                    replaceTextInNode(btn, 'إلغاء البيع', 'إلغاء');
                    replaceTextInNode(btn, 'Cancel Sale', 'Cancel');
                    replaceTextInNode(btn, 'APPLY OFFERS', 'Offers');
                    replaceTextInNode(btn, 'Apply Offers', 'Offers');
                    btn.dataset.madarModified = 'true';
                }
            }
        } else {
            safeUpdateClasses(btn, [], allBtnClasses);
        }
    });
    
    let fieldIndex = 1;
    filteredFields.forEach(field => {
        let inBottomSection = false;
        if (lastTable) {
            const pos = lastTable.compareDocumentPosition(field);
            if ((pos & Node.DOCUMENT_POSITION_FOLLOWING) && !(pos & Node.DOCUMENT_POSITION_CONTAINED_BY)) {
                inBottomSection = true;
            }
        } else if (bottomField) {
            if (field.compareDocumentPosition(payBtn) & Node.DOCUMENT_POSITION_PRECEDING || payBtn.compareDocumentPosition(field) & Node.DOCUMENT_POSITION_PRECEDING) {
                inBottomSection = true;
            }
        }

        if (inBottomSection) {
            safeUpdateClasses(field, ['madar-cart-field', `madar-f${fieldIndex}`], allFieldClasses);
            fieldIndex++;
        } else {
            safeUpdateClasses(field, [], allFieldClasses);
        }
    });

    // Reconnect observer
    if (typeof madarCartObserver !== 'undefined' && madarCartObserver) {
        madarCartObserver.observe(cartCol, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
    }
}

let madarCartObserver = null;
function setupMadarCartObserver() {
    const cartCol = document.querySelector('.dynamic-main-row > .dynamic-col:last-child');
    if (!cartCol) return;
    
    if (madarCartObserver) madarCartObserver.disconnect();
    
    madarCartObserver = new MutationObserver((mutations) => {
        let shouldFix = false;
        for (let m of mutations) {
            if (m.type === 'childList' || m.type === 'attributes') {
                shouldFix = true;
                break;
            }
        }
        if (shouldFix) {
            applyMadarCartLayoutFix();
        }
    });
    
    madarCartObserver.observe(cartCol, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
}

setInterval(() => {
    applyMadarCartLayoutFix();
    updatePosAwesomeTitleText();
    const cartCol = document.querySelector('.dynamic-main-row > .dynamic-col:last-child');
    if (cartCol && (!madarCartObserver || !document.contains(cartCol))) {
        setupMadarCartObserver();
    }
}, 1000);
