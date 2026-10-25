// madar-notifications.js - Native Bootstrap Implementation
document.addEventListener('DOMContentLoaded', () => {
    // تحديث الشارة عند تحميل الصفحة
    fetchUnreadNotificationsCount();
    
    // تحديث الشارة كل 60 ثانية
    setInterval(fetchUnreadNotificationsCount, 60000);
    
    // عندما يتم فتح القائمة المنسدلة، جلب الإشعارات
    const notifBtn = document.getElementById('madarNotificationBtn');
    if (notifBtn) {
        notifBtn.addEventListener('show.bs.dropdown', () => {
            fetchAndRenderNotifications();
        });
    }

    // تبديل ستايل التابات
    const notifTab = document.getElementById('notif-tab');
    const eventsTab = document.getElementById('events-tab');
    
    if (notifTab && eventsTab) {
        notifTab.addEventListener('click', function() {
            this.classList.add('text-primary');
            this.classList.remove('text-muted');
            this.style.borderBottom = '2px solid #0052cc';
            
            eventsTab.classList.remove('text-primary');
            eventsTab.classList.add('text-muted');
            eventsTab.style.borderBottom = 'none';
        });
        
        eventsTab.addEventListener('click', function() {
            this.classList.add('text-primary');
            this.classList.remove('text-muted');
            this.style.borderBottom = '2px solid #0052cc';
            
            notifTab.classList.remove('text-primary');
            notifTab.classList.add('text-muted');
            notifTab.style.borderBottom = 'none';
        });
    }
});

function fetchUnreadNotificationsCount() {
    fetch('/api/method/frappe.desk.notifications.get_notifications', {
        headers: { 'Accept': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.message) {
            let unreadCount = 0;
            const notifs = data.message.notification_info || data.message;
            
            if (notifs.unread_count !== undefined) {
                unreadCount = notifs.unread_count;
            } else if (notifs.open_count !== undefined) {
                unreadCount = notifs.open_count;
            }
            
            updateBadge(unreadCount);
        }
    })
    .catch(error => console.error('Error fetching notification count:', error));
}

function updateBadge(count) {
    const badge = document.getElementById('madar-notification-badge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = 'block';
        } else {
            badge.style.display = 'none';
        }
    }
}

window.fetchAndRenderNotifications = function() {
    const listContainer = document.getElementById('madar-notifications-list');
    if (!listContainer) return;
    
    // إذا كان محمل مسبقاً وفيه عناصر، لا تقم بالتحميل مجدداً لإعطاء تجربة أسرع
    if (listContainer.innerHTML.includes('list-group')) return;
    
    listContainer.innerHTML = '<div class="text-center p-5 text-muted" style="margin-top: 40px;"><i class="fas fa-spinner fa-spin fa-2x mb-3"></i><br>جاري تحميل الإشعارات...</div>';
    
    fetch('/api/resource/Notification Log?limit_page_length=10&order_by=creation desc&fields=["name","subject","document_type","document_name","read","creation"]', {
        headers: { 'Accept': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.data && data.data.length > 0) {
            renderNotificationList(data.data, listContainer);
        } else {
            listContainer.innerHTML = `
                <div class="text-center p-5 text-muted" style="margin-top: 40px;">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3 text-secondary"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                    <h6 class="fw-bold mb-1 text-dark">لا توجد إشعارات جديدة</h6>
                    <p class="small mb-0">يبدو أنك لم تتلقَ أي إشعارات مؤخراً.</p>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Error fetching notifications:', error);
    });
};

function renderNotificationList(notifications, container) {
    let html = '<div class="list-group list-group-flush">';
    
    notifications.forEach(notif => {
        const isRead = notif.read === 1;
        const bgClass = isRead ? 'bg-transparent' : 'bg-light';
        const fontWeight = isRead ? '' : 'fw-bold';
        
        const dateObj = new Date(notif.creation);
        const timeStr = dateObj.toLocaleDateString('ar-SA') + ' ' + dateObj.toLocaleTimeString('ar-SA', {hour: '2-digit', minute:'2-digit'});
        
        const docTypeURL = notif.document_type ? notif.document_type.toLowerCase().replace(/ /g, '-') : 'notification-log';
        const docNameURL = notif.document_name || notif.name;
        
        html += `
            <a href="javascript:MadarRouter.navigate('app/${docTypeURL}/${docNameURL}')" 
               class="list-group-item list-group-item-action ${bgClass} border-bottom p-3">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1 ${fontWeight} text-truncate" style="max-width: 85%; font-size: 0.9rem;">${notif.subject || 'إشعار جديد'}</h6>
                    ${!isRead ? '<span class="badge bg-primary rounded-circle p-1" style="width: 10px; height: 10px;"></span>' : ''}
                </div>
                <small class="text-muted d-block mt-1">${timeStr}</small>
            </a>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

window.fetchMadarEvents = function() {
    const listContainer = document.getElementById('madar-events-list');
    if (!listContainer) return;
    
    if (listContainer.innerHTML.includes('list-group')) return;

    listContainer.innerHTML = '<div class="text-center p-5 text-muted" style="margin-top: 40px;"><i class="fas fa-spinner fa-spin fa-2x mb-3"></i><br>جاري تحميل الفعاليات...</div>';
    
    const today = new Date().toISOString().split('T')[0];
    fetch(`/api/resource/Event?filters=[["starts_on", ">=", "${today}"]]&limit_page_length=5&order_by=starts_on asc&fields=["name","subject","starts_on","event_type"]`, {
        headers: { 'Accept': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.data && data.data.length > 0) {
            let html = '<div class="list-group list-group-flush">';
            data.data.forEach(event => {
                const dateObj = new Date(event.starts_on);
                const dateStr = dateObj.toLocaleDateString('ar-SA');
                html += `
                    <a href="javascript:MadarRouter.navigate('app/event/${event.name}')" 
                       class="list-group-item list-group-item-action border-bottom p-3">
                        <div class="d-flex w-100 justify-content-between">
                            <h6 class="mb-1 text-truncate" style="max-width: 85%; font-size: 0.9rem;">${event.subject}</h6>
                        </div>
                        <small class="text-muted d-block mt-1">${event.event_type || ''} - ${dateStr}</small>
                    </a>
                `;
            });
            html += '</div>';
            listContainer.innerHTML = html;
        } else {
            listContainer.innerHTML = `
                <div class="text-center p-5 text-muted" style="margin-top: 40px;">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mb-3 text-secondary"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    <h6 class="fw-bold mb-1 text-dark">لا توجد فعاليات قادمة</h6>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Error fetching events:', error);
    });
};

window.markAllNotificationsAsRead = function() {
    // Attempt to mark as read
    fetch('/api/method/frappe.desk.notifications.mark_all_read', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Frappe-CSRF-Token': (window.frappe && window.frappe.csrf_token) ? window.frappe.csrf_token : ''
        }
    })
    .then(r => r.json())
    .then(() => {
        // Force refresh list
        const listContainer = document.getElementById('madar-notifications-list');
        if (listContainer) listContainer.innerHTML = '';
        fetchAndRenderNotifications();
        fetchUnreadNotificationsCount();
    })
    .catch(() => {
        // Fallback or ignore if CSRF fails
        const listContainer = document.getElementById('madar-notifications-list');
        if (listContainer) listContainer.innerHTML = '';
        fetchAndRenderNotifications();
    });
};
