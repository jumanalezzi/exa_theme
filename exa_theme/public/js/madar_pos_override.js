// madar_pos_override.js

function syncThemeFromParent() {
    try {
        if (window.parent && window.parent !== window && window.parent.document) {
            const parentRoot = window.parent.document.documentElement;
            const root = document.documentElement;
            
            // Function to copy variables
            const copyVars = () => {
                const parentStyle = window.getComputedStyle(parentRoot);
                const vars = ['--bg-color', '--fg-color', '--text-color', '--text-muted', '--border-color', '--primary', '--control-bg'];
                vars.forEach(v => {
                    let val = parentStyle.getPropertyValue(v);
                    if(val) root.style.setProperty(v, val);
                });
                root.style.fontFamily = parentStyle.fontFamily;
                root.style.setProperty('--font-family', parentStyle.fontFamily);
            };
            
            // Copy immediately
            copyVars();
            
            // Set up an observer on the parent's HTML element to catch theme changes
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.attributeName === 'style') {
                        copyVars();
                    }
                });
            });
            observer.observe(parentRoot, { attributes: true });
        }
    } catch (e) {
        console.warn("Could not sync theme from parent.", e);
    }
}

// Setup an observer to dynamically tag elements for our CSS overrides
function setupMadarDOMObserver() {
    function tagElements() {
        try {
            const root = document.body;
            if (!root.classList.contains('madar-pos-skin')) return;
            
            // 1. Tag MAIN Columns (Cart vs Items)
            const rows = root.querySelectorAll('.row, .v-row');
            let mainRow = null;
            for (let i = 0; i < rows.length; i++) {
                const row = rows[i];
                const directCols = Array.from(row.children).filter(el => el.matches && el.matches('[class*="col-"], .col, .v-col'));
                if (directCols.length >= 2) {
                    let hasCart = false;
                    let hasItems = false;
                    directCols.forEach(col => {
                        const text = col.textContent || "";
                        if (text.includes('دفع') || text.includes('حفظ ومسح')) hasCart = true;
                        if (text.includes('مجموعة الأصناف') || text.includes('قائمة الأسعار') || text.includes('البحث عن الأصناف')) hasItems = true;
                    });
                    if (hasCart && hasItems) {
                        mainRow = row;
                        break;
                    }
                }
            }
            
            if (mainRow) {
                const directCols = Array.from(mainRow.children).filter(el => el.matches && el.matches('[class*="col-"], .col, .v-col'));
                directCols.forEach(col => {
                    const text = col.textContent || "";
                    if (text.includes('دفع') || text.includes('حفظ ومسح')) {
                        if (!col.classList.contains('madar-cart-col')) col.classList.add('madar-cart-col');
                    } else {
                        if (!col.classList.contains('madar-items-col')) col.classList.add('madar-items-col');
                    }
                });
            }
            
            // 2. Tag Item Cards
            const itemsCol = root.querySelector('.madar-items-col') || root;
            // POS Awesome can use .v-card, or in newer versions .card-item-card or .dynamic-item-card
            const cards = itemsCol.querySelectorAll('.v-card, .card-item-card, .dynamic-item-card');
            
            cards.forEach(card => {
                // BULLETPROOF CHECKS FOR WRAPPER VS ITEM
                
                // If it's explicitly a card-item-card, it's definitely an item
                let isDefiniteItem = card.classList.contains('card-item-card') || card.classList.contains('dynamic-item-card');
                
                if (!isDefiniteItem) {
                    // 1. If it contains another card, it's a wrapper.
                    if (card.querySelector('.v-card, .card-item-card, .dynamic-item-card')) {
                        card.classList.remove('madar-item-card');
                        return;
                    }
                    
                    // 2. If it contains a data table or search bar, it's a wrapper.
                    if (card.querySelector('input[placeholder*="البحث"]') || 
                        card.querySelector('input[placeholder*="Search"]') ||
                        card.querySelector('.v-data-table')) {
                        card.classList.remove('madar-item-card');
                        return;
                    }
                    
                    // 3. An item card MUST have a visual area (v-image, img, card-item-image)
                    const hasImage = card.querySelector('.v-image, .v-responsive, img, .card-item-image, .card-item-image-container');
                    if (!hasImage) {
                        card.classList.remove('madar-item-card');
                        return;
                    }
                }
                
                // It passed all checks, it's an item card!
                if (!card.classList.contains('madar-item-card')) {
                    card.classList.add('madar-item-card');
                }
                
                // Tag internal elements for CSS to position them
                if (card.classList.contains('madar-item-card')) {
                    // Pre-tag any existing classes from new POS awesome
                    const nativeName = card.querySelector('.card-item-name');
                    if (nativeName) nativeName.classList.add('madar-item-title');
                    
                    const nativeCode = card.querySelector('.card-item-code');
                    if (nativeCode) nativeCode.classList.add('madar-sku');
                    
                    let titleFound = !!nativeName;
                    const allElements = card.querySelectorAll('div, span');
                    
                    allElements.forEach(el => {
                        // Only process elements that contain direct text
                        const txt = el.textContent.trim();
                        if (!txt || el.children.length > 1) return;
                        
                        // Price
                        if (/\d/.test(txt) && (txt.includes('ر.س') || txt.includes('$') || txt.includes('SAR'))) {
                            if (!txt.toLowerCase().includes('sku') && !el.classList.contains('madar-price-sticker')) {
                                el.classList.add('madar-price-sticker');
                            }
                        } 
                        // SKU
                        else if (txt.toLowerCase().includes('sku')) {
                            el.classList.add('madar-sku');
                        } 
                        // Unit
                        else if (txt.includes('Nos') || txt.includes('Unit') || txt.includes('الوحدة') || txt.includes('حبه') || txt.includes('حبة')) {
                            // Check if this text is alone or inside a container we can tag
                            const unitContainer = el.closest('.d-flex, .justify-space-between, .card-item-content') || el;
                            if (unitContainer) unitContainer.classList.add('madar-item-unit');
                        } 
                        // Title (fallback if no native .card-item-name found)
                        else if (!titleFound && txt.length > 2 && /[a-zA-Zأ-ي]/.test(txt)) {
                            el.classList.add('madar-item-title');
                            titleFound = true;
                        }
                    });
                }
            });
            
        } catch (e) {
            console.error("Madar POS Skin Error:", e);
        }
    }

    // Run aggressively at first
    let attempts = 0;
    const interval = setInterval(() => {
        tagElements();
        attempts++;
        if (attempts > 10) clearInterval(interval);
    }, 500);
    
    // Then rely on mutations
    const observer = new MutationObserver((mutations) => {
        let shouldTag = false;
        for (let m of mutations) {
            if (m.addedNodes.length > 0) {
                shouldTag = true;
                break;
            }
        }
        if (shouldTag) {
            clearTimeout(window.madarTagTimer);
            window.madarTagTimer = setTimeout(tagElements, 100);
        }
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
}

function applyMadarSkin() {
    document.body.classList.add('madar-pos-skin');
    syncThemeFromParent();
}

function checkPosAwesomeRoute() {
    if (window.frappe && frappe.get_route) {
        const route = frappe.get_route()[0];
        if (route === "pos-awesome" || route === "posapp") {
            applyMadarSkin();
        } else {
            document.body.classList.remove('madar-pos-skin');
        }
    }
}

// Hook into Frappe's route change
if (window.frappe && frappe.router) {
    frappe.router.on('change', () => {
        checkPosAwesomeRoute();
    });
}

// Also run on document ready
$(document).ready(function() {
    setTimeout(() => {
        checkPosAwesomeRoute();
        setupMadarDOMObserver();
    }, 500);
});
