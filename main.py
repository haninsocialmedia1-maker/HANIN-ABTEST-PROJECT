from simulation import simulate_iv, wald_estimator, calculate_f_stat
from reports import one_page_report

def run_pipeline():
    print("==================================================")
    print("   منصة نقاء (Nugaa) - A/B Testing & Causal Engine   ")
    print("==================================================\n")
    
    # 1. تحليل المتغيرات الأداتية (IV Analysis)
    print("--- 1. تشغيل محاكاة وفحص المتغيرات الأداتية ---")
    df_strong = simulate_iv(strength=1.5)
    f_strong = calculate_f_stat(df_strong)
    wald_strong = wald_estimator(df_strong)
    print(f"الأداة القوية: F-statistic = {f_strong:.2f} | تقدير Wald = {wald_strong:.2f}")

    df_weak = simulate_iv(strength=0.1)
    f_weak = calculate_f_stat(df_weak)
    wald_weak = wald_estimator(df_weak)
    print(f"الأداة الضعيفة: F-statistic = {f_weak:.2f} | تقدير Wald = {wald_weak:.2f}\n")

    # 2. توليد تقرير الصفحة الواحدة للقرار الإداري
    print("--- 2. توليد تقرير الصفحة الواحدة للقرار الإداري ---")
    report = one_page_report(
        title="تجربة واجهة التصفح المحسنة في منصة نقاء",
        effect=0.0040, 
        ci_low=-0.0030, 
        ci_high=0.0110, 
        baseline=0.0800, 
        mde=0.0050,
        guardrails={"زمن تحميل الصفحة": "سليم", "أخطاء النظام": "سليم", "معدل الإلغاء": "سليم"},
        annual_visitors=1_200_000, 
        avg_order_value=250,
        caveats="النتائج غير حاسمة؛ فترة الثقة تتضمن الصفر وتتجاوز أصغر أثر يهمنا (MDE)، مما يمنعنا من تأكيد الجدوى أو استبعاد الأثر نهائياً. يُقترح تمديد التجربة أو زيادة حجم العينة."
    )
    
    print(report)
    print("==================================================")
    print("               تم اكتمال التنفيذ بنجاح             ")
    print("==================================================")

if __name__ == "__main__":
    run_pipeline()
