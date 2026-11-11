import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

def simulate_iv(n=20_000, strength=1.5, seed=3):
    r = np.random.default_rng(seed)
    motivation = r.normal(size=n)
    sms = r.binomial(1, 0.5, n)
    uses = r.binomial(1, 1 / (1 + np.exp(-(-1.0 + strength * sms + 1.2 * motivation))))
    spend = 50 + 10 * uses + 15 * motivation + r.normal(0, 10, n)
    return pd.DataFrame({"sms": sms, "uses": uses, "spend": spend})

def wald_estimator(df):
    z1, z0 = df["sms"] == 1, df["sms"] == 0
    numerator = df.loc[z1, "spend"].mean() - df.loc[z0, "spend"].mean()
    denominator = df.loc[z1, "uses"].mean() - df.loc[z0, "uses"].mean()
    return numerator / denominator if denominator != 0 else np.nan

def calculate_f_stat(df):
    first_stage = smf.ols("uses ~ sms", data=df).fit()
    return first_stage.fvalue
