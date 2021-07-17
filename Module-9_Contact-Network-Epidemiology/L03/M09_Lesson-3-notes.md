---
title: "Module 9: Lesson 3 Notes"
author: "Callum Arnold"
output:
   html_document:
     toc: yes
     toc_float:
       collapsed: yes
       smooth_scroll: yes
---

# Discrete-time SIR and percolation

![](2021-07-15-14-55-01.png)
- We are assuming that an infected node remains infected for a single time step
  - Transmits to a partner with probability p

- Let's look at a very simple network where we can map out all possibilities
  - Normally can't do this and would use a random number generator to just
    follow a single path forward

![](2021-07-15-15-00-24.png)

  - The probability of ending up in the final state in the right side $p^2
    (1-p)$, for example, is because there's only one path to infect someone from
    2 infected individuals.

- There's an alternative way of doing this calculation
  - Instead of doing a weighted coin-flip of what happens for each SI pair after
    following each path, we can do the calculation in advanced of the disease
    introduction!
  - This is **percolation!**

- Percolation steps:
  - Let's start by deleting edges and calculating the probability of being
  infected
    - ![](2021-07-15-15-23-24.png)
  - If possible, the infection passes to the neighbour(s), and the infected node
    from the previous step recovers
    - ![](2021-07-15-15-18-31.png)
    - ![](2021-07-15-15-18-49.png)
  - Show the final probabilities
    - ![](2021-07-15-15-21-11.png)

- Percolation is indistinguishable from the original model in terms of the
  outcome of the network

# Continuous time SIR

- Hard to simulate on a network in continuous time
  - Tradeoff between complexity and accuracy
- Having a mathematical approach helps us understand the mechanisms and disease
  properties that determine the final outcomes

## Towards an analytic model for homogenous networks

- Let's count pairs/triples 
  - The order matters, which is why homogenous simulations can be different than
    network simulations
  - Note that for SSI triples, once the middle S becomes infected, it's no
    longer a triple and is an SI pair

![](2021-07-15-15-29-04.png)

We have our standard SIR ODEs, but there are problems here

$$
\begin{aligned}
\frac{d}{dt}[S] &= -\beta [SI] \\
\frac{d}{dt}[I] &= \beta [SI] - \gamma [I] \\
\text{where } &: [SI] = \text{SI pairs!!}
\end{aligned}
$$

Instead, we need to adapt it to included SSI and ISI pairs as well

$$
\begin{aligned}
\frac{d}{dt}[SI] &= -(\beta + \gamma)[SI] + \beta ([SSI] - [ISI]) \\
\frac{d}{dt}[SSI] &= ...
\end{aligned}
$$

However, our equations get longer and longer, and we need to add more and more
equations because there are many ways to transition from SSI to SI etc that we
need to keep track of. Instead, we can use a "closure approximation"

$$
\begin{aligned}
[SI] &\approx [I] \left(\frac{[S]}{[N]} \right)\langle K \rangle \\
&\therefore \\
\frac{d}{dt}[S] &= -\beta \langle K \rangle \frac{[S][I]}{N} \\
\frac{d}{dt}[I] &= \beta \langle K \rangle \frac{[S][I]}{N} - \gamma[I] \\
\text{where: } \langle K \rangle &= \text{average degree}
\end{aligned}
$$

- Here, the number of $SI$ partnerships is equal to (the number of infected
  nodes) x (the probability a random node is susceptible) x (the average degree)

- Assumes:
    - $[S]/N$ is the probability that a partner of an infected node is susceptible
    - $\langle K \rangle$ is the expected number of partners of infected nodes
    - Partners of infected nodes have the same risk as every other node
    - Nodes are not preferentially infected by degree

- $R_0$:
  - The expected number of transmission attempts to partners is the
    (transmission rate) x (the average number of contacts) over the amount of
    time than an individual in infectious for, and the proportion of these
    attempts that are successful is the number of susceptibles / total
    population
      - $\Delta[I] = \frac{\beta \langle K \rangle}{\gamma} \frac{[S]}{N}$
  - Since $[S]/N \approx 1$ at early times
  - $R_0 = \frac{\beta \langle K \rangle}{\gamma}$

- The assumptions means that this model is only appropriate when:
  - Homogenous population with rapid partnership changes
  - Large very similar degrees
  - Transmission probability per partnership low
  - Low clustering

We can futher improve the model if we write $[SSI]$ and $[ISI]$ in terms of
$[SS]$ and $[SI]$, rather than singles.