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
from Vis_Options import vis

def streamlt():    
    st.title("Option price calculator")
    st.text("Use Monte-Carlo (European) or Longstaff-Schwartz-Monte-Carlo (American) simulations to estimate option prices")
    
    #General setup and initialization of values and variables
    
    h = 1e-3 #Bump Size for Greeks
    user_decimal_format = st.number_input("Enter the number of decimals you wish to enter your data in (calculations will use full length no matter what)", value = 3) 
    option_style = st.selectbox("Option Style", ['American', 'European'])
    option_type = st.selectbox("Option Type", ['Call', 'Put'], index = 0)
    S0 = st.number_input("Initial Stock Price (S₀)", value = 100, step = 1)    
    K = st.number_input("Strike Price (K)", value = 105, step = 1)
    T = st.number_input("Time to Maturity (T in years). Enter as fraction of year, i.e 3 months = 0.25", value = 0.25, format = f"%.{user_decimal_format}f") 
    q = st.number_input("Dividend Yield (q). Enter as decimal, i.e 4.5% = 0.045", value = 0.045, format = f"%.{user_decimal_format}f", step = 0.0001)
    r = st.number_input("Risk-Free Rate (r). Enter as decimal, i.e 4.5% = 0.045", value = 0.05, format = f"%.{user_decimal_format}f", step = 0.0001)
    sigma = st.number_input("Implied Volatility. Enter as decimal, i.e 4.5% = 0.045", value = 0.25, format = f"%.{user_decimal_format}f", step = 0.0001)
   
                      
    #If option style is European  
    
    if option_style == 'European':
        BS_comp = st.selectbox("Do You want to compare Monte-Carlo (European) price with Black-Scholes Analytical?", ['Yes', 'No'], index = 1)
        N = st.slider("Number of Simulations for Monte-Carlo (European)", 1000, 50000, 10000, step=10)
        price, _ = European(S0, K, T, r, q, sigma, N, option_type)
        st.success(f"Estimated {option_style.capitalize()} {option_type.capitalize()} Option Price Calculated Using Monte Carlo: {price.item():.4f}")
        
        if BS_comp == 'Yes':
            BS_price = Black_Scholes_Comp(S0, K, T, r, q, sigma, option_type)
            st.success(f"Analytical European {option_type.capitalize()} Option Black-Scholes price is {BS_price:.4f}")
            
        greeks = compute_greeks_european(S0, K, r, q, sigma, T, N, option_type, h)
        st.subheader(f"European {option_type.capitalize()} Option Greeks Calculated Using Monte-Carlo Method: " )
        
        for greek, value in greeks[option_type].items():
            st.write(f"{greek.capitalize()}: {value:.4f}")
            
        visu = st.selectbox("Do you want visualisations along with the numerical result?", ['Yes', 'No'], index = 1)
        
        
        if visu == 'Yes':
            option_price, ST = European(S0, K, T, r, q, sigma, N, option_type)
            fig = plot_european(K, ST)
            st.pyplot(fig)
            
            vis(S0, K, T, r, q, sigma, N, option_type)
             
            greek_vis = st.selectbox("Do you want visualisations of option greeks as well?", ['Yes', 'No'], index = 1)
            
            if greek_vis == "Yes":
                plot_greeks_european(S0, K, r, q, sigma, T, N, option_type)
        
       
        
        
        
        
    #If option style is American    
        
    elif option_style == 'American':
        n_sim = st.slider("Number of Simulations for Longstaff-Schwartz-Monte-Carlo (American)", 1000, 50000, 10000, step=10)
        n_steps =st.slider("Number of discrete time steps in Longstaff-Schwartz-Monte-Carlo (American)", 10, 500, 100, step=1) 
        n_nodes =st.slider("Number of tree nodes in Cox-Ross-Rubenstein Binomial Tree for Greek Calculations", 10, 500, 100, step=1) 
        price, _, _, _ = American(S0, K, T, r, q, sigma, n_sim, n_steps, option_type)
        st.success(f"Estimated {option_style.capitalize()} {option_type.capitalize()} Option Price Calculated Using Longstaff Schwartz Monte Carlo: {price.item():.4f}")
        greeks = compute_greeks_american(S0, K, r, q, sigma, T, n_nodes, option_type, h)
        st.subheader(f" American {option_type.capitalize()} Option Greeks Calculated Using CRR Binomial Tree: " )
        
        for greek, value in greeks[option_type].items():
            st.write(f"{greek.capitalize()}: {value:.4f}")
  
        visu = st.selectbox("Do you want visualisations along with the numerical result?", ['Yes', 'No' ], index = 1)
        
        if visu == 'Yes':
            
            option_price, dt, cashflow, exercise_time = American(S0, K, T, r, q, sigma, n_sim, n_steps, option_type)
            fig2 = plot_american(dt, cashflow, exercise_time)
            st.pyplot(fig2)

            greek_vis = st.selectbox("Do you want visualisations of option greeks as well?", ['Yes', 'No'], index = 1)
            
            if greek_vis == "Yes":
                plot_greeks_american(S0, K, r, q, sigma, T, n_nodes, option_type)
        
       
       
    
    
    
        
        
    
    
        

