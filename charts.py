import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# إعدادات ألوان ورسومات منصة نقاء
TEAL, ORANGE, NAVY, GRAY = "#0E7490", "#E58A1F", "#0F2A3F", "#A9B4BC"
plt.rcParams.update({
    "figure.figsize": (9, 4.5), "figure.dpi": 110,
    "axes.edgecolor": "#56656F", "axes.labelcolor": NAVY, "text.color": NAVY,
    "xtick.color": "#3D4F5C", "ytick.color": "#3D4F5C",
    "axes.grid": True, "grid.color": "#D8E1E7", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.titleweight": "bold", "font.size": 11,
})

def generate_project_charts():
    # محاكاة بيانات أثر الحداثة عبر 7 أيام
    days = np.arange(1, 8)
    daily_lift = [1.4, 1.3, 1.25, 1.2, 1.22, 1.19, 1.21] # نقاط مئوية
    
    plt.figure()
    plt.plot(days, daily_lift, marker="o", color=TEAL, linewidth=2, label="الأثر اليومي (Lift %)")
    plt.axhline(1.20, color=ORANGE, linestyle="--", label="الأثر الكلي المستهدف")
    plt.axhline(0, color=GRAY, linewidth=0.8)
    plt.xlabel("أيام التجربة")
    plt.ylabel("الأثر (نقطة مئوية)")
    plt.title("فحص أثر الحداثة واستقرار الأثر عبر أ أيام التجربة - منصة نقاء")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    
    # حفظ الرسمة في مجلد الأكواد أو المخرجات
    plt.savefig("novelty_effect_chart.png", bbox_inches="tight")
    plt.show()
    print("📊 تم إنشاء وحفظ الرسم البياني بنجاح باسم novelty_effect_chart.png")

if __name__ == "__main__":
    generate_project_charts()
