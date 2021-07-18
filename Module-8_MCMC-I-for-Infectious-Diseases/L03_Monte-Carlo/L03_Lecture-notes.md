---
title: "Monte Carlo Notes"
subtitle: "M08: Lecture 3 (Pages 8-14)"
author: "Callum Arnold"
---

# Monte Carlo methods

-   Should view MC methods as numerical intergration problems

-   Many high dimensional problems can be very hard to integrate numerically, so
    MC techniques help using stochastic simulation

    -   E.g.
        $E[f(\vec{x},\vec{\theta})] = \sum_x f(\vec{x},\vec{\theta})\Pr(\vec{x},\vec{\theta}) d\vec{\theta}$
        when $\vec{x}$ and/or $\vec{\theta}$ are of the order $10^3 - 10^6$

## Classical MC

-   We known that because of the strong law of large numbers, the expectation
    $\frac{1}{n}\sum_{i=1}^n h(X_i) \approx E_f[h(X_1)]$ at large and finite $n$

-   Need to think about Monte Carlo numerical error

    -   Use variance of the MC estimator

        -   All the variances are the same, hence we can make that 2nd step (and
            factor out the $1/n$

        -   We can estimate the variance term in line 2 from the sample variance
            $h(X_1), …, h(X_n)$ very easily in R

        -   The central limit theorem tells us that error in the Monte Carlo
            estimate ($\bar{h_n}$) is normally distributed, so we can get the
            95% CI using $\bar{h_n} \pm 1.96 \sqrt{v_n /n}$

$$
\begin{aligned}
\text{Var}(\bar{h_n}) &= \text{Var}\left(\frac{1}{n}\sum_{i=1}^n h(X_i) \right) \\
&= \frac{1}{n^2} \times n \times \text{Var}[h(X_1)] \\
&\approx \frac{1}{n} \times \frac{1}{n-1} \sum_{i=1}^n [h(X_i) - \bar{h_n}]^2
\end{aligned}
$$

-   The issue is that decreasing the MC error scales with $\sqrt{n}$, so to
    decrease by a factor of 10, we need to increase the number of samples by a
    factor of 100
