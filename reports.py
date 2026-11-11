def decide(ci_low, ci_high, mde, guardrails_ok=True):
    """
    قاعدة القرار الإداري بناءً على فترة الثقة وشروط مقاييس الحماية وMDE.
    """
    if ci_high < 0:
        return "لا نطلق، لأن النسخة الجديدة أضرت بالمقياس الرئيسي."
    if ci_low > 0 and not guardrails_ok:
        return "لا نطلق الآن، لأن المقياس الرئيسي تحسن لكن أحد مقاييس الحماية ساء. نعالج المشكلة ثم نعيد التحقق."
    if ci_low > 0:
        return "نطلق، لأن الأثر إيجابي بثقة ومقاييس الحماية سليمة."
    if ci_high < mde:
        return "لا نطلق، لأننا استبعدنا وجود أثر بالحجم الذي يهمنا."
    return "لا نقرر بعد. نمدد التجربة، أو نعيد تصميمها بقوة أعلى."

def one_page_report(title, effect, ci_low, ci_high, baseline, mde, guardrails, annual_visitors, avg_order_value, caveats):
    """
    توليد تقرير الصفحة الواحدة بصيغة الماركداون للنتائج الإدارية.
    """
    value = lambda x: x * annual_visitors * avg_order_value / 1e6
    guard_rows = "\n".join(f"| {name} | {status} |" for name, status in guardrails.items())
    guardrails_ok = all(status.strip().startswith("سليم") for status in guardrails.values())
    
    return f"""
<div dir="rtl">

### {title}

**القرار:** {decide(ci_low, ci_high, mde, guardrails_ok)}

| البند | القيمة |
|---|---|
| المقياس الرئيسي | نسبة الشراء: من {baseline:.1%} إلى {baseline + effect:.1%} |
| الأثر | {effect * 100:.2f} نقطة (فترة الثقة 95%: من {ci_low * 100:.2f} إلى {ci_high * 100:.2f}) |
| القيمة السنوية التقديرية | حوالي {value(effect):.1f} مليون ريال (من {value(ci_low):.1f} إلى {value(ci_high):.1f}) |

| مقياس الحماية | الحالة |
|---|---|
{guard_rows}

**القيود:** {caveats}

</div>
"""
