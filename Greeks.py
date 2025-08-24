#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 16:15:54 2025

@author: jesseruijer
"""

#Calcation and plotting of option greeks

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from European_Options import European
from American_Options import american_binomial

def compute_greeks_european(S0, K, r, q, sigma, T, N, option_type, h):      #Computes Greeks for European options
    
    #Use different bump sizes for different scales
    h_S0 = h
    h_sigma = 0.01 # Bumps vol by 1%
    h_r = 0.0001 # Bumps rates by 1 basis point (1bp)
    h_T = T * 1e-3 # Small bump in time
    
    greeks = {}
        
    for option_type in ["Call", "Put"]: 
    
        #Delta 
        price_up, _ = European(S0 + h_S0, K, T, r, q, sigma, N, option_type) 
        price_down, _  = European(max(1e-7,S0 - h_S0), K, T, r, q, sigma, N, option_type)
        delta = (price_up - price_down) / (2 * h_S0)
        
        #Gamma 
        price_center, _  = European(S0, K, T, r, q, sigma, N, option_type)
        gamma = (price_up + price_down - 2 * price_center) / (h_S0**2)
        
        #Vega 
        price_up, _  = European(S0 , K, T, r, q, sigma + h_sigma, N, option_type)
        price_down, _  = European(S0 , K, T, r, q, max(1e-7,sigma - h_sigma), N, option_type)
        vega = ((price_up - price_down) / (2 * h_sigma)/100) #Divided by 100 to report per 1%change itstead of per 100%change in volatility
        
        #Rho 
        price_up, _  = European(S0 , K, T, r + h_r, q, sigma, N, option_type)
        price_down, _  = European(S0 , K, T, max(1e-7,r - h_r), q, sigma, N, option_type)
        rho = ((price_up - price_down) / (2 * h_r)/100) #Divided by 100 to report per 1%change itstead of per 100%change in interest rates
        
        #Theta
        price_up, _  = European(S0 , K, T + h_T, r, q, sigma, N, option_type)
        price_down, _  = European(S0 , K, max(1e-7, T - h_T), r, q, sigma, N, option_type)
        theta = -(((price_up - price_down) / (2 * h_T))/252) #Divided by 252 (number of trading days in a year) to obtain daily theta (since variable T is measured in years) 

    
        greeks[option_type] = {
            'delta' : delta,
            'gamma' : gamma,
            'vega' : vega,
            'rho' : rho,
            'theta' : theta
            }

        
    return greeks
    
    
    
def compute_greeks_american(S0, K, r, q, sigma, T, n_nodes, option_type, h):    #Computes Greeks for American options
        
    #Use different bump sizes for different scales
    h_S0 = h
    h_sigma = 0.01 # Bumps vol by 1%
    h_r = 0.0001 # Bumps rates by 1 basis point (1bp)
    h_T = T * 1e-3 # Small bump in time
    greeks = {}
        
    for option_type in ["Call", "Put"]: 
    
        #Delta
        price_up= american_binomial(S0 + h_S0, K, T, r, q, sigma, n_nodes, option_type)
        price_down = american_binomial(max(1e-7,S0 - h_S0), K, T, r, q, sigma, n_nodes, option_type)
        delta = (price_up- price_down) / (2 * h_S0)
    
        #Gamma 
        price_center = american_binomial(S0, K, T, r, q, sigma, n_nodes,option_type)
        gamma = (price_up + price_down - 2 * price_center) / (h_S0**2)
    
        #Vega 
        price_up = american_binomial(S0 , K, T, r, q, sigma + h_sigma, n_nodes, option_type)
        price_down = american_binomial(S0 , K, T, r, q, max(1e-7,sigma - h_sigma), n_nodes,option_type)
        vega = ((price_up - price_down) / (2 * h_sigma)/100) #Divided by 100 to report per 1%change itstead of per 100%change in volatility
    
        #Rho 
        price_up = american_binomial(S0 , K, T, r + h_r, q, sigma, n_nodes, option_type)
        price_down = american_binomial(S0 , K, T, max(1e-7,r - h_r), q, sigma, n_nodes, option_type)
        rho = ((price_up - price_down) / (2 * h_r)/100) #Divided by 100 to report per 1%change itstead of per 100%change in interest rates
    
        #Theta 
        price_up = american_binomial(S0 , K, T + h_T, r, q, sigma, n_nodes, option_type)
        price_down = american_binomial(S0 , K, max(1e-7,T - h_T), r, q, sigma, n_nodes, option_type)
        theta = -(((price_up - price_down) / (2 * h_T))/252) #Divided by 252 (number of trading days in a year) to obtain daily theta (since variable T is measured in years) 
    
        greeks[option_type] = {
            'delta' : delta,
            'gamma' : gamma,
            'vega' : vega,
            'rho' : rho,
            'theta' : theta
            }

        
    return greeks


def plot_greeks_european(S0, K, r, q, sigma, T, N, option_type,h):    #Plots for European Greeks
    
    #Range of spot prices
    S_range = np.linspace(max(0, S0 - 30), S0 + 30, 30)
    
   
    
    call_deltas, put_deltas, call_gammas, put_gammas, call_vegas, put_vegas, call_rhos, put_rhos, call_thetas, put_thetas = [], [], [], [], [], [], [], [], [], []
        
    #Compute for each S
        
    for S0 in S_range:
        greeks = compute_greeks_european(S0, K, r, q, sigma, T, N, option_type, h)        
        delta_call = greeks["Call"]["delta"]
        gamma_call = greeks["Call"]["gamma"]
        vega_call = greeks["Call"]["vega"]
        rho_call = greeks["Call"]["rho"]
        theta_call = greeks["Call"]["theta"]
    
        delta_put = greeks["Put"]["delta"]
        gamma_put = greeks["Put"]["gamma"]
        vega_put = greeks["Put"]["vega"]
        rho_put = greeks["Put"]["rho"]
        theta_put = greeks["Put"]["theta"]
            
        call_deltas.append(delta_call)
        put_deltas.append(delta_put)
        call_gammas.append(gamma_call)
        put_gammas.append(gamma_put)
        call_vegas.append(vega_call)
        put_vegas.append(vega_put)
        call_rhos.append(rho_call)
        put_rhos.append(rho_put)
        call_thetas.append(theta_call)
        put_thetas.append(theta_put)
                
        
    #Plotting
        
    fig, axs = plt.subplots(5, 2, figsize=(12, 14))
    fig.tight_layout(pad=5.0)
        
    axs[0,0].plot(S_range, call_deltas)
    axs[0,0].grid(True)
    axs[0,0].set_title("Delta vs Spot prices for call")
    axs[0,0].set_xlabel("Spot Price")
    axs[0,0].set_ylabel("Delta")
        
    axs[0,1].plot(S_range, put_deltas)
    axs[0,1].grid(True)
    axs[0,1].set_title("Delta vs Spot prices for put")
    axs[0,1].set_xlabel("Spot Price")
    axs[0,1].set_ylabel("Delta")
            
    axs[1,0].plot(S_range, call_gammas)
    axs[1,0].grid(True)
    axs[1,0].set_title("Gamma vs Spot prices for call")
    axs[1,0].set_xlabel("Spot Price")
    axs[1,0].set_ylabel("Gamma")
    
    axs[1,1].plot(S_range, put_gammas)
    axs[1,1].grid(True)
    axs[1,1].set_title("Gamma vs Spot prices for put")
    axs[1,1].set_xlabel("Spot Price")
    axs[1,1].set_ylabel("Gamma")
        
    axs[2,0].plot(S_range, call_vegas)
    axs[2,0].grid(True)
    axs[2,0].set_title("Vega vs Spot prices for call")
    axs[2,0].set_xlabel("Spot Price")
    axs[2,0].set_ylabel("Vega")
        
    axs[2,1].plot(S_range, put_vegas)
    axs[2,1].grid(True)
    axs[2,1].set_title("Vega vs Spot prices for put")
    axs[2,1].set_xlabel("Spot Price")
    axs[2,1].set_ylabel("Vega")
        
    axs[3,0].plot(S_range, call_rhos)
    axs[3,0].grid(True)
    axs[3,0].set_title("Rho vs Spot prices for call")
    axs[3,0].set_xlabel("Spot Price")
    axs[3,0].set_ylabel("Rho")
        
    axs[3,1].plot(S_range, put_rhos)
    axs[3,1].grid(True)
    axs[3,1].set_title("Rho vs Spot prices for put")
    axs[3,1].set_xlabel("Spot Price")
    axs[3,1].set_ylabel("Rho")
        
        
    axs[4,0].plot(S_range, call_thetas)
    axs[4,0].grid(True)
    axs[4,0].set_title("Theta vs Spot prices for call")
    axs[4,0].set_xlabel("Spot Price")
    axs[4,0].set_ylabel("Theta")
        
        
    axs[4,1].plot(S_range, put_thetas)
    axs[4,1].grid(True)
    axs[4,1].set_title("Theta vs Spot prices for put")
    axs[4,1].set_xlabel("Spot Price")
    axs[4,1].set_ylabel("Theta")
        
    st.pyplot(fig)
    
    
    
    
def plot_greeks_american(S0, K, r, q, sigma, T, n_nodes, option_type, h):  #Plots for American Greeks
        
    #Range of spot prices
    S_range = np.linspace(max(0, S0 - 30), S0 + 30, 30)
        
       
        
        #Store Greeks
    call_deltas, put_deltas, call_gammas, put_gammas, call_vegas, put_vegas, call_rhos, put_rhos, call_thetas, put_thetas = [], [], [], [], [], [], [], [], [], []
        
    #Compute for each S
        
    for S0 in S_range:
        greeks = compute_greeks_american(S0, K, r, q, sigma, T, n_nodes, option_type, h)            
        delta_call = greeks["Call"]["delta"]
        gamma_call = greeks["Call"]["gamma"]
        vega_call = greeks["Call"]["vega"]
        rho_call = greeks["Call"]["rho"]
        theta_call = greeks["Call"]["theta"]
    
        delta_put = greeks["Put"]["delta"]
        gamma_put = greeks["Put"]["gamma"]
        vega_put = greeks["Put"]["vega"]
        rho_put = greeks["Put"]["rho"]
        theta_put = greeks["Put"]["theta"]
            
        call_deltas.append(delta_call)
        put_deltas.append(delta_put)
        call_gammas.append(gamma_call)
        put_gammas.append(gamma_put)
        call_vegas.append(vega_call)
        put_vegas.append(vega_put)
        call_rhos.append(rho_call)
        put_rhos.append(rho_put)
        call_thetas.append(theta_call)
        put_thetas.append(theta_put)
                
        
    #Plotting
        
    fig, axs = plt.subplots(5, 2, figsize=(12, 14))
    fig.tight_layout(pad=5.0)
        
    axs[0,0].plot(S_range, call_deltas)
    axs[0,0].grid(True)
    axs[0,0].set_title("Delta vs Spot prices for call")
    axs[0,0].set_xlabel("Spot Price")
    axs[0,0].set_ylabel("Delta")
        
    axs[0,1].plot(S_range, put_deltas)
    axs[0,1].grid(True)
    axs[0,1].set_title("Delta vs Spot prices for put")
    axs[0,1].set_xlabel("Spot Price")
    axs[0,1].set_ylabel("Delta")
            
    axs[1,0].plot(S_range, call_gammas)
    axs[1,0].grid(True)
    axs[1,0].set_title("Gamma vs Spot prices for call")
    axs[1,0].set_xlabel("Spot Price")
    axs[1,0].set_ylabel("Gamma")
    
    axs[1,1].plot(S_range, put_gammas)
    axs[1,1].grid(True)
    axs[1,1].set_title("Gamma vs Spot prices for put")
    axs[1,1].set_xlabel("Spot Price")
    axs[1,1].set_ylabel("Gamma")
        
    axs[2,0].plot(S_range, call_vegas)
    axs[2,0].grid(True)
    axs[2,0].set_title("Vega vs Spot prices for call")
    axs[2,0].set_xlabel("Spot Price")
    axs[2,0].set_ylabel("Vega")
        
    axs[2,1].plot(S_range, put_vegas)
    axs[2,1].grid(True)
    axs[2,1].set_title("Vega vs Spot prices for put")
    axs[2,1].set_xlabel("Spot Price")
    axs[2,1].set_ylabel("Vega")
        
    axs[3,0].plot(S_range, call_rhos)
    axs[3,0].grid(True)
    axs[3,0].set_title("Rho vs Spot prices for call")
    axs[3,0].set_xlabel("Spot Price")
    axs[3,0].set_ylabel("Rho")
        
    axs[3,1].plot(S_range, put_rhos)
    axs[3,1].grid(True)
    axs[3,1].set_title("Rho vs Spot prices for put")
    axs[3,1].set_xlabel("Spot Price")
    axs[3,1].set_ylabel("Rho")
        
        
    axs[4,0].plot(S_range, call_thetas)
    axs[4,0].grid(True)
    axs[4,0].set_title("Theta vs Spot prices for call")
    axs[4,0].set_xlabel("Spot Price")
    axs[4,0].set_ylabel("Theta")
        
        
    axs[4,1].plot(S_range, put_thetas)
    axs[4,1].grid(True)
    axs[4,1].set_title("Theta vs Spot prices for put")
    axs[4,1].set_xlabel("Spot Price")
    axs[4,1].set_ylabel("Theta")
        
    st.pyplot(fig)
   
       
   
        
    
