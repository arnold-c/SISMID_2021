---
title: "Module 9: Lab 1 Answers"
author: "Callum Arnold"
output:
   html_document:
     toc: yes
     toc_float:
       collapsed: yes
       smooth_scroll: yes
---

# Exercise 3.2 Poisson vs power law

## Power law
- $R_0 = 20.13$
- Epidemics definitely possible
- 57% of the time epidemics occur
- Mean = 6258 nodes, sd = 45.45

## Poisson Network
- $R_0 = 20.52$ when $\lambda = 50$
- 100% of the time epidemics occur
- Mean = 10000 nodes (all of them), sd = 0

## Comparison
- $R_0$ doesn't tell you much in the absence of network structure information
- Poisson distribution seems to better approximate the mass action model as more
  homogenous mixing of individuals (normal distribution of degree)
- 

# Exercise 3.3 Is the urban network a good model for influenza?

- 