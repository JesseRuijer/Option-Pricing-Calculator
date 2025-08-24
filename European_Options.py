#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 16:13:19 2025

@author: jesseruijer
"""

#MONTECARLO OPTION PRICING FOR EUROPEAN OPTIONS

import numpy as np
import matplotlib.pyplot as plt


def European(S0, K, T, r, q, sigma, N, option_type): #Calculate European Option Prices Using Monte Carlo Simulation

#Simulate end of period prices using Geometric Brownian Motion
    np.random.seed(69)  #setting seed for reproducibility
    Z = np.random.standard_normal(N)    #simulates N standard normal random variables
    ST = S0*np.exp((r - q - 0.5 * sigma**2) * T + sigma* np.sqrt(T) * Z) #Simulates final stock price ST under GBM, Uses Continuous Yield Dividend Model

    if option_type == 'Call':
        payoffs = np.maximum(ST - K, 0)
    elif option_type == 'Put':
        payoffs = np.maximum(K- ST, 0)
        
        #Discount expected payoff under risk-neutral rate
    option_price = np.exp(-r * T) * np.mean(payoffs)

    return option_price, ST 

def plot_european(K, ST):   #Plots Histogram of simulated final stock price

    fig, ax = plt.subplots(dpi=2048)
    ax.hist(ST, bins=50 , color='blue')
    ax.axvline(K, color='red', label = 'Strike Price')
    ax.set_title("Simulated distribution of final stock price")
    ax.set_xlabel("Price at maturity")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize = 9)
    return fig
        
    
   

