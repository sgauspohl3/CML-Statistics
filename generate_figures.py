"""
Generate all static figures for the book.

Run once from the book root:
    python generate_figures.py

Saves PNGs into images/ for inclusion via Jupyter Book's image directives.
All figures use a consistent style: transparent backgrounds, despined axes,
no gridlines, blue/coral/seagreen palette.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import (norm, expon, gamma, beta, lognorm, weibull_min,
                          uniform, halfnorm, binom, bernoulli, poisson,
                          randint, skewnorm, gaussian_kde, laplace)

OUT = 'images'
os.makedirs(OUT, exist_ok=True)


def save(fig, name, dpi=150):
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, dpi=dpi, bbox_inches='tight', transparent=True)
    plt.close(fig)
    print(f"  -> {path}")


def style(ax):
    """Apply the house style to an axis."""
    ax.patch.set_alpha(0)
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ============================================================
# CHAPTER 1 — DESCRIPTIVE STATISTICS
# ============================================================

def fig_central_tendency():
    np.random.seed(42)
    data = np.random.gamma(shape=1, scale=7, size=50).astype(int)
    m, med, mo = data.mean(), np.median(data), stats.mode(data).mode

    fig, ax = plt.subplots(figsize=(5, 3.5))
    fig.patch.set_alpha(0)
    sns.histplot(data, color='steelblue', alpha=0.5, ax=ax)
    ax.axvline(m,   color='#C03A2B', lw=1.5, label=f'Mean: {m:.2f}')
    ax.axvline(med, color='mediumseagreen', lw=1.5, label=f'Median: {med:.2f}')
    ax.axvline(mo,  color='coral', lw=1.5, label=f'Mode: {mo:.2f}')
    ax.set_title('Central Tendency')
    ax.set_xlabel('Value'); ax.set_ylabel('Count')
    ax.legend()
    style(ax)
    save(fig, 'central_tendency')


def fig_variability():
    np.random.seed(42)
    d1 = np.random.normal(50, 3, 300)
    d2 = np.random.normal(50, 12, 300)
    df = pd.DataFrame({'value': np.concatenate([d1, d2]),
                       'distribution': ['σ=3']*300 + ['σ=12']*300})
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5), sharex=True,
                                    gridspec_kw={'height_ratios': [4, 1]})
    fig.patch.set_alpha(0)
    sns.histplot(data=df, x='value', hue='distribution', bins=30,
                 alpha=0.5, kde=True, ax=ax1)
    ax1.set_title('Variability'); ax1.set_xlabel(''); ax1.set_ylabel('Count')
    sns.boxplot(data=df, x='value', y='distribution', hue='distribution',
                ax=ax2, boxprops=dict(alpha=0.5))
    ax2.set_xlabel('Value'); ax2.set_ylabel('')
    for a in (ax1, ax2): style(a)
    plt.tight_layout()
    save(fig, 'variability')


def fig_skew():
    np.random.seed(42)
    # Place each distribution where it visually matches its label
    left  = skewnorm.rvs(a=-6, loc=-1, scale=1.5, size=2000)  # long tail to the left
    sym   = np.random.normal(loc=1,    scale=1.2, size=2000)
    right = skewnorm.rvs(a=6,  loc=3,  scale=1.5, size=2000)  # long tail to the right

    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_alpha(0)
    for data, color, label in [
        (left,  '#C03A2B', 'Left-skewed (mean < median)'),
        (sym,   '#1E3F66', 'Symmetric (mean ≈ median)'),
        (right, 'mediumseagreen', 'Right-skewed (mean > median)'),
    ]:
        kde = gaussian_kde(data, bw_method=1)
        x = np.linspace(data.min(), data.max(), 1000)
        y = kde(x)
        ax.plot(x, y, color=color, lw=2.5, label=label)
        ax.fill_between(x, y, alpha=0.1, color=color)
        ax.axvline(np.mean(data),   color=color, lw=0.8, ls='--', alpha=0.5)
        ax.axvline(np.median(data), color=color, lw=0.8, ls='-',  alpha=0.5)
    ax.set_title('Skew of Distributions')
    ax.set_xlabel('Value'); ax.set_ylabel('Density')
    ax.set_xlim(-5, 7); ax.set_ylim(0)
    ax.legend(fontsize=9)
    style(ax)
    plt.tight_layout()
    save(fig, 'skew')


def fig_kurtosis():
    np.random.seed(42)
    lepto = laplace.rvs(loc=0, scale=.4, size=5000)
    meso  = norm.rvs(loc=0, scale=1, size=5000)
    platy = uniform.rvs(loc=-3, scale=6, size=5000)

    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_alpha(0)
    for data, color, label in [
        (lepto, '#C03A2B', 'Leptokurtic (heavy tails, sharp peak)'),
        (meso,  '#1E3F66', 'Mesokurtic (normal)'),
        (platy, 'mediumseagreen', 'Platykurtic (light tails, flat peak)'),
    ]:
        kde = gaussian_kde(data, bw_method=.5)
        x = np.linspace(-5, 5, 1000)
        y = kde(x)
        ax.plot(x, y, color=color, lw=2.5, label=label)
        ax.fill_between(x, y, alpha=0.1, color=color)
    ax.set_title('Kurtosis of Distributions')
    ax.set_xlabel('Value'); ax.set_ylabel('Density')
    ax.set_xlim(-4, 4); ax.set_ylim(0)
    ax.legend(fontsize=9)
    style(ax)
    plt.tight_layout()
    save(fig, 'kurtosis')


def fig_bin_count():
    np.random.seed(42)
    data = np.random.normal(50, 10, 500)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3))
    fig.patch.set_alpha(0)
    for ax, (bins, color, title) in zip(axes, [
        (3,   '#C03A2B', 'Too Few Bins (3)'),
        (200, '#C03A2B', 'Too Many Bins (200)'),
        (25,  '#1E3F66', 'Just Right (25)'),
    ]):
        sns.histplot(data, bins=bins, color=color, alpha=0.5,
                     kde=True, ax=ax, edgecolor='white', linewidth=0.5)
        ax.set_title(title)
        ax.set_xlabel('Value'); ax.set_ylabel('Count')
        style(ax)
    plt.suptitle('Effect of Bin Count on Histograms', y=1.02)
    plt.tight_layout()
    save(fig, 'bin_count')


def fig_ecdf():
    sns.set_style('dark')
    np.random.seed(42)
    data = np.random.normal(50, 10, 500)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_alpha(0)
    sns.ecdfplot(data, color='steelblue', linewidth=2.5, ax=ax)
    ax.axhline(0.25, color='grey', lw=0.8, ls='--', alpha=0.7, label='Q1 (25%)')
    ax.axhline(0.50, color='#C03A2B', lw=0.8, ls='--', alpha=0.7, label='Median (50%)')
    ax.axhline(0.75, color='grey', lw=0.8, ls='--', alpha=0.7, label='Q3 (75%)')
    ax.set_title('Empirical CDF')
    ax.set_xlabel('Value'); ax.set_ylabel('Cumulative Probability')
    ax.set_ylim(0, 1)
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'ecdf')


def fig_ecdf_compare():
    np.random.seed(42)
    d1 = np.random.normal(50, 10, 500)
    d2 = np.random.normal(60, 15, 500)
    df = pd.DataFrame({
        'value': np.concatenate([d1, d2]),
        'distribution': ['Dist 1 (μ=50, σ=10)']*500 + ['Dist 2 (μ=60, σ=15)']*500
    })
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_alpha(0)
    sns.ecdfplot(data=df, x='value', hue='distribution', linewidth=2.5,
                 ax=ax, legend=True)
    ax.axhline(0.50, color='#C03A2B', lw=0.8, ls='-', alpha=0.5)
    ax.set_title('ECDF Comparison')
    ax.set_xlabel('Value'); ax.set_ylabel('Cumulative Probability')
    ax.set_ylim(0, 1)
    style(ax)
    plt.tight_layout()
    save(fig, 'ecdf_compare')


def fig_qq_norm():
    np.random.seed(42)
    data = np.random.normal(20, 5, 500)
    n = len(data)
    i = np.arange(1, n+1)
    p = (i - 0.3175) / (n + 0.365)
    z = norm.ppf(p)
    data_sorted = np.sort(data)
    mu, sigma = data.mean(), data.std(ddof=1)
    # Standardize sample for plotting
    data_std = (data_sorted - mu) / sigma
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    fig.patch.set_alpha(0)
    ax.scatter(z, data_std, color='steelblue', alpha=0.5, s=10)
    ax.plot([-3, 3], [-3, 3], color='#C03A2B', lw=2, label='Reference line')
    ax.set_title('Normal Probability Plot')
    ax.set_xlabel('Theoretical Quantiles')
    ax.set_ylabel('Sample Quantiles (standardized)')
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'qq_norm')


# ============================================================
# DISTRIBUTIONS — PMF/PDF + CDF panels
# ============================================================

def fig_dist_uniform_discrete():
    low, high = 1, 7
    x = np.arange(low, high)
    pmf = randint.pmf(x, low, high)
    cdf = randint.cdf(x, low, high)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
    fig.patch.set_alpha(0)
    ax1.vlines(x, 0, pmf, color='steelblue', lw=2)
    ax1.scatter(x, pmf, color='steelblue', s=80, zorder=5)
    ax1.set_title('Discrete Uniform — PMF and CDF')
    ax1.set_ylabel('P(X = x)')
    ax1.set_ylim(0, max(pmf)*1.4)
    cdf_prev = np.append(0, cdf[:-1])
    for i in range(len(x)):
        xe = x[i+1] if i < len(x)-1 else x[i]+1
        ax2.hlines(cdf[i], x[i], xe, color='coral', lw=2.5)
        ax2.scatter(x[i], cdf[i], color='coral', s=80, zorder=5)
        ax2.scatter(x[i], cdf_prev[i], color='white', edgecolors='coral',
                    lw=1.5, s=80, zorder=5)
    ax2.set_ylabel('F(x) = P(X ≤ x)'); ax2.set_xlabel('x')
    ax2.set_ylim(-0.05, 1.1); ax2.set_xticks(x)
    for a in (ax1, ax2): style(a)
    plt.tight_layout()
    save(fig, 'dist_uniform_discrete')


def fig_dist_binomial():
    configs = [(10, 0.3, 'steelblue', 'n=10, p=0.3'),
               (10, 0.7, 'coral', 'n=10, p=0.7'),
               (20, 0.5, 'mediumseagreen', 'n=20, p=0.5')]
    x = np.arange(0, 22)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    fig.patch.set_alpha(0)
    for n, p, color, label in configs:
        pmf = binom.pmf(x, n, p)
        cdf = binom.cdf(x, n, p)
        ax1.vlines(x, 0, pmf, color=color, lw=2, alpha=0.7)
        ax1.scatter(x, pmf, color=color, s=50, zorder=5, alpha=0.7, label=label)
        cdf_prev = np.append(0, cdf[:-1])
        for i in range(len(x)):
            xe = x[i+1] if i < len(x)-1 else x[i]+1
            ax2.hlines(cdf[i], x[i], xe, color=color, lw=2, alpha=0.7)
            ax2.scatter(x[i], cdf[i], color=color, s=50, zorder=5, alpha=0.7)
            ax2.scatter(x[i], cdf_prev[i], color='white', edgecolors=color,
                        lw=1.5, s=50, zorder=5)
    ax1.set_title('Binomial — PMF and CDF')
    ax1.set_ylabel('P(X = x)'); ax1.set_ylim(0, 0.35); ax1.legend()
    ax2.set_ylabel('F(x) = P(X ≤ x)'); ax2.set_xlabel('x')
    ax2.set_ylim(-0.05, 1.1)
    for a in (ax1, ax2): style(a)
    plt.tight_layout()
    save(fig, 'dist_binomial')


def fig_dist_bernoulli():
    configs = [(0.3, 'steelblue', 'p=0.3'),
               (0.5, 'coral', 'p=0.5'),
               (0.7, 'mediumseagreen', 'p=0.7')]
    x = np.array([0, 1])
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6), sharex=True)
    fig.patch.set_alpha(0)
    for p, color, label in configs:
        pmf = bernoulli.pmf(x, p)
        cdf = bernoulli.cdf(x, p)
        ax1.vlines(x, 0, pmf, color=color, lw=2, alpha=0.7)
        ax1.scatter(x, pmf, color=color, s=80, zorder=5, alpha=0.7, label=label)
        cdf_prev = np.append(0, cdf[:-1])
        for i in range(len(x)):
            xe = x[i+1] if i < len(x)-1 else x[i]+1
            ax2.hlines(cdf[i], x[i], xe, color=color, lw=2, alpha=0.7)
            ax2.scatter(x[i], cdf[i], color=color, s=80, zorder=5, alpha=0.7)
            ax2.scatter(x[i], cdf_prev[i], color='white', edgecolors=color,
                        lw=1.5, s=80, zorder=5)
    ax1.set_title('Bernoulli — PMF and CDF')
    ax1.set_ylabel('P(X = x)'); ax1.set_ylim(0, 1.1); ax1.legend()
    ax2.set_ylabel('F(x) = P(X ≤ x)'); ax2.set_xlabel('x')
    ax2.set_ylim(-0.05, 1.1)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['0\n(Failure)', '1\n(Success)'])
    for a in (ax1, ax2): style(a)
    plt.tight_layout()
    save(fig, 'dist_bernoulli')


def fig_dist_poisson():
    configs = [(1,  'steelblue', 'λ=1'),
               (4,  'coral', 'λ=4'),
               (10, 'mediumseagreen', 'λ=10')]
    x = np.arange(0, 21)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    fig.patch.set_alpha(0)
    for lam, color, label in configs:
        pmf = poisson.pmf(x, lam)
        cdf = poisson.cdf(x, lam)
        ax1.vlines(x, 0, pmf, color=color, lw=2, alpha=0.7)
        ax1.scatter(x, pmf, color=color, s=50, zorder=5, alpha=0.7, label=label)
        cdf_prev = np.append(0, cdf[:-1])
        for i in range(len(x)):
            xe = x[i+1] if i < len(x)-1 else x[i]+1
            ax2.hlines(cdf[i], x[i], xe, color=color, lw=2, alpha=0.7)
            ax2.scatter(x[i], cdf[i], color=color, s=50, zorder=5, alpha=0.7)
            ax2.scatter(x[i], cdf_prev[i], color='white', edgecolors=color,
                        lw=1.5, s=50, zorder=5)
    ax1.set_title('Poisson — PMF and CDF')
    ax1.set_ylabel('P(X = x)'); ax1.set_ylim(0, 0.4); ax1.legend()
    ax2.set_ylabel('F(x) = P(X ≤ x)'); ax2.set_xlabel('x')
    ax2.set_ylim(-0.05, 1.1)
    for a in (ax1, ax2): style(a)
    plt.tight_layout()
    save(fig, 'dist_poisson')


def _continuous_two_panel(name, configs, x, dist_fn, ylim_pdf=None,
                           title=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    fig.patch.set_alpha(0)
    for params, color, label in configs:
        pdf, cdf = dist_fn(x, params)
        ax1.plot(x, pdf, color=color, lw=2.5, label=label)
        ax1.fill_between(x, pdf, alpha=0.1, color=color)
        ax2.plot(x, cdf, color=color, lw=2.5, label=label)
    ax1.set_title(title or f'{name} — PDF and CDF')
    ax1.set_ylabel('Density')
    if ylim_pdf: ax1.set_ylim(*ylim_pdf)
    ax1.legend(fontsize=9)
    ax2.set_ylabel('F(x)'); ax2.set_xlabel('x')
    ax2.set_ylim(-0.05, 1.1)
    ax2.legend(fontsize=9)
    for a in (ax1, ax2): style(a)
    plt.tight_layout()
    save(fig, f'dist_{name}')


def fig_dist_uniform_continuous():
    a, b = 2, 8
    x = np.linspace(a-1, b+1, 1000)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    fig.patch.set_alpha(0)
    pdf = uniform.pdf(x, loc=a, scale=b-a)
    cdf = uniform.cdf(x, loc=a, scale=b-a)
    ax1.plot(x, pdf, color='steelblue', lw=2.5)
    ax1.fill_between(x, pdf, alpha=0.2, color='steelblue')
    ax1.set_title(f'Continuous Uniform (a={a}, b={b}) — PDF and CDF')
    ax1.set_ylabel('Density'); ax1.set_ylim(0, max(pdf)*2)
    ax2.plot(x, cdf, color='steelblue', lw=2.5)
    ax2.set_ylabel('F(x)'); ax2.set_xlabel('x'); ax2.set_ylim(-0.05, 1.1)
    for a_ in (ax1, ax2): style(a_)
    plt.tight_layout()
    save(fig, 'dist_uniform_continuous')


def fig_dist_normal():
    configs = [((0,1), 'steelblue', 'μ=0, σ=1'),
               ((0,2), 'coral', 'μ=0, σ=2'),
               ((3,1), 'mediumseagreen', 'μ=3, σ=1')]
    x = np.linspace(-8, 10, 1000)
    fn = lambda x, p: (norm.pdf(x, *p), norm.cdf(x, *p))
    _continuous_two_panel('normal', configs, x, fn, title='Normal — PDF and CDF')


def fig_dist_halfnormal():
    configs = [((0,1), 'steelblue', 'σ=1'),
               ((0,2), 'coral', 'σ=2'),
               ((0,3), 'mediumseagreen', 'σ=3')]
    x = np.linspace(0, 12, 1000)
    fn = lambda x, p: (halfnorm.pdf(x, *p), halfnorm.cdf(x, *p))
    _continuous_two_panel('halfnormal', configs, x, fn,
                          title='Half-Normal — PDF and CDF')


def fig_dist_lognormal():
    configs = [((0.3,), 'steelblue', 'σ=0.3'),
               ((0.7,), 'coral', 'σ=0.7'),
               ((1.0,), 'mediumseagreen', 'σ=1.0')]
    x = np.linspace(0, 10, 1000)
    fn = lambda x, p: (lognorm.pdf(x, s=p[0]), lognorm.cdf(x, s=p[0]))
    _continuous_two_panel('lognormal', configs, x, fn,
                          title='Log-Normal — PDF and CDF')


def fig_dist_beta():
    configs = [((0.5, 0.5), 'steelblue', 'α=0.5, β=0.5'),
               ((2, 5), 'coral', 'α=2, β=5'),
               ((5, 2), 'mediumseagreen', 'α=5, β=2'),
               ((2, 2), 'purple', 'α=2, β=2')]
    x = np.linspace(0.001, 0.999, 1000)
    fn = lambda x, p: (beta.pdf(x, *p), beta.cdf(x, *p))
    _continuous_two_panel('beta', configs, x, fn, ylim_pdf=(0, 4),
                          title='Beta — PDF and CDF')


def fig_dist_exponential():
    configs = [((0.5,), 'steelblue', 'λ=0.5'),
               ((1.0,), 'coral', 'λ=1.0'),
               ((2.0,), 'mediumseagreen', 'λ=2.0')]
    x = np.linspace(0, 8, 1000)
    fn = lambda x, p: (expon.pdf(x, scale=1/p[0]), expon.cdf(x, scale=1/p[0]))
    _continuous_two_panel('exponential', configs, x, fn,
                          title='Exponential — PDF and CDF')


def fig_dist_gamma():
    configs = [((1, 2),  'steelblue', 'α=1, β=2'),
               ((2, 2),  'coral', 'α=2, β=2'),
               ((5, 1),  'mediumseagreen', 'α=5, β=1')]
    x = np.linspace(0, 20, 1000)
    fn = lambda x, p: (gamma.pdf(x, a=p[0], scale=p[1]),
                       gamma.cdf(x, a=p[0], scale=p[1]))
    _continuous_two_panel('gamma', configs, x, fn, title='Gamma — PDF and CDF')


def fig_dist_weibull():
    configs = [((0.5, 1), 'steelblue', 'β=0.5, η=1'),
               ((1.0, 1), 'coral', 'β=1.0, η=1'),
               ((3.0, 1), 'mediumseagreen', 'β=3.0, η=1')]
    x = np.linspace(0.001, 3, 1000)
    fn = lambda x, p: (weibull_min.pdf(x, c=p[0], scale=p[1]),
                       weibull_min.cdf(x, c=p[0], scale=p[1]))
    _continuous_two_panel('weibull', configs, x, fn, ylim_pdf=(0, 2),
                          title='Weibull — PDF and CDF')


# ============================================================
# LLN / CLT
# ============================================================

def fig_lln():
    np.random.seed(42)
    rolls = np.random.randint(1, 7, size=10000)
    rm = np.cumsum(rolls) / np.arange(1, len(rolls)+1)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_alpha(0)
    ax.plot(rm, color='steelblue', lw=1.5, label='Running mean')
    ax.axhline(3.5, color='#C03A2B', lw=2, ls='--', label='True mean = 3.5')
    ax.fill_between(range(len(rm)), rm, 3.5, alpha=0.1, color='steelblue')
    ax.set_xscale('log')
    ax.set_title('Law of Large Numbers — Running Mean of Die Rolls')
    ax.set_xlabel('Number of Rolls (log scale)')
    ax.set_ylabel('Running Mean')
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'lln')


def fig_clt():
    np.random.seed(42)
    fig, axes = plt.subplots(1, 4, figsize=(13, 3))
    fig.patch.set_alpha(0)
    for ax, n in zip(axes, [2, 5, 15, 50]):
        means = [np.random.exponential(scale=2, size=n).mean() for _ in range(5000)]
        sns.histplot(means, bins=40, kde=True, color='steelblue', alpha=0.5, ax=ax)
        ax.set_title(f'n = {n}')
        ax.set_xlabel('Sample mean')
        if ax is axes[0]: ax.set_ylabel('Count')
        else: ax.set_ylabel('')
        style(ax)
    plt.suptitle('CLT — sampling distribution of the mean from Exponential(2)',
                 y=1.05, fontsize=12)
    plt.tight_layout()
    save(fig, 'clt')


# ============================================================
# CHAPTER 1 — BAYES / MOMENTS / BIAS-VARIANCE
# ============================================================

def fig_bias_variance():
    """Conceptual bullseye showing bias and variance."""
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
    fig.patch.set_alpha(0)
    np.random.seed(42)
    titles = ['Low bias\nLow variance', 'Low bias\nHigh variance',
              'High bias\nLow variance', 'High bias\nHigh variance']
    centers = [(0, 0), (0, 0), (1.2, 1.2), (1.2, 1.2)]
    spreads = [0.15, 0.6, 0.15, 0.6]
    for ax, title, (cx, cy), spread in zip(axes, titles, centers, spreads):
        for r, alpha in [(2.0, 0.10), (1.5, 0.18), (1.0, 0.28), (0.5, 0.40)]:
            circle = plt.Circle((0, 0), r, color='steelblue', alpha=alpha,
                                  fill=True, ec='none')
            ax.add_patch(circle)
        pts = np.random.normal(loc=[cx, cy], scale=spread, size=(20, 2))
        ax.scatter(pts[:, 0], pts[:, 1], color='#C03A2B', s=30, zorder=5,
                   edgecolor='white', linewidth=0.5)
        ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5)
        ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(title, fontsize=10)
        for s in ax.spines.values(): s.set_visible(False)
    plt.suptitle('Bias-Variance Tradeoff', y=1.02, fontsize=12)
    plt.tight_layout()
    save(fig, 'bias_variance')


# ============================================================
# CHAPTER 1 — GoF (P-P and Q-Q)
# ============================================================

def fig_pp_plot():
    np.random.seed(42)
    good = np.random.normal(0, 1, 100)
    poor = np.random.exponential(scale=1, size=100)
    n = len(good)
    i = np.arange(1, n+1)
    pp = (i - 0.3) / (n + 0.4)
    th_g = norm.cdf(np.sort(good), loc=good.mean(), scale=good.std())
    th_p = norm.cdf(np.sort(poor), loc=poor.mean(), scale=poor.std())
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0)
    ax.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Perfect fit')
    ax.scatter(th_g, pp, color='steelblue', s=40, alpha=0.7, label='Good fit')
    ax.scatter(th_p, pp, color='#C03A2B', s=40, alpha=0.7, label='Poor fit')
    ax.set_title('P-P Plot — Normal Distribution Fit')
    ax.set_xlabel('Theoretical Cumulative Probability')
    ax.set_ylabel('Empirical Cumulative Probability')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'pp_plot')


def fig_qq_plot():
    np.random.seed(42)
    good = np.random.normal(0, 1, 100)
    poor = np.random.exponential(scale=1, size=100)
    n = len(good)
    i = np.arange(1, n+1)
    pp = (i - 0.3) / (n + 0.4)
    th_g = norm.ppf(pp, loc=good.mean(), scale=good.std())
    th_p = norm.ppf(pp, loc=poor.mean(), scale=poor.std())
    q1, q3 = np.percentile(good, [25, 75])
    tq1 = norm.ppf(0.25, loc=good.mean(), scale=good.std())
    tq3 = norm.ppf(0.75, loc=good.mean(), scale=good.std())
    slope = (q3 - q1) / (tq3 - tq1)
    intercept = q1 - slope*tq1
    xl = np.linspace(th_g.min(), th_g.max(), 100)
    yl = slope*xl + intercept
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0)
    ax.plot(xl, yl, 'k--', lw=1.5, label='Reference line')
    ax.scatter(th_g, np.sort(good), color='steelblue', s=40, alpha=0.7, label='Good fit')
    ax.scatter(th_p, np.sort(poor), color='#C03A2B', s=40, alpha=0.7, label='Poor fit')
    ax.set_title('Q-Q Plot — Normal Distribution Fit')
    ax.set_xlabel('Theoretical Quantiles')
    ax.set_ylabel('Sample Quantiles')
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'qq_plot')


# ============================================================
# CHAPTER 1 — CENSORING / TRUNCATION
# ============================================================

def fig_censoring_truncation():
    np.random.seed(42)
    data = np.random.normal(50, 15, 100)
    threshold = 65
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    fig.patch.set_alpha(0)
    np.random.seed(0)
    j = np.random.uniform(0, 1, len(data))
    obs = data <= threshold
    cen = data > threshold
    ax1.scatter(data[obs], j[obs], color='steelblue', s=40, alpha=0.7, label='Observed')
    ax1.scatter(np.full(cen.sum(), threshold), j[cen], color='#C03A2B', s=40, alpha=0.7,
                label=f'Censored (> {threshold})')
    ax1.axvline(threshold, color='#C03A2B', ls='--', lw=1.5, alpha=0.5,
                label=f'Threshold = {threshold}')
    ax1.set_title('Right Censoring')
    ax1.set_xlabel('Value'); ax1.set_yticks([])
    ax1.legend(fontsize=9)
    np.random.seed(0)
    j2 = np.random.uniform(0, 1, len(data))
    below = data <= threshold
    above = data > threshold
    ax2.scatter(data[below], j2[below], color='steelblue', s=40, alpha=0.7, label='Observed')
    ax2.scatter(data[above], j2[above], color='steelblue', s=80, alpha=0.3,
                marker='x', linewidths=1.5, label=f'Truncated (> {threshold})')
    ax2.axvline(threshold, color='#C03A2B', ls='--', lw=1.5, alpha=0.5,
                label=f'Threshold = {threshold}')
    ax2.set_title('Right Truncation')
    ax2.set_xlabel('Value'); ax2.set_yticks([])
    ax2.legend(fontsize=9)
    for a in (ax1, ax2): style(a)
    plt.suptitle('Censoring vs Truncation', y=1.02)
    plt.tight_layout()
    save(fig, 'censoring_truncation')


# ============================================================
# CHAPTER 1 — FITTING (MoM, LSE, MLE)
# ============================================================

def fig_mom_gamma():
    np.random.seed(42)
    data = np.random.gamma(shape=3, scale=2, size=500)
    m, v = data.mean(), data.var(ddof=1)
    a_hat = m**2 / v
    b_hat = v / m
    x = np.linspace(0, data.max()+5, 1000)
    pdf = gamma.pdf(x, a=a_hat, scale=b_hat)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_alpha(0)
    sns.histplot(data, bins=30, stat='density', color='steelblue', alpha=0.5,
                 lw=0.5, ax=ax)
    ax.plot(x, pdf, color='#C03A2B', lw=2.5,
            label=f'MoM fit: α={a_hat:.2f}, β={b_hat:.2f}')
    ax.axvline(m, color='grey', lw=1, ls='--', label=f'Sample mean = {m:.2f}')
    ax.set_title('Gamma Distribution — Method of Moments Fit')
    ax.set_xlabel('Value'); ax.set_ylabel('Density')
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'mom_gamma')


def fig_lse_weibull():
    np.random.seed(42)
    data = np.array([25, 43, 53, 65, 76, 86, 95, 115, 132, 150])
    n = len(data)
    i = np.arange(1, n+1)
    F_i = (i - 0.3) / (n + 0.4)
    X = np.log(np.sort(data))
    Y = np.log(-np.log(1 - F_i))
    coeffs = np.polyfit(X, Y, 1)
    beta_hat = coeffs[0]
    eta_hat = np.exp(-coeffs[1] / beta_hat)
    Y_pred = np.polyval(coeffs, X)
    ss_res = np.sum((Y - Y_pred)**2)
    ss_tot = np.sum((Y - np.mean(Y))**2)
    r2 = 1 - ss_res/ss_tot
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_alpha(0)
    ax.scatter(X, Y, color='steelblue', s=60, zorder=5, label='Data')
    ax.plot(X, Y_pred, color='#C03A2B', lw=2,
            label=f'LS fit (β={beta_hat:.2f}, η={eta_hat:.1f}, R²={r2:.4f})')
    ax.set_title('Weibull — Least Squares Estimation (Linearized)')
    ax.set_xlabel('ln(x)'); ax.set_ylabel('ln(-ln(1-F(x)))')
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'lse_weibull')


def fig_mle_weibull():
    np.random.seed(42)
    true_beta, true_eta = 2.5, 100.0
    data = weibull_min.rvs(c=true_beta, scale=true_eta, size=50)
    c_mle, _, scale_mle = weibull_min.fit(data, floc=0)
    t = np.linspace(0, max(data)*1.3, 1000)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    fig.patch.set_alpha(0)
    ax.hist(data, bins=15, density=True, color='steelblue', alpha=0.4,
            edgecolor='white', label='Data')
    ax.plot(t, weibull_min.pdf(t, c=true_beta, scale=true_eta),
            color='grey', lw=2, ls='--', label=f'True (β={true_beta}, η={true_eta})')
    ax.plot(t, weibull_min.pdf(t, c=c_mle, scale=scale_mle),
            color='#C03A2B', lw=2.5,
            label=f'MLE (β={c_mle:.2f}, η={scale_mle:.1f})')
    ax.set_title('Weibull — Maximum Likelihood Estimation')
    ax.set_xlabel('t'); ax.set_ylabel('Density')
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'mle_weibull')


def fig_bootstrap_ci():
    np.random.seed(42)
    true_beta, true_eta = 2.5, 100.0
    n = 50
    data = weibull_min.rvs(c=true_beta, scale=true_eta, size=n)
    B = 2000
    boot_betas = np.zeros(B)
    for b in range(B):
        sample = np.random.choice(data, size=n, replace=True)
        c, _, _ = weibull_min.fit(sample, floc=0)
        boot_betas[b] = c
    ci = np.percentile(boot_betas, [2.5, 97.5])
    c_mle, _, _ = weibull_min.fit(data, floc=0)
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0)
    ax.hist(boot_betas, bins=40, density=True, color='steelblue',
            alpha=0.5, edgecolor='white')
    ax.axvline(c_mle, color='steelblue', lw=2, label=f'MLE β = {c_mle:.2f}')
    ax.axvline(ci[0], color='steelblue', lw=1.5, ls='--',
               label=f'95% CI [{ci[0]:.2f}, {ci[1]:.2f}]')
    ax.axvline(ci[1], color='steelblue', lw=1.5, ls='--')
    ax.axvline(true_beta, color='#C03A2B', lw=2, label=f'True β = {true_beta}')
    ax.set_title('Bootstrap Distribution — Shape Parameter β')
    ax.set_xlabel('β'); ax.set_ylabel('Density')
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'bootstrap_ci')


# ============================================================
# CHAPTER 4 — POOLING (illustrative)
# ============================================================

def fig_pooling():
    """Three-panel illustration of unpooled / pooled / partial-pooled."""
    np.random.seed(42)
    n_groups = 6
    n_per = [2, 3, 4, 6, 30, 50]
    true_mu = 5.0
    group_true = np.random.normal(true_mu, 1.5, n_groups)
    data = [np.random.normal(group_true[g], 1.0, n_per[g]) for g in range(n_groups)]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    fig.patch.set_alpha(0)
    titles = ['Unpooled\n(each group on its own)',
              'Pooled\n(one common estimate)',
              'Partial pooling\n(hierarchical shrinkage)']

    # Unpooled — group means with wide error bars on small groups
    ax = axes[0]
    for g in range(n_groups):
        m = data[g].mean()
        se = data[g].std(ddof=1)/np.sqrt(len(data[g]))
        ax.errorbar(g, m, yerr=1.96*se, fmt='o', color='steelblue',
                    capsize=4, markersize=8)
        ax.scatter(g, group_true[g], marker='x', color='#C03A2B', s=80, zorder=5)
    ax.axhline(true_mu, color='grey', ls=':', alpha=0.5, label='True μ')
    ax.set_title(titles[0])

    # Pooled — single estimate
    ax = axes[1]
    all_data = np.concatenate(data)
    pooled = all_data.mean()
    pooled_se = all_data.std(ddof=1) / np.sqrt(len(all_data))
    for g in range(n_groups):
        ax.errorbar(g, pooled, yerr=1.96*pooled_se, fmt='o',
                    color='mediumseagreen', capsize=4, markersize=8)
        ax.scatter(g, group_true[g], marker='x', color='#C03A2B', s=80, zorder=5)
    ax.axhline(true_mu, color='grey', ls=':', alpha=0.5)
    ax.set_title(titles[1])

    # Partial — shrunk toward pooled
    ax = axes[2]
    for g in range(n_groups):
        n = len(data[g])
        m = data[g].mean()
        # Shrinkage factor: more data, less shrinkage toward pooled
        w = n / (n + 5)
        shrunk = w*m + (1-w)*pooled
        se = data[g].std(ddof=1) / np.sqrt(n) * 0.7  # narrower than unpooled
        ax.errorbar(g, shrunk, yerr=1.96*se, fmt='o', color='coral',
                    capsize=4, markersize=8)
        ax.scatter(g, group_true[g], marker='x', color='#C03A2B', s=80, zorder=5)
    ax.axhline(true_mu, color='grey', ls=':', alpha=0.5)
    ax.set_title(titles[2])

    for ax in axes:
        ax.set_xticks(range(n_groups))
        ax.set_xticklabels([f'G{i+1}\nn={n_per[i]}' for i in range(n_groups)])
        ax.set_xlabel('Group')
        style(ax)
    axes[0].set_ylabel('Estimate')
    plt.suptitle('Three pooling strategies (× = true group mean)', y=1.02)
    plt.tight_layout()
    save(fig, 'pooling')


# ============================================================
# CHAPTER 4 — CONJUGATE UPDATE (Beta-Binomial)
# ============================================================

def fig_conjugate_beta_binomial():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_alpha(0)
    x = np.linspace(0.001, 0.999, 1000)
    # Prior: Beta(2, 2)
    prior = beta.pdf(x, 2, 2)
    # Observe: 7 successes out of 10
    successes, trials = 7, 10
    # Posterior: Beta(2+7, 2+3) = Beta(9, 5)
    posterior = beta.pdf(x, 9, 5)
    # Likelihood (un-normalized) — scale to overlay
    lik = stats.binom.pmf(successes, trials, x)
    lik = lik / lik.max() * prior.max()
    ax.plot(x, prior, color='steelblue', lw=2.5, label='Prior: Beta(2,2)')
    ax.fill_between(x, prior, alpha=0.15, color='steelblue')
    ax.plot(x, lik, color='mediumseagreen', lw=2.5,
            label='Likelihood: 7/10 (scaled)')
    ax.fill_between(x, lik, alpha=0.15, color='mediumseagreen')
    ax.plot(x, posterior, color='#C03A2B', lw=2.5,
            label='Posterior: Beta(9,5)')
    ax.fill_between(x, posterior, alpha=0.15, color='#C03A2B')
    ax.set_title('Conjugate Update — Beta-Binomial')
    ax.set_xlabel('θ (probability)'); ax.set_ylabel('Density')
    ax.legend()
    style(ax)
    plt.tight_layout()
    save(fig, 'conjugate_beta_binomial')


# ============================================================
# CHAPTER 4 — FUNNEL / NON-CENTERED
# ============================================================

def fig_funnel():
    """The neal's funnel — pathological geometry."""
    np.random.seed(42)
    v = np.random.normal(0, 3, 10000)
    x = np.random.normal(0, np.exp(v/2), 10000)
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0)
    ax.scatter(x, v, s=2, alpha=0.3, color='steelblue')
    ax.set_xlim(-15, 15); ax.set_ylim(-9, 6)
    ax.set_title("Neal's Funnel — a pathological posterior geometry")
    ax.set_xlabel('x'); ax.set_ylabel('log scale (v)')
    style(ax)
    plt.tight_layout()
    save(fig, 'funnel')


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("Generating figures into images/...")

    # Chapter 1
    fig_central_tendency()
    fig_variability()
    fig_skew()
    fig_kurtosis()
    fig_bin_count()
    fig_ecdf()
    fig_ecdf_compare()
    fig_qq_norm()

    # Distributions
    fig_dist_uniform_discrete()
    fig_dist_binomial()
    fig_dist_bernoulli()
    fig_dist_poisson()
    fig_dist_uniform_continuous()
    fig_dist_normal()
    fig_dist_halfnormal()
    fig_dist_lognormal()
    fig_dist_beta()
    fig_dist_exponential()
    fig_dist_gamma()
    fig_dist_weibull()

    # LLN/CLT/bias-variance
    fig_lln()
    fig_clt()
    fig_bias_variance()

    # GoF
    fig_pp_plot()
    fig_qq_plot()

    # Censoring/truncation
    fig_censoring_truncation()

    # Fitting
    fig_mom_gamma()
    fig_lse_weibull()
    fig_mle_weibull()
    fig_bootstrap_ci()

    # Chapter 4
    fig_pooling()
    fig_conjugate_beta_binomial()
    fig_funnel()

    print("\nDone. Figures in images/")
