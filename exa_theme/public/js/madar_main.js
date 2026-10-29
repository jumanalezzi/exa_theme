/* madar_main.js 
   المحرك البرمجي لنظام مدار - الإصدار المطور
*/

// 1. تطبيق الثيم المختار
function applyThemeb(themeId) {
    const theme = MADAR_THEMES.find(t => t.id === themeId);
    if (!theme) {
        console.warn(`Theme ${themeId} not found, using default.`);
        return;
    }
    
    const root = document.documentElement;
    for (const [property, value] of Object.entries(theme.colors)) {
        root.style.setProperty(property, value);
    }
}

// 2. التحكم في تقليص وتوسيع القائمة الجانبية
function toggleSidebar() {
    const sidebar = document.getElementById('mainSidebar');
    const content = document.querySelector('.madar-content');
    if (!sidebar || !content) return;
    
    sidebar.classList.toggle('collapsed');
    
    // تعديل الهامش بناءً على الحالة
    if (window.innerWidth >= 992) {
        // Desktop
        if (sidebar.classList.contains('collapsed')) {
            // No need to set hard margins if flex layout adjusts, but keeping for compatibility
            // The sidebar width is 70px in collapsed mode on desktop
        } else {
            content.style.marginRight = '';
            content.style.marginLeft = '';
        }
    } else {
        // Mobile
        if (sidebar.classList.contains('collapsed')) {
            content.style.marginRight = '30px';
        } else {
            content.style.marginRight = '0px';
        }
    }
}


// 3. المحرك الرئيسي لرسم القائمة الجانبية (3 مستويات)
function renderSidebarMenu(menuData) {
    const container = document.getElementById('sidebarMenuContainer');
    if (!container) return;

    let html = '<ul class="nav flex-column p-0" id="madarAccordion">';

    menuData.forEach((l1, index) => {
        const collapseId = `collapse-l1-${index}`;
        const hasChildren = l1.children && l1.children.length > 0;

        html += `
            <li class="nav-item">
                <a class="nav-link menu-l1 d-flex justify-content-between align-items-center p-3" 
                   ${l1.type === 'folder' ? `data-bs-toggle="collapse" data-bs-target="#${collapseId}" aria-expanded="false"` : `onclick="loadPage('${l1.route}', this)"`}>
                    <span>
                        <i class="fas ${l1.icon} me-2"></i>
                        <span class="nav-text">${l1.title}</span>
                    </span>
                    ${l1.type === 'folder' ? '<i class="fas fa-chevron-down small chevron-icon"></i>' : ''}
                </a>
                ${hasChildren ? `
                    <div class="collapse" id="${collapseId}" data-bs-parent="#madarAccordion">
                        <ul class="nav flex-column">
                            ${renderLevel2(l1.children, collapseId)}
                        </ul>
                    </div>` : ''}
            </li>`;
    });

    html += '</ul>';
    container.innerHTML = html;
}

// 4. رسم المستوى الثاني (دعم المجلدات والروابط المباشرة)
function renderLevel2(children, parentId) {
    return children.map((l2, index) => {
        const collapseId = `collapse-l2-${index}`;
        const hasChildren = l2.children && l2.children.length > 0;

        return `
            <li class="nav-item">
                <a class="nav-link menu-l2 d-flex justify-content-between align-items-center py-2 ps-4" 
                   ${l2.type === 'folder' ? `data-bs-toggle="collapse" data-bs-target="#${collapseId}"` : `onclick="loadPage('${l2.route}', this)"`}>
                    <span>
                        <i class="fas ${l2.icon || 'fa-circle-notch'} me-2 small"></i>
                        <span class="nav-text">${l2.title}</span>
                    </span>
                    ${l2.type === 'folder' ? '<i class="fas fa-chevron-down small chevron-icon"></i>' : ''}
                </a>
                ${hasChildren ? `
                    <div class="collapse" id="${collapseId}">
                        <ul class="nav flex-column">
                            ${renderLevel3(l2.children)}
                        </ul>
                    </div>` : ''}
            </li>`;
    }).join('');
}

// 5. رسم المستوى الثالث (روابط فقط)
function renderLevel3(links) {
    return links.map(l3 => `
        <li class="nav-item">
            <a class="nav-link menu-l3 py-1 ps-5 small" onclick="loadPage('${l3.route}', this)">
                <span class="nav-text">${l3.title}</span>
            </a>
        </li>
    `).join('');
}

// 6. دالة تحميل الروابط في الفريم مع تمييز الزر النشط
function loadPage(route, element) {
    if (!route) return;
    
    const frame = document.getElementById('systemFrame');
    if (frame) {
        frame.src = route;
    }

    // إزالة التميز (Active) من جميع الروابط
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    
    // إضافة التميز للرابط الذي تم الضغط عليه
    if (element) {
        element.classList.add('active');
    }

    // في الشاشات الصغيرة، نغلق السايدبار تلقائياً بعد اختيار رابط
    if (window.innerWidth < 768) {
        toggleSidebar();
    }
}

// 7. دالة تسجيل الخروج (Logout)
function handleLogout() {
    // 1. طلب التأكيد من المستخدم أولاً
    if (!confirm("هل أنت متأكد من تسجيل الخروج؟")) {
        return; // الخروج من الدالة إذا ضغط المستخدم "إلغاء"
    }

    // 2. إرسال طلب تسجيل الخروج للسيرفر في الخلفية
    fetch('/?cmd=logout')
        .then(() => {
            // استخدام replace لضمان عدم تمكن المستخدم من العودة للخلف (Back)
            window.location.replace("/login?redirect-to=/exa");
        })
        .catch(() => {
            // في حال حدوث خطأ في الشبكة مثلاً، نضمن الخروج أيضاً
            window.location.replace("/login?redirect-to=/exa");
        });
}

function toggleLanguage() {
    const currentLang = document.documentElement.lang;
    const newLang = (currentLang === 'ar') ? 'en' : 'ar';
    
    const url = new URL(window.location.href);
    
    // تطهير الرابط: حذف أي معاملات قديمة للغة لضمان عدم التكرار
    url.searchParams.delete('set_lang');
    url.searchParams.delete('lang');
    
    // إضافة المعامل الجديد فقط
    url.searchParams.set('set_lang', newLang);
    
    window.location.href = url.toString();
}