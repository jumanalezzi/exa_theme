// 2. التحكم في تقليص وتوسيع القائمة الجانبية
function toggleSidebar() {
    const sidebar = document.getElementById('mainSidebar');
    if (!sidebar) return;
    
    sidebar.classList.toggle('collapsed');
}