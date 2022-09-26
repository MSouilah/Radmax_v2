#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

import numpy as np
from Parameters import P4Rm
from scipy import tan, exp, sin, pi, convolve, sqrt
a = P4Rm()

def signe(x):
    '''sign function'''
    return x.real / abs(x.real)

# =============================================================================
# Calcul de la réflectivité dynamique
# =============================================================================
def f_Refl_fit(choice, Data=None):
    if choice == 0:
        res = f_Refl_Default_fit(Data)
    elif choice == 1:
        res = f_Refl_Thin_Film_fit(Data)
    elif choice == 2:
        res = f_Refl_Thick_Film_fit(Data)
    elif choice == 3:
        res = f_Refl_Thick_Film_and_Substrate_fit(Data)
    return res

# =============================================================================
# label_1 = "Default"
# =============================================================================
def f_Refl_Default_fit(Data):
    strain = Data[0]
    DW = Data[1]
    dat = Data[2]
    th = dat['th']+dat['offset']
    thB = dat['thB_S']-strain*tan(dat['thB_S'])  # angle de Bragg dans chaque lamelle
    eta = ((-dat['b_S']*(th-dat['thB_S'])*sin(2*dat['thB_S'])-0.5*dat['G']*dat['F0']*(1-dat['b_S']))/((abs(dat['b_S'])**0.5)*dat['G']*(dat['FH']*dat['FmH'])**0.5))
    res = (eta-signe(eta.real)*((eta*eta-1)**0.5))
    n = 1
    while (n <= dat['N']):
        g0 = sin(thB[n]-dat['phi'])  # gamma 0
        gH = -sin(thB[n]+dat['phi'])  # gamma H
        b = g0/gH
        T = (pi*dat['G']*((dat['FH']*dat['FmH'])**0.5)*dat['t_l']*DW[n]/(dat['wl']*(abs(g0*gH)**0.5)))
        eta = ((-b*(th-thB[n])*sin(2*dat['thB_S'])-0.5*dat['G']*dat['F0']*(1-b))/((abs(b)**0.5)*dat['G']*DW[n]*(dat['FH']*dat['FmH'])**0.5))
        S1 = (res-eta+sqrt(eta*eta-1))*exp(-1j*T*sqrt(eta*eta-1))
        S2 = (res-eta-sqrt(eta*eta-1))*exp(1j*T*sqrt(eta*eta-1))
        res = (eta+((eta*eta-1)**0.5)*((S1+S2)/(S1-S2)))
        n += 1
    return convolve(abs(res)**2, dat['resol'], mode='same')


# =============================================================================
# label_2 = "Thin film"
# =============================================================================
def f_Refl_Thin_Film_fit(Data):
    strain = Data[0]
    DW = Data[1]
    dat = Data[2]

    th = dat['th']+dat['offset']
    thB = dat['thB_S']-strain*tan(dat['thB_S'])  # angle de Bragg dans chaque lamelle
    eta = 0
    res = 0
    n = 1
    while (n <= dat['N']):
        g0 = sin(thB[n]-dat['phi'])  # gamma 0
        gH = -sin(thB[n]+dat['phi'])  # gamma H
        b = g0/gH
        T = pi*dat['G']*((dat['FH']*dat['FmH'])**0.5)*dat['t_l']*DW[n]/(dat['wl']*(abs(g0*gH)**0.5))
        eta = (-b*(th-thB[n])*sin(2*dat['thB_S'])-0.5*dat['G']*dat['F0']*(1-b))/((abs(b)**0.5)*dat['G']*DW[n]*(dat['FH']*dat['FmH'])**0.5)
        S1 = (res-eta+(eta*eta-1)**0.5)*exp(-1j*T*(eta*eta-1)**0.5)
        S2 = (res-eta-(eta*eta-1)**0.5)*exp(1j*T*(eta*eta-1)**0.5)
        res = (eta+((eta*eta-1)**0.5)*((S1+S2)/(S1-S2)))
        n += 1
    return convolve(abs(res)**2, dat['resol'], mode='same')


# =============================================================================
# label_3 = "Thick film"
# =============================================================================
def f_Refl_Thick_Film_fit(Data):
    strain = Data[0]
    DW = Data[1]
    dat = Data[2]

    th = dat['th']+dat['offset']
    delta_t = dat['t_film']-dat['t']
    thB = dat['thB_S']-strain*tan(dat['thB_S'])  # angle de Bragg dans chaque lamelle
    eta = 0
    res = 0
    g0 = sin(thB[0]-dat['phi'])  # gamma 0
    gH = -sin(thB[0]+dat['phi'])  # gamma H
    b = g0/gH
    T = pi*dat['G']*((dat['FH']*dat['FmH'])**0.5)*delta_t/(dat['wl']*(abs(g0*gH)**0.5))
    eta = (-b*(th-thB[0])*sin(2*dat['thB_S'])-0.5*dat['G']*dat['F0']*(1-b))/((abs(b)**0.5)*dat['G']*(dat['FH']*dat['FmH'])**0.5)
    S1 = (res-eta+(eta*eta-1)**0.5)*exp(-1j*T*(eta*eta-1)**0.5)
    S2 = (res-eta-(eta*eta-1)**0.5)*exp(1j*T*(eta*eta-1)**0.5)
    res = (eta+((eta*eta-1)**0.5)*((S1+S2)/(S1-S2)))

    n = 1
    while (n <= dat['N']):
        g0 = sin(thB[n]-dat['phi'])  # gamma 0
        gH = -sin(thB[n]+dat['phi'])  # gamma H
        b = g0/gH
        T = pi*dat['G']*((dat['FH']*dat['FmH'])**0.5)*dat['t_l']* DW[n]/(dat['wl']*(abs(g0*gH)**0.5))
        eta = (-b*(th-thB[n])*sin(2*dat['thB_S'])-0.5*dat['G']*dat['F0']*(1-b))/((abs(b)**0.5)*dat['G']*DW[n]*(dat['FH']*dat['FmH'])**0.5)
        S1 = (res-eta+(eta*eta-1)**0.5)*exp(-1j*T*(eta*eta-1)**0.5)
        S2 = (res-eta-(eta*eta-1)**0.5)*exp(1j*T*(eta*eta-1)**0.5)
        res = (eta+((eta*eta-1)**0.5)*((S1+S2)/(S1-S2)))
        n += 1
    return convolve(abs(res)**2, dat['resol'], mode='same')


# =============================================================================
# label_4 = "Thick film + substrate"
# =============================================================================
def f_Refl_Thick_Film_and_Substrate_fit(Data):
    strain = Data[0]
    DW = Data[1]
    dat = Data[2]

    th = dat['th']+dat['offset']
    delta_t = dat['t_film']-dat['t']
    thB = dat['thB_S']-strain*tan(dat['thB_S'])  # angle de Bragg dans chaque lamelle

    temp1 = -dat['b_S_s']*(th-dat['thB_S_s'])*sin(2*dat['thB_S_s'])-(0.5*dat['G_s']*dat['F0_s']*(1-dat['b_S_s']))
    temp2 = (abs(dat['b_S_s'])**0.5)*dat['G_s']*(dat['FH_s']*dat['FmH_s'])**0.5
    eta = temp1/temp2
    res = (eta-signe(eta.real)*((eta*eta - 1)**0.5))

    g0 = sin(thB[0]-dat['phi'])  # gamma 0
    gH = -sin(thB[0]+dat['phi'])  # gamma H
    b = g0/gH
    T = pi*dat['G']*((dat['FH']*dat['FmH'])**0.5)*delta_t*dat['dw_film']/(dat['wl'] (abs(g0*gH)**0.5))
    eta = (-b*(th-thB[0])*sin(2*dat['thB_S'])-0.5*dat['G']*dat['F0']*(1-b))/((abs(b)**0.5)*dat['G']*dat['dw_film']*(dat['FH']*dat['FmH'])**0.5)
    S1 = (res-eta+(eta*eta-1)**0.5)*exp(-1j*T*(eta*eta-1)**0.5)
    S2 = (res-eta-(eta*eta-1)**0.5)*exp(1j*T*(eta*eta-1)**0.5)
    res = (eta+((eta*eta-1)**0.5) * ((S1+S2)/(S1-S2)))

    n = 1
    while (n <= dat['N']):
        g0 = sin(thB[n]-dat['phi'])  # gamma 0
        gH = -sin(thB[n]+dat['phi'])  # gamma H
        b = g0/gH
        T = pi*dat['G']*((dat['FH']*dat['FmH'])**0.5)*dat['t_l']*DW[n]*dat['dw_film']/(dat['wl']*(abs(g0*gH)**0.5))
        eta = (-b*(th-thB[n])*sin(2*dat['thB_S'])-0.5*dat['G']*dat['F0']*(1-b))/((abs(b)**0.5)*dat['G']*DW[n]*dat['dw_film']*(dat['FH']*dat['FmH'])**0.5 )
        S1 = (res-eta+(eta*eta-1)**0.5)*exp(-1j*T*(eta*eta-1)**0.5)
        S2 = (res-eta-(eta*eta-1)**0.5)*exp(1j*T*(eta*eta-1)**0.5)
        res = (eta+((eta*eta-1)**0.5)*((S1+S2)/(S1-S2)))
        n += 1
    return convolve(abs(res)**2, dat['resol'], mode='same')


# =============================================================================
# Only substrate for t=0 --> damaged depth
# =============================================================================
def f_Refl_Substrate_fit(Data):

    offset = float(a.AllDataDict['exp_offset'])*np.pi/360
    G = a.ParamDict['G']
    thB_S = a.ParamDict['thB_S']
    resol = a.ParamDict['resol']
    b_S = a.ParamDict['b_S']
    FH = a.ParamDict['FH']
    FmH = a.ParamDict['FmH']
    F0 = a.ParamDict['F0']
    th = a.ParamDict['th']

    th = th + offset
    eta = (-b_S*(th-thB_S)*sin(2*thB_S) - 0.5*G*F0[0]*(1-b_S)) / ((abs(b_S)**0.5) * G * (FH[0]*FmH[0])**0.5)
    res = (eta - signe(eta.real)*((eta*eta - 1)**0.5)) * (FH[0] / FmH[0])**0.5
    return convolve(abs(res)**2, resol, mode='same')
