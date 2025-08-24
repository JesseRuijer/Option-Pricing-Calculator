#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 16:14:59 2025

@author: jesseruijer
"""

#Longstaff-Schwartz-Monte-Carlo (LSMC) Option Pricing For American Options

import numpy as np
import matplotlib.pyplot as plt

def American(S0, K, T, r, q, sigma, n_sim, n_steps, option_type):   #Calculate American Option Prices Using LSMC under geometric brownian motion under continuous dividend yield
    
    dt = T / n_steps    # time step size         
    discount = np.exp(-r * dt)  #discount factor to move cashflows back one step
    
    #Simulate asset price paths
    Z = np.random.normal(size = (n_sim, n_steps))
    S = np.zeros((n_sim, n_steps + 1))
    S[:, 0] = S0
    for t in range(1, n_steps + 1):
        S[:, t] = S[:, t - 1] * np.exp((r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t - 1])
     
    #Compute payoff at maturity
    if option_type == 'Put':
        payoff = np.maximum(K - S[: , -1], 0) 
    else:
        payoff = np.maximum(S[:, -1] - K , 0)
        
    cashflow = payoff.copy()
    exercise_time = np.full(n_sim, n_steps)
    
    #Backward induction using regression
    for t in range(n_steps - 1, 0, -1):
        if option_type == 'Put':
            in_the_money = np.where((K - S[:, t]) > 0)[0]
            immediate_exercise = K - S[in_the_money, t]
        else:
            in_the_money = np.where((S[:, t] - K) > 0)[0]
            immediate_exercise = S[in_the_money, t] - K
        
        if len(in_the_money) == 0:
            continue
        
        X = S[in_the_money, t]
        Y = cashflow[in_the_money] * discount
        
        A = np.vstack([np.ones_like(X), X, X**2]).T
        coeffs = np.linalg.lstsq(A, Y, rcond=None)[0]
        continuation_value = A @ coeffs
        
        exercise = immediate_exercise > continuation_value
        index = in_the_money[exercise]
        cashflow[index] = immediate_exercise[exercise]
        exercise_time[index] = t  #Update time of early exercise
        
    price = np.mean(cashflow * np.exp(-r * dt * exercise_time))
    
    return price, dt, cashflow, exercise_time


def plot_american(dt, cashflow, exercise_time): #Plot Histograms of Early Exercise times and Option Payoffs

    fig, axs = plt.subplots(2, 1, figsize=(12, 14))
    fig.tight_layout(pad=5.0)
    
    axs[0].hist(exercise_time * dt, bins = 30, color = 'red', edgecolor = 'black')
    axs[0].grid("True")
    axs[0].set_xlabel("Time (Yr)")
    axs[0].set_ylabel("Number of exercises")
    axs[0].set_title("Histogram of early exercise times")
    
    axs[1].hist(cashflow, bins = 60, color = 'green', edgecolor = 'black')    
    axs[1].grid("True")
    axs[1].set_xlabel("Payoff")
    axs[1].set_ylabel("Frequency")
    axs[1].set_title("Histogram of option payoffs")
   
    return fig

def american_binomial(S0, K, T, r, q, sigma, n_nodes, option_type):    #Pricing via a Cox-Ross-Rubenstein binomial tree with continuous dividend yield 

    dt = T / n_nodes
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp((r - q) * dt) - d) / (u - d)

# Initialize stock price tree
    ST = np.zeros((n_nodes + 1, n_nodes + 1))
    ST[0, 0] = S0
    for i in range(1, n_nodes + 1):
        ST[i, 0] = ST[i-1, 0] * u
        for j in range(1, i + 1):
            ST[i, j] = ST[i-1, j-1] * d
    
    # Initialize option value at maturity
    option_values = np.zeros((n_nodes + 1, n_nodes + 1))
    for j in range(n_nodes + 1):
        if option_type == "Call":
            option_values[n_nodes, j] = max(ST[n_nodes, j] - K, 0)
        else:
            option_values[n_nodes, j] = max(K - ST[n_nodes, j], 0)
    
    # Backward induction
    for i in range(n_nodes-1, -1, -1):
        for j in range(i+1):
            cont = np.exp(-r * dt) * (p * option_values[i+1, j] + (1 - p) * option_values[i+1, j+1])
            if option_type == "Call":
                option_values[i, j] = max(cont, ST[i, j] - K)
            else:
                option_values[i, j] = max(cont, K - ST[i, j])
    
    return option_values[0, 0]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
