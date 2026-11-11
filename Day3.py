import warnings
warnings.filterwarnings("ignore")

import html
from IPython.display import HTML, display

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

# إعدادات العرض ودعم النصوص
def say(*parts, sep=" "):
    text = html.escape(sep.join(str(p) for p in parts))
    display(HTML(f'<div dir="rtl" style="white-space: pre-wrap; line-height: 1.7;">{text}</div>'))

# إعدادات المعلمات الأساسية لتجربة منصة نقاء
CONFIG = {
    "project": "منصة نقاء (Nugaa) - تحليل بيانات التجربة",
    "baseline_conversion": 0.12,
    "mde_abs": 0.015,
    "alpha": 0.05,
    "power": 0.80,
    "daily_new_users": 4_000,
    "treatment_share": 0.5,
    "true_lift_abs": 0.012,
    "order_value_mean": 150,
    "order_value_sd": 40,
    "order_value_effect": 0,
    "margin": 0.25,
    "extra_cost_per_order_b": 0,
    "cancel_rate": 0.05,
    "cancel_effect": 0.0,
    "support_rate": 0.03,
    "support_effect": 0.0,
    "activity_strength": 0.8,
    "novelty_boost": 0.0,
    "srm_bug_share": 0.0,
    "seed": 2026,
}

def srm_check(n_a, n_b, p_expected=0.5):
    n_total = n_a + n_b
    expected_a = n_total * p_expected
    chi2 = (n_a - expected_a)**2 / expected_a + (n_b - expected_a)**2 / expected_a
    p_val = 1 - stats.chi2.cdf(chi2, df=1)
    say(f"فحص SRM: مجموعة A = {n_a:,}، مجموعة B = {n_b:,} (قيمة p = {p_val:.4f})")
    return p_val

def diff_ci(control, treatment, alpha=0.05):
    n_c, n_t = len(control), len(treatment)
    mean_c, mean_t = control.mean(), treatment.mean()
    var_c, var_t = control.var(ddof=1), treatment.var(ddof=1)
    diff = mean_t - mean_c
    se = np.sqrt(var_c / n_c + var_t / n_t)
    z = stats.norm.ppf(1 - alpha / 2)
    return {
        "الفرق": diff,
        "أدنى 95%": diff - z * se,
        "أعلى 95%": diff + z * se,
        "SE": se,
        "p": 2 * (1 - stats.norm.cdf(abs(diff / se)))
    }

# 5. إنشاء البيانات بالمحاكاة
def simulate_experiment(cfg, duration_days):
    r = np.random.default_rng(cfg["seed"])
    n = duration_days * cfg["daily_new_users"]
    is_b = (r.random(n) < cfg["treatment_share"]).astype(int)
    day = r.integers(1, duration_days + 1, n)
    activity = r.normal(0, 1, n)
    base = cfg["baseline_conversion"]
    
    logit = np.log(base / (1 - base)) + cfg["activity_strength"] * activity
    p0 = 1 / (1 + np.exp(-logit))
    p0 = np.clip(p0 * base / p0.mean(), 0, 1)
    
    pre_orders_90d = r.poisson(5 * p0 / base)
    lift = cfg["true_lift_abs"] * (1 + cfg["novelty_boost"] * np.exp(-(day - 1) / 3))
    
    ordered = r.binomial(1, np.clip(p0 + lift * is_b, 0, 1))
    value = np.maximum(10, r.normal(cfg["order_value_mean"] + cfg["order_value_effect"] * is_b, cfg["order_value_sd"]))
    order_value = np.where(ordered == 1, value, np.nan)
    revenue = ordered * value
    
    profit = ordered * (cfg["margin"] * value - cfg["extra_cost_per_order_b"] * is_b)
    cancelled = np.where(ordered == 1, r.binomial(1, np.clip(cfg["cancel_rate"] + cfg["cancel_effect"] * is_b, 0, 1)), np.nan)
    support = r.binomial(1, np.clip(cfg["support_rate"] + cfg["support_effect"] * is_b, 0, 1))
    
    df = pd.DataFrame({
        "variant": np.where(is_b == 1, "B", "A"),
        "day": day,
        "pre_orders_90d": pre_orders_90d,
        "ordered": ordered,
        "order_value": order_value,
        "revenue": revenue,
        "profit": profit,
        "cancelled": cancelled,
        "contacted_support": support
    })
    
    if cfg["srm_bug_share"] > 0:
        lost = (df["variant"] == "B") & (activity < 0) & (r.random(n) < cfg["srm_bug_share"] / 2)
        df = df[~lost]
        
    return df.reset_index(drop=True)

# تشغيل المحاكاة لمدة 7 أيام
days = 7
data = simulate_experiment(CONFIG, days)
say(f"🛒 عدد المستخدمين في المحاكاة: {len(data):,}")

# 6. فحوص الثقة و SRM
counts = data["variant"].value_counts()
srm_check(counts.get("A", 0), counts.get("B", 0), CONFIG["treatment_share"])

# 7. التحليل الأساسي مع CUPED
A, B = data[data.variant == "A"], data[data.variant == "B"]
primary = diff_ci(A["ordered"], B["ordered"])

theta = np.cov(data["ordered"], data["pre_orders_90d"])[0, 1] / data["pre_orders_90d"].var(ddof=1)
adjusted = data["ordered"] - theta * (data["pre_orders_90d"] - data["pre_orders_90d"].mean())
primary_cuped = diff_ci(adjusted[data.variant == "A"], adjusted[data.variant == "B"])

out = pd.DataFrame([primary, primary_cuped], index=["بدون تعديل", "مع CUPED"])
out[["الفرق", "أدنى 95%", "أعلى 95%"]] *= 100

say(f"نسبة الطلب في A: {A['ordered'].mean():.2%}، وفي B: {B['ordered'].mean():.2%}")
variance_reduction = (1 - (primary_cuped['SE'] / primary['SE']) ** 2) * 100
say(f"📉 انخفاض التباين بطريقة CUPED بنسبة: {variance_reduction:.0f}%")
display(out.round(3))

# 7.2 المقاييس الثانوية
secondary = {
    "قيمة الطلب (لمن طلب)": diff_ci(A["order_value"].dropna(), B["order_value"].dropna()),
    "الإيراد لكل مستخدم": diff_ci(A["revenue"], B["revenue"]),
}

sec = pd.DataFrame(secondary).T
sec["دال بعد تصحيح BH"] = multipletests(sec["p"].astype(float), alpha=0.05, method="fdr_bh")[0]
display(sec.round(3))

# 7.3 مقاييس الحماية
guardrail_defs = {
    "profit": ("الربح لكل مستخدم", "down"),
    "cancelled": ("نسبة إلغاء الطلبات", "up"),
    "contacted_support": ("التواصل مع الدعم", "up"),
}

rows = []
for col, (label, bad) in guardrail_defs.items():
    res = diff_ci(A[col].dropna(), B[col].dropna())
    harmful = res["أعلى 95%"] < 0 if bad == "down" else res["أدنى 95%"] > 0
    status = "تدهور دال" if harmful else "سليم"
    rows.append({"المقياس": label, "A": A[col].mean(), "B": B[col].mean(), **res, "الحالة": status})

guard_table = pd.DataFrame(rows).set_index("المقياس")
display(guard_table.round(4))

# 7.4 فحص أثر الحداثة
daily = data.groupby(["day", "variant"])["ordered"].mean().unstack()
daily_lift = (daily["B"] - daily["A"]) * 100

plt.figure(figsize=(9, 4.5))
plt.plot(daily_lift.index, daily_lift.values, marker="o", color="#0E7490", label="الأثر في كل يوم")
plt.axhline(primary["الفرق"] * 100, color="#E58A1F", linestyle="--", label="الأثر الكلي")
plt.axhline(0, color="gray", linewidth=0.8)
plt.xlabel("يوم دخول المستخدم")
plt.ylabel("الأثر (نقطة مئوية)")
plt.title("فحص أثر الحداثة واستقرار الأثر عبر الأيام")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)
plt.show()

# 8. الفروق في الفروق (Difference-in-Differences - DiD) كبديل تقديري
def simulate_policy_panel(n_units=20, n_treated=6, n_periods=24, policy_period=13, effect=8.0, seed=32):
    r = np.random.default_rng(seed)
    level = r.normal(100, 15, n_units)
    shock = r.normal(0, 2, n_periods)
    rows = []
    
    for i in range(n_units):
        for t in range(1, n_periods + 1):
            treated, post = int(i < n_treated), int(t >= policy_period)
            y = level[i] + 0.8 * t + shock[t - 1] + effect * treated * post + r.normal(0, 3)
            rows.append({"unit": i, "period": t, "treated": treated, "post": post, "y": y})
            
    df = pd.DataFrame(rows)
    df["treated_post"] = df["treated"] * df["post"]
    return df

policy = simulate_policy_panel()
twfe = smf.ols("y ~ treated_post + C(unit) + C(period)", data=policy).fit(
    cov_type="cluster", cov_kwds={"groups": policy["unit"]}
)

lo, hi = twfe.conf_int().loc["treated_post"]
say(f"📊 أثر السياسة (DiD): {twfe.params['treated_post']:.2f}، وفترة الثقة 95% من {lo:.2f} إلى {hi:.2f}")
display(twfe.summary().tables[1])
