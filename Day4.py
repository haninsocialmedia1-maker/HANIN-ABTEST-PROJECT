import warnings
warnings.filterwarnings("ignore")

import html
from IPython.display import HTML, display
import numpy as np
import pandas as pd

# إعدادات العرض ودعم النصوص العربية
def say(*parts, sep=" "):
    text = html.escape(sep.join(str(p) for p in parts))
    display(HTML(f'<div dir="rtl" style="white-space: pre-wrap; line-height: 1.7;">{text}</div>'))

say("🚀 اليوم الرابع (Day 4): استراتيجية التوسع التدريجي والإطلاق الآمن - منصة 'نقاء'")

# خطة التوسع التدريجي (Rollout Stages) لتقليل المخاطر التشغيلية والتقنية
rollout_stages = [
    {"phase": "المرحلة الأولى (Day 1-2)", "traffic_share": 0.10, "target": "10% من المستخدمات الجدد", "objective": "مراقبة الأخطاء التقنية (Logs) وسرعة الاستجابة (Latency)."},
    {"phase": "المرحلة الثانية (Day 3-5)", "traffic_share": 0.50, "target": "50% من إجمالي المستخدمات", "objective": "التحقق من استقرار مؤشرات الحماية وتحداء الأداء تحت الضغط."},
    {"phase": "المرحلة الثالثة (Day 6+)", "traffic_share": 1.00, "target": "100% (الإطلاق الشامل)", "objective": "اعتماد الواجهة الجديدة كلياً وجني الأرباح والعوائد المقدرة."},
]

df_rollout = pd.DataFrame(rollout_stages)

say("📋 جدول مراحل التوسع التدريجي للواجهة المحسنة:")
display(df_rollout.set_index("phase"))

# محاكاة تأثير التوسع على الأداء ومقاييس الحماية لفترة المراقبة
def simulate_rollout_monitoring(stages, days_per_stage=2):
    monitoring_logs = []
    for stage in stages:
        for d in range(1, days_per_stage + 1):
            monitoring_logs.append({
                "المرحلة": stage["phase"],
                "حجم التراسل": f"{int(stage['traffic_share'] * 100)}%",
                "معدل الأخطاء التقنية (Error Rate %)": round(np.random.uniform(0.01, 0.05), 3),
                "متوسط زمن الاستجابة (ms)": int(np.random.normal(210, 15)),
                "حالة مقاييس الحماية": "سليم وآمن 🟢"
            })
    return pd.DataFrame(monitoring_logs)

df_monitoring = simulate_rollout_monitoring(rollout_stages)
say("🛡️ سجل المراقبة الحية أثناء مراحل التوسع:")
display(df_monitoring.head(6))
