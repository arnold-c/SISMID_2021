---
title: "Module 9: Introduction 1 Notes"
author: "Callum Arnold"
output:
   html_document:
     toc: yes
     toc_float:
       collapsed: yes
       smooth_scroll: yes
---

# Introduction 

- Networks used to capture host population contact heterogeneity and structure
- Process of building a contact network model
  - Define a realistic contact network
  - Predict the spread of disease through the network
  - Apply understanding of network structure and disease spread for public
    health questions

- Issues with traditional compartmental models:
  - Assumes homogeneous mixing ($\beta$)
    - Know this is not true

- Basic description of a contact network model
  - Individual nodes connected through edges (contacts)
  - Degree = number of edges 
  - Are specific to a population and disease class
    - Different disease transmit via different methods in different populations!

- Contacts:
  - Summarizes
    - Potential for individual to infect others
    - Potential vulnerability

# Defining a realistic contact network

- How to define a contact network (in decreasing realism)
  - Empirical networks
    - Based on data from population
    - Not feasible for large populations
  - Heuristic networks
    - Tries to merge other two types
    - ![](2021-07-14-15-01-50.png)
  - Idealized networks
    - Networks that are computationally generated/mathematically described
    - Depend on small pieces of information from data to generate
    - Fast as well described
    - ![](2021-07-14-15-02-50.png)
      - Lattice may capture spatial structure
      - Small world when most interactions with nearby individuals
    - Also includes random networks

## Adding more information in contact networks

- Network across scales
  - Think about network where node represents location, not individuals
    - E.g. livestock movement

- Weighted contacts
  - Instead of edge being binary, can be weighted edge/contact
    - Represent strength of contact between individuals
    - ![](2021-07-14-15-11-32.png)

- Directed edges
  - Represent asymmetry in contact
  - Note always the best way to represent but sometimes useful e.g. city dweller
    to healthcare worker

- Bipartite network
  - Only transmission between certain nodes
  - ![](2021-07-14-15-14-08.png)

- Co-location network
  - ![](2021-07-14-15-15-01.png)

# Predict the spread of a disease through the network

- Network itself contains lots of information about how the disease will spread
- Degree distribution
  - Larger variance in degree decreases the epidemic threshold
  - ![](2021-07-14-15-22-35.png)

- Network transitivity
  - Property that measures the propensity of triangles
  - Transitivity makes populations hard to invade and leads to smaller and
    longer epidemics

- Dynamic network
  - Contact networks are static in reality, so sometimes want to change
    throughout the model