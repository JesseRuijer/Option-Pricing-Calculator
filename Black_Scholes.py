#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 16:17:29 2025

@author: jesseruijer
"""

import numpy as np
import scipy.stats as sts

#Calculate Black-Scholes analytical price

def Black_Scholes_Comp(S0, K, T, r, q, sigma, option_type):
    d1 = (np.log(S0 / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'Call':
        return S0 * sts.norm.cdf(d1) - K * np.exp(-r * T) * sts.norm.cdf(d2)
        
    elif option_type == 'Put':
        return K * np.exp(-r * T) * sts.norm.cdf(-d2) - S0 * sts.norm.cdf(-d1)
    
    


 

    