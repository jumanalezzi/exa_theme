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