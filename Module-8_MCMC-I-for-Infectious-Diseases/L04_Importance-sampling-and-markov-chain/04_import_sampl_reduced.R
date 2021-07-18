## This script illustrates the Importance-Sampling algorithm
## Author: Vladimir N. Minin
## last update: 07/11/2021

## define a threshold value and number of Monte Carlo samples
my_const = 4.5
sim_size = 10000

## true probability of interest
(true_prob = pnorm(my_const,lower.tail=FALSE))


## naive Monte Carlo estimate

## Your task: create a naive and an importance sampling
## estimate of the normal tail probability.
## To generate realizations from the standard normal
## distribution use `rnorm()` function.
## To generate realizations from the shifted exponential
## use `rexp()` to generate regular exponentials and
## then add my_const to them. Also, remember that you
## don't have to code the formula for the normal
## density, because it is available via `dnorm()'.
## If you finish early, get Monte Carlo errors for
## naive and important sampling schemes.

# Native MC
native_samples <- rnorm(sim_size)
native_above <- ifelse(native_samples > my_const, 1, 0)
native_mean <- sum(native_above)

# Importance sampling
## Let's use an exponential function as the instrument density q(x) = exp(-x-c)
## where c=4.5
shifted_samples <- rexp(sim_size) + my_const
is_samples <- dnorm(shifted_samples)/exp(-(shifted_samples - my_const)) # our weights
shifted_mean <- sum(is_samples)

native_mean
shifted_mean

# Variances
naive_var <- var(native_samples)/sim_size
shifted_var <- var(is_samples)/sim_size

naive_var
shifted_var
