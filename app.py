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
    
    tab1, tab2 = st.tabs(["Calculator", "Instructions and Background Info"])
    
    with tab1:
    
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
        
    with tab2:
          st.subheader("User Instructions") 
          st.markdown(
               """
               
               First, choose your option type and style and submit all your data into the calculator. 
               
               The calculator presents the numerical results of pricing and option greeks as well as plots to provide background and visualisation.
               It will also give you the choice at each step whether to include more plots (below the page) or keep it to a simple calculator.
               
               Lastly, don't forget to play around and investigate how values and behaviours relate to eachother!
               
               """
               
               )
          st.subheader("Background Info") 
          st.markdown(
               """
               
               If you choose American options, the calculator will use Longstaff-Schwartz-Monte-Carlo (LSMC) numerical methods to estimate the option price.
               
               
               Pricing of American options is very difficult because its exercise features are much more complex than European options. Finite difference and binomial techniques become impractical in complex situations. 
               
               This is where LSMC simulation comes in to play. At its core, LSMC combines Monte Carlo simulations of possible future price paths with least-squares regression to estimate the value of waiting to exercise. It works by simulating many paths of the underlying asset price under the risk-neutral measure and then using backward induction to decide at each time step whether to exercise or continue. 
               The key step is estimating the continuation value—the expected value of holding the option—via regression of future discounted payoffs on basis functions of the current asset price. If the immediate payoff exceeds this continuation value, the algorithm assumes exercise; otherwise, it continues. 
               Averaging discounted payoffs across all paths yields the option price.
               
               Since the option greeks are calculated using finite difference methods, we use the Cox-Ross-Rubenstein binomial tree here as the LSMC method is unstable due to inherent noise from the Monte Carlo process.
               
               For more detailed information, see: https://people.math.ethz.ch/~hjfurrer/teaching/LongstaffSchwartzAmericanOptionsLeastSquareMonteCarlo.pdf
               
               If you choose European options, the calculator will use Monte-Carlo numerical methods to estimate the option price as well as prompt you with the analytical Black-Scholes price to compare. It will also present plots of relevant performance measure compared to Black-Scholes and option greeks calculated using the regular Monte-Carlo method.
               
               First, we start by generating future stock prices under the risk neutral measure and assuming the stock prices follow geometric brownian motion.
               Then, for each simulated path, the discounted payoff of the option is computed according to the payoff formula for European options.
               Finally, averaging all this over numerous iterations brings the Monte-Carlo element into play and gives us the final estimated option price. As the number of iterations grows larger, the estimated price approaches the analytical Black-Scholes price.
               
               Finally, some small info on option greeks:
                   
               Delta: the rate the option price changes per change of value in the underlying asset's price
               
               Gamma: the rate Delta changes with respect to the underlying asset's price
               
               Vega: the rate the option price changes with respect to volatilty
               
               Rho: the rate the option price changes with respect to the risk-free rate
               
               Theta: the rate the option price changes with respect to the passage of time
                   
               Further literature on all these subjects is abundant online and in textbooks.
               
               
               
               """
               
               )
       
   
    
        
        
    
    
        

