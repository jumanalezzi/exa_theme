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
            window.location.replace("/login?redirect-to=/madar");
        })
        .catch(() => {
            // في حال حدوث خطأ في الشبكة مثلاً، نضمن الخروج أيضاً
            window.location.replace("/login?redirect-to=/madar");
        });
}