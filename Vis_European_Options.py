#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 16:19:42 2025

@author: jesseruijer
"""

#Some visualisations for European Options

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from European_Options import European
from Black_Scholes import Black_Scholes_Comp



def vis(S0, K, T, r, q, sigma, N, option_type):     #Visualise performance of MC method versus Black-Scholes method for European Options
   
    #Initializing ranges
    K_range = np.linspace(max(0, K - 30), K + 30, 60)
    S0_range = np.linspace(max(0, S0 - 30), S0 + 30, 60)
    sigma_range = np.linspace(min(0.01, abs(sigma)), min(sigma + 0.2, 1), 60) # volatility
    option_prices = []
    bs_prices = []
    option_prices2 = []
    bs_prices2 = []
    option_prices3 = []
    bs_prices3 = []
    
    for k in K_range:
        MC_price, _ = European(S0, k, T, r, q, sigma, N, option_type)
        option_prices.append(MC_price)
        BS_price = Black_Scholes_Comp(S0, k, T, r, q, sigma, option_type)
        bs_prices.append(BS_price)
    
    for s in S0_range:
        MC_price2, _ = European(s, K, T, r, q, sigma, N, option_type)
        option_prices2.append(MC_price2)
        BS_price2 = Black_Scholes_Comp(s, K, T, r, q, sigma, option_type)
        bs_prices2.append(BS_price2)
        
    for sig in sigma_range:
        MC_price3, _ = European(S0, K, T, r, q, sig, N, option_type)
        option_prices3.append(MC_price3)
        BS_price3 = Black_Scholes_Comp(S0, K, T, r, q, sig, option_type)
        bs_prices3.append(BS_price3)

    #Plotting

    fig1, axs = plt.subplots(3, 1, figsize=(12, 14))
    fig1.tight_layout(pad=5.0)
        
    axs[0].plot(K_range, option_prices, color = 'red', label = "Monte-Carlo")
    axs[0].plot(K_range, bs_prices, color = 'black', label = "Black-Scholes")
    axs[0].set_title("Strike price versus option price for MC and BS")
    axs[0].set_xlabel("Strike price")
    axs[0].set_ylabel("European " + option_type + " option Price")
    axs[0].legend(fontsize = 9)
    axs[0].grid('True')

    
    axs[1].plot(S0_range, option_prices2, color = 'red', label = "Monte-Carlo")
    axs[1].plot(S0_range, bs_prices2, color = 'black', label = "Black-Scholes")
    axs[1].set_title("Spot price versus option price for MC and BS")
    axs[1].set_xlabel("Spot price")
    axs[1].set_ylabel("European " + option_type + " option Price")
    axs[1].legend(fontsize = 9)
    axs[1].grid('True')
    
    
    axs[2].plot(sigma_range, option_prices3, color = 'red', label = "Monte-Carlo")
    axs[2].plot(sigma_range, bs_prices3, color = 'black', label = "Black-Scholes")
    axs[2].set_title("Volatility versus option price for MC and BS")
    axs[2].set_xlabel("Volatility")
    axs[2].set_ylabel("European " + option_type + " option Price")
    axs[2].legend(fontsize = 9)
    axs[2].grid('True')
    
    
    st.pyplot(fig1)
    
    #Plotting 3D Figure for behaviour Option Price under Spot price and Volatility
    
    #Grid of spot prices and volatilities
    S0_grid, sigma_grid = np.meshgrid(S0_range, sigma_range)
    price_grid = np.zeros_like(S0_grid)
       
    #Filling surface
    for i in range (len(S0_range)):
         for j in range(len(sigma_range)):
               price_grid[j, i], _ = European(S0_range[i], K, T, r, q, sigma_range[j], N, option_type)
  
        #Plot 3D  
    fig2 = plt.figure(figsize = (12,14))
    axs = fig2.add_subplot(111, projection = '3d')
    axs.plot_surface(S0_grid, sigma_grid, price_grid, cmap = 'plasma')
    axs.set_title(f'European {option_type} Option Price Surface\n(Spot Price vs Volatility)')
    axs.set_xlabel('Spot Price')
    axs.set_ylabel('Volatility')
    axs.set_zlabel('Option Price')
        
    st.pyplot(fig2)
    

    
    
  