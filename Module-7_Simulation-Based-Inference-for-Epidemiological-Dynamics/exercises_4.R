### Exercise 4.1-- Fit the SEIR model-----------------------------------------------------

library(tidyverse)
# load in the data 
read_csv(paste0("https://kingaa.github.io/sbied/stochsim/",
                "Measles_Consett_1948.csv")) %>%
  select(week,reports=cases) -> meas
meas %>% as.data.frame() %>% head()



#Write the stochastic version of the model.
# exponential transition probabilities (from differential equations) and binomial approx. 
#NSI(t+delta) = NSI(t) + Binomial[S(t), 1-exp(-beta*I*delta)]
seir_step <- Csnippet("
double dN_SE = rbinom(S,1-exp(-Beta*I/N*dt)); 
double dN_EI = rbinom(E,1-exp(-mu_EI*dt)); 
double dN_IR = rbinom(I,1-exp(-mu_IR*dt)); 
S -= dN_SE;
E += dN_SE - dN_EI;
I += dN_EI - dN_IR;
R += dN_IR;
H += dN_IR;
")

seir_rinit <- Csnippet("
S = nearbyint(eta*N);
E = 0;
I = 1;
R = nearbyint((1-eta)*N);
H = 0;
")

seir_dmeas <- Csnippet("
lik = dnbinom_mu(reports,k,rho*H,give_log);
")

seir_rmeas <- Csnippet("
reports = rnbinom_mu(k,rho*H);
")

library(pomp)


# This creates the pomp object (holds a model, and some data). COnstruct it by calling it pomp.
# Updates the measSEIR pomp object.
measSEIR <- meas %>%
  pomp(times="week",t0=0,
       rprocess=euler(seir_step,delta.t=1/7),
       rinit=seir_rinit,
       rmeasure=seir_rmeas,
       dmeasure=seir_dmeas,
       accumvars="H",
       statenames=c("S","E","I","R","H"), #which are parameters and which are states
       paramnames=c("Beta","mu_EI","mu_IR","N","eta","rho","k")
  )

measSEIR %>%
  pomp(
    params=c(Beta=17,mu_EI = 0.3, mu_IR=0.2,rho=0.5,k=10,eta=0.04,N=38000)
  ) -> measSEIR

##----------------------------------------------------------------------------------

measSEIR %>%
  pfilter(Np=1000) -> pf

fixed_params <- c(N=38000, mu_EI=0.7, k=10)
coef(measSEIR,names(fixed_params)) <- fixed_params

library(foreach)
library(doParallel)
registerDoParallel()




library(doRNG)
registerDoRNG(625904618)
tic <- Sys.time()
foreach(i=1:10,.combine=c) %dopar% {
  library(pomp)
  measSEIR %>% pfilter(Np=5000)
} -> pf

pf %>% logLik() %>% logmeanexp(se=TRUE) -> L_pf
L_pf
toc <- Sys.time()

pf[[1]] %>% coef() %>% bind_rows() %>%
  bind_cols(loglik=L_pf[1],loglik.se=L_pf[2]) %>%
  write_csv("measles_params_SEIR.csv")
# Biological parameters tend to be positive, we search for them in log scale.
#A perturbation of 2% seems to work (doesn't have a dramatic effect)

#bake(file="local_search_SEIR.rds",{
  registerDoRNG(482947940)
  foreach(i=1:20,.combine=c) %dopar% {
    library(pomp)
    library(tidyverse)
    measSEIR %>%
      mif2(
        Np=2000, Nmif=50,
        cooling.fraction.50=0.5,
        rw.sd=rw.sd(Beta=0.02, rho=0.02, mu_IR = 0.02, eta=ivp(0.02)), # search by steps of 2% on the parameter
        partrans=parameter_trans(log=c("Beta","mu_IR"),logit=c("rho","eta")),
        paramnames=c("Beta","rho","mu_IR", "eta")
      )
  } -> mifs_local
  attr(mifs_local,"ncpu") <- getDoParWorkers()
  mifs_local
#}) -> mifs_local
t_loc <- attr(mifs_local,"system.time")
ncpu_loc <- attr(mifs_local,"ncpu")

mifs_local %>%
  traces() %>%
  melt() %>%
  ggplot(aes(x=iteration,y=value,group=L1,color=factor(L1)))+
  geom_line()+
  guides(color="none")+
  facet_wrap(~variable,scales="free_y")




#bake(file="lik_local.rds",{
  registerDoRNG(900242057)
  foreach(mf=mifs_local,.combine=rbind) %dopar% {
    library(pomp)
    library(tidyverse)
    evals <- replicate(10, logLik(pfilter(mf,Np=5000)))
    ll <- logmeanexp(evals,se=TRUE)
    mf %>% coef() %>% bind_rows() %>%
      bind_cols(loglik=ll[1],loglik.se=ll[2])
  } -> results
  attr(results,"ncpu") <- getDoParWorkers()
  results
#}) -> results
t_local <- attr(results,"system.time")
ncpu_local <- attr(results,"ncpu")

pairs(~loglik+Beta+eta+rho+mu_IR,data=results,pch=16)

read_csv("measles_params.csv") %>%
  bind_rows(results) %>%
  arrange(-loglik) %>%
  write_csv("measles_params.csv")

if (file.exists("CLUSTER.R")) {
  source("CLUSTER.R")
}



set.seed(2062379496)

fixed_params <- c(N=38000, mu_EI=0.7, k=10, rho = 0.5, eta = 0.04)
coef(measSEIR,names(fixed_params)) <- fixed_params

runif_design(
  lower=c(Beta=5,mu_IR=1/2),
  upper=c(Beta=80, mu_IR=1/0.3),
  nseq=100
) -> guesses

mf1 <- mifs_local[[1]]


#bake(file="global_search.rds",{
  registerDoRNG(1270401374)
  foreach(guess=iter(guesses,"row"), .combine=rbind) %dopar% {
    library(pomp)
    library(tidyverse)
    mf1 %>%
      mif2(params=c(unlist(guess),fixed_params)) %>%
      mif2(Nmif=100) -> mf
    replicate(
      10,
      mf %>% pfilter(Np=1000) %>% logLik()
    ) %>%
      logmeanexp(se=TRUE) -> ll
    mf %>% coef() %>% bind_rows() %>%
      bind_cols(loglik=ll[1],loglik.se=ll[2])
  } -> results
  attr(results,"ncpu") <- getDoParWorkers()
  results%>%
#}) %>%
  filter(is.finite(loglik)) -> results
t_global <- attr(results,"system.time")
ncpu_global <- attr(results,"ncpu")
read_csv("measles_params.csv") %>%
  bind_rows(results) %>%
  filter(is.finite(loglik)) %>%
  arrange(-loglik) %>%
  write_csv("measles_params.csv")

read_csv("measles_params.csv") %>%
  filter(loglik>max(loglik)-50) %>%
  bind_rows(guesses) %>%
  mutate(type=if_else(is.na(loglik),"guess","result")) %>%
  arrange(type) -> all

pairs(~loglik+Beta+mu_IR, data=all, pch=16, cex=0.3,
      col=ifelse(all$type=="guess",grey(0.5),"red"))

all %>%
  filter(type=="result") %>%
  filter(loglik>max(loglik)-10) %>%
  ggplot(aes(x=eta,y=loglik))+
  geom_point()+
  labs(
    x=expression("eta"),
    title="poor man's profile likelihood"
  )
#------------------------------------Profile Likelihood on beta
## ----- on beta ----

read_csv("measles_params.csv") %>%
  filter(loglik>max(loglik)-20,loglik.se<2) %>%
  sapply(range) -> box
box

table<-read_csv("measles_params.csv")

set.seed(1196696958)
profile_design(
  Beta=seq(5,40,length=10),
  mu_EI = seq(1/.5, 1/1.5, length = 10),
  
  lower=box[1,c("eta","rho", "mu_IR")],
  upper=box[2,c("eta","rho", "mu_IR")],
  nprof=15, type="runif"
) -> guesses
plot(guesses)

fixed_params <- c(N=38000, k=10)

foreach(guess=iter(guesses,"row"), .combine=rbind) %dopar% {
  library(pomp)
  library(tidyverse)
  mf1 %>%
    mif2(params=c(unlist(guess),fixed_params),
         partrans=parameter_trans(log = c("mu_IR", "mu_EI"), logit = c("eta", "rho")),
         paramnames = c("mu_IR", "mu_EI", "eta", "rho"),
         rw.sd=rw.sd(eta=0.02,rho=0.02, mu_IR = 0.02)) %>%
    mif2(Nmif=50,cooling.fraction.50=0.3) -> mf
  replicate(
    3,
    mf %>% pfilter(Np=1000) %>% logLik()) %>%
    logmeanexp(se=TRUE) -> ll
  mf %>% coef() %>% bind_rows() %>%
    bind_cols(loglik=ll[1],loglik.se=ll[2])
} -> results

