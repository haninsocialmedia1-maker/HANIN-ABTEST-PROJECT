import warnings
warnings.filterwarnings("ignore")

import html
from IPython.display import HTML, display

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib import ft2font
from scipy import stats

# التحقق من دعم العربية في الرسوم
NATIVE_ARABIC = hasattr(ft2font, "__libraqm_version__")
if not NATIVE_ARABIC:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
    except ImportError:
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "arabic-reshaper", "python-bidi"], check=True)
        import arabic_reshaper
        from bidi.algorithm import get_display

rng = np.random.default_rng(2026)

# تخصيص ألوان منصة نقاء الاحترافية
TEAL, ORANGE, NAVY, GRAY = "#0E7490", "#E58A1F", "#0F2A3F", "#A9B4BC"
plt.rcParams.update({
    "figure.figsize": (9, 4.5), "figure.dpi": 110,
    "axes.prop_cycle": cycler(color=[TEAL, ORANGE, NAVY, GRAY]),
    "axes.edgecolor": "#56656F", "axes.labelcolor": NAVY, "text.color": NAVY,
    "xtick.color": "#3D4F5C", "ytick.color": "#3D4F5C",
    "axes.grid": True, "grid.color": "#D8E1E7", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 13, "axes.titleweight": "bold", "font.size": 11,
    "legend.frameon": False,
})
pd.set_option("display.precision", 4)

def ar(text):
    text = str(text)
    return text if NATIVE_ARABIC else get_display(arabic_reshaper.reshape(text))

def say(*parts, sep=" "):
    text = html.escape(sep.join(str(p) for p in parts))
    display(HTML(f'<div dir="rtl" style="white-space: pre-wrap; line-height: 1.7;">{text}</div>'))

# تهيئة وتوثيق اليوم الأول لمنصة نقاء
say("=" * 60)
say("📌 اليوم الأول (Day 1): تصميم وتخطيط التجربة - منصة 'نقاء' (Nugaa)")
say("=" * 60)
say("🎯 هدف التجربة: قياس أثر الواجهة المحسنة على معدل التحويل والمشتريات.")
say("📊 المؤشرات الأساسية:")
say("  - معدل التحويل الحالي (Baseline Conversion): 12%")
say("  - حجم المستخدمين الجدد المتوقع يومياً: 4,000 مستخدمة")
say("  - نسبة التوزيع بين المجموعتين (Control & Treatment): 50% / 50%")
say("=" * 60)
