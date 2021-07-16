---
title: "Simple Gibbs Sampler Notes"
subtitle: "M08: Lecture 2"
author: "Callum Arnold"
---

# Simple Gibbs sampler
## Chain binomial model 

- Let's go back to the chain binomial example from the motivating examples
  section

- The multinomial complete data likelihood for $q$ (the probability of failure) is:

$$
\begin{aligned}
  f(n_1, n_{11}, N_3, n_{111} | q) &= \binom{334}{n_1, n_{11}, n_{111}, N_3 -
  n_{111}} (q^2)^{n_1}(2q^2p)^{n_{11}}(2qp^2)^{n_{111}}(p^2)^{N_3 - n_{111}}\\
  \text{where: } N_3 &= n_{111} + n_{12} \\
  &= 275
\end{aligned}
$$

- We do not observe either $n_{111}$ or $n_{12}$, just their total $N_3$

- The Gibbs sampler iteratively samples the model unknowns from a sequence of
  full conditional distributions
- To sample one draw from each full conditional distribution at each iteration,
  it assumes that all other model quantities are known at that iteration
- The Gibbs sampler converges to the posterior distribution of the model
  unknowns 
- Here, $n_{111}$ should be augmented, and the posterior distribution of $q$
  estimated.

- The joint distribution of the observations and the model unknowns is:

$$
f(n_1, n_{11}, N_3, n_{111}, q) = \underbrace{f(n_1, n_{11}, N_3, n_{111} |
q)}_{\text{complete data likelihood}} \times \underbrace{f(q)}_{\text{prior}}
$$

- We want to make inference about the joint distribution of the model unknowns
  - $f(n_{111}, q | n_1, n_{11}, N_3)$
  - Possible by using the Gibbs sampler to sample from the full conditionals
    - $f(q | n_1, n_{11}, N_3, n_{111})$
    - $f(n_{111}| n_1, n_{11}, N_3, q)$

### Process

- Start with initial values for unknowns
- For $t=1 \to M$:
  - Sample $q^{(t+1)} \sim f(q | n_1, n_{11}, N_3, n_{111}^{(t)})$
  - Sample $n_{111}^{(t+1)} \sim f(q | n_1, n_{11}, N_3, q^{(t+1)})$

## Full conditionals

- Getting the full conditionals is the tricky bit, but we can calculate if we
  assume the other unknown value are actually known

### $n_{111}$

- Assume $q$ is known
- The conditional probability for the chain $1 \to 1 \to 1$

$$
\begin{aligned}
  \Pr(1 \to 1 \to 1 | N=3, q) &= \frac{\Pr(N=3, 1 \to 1 \to 1 | q)}{\Pr (N=3 |
  q)} \\
  &= \frac{\Pr(N=3| 1 \to 1 \to 1, q)\Pr(1 \to 1 \to 1 | q)}{\Pr(N=3 | 1 \to 1
  \to 1, q)\Pr(1 \to 1 \to 1 | q) + \Pr(N=3 |1 \to 2, q)\Pr(1 \to 2 | q)} \\
  &= \frac{2p^2 q}{2p^2 q + p^2} \\
  &= \frac{2q}{2q + 1}, (0 \le q \le 1) \\
  &\therefore \\
  \text{full conditional } &\text{distribution of } n_{111}: \\
  n_{111} | (n_1, n_{11}, N_3, q) &\sim \text{Binomial}\left(275,
  \frac{2q}{2q+1}\right)
\end{aligned}
$$

### $q$

- Assume $n_{111}$ is known
- Assume a Beta prior distribution for $q$
  - $q \sim \text{Beta}(\alpha, \beta)$
  - $f(q) \equiv f(q|\alpha, \beta) \propto q^{\alpha  - 1}(1-q)^{\beta - 1}$

- The full conditional distribution of $q$:

$$
\begin{aligned}
  f(q | n_1, n_{11}, N_3, n_{111}, \alpha, \beta) &\propto f(n_1, n_{11}, N_3,
  n_{111} | q, \alpha, \beta) f( q | \alpha, \beta) \\
  &\propto \underbrace{q^{2n_1 + 2n_{11} + n_{111}}p^{n_{11} +
  2N_3}}_{\text{complete data likelihood}} \times
  \underbrace{q^{\alpha-1}(1-q)^{\beta -1}}_{prior} \\\\
  q|\text{complete data}, \alpha, \beta &\sim \text{Beta}(2n_1 +2n_{11} +
  n_{111} + \alpha, n_{11} + 2N_3 + \beta)
\end{aligned}
$$

- If we set $\alpha = \beta = 1$, we have a uniform prior on $q$
- A natural point estimate would be the mean of the Beta distribution
  - $\frac{2n_1 +2n_{11} + n_{111} + \alpha}{2n_1 +3n_{11} + 3n_{111} + 2n_{12}+ \alpha + \beta}$
  - Proportion of "escapes" from all exposures

## Sampling with the Gibbs sampler

Now we have the full conditionals, we can update our process from earlier:

- Start with initial values for unknowns
- For $t=1 \to M$:
  - Sample $q^{(t+1)} \sim \text{Beta}(2n_1 +2n_{11} + n_{111}^{(t)} + \alpha, n_{11} + 2N_3 + \beta)$
  - Sample $n_{111}^{(t+1)} \sim \text{Binomial}\left(275, \frac{2q^{(t+1)}}{2q^{(t+1)}+1}\right)$
- Get summaries of the marginal posterior distributions