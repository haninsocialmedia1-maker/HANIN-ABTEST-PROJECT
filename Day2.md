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

# إعدادات المعلمات الأساسية لتجربة منصة نقاء
CONFIG = {
    "project": "منصة نقاء (Nugaa) - تحليل تجربة الواجهة المحسنة",
    "baseline_conversion": 0.12,
    "mde_abs": 0.015,
    "alpha": 0.05,
    "power": 0.80,
    "daily_new_users": 4_000,
    "treatment_share": 0.5,
    "true_lift_abs": 0.012,
    "order_value_mean": 150,
    "order_value_sd": 40,
    "seed": 2026,
}

c = CONFIG

def n_per_group_proportions(p_control, p_treatment, alpha=0.05, power=0.80):
    z_a = stats.norm.ppf(1 - alpha / 2)
    z_b = stats.norm.ppf(power)
    var = p_control * (1 - p_control) + p_treatment * (1 - p_treatment)
    return int(np.ceil((z_a + z_b) ** 2 * var / (p_treatment - p_control) ** 2))

def mde_proportions(p_control, n_per_group, alpha=0.05, power=0.80):
    z_a = stats.norm.ppf(1 - alpha / 2)
    z_b = stats.norm.ppf(power)
    return (z_a + z_b) * np.sqrt(2 * p_control * (1 - p_control) / n_per_group)

def duration_days(n_per_group, daily_new_users, groups=2, round_to_weeks=True):
    days = int(np.ceil(n_per_group * groups / daily_new_users))
    return int(np.ceil(days / 7) * 7) if round_to_weeks else days

# تنفيذ حسابات العينة والمدة لمنصة نقاء
n_per_group = n_per_group_proportions(c["baseline_conversion"], c["baseline_conversion"] + c["mde_abs"], c["alpha"], c["power"])
days = duration_days(n_per_group, c["daily_new_users"])

say(f"🛒 المشروع: {c['project']}")
say(f"📊 حجم العينة المحسوب: {n_per_group:,} مستخدمة في كل مجموعة، ليصبح الإجمالي {2 * n_per_group:,} مستخدمة.")
say(f"⏱️ مدة التجربة المقترحة: {days} أيام (تغطي أسبوعاً كاملاً لضمان شمولية الأنماط السلوكية).")

n_planned = days * c["daily_new_users"] // 2
say(f"👥 إجمالي المستخدمات المتوقعات خلال فترة التجربة: {n_planned:,} مستخدمة لكل مجموعة.")

# تقييم MDE بناءً على الفترات الزمنية
for label, n_g in [("خلال المدة المخططة (7 أيام)", n_planned), ("لو اكتفينا بأسبوع تجريبي أول", 7 * c["daily_new_users"] // 2)]:
    m = mde_proportions(c["baseline_conversion"], n_g, c["alpha"], c["power"])
    say(f"🔍 {label}: أص
