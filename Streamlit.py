#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 16:16:47 2025

@author: jesseruijer
"""

#Streamlit File 

import streamlit as st

from European_Options import European, plot_european
from American_Options import American, plot_american
from Black_Scholes import Black_Scholes_Comp
from Greeks import compute_greeks_european, compute_greeks_american, plot_greeks_european, plot_greeks_american
from Vis_European_Options import vis

def streamlt():    
    st.title("Option Pricing Calculator")
    st.text("Use Monte-Carlo (European) or Longstaff-Schwartz-Monte-Carlo (American) simulations to estimate option prices")
    
    #General setup and initialization of values and variables
    
   
    user_decimal_format = st.number_input("Enter the number of decimals you wish to enter your data in (calculations will use full length no matter what)", 1, value = 3) 
    option_style = st.selectbox("Option Style", ['American', 'European'])
    option_type = st.selectbox("Option Type", ['Call', 'Put'], index = 0)
    S0 = st.number_input("Initial Stock Price (S₀)", min_value = 1, value = 100, step = 1) 
    h = 0.01*S0 #Bump Size for Greeks
    K = st.number_input("Strike Price (K)", min_value = 1, value = 95, step = 1)
    T = st.number_input("Time to Maturity (T in years). Enter as fraction of year, i.e 3 months = 0.25", min_value = 0.0, value = 0.25, format = f"%.{user_decimal_format}f") 
    q = st.number_input("Dividend Yield (q). Enter as decimal, i.e 4.5% = 0.045", min_value = 0.0, value = 0.01, format = f"%.{user_decimal_format}f", step = 0.0001)
    r = st.number_input("Risk-Free Rate (r). Enter as decimal, i.e 4.5% = 0.045", min_value = 0.0, value = 0.05, format = f"%.{user_decimal_format}f", step = 0.0001)
    sigma = st.number_input("Implied Volatility. Enter as decimal, i.e 4.5% = 0.045", min_value = 0.0, value = 0.25, format = f"%.{user_decimal_format}f", step = 0.0001)
   
                      
    #If option style is European  
    
    if option_style == 'European':
        N = st.slider("Number of Simulations for Monte-Carlo (European)", 1000, 50000, 10000, step=10)
        price, _ = European(S0, K, T, r, q, sigma, N, option_type)
        st.success(f"Estimated {option_style.capitalize()} {option_type.capitalize()} Option Price Calculated Using Monte Carlo: {price.item():.4f}")
        BS_price = Black_Scholes_Comp(S0, K, T, r, q, sigma, option_type)
        st.success(f"Analytical European {option_type.capitalize()} Option Black-Scholes price: {BS_price:.4f}")
            
        greeks = compute_greeks_european(S0, K, r, q, sigma, T, N, option_type, h)
        st.subheader(f"European {option_type.capitalize()} Option Greeks Calculated Using Monte-Carlo Method: " )
        
        for greek, value in greeks[option_type].items():
            st.write(f"{greek.capitalize()}: {value:.4f}")
            
        visu = st.selectbox("Do you want visualisations along with the numerical result?", ['Yes', 'No'], index = 0)
        
        
        if visu == 'Yes':
            option_price, ST = European(S0, K, T, r, q, sigma, N, option_type)
            fig = plot_european(K, ST)
            st.pyplot(fig)
            
            vis(S0, K, T, r, q, sigma, N, option_type)
             
            greek_vis = st.selectbox("Do you want visualisations of option greeks as well?", ['Yes', 'No'], index = 1)
            
            if greek_vis == "Yes":
                plot_greeks_european(S0, K, r, q, sigma, T, N, option_type, h)
        
       
        
        
        
        
    #If option style is American    
        
    elif option_style == 'American':
        n_sim = st.slider("Number of Simulations for Longstaff-Schwartz-Monte-Carlo (American)", 1000, 50000, 10000, step=10)
        n_steps =st.slider("Number of discrete time steps in Longstaff-Schwartz-Monte-Carlo (American)", 10, 500, 100, step=1) 
        n_nodes =st.slider("Number of tree nodes in Cox-Ross-Rubenstein Binomial Tree for American Option Greek Calculations", 10, 500, 100, step=1) 
        price, _, _, _ = American(S0, K, T, r, q, sigma, n_sim, n_steps, option_type)
        st.success(f"Estimated {option_style.capitalize()} {option_type.capitalize()} Option Price Calculated Using Longstaff Schwartz Monte Carlo: {price.item():.4f}")
        greeks = compute_greeks_american(S0, K, r, q, sigma, T, n_nodes, option_type, h)
        st.subheader(f" American {option_type.capitalize()} Option Greeks Calculated Using CRR Binomial Tree: " )
        
        for greek, value in greeks[option_type].items():
            st.write(f"{greek.capitalize()}: {value:.4f}")
  
        visu = st.selectbox("Do you want visualisations along with the numerical result?", ['Yes', 'No' ], index = 0)
        
        if visu == 'Yes':
            
            option_price, dt, cashflow, exercise_time = American(S0, K, T, r, q, sigma, n_sim, n_steps, option_type)
            fig2 = plot_american(dt, cashflow, exercise_time)
            st.pyplot(fig2)

            greek_vis = st.selectbox("Do you want visualisations of option greeks as well?", ['Yes', 'No'], index = 1)
            
            if greek_vis == "Yes":
                plot_greeks_american(S0, K, r, q, sigma, T, n_nodes, option_type, h)
        
       
       
    
    
    
        
        
    
    
        

