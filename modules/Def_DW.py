#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

import numpy as np
from numpy import array, append, ones, zeros
from scipy.optimize import leastsq
from scipy.interpolate import interp1d
from BSplines import constantSpline, cubicSpline
from Functions import f_pVoigt
import Parameters as p4R

def f_DW_spline3_smooth(alt, dwp, t):
    w_DW_free = dwp
    w_DW = array([1.0, 1.0, 1.0])
    w_DW = append(w_DW, w_DW_free)
    N_abscisses = len(w_DW) - 3.
    z = alt * N_abscisses / t
    index = 0
    DW = ones(len(z))
    for i in z:
        DW[index] = cubicSpline(i, w_DW)
        index = index + 1
    return DW

def f_DW_spline3_abrupt(alt, dwp, t):
    w_DW = dwp
    N_abscisses = len(w_DW) - 3.
    z = alt * N_abscisses / t
    index = 0
    DW = ones(len(z))
    for i in z:
        DW[index] = cubicSpline(i, w_DW)
        index = index + 1
    return DW

def f_DW_histogram(alt, dwp, t):
    w_DW = dwp[:]
    N_abscisses = len(w_DW)
    z = alt * N_abscisses / t
    index = 0
    DW = ones(len(z))
    for i in z:
        DW[index] = constantSpline(i, w_DW)
        index = index + 1
    return DW

def f_DW_pv(alt, pv_p, t):
    height = 1 - pv_p[0]
    loc = pv_p[1] * t
    fwhm1 = pv_p[2] * t
    fwhm2 = pv_p[3] * t
    eta1 = pv_p[4]
    eta2 = pv_p[5]
    bkg = 1 - pv_p[6]
    DW = zeros(len(alt))
    DW[(alt <= loc)] = (1. -
                        f_pVoigt(alt[alt <= loc], [height, loc, fwhm1, eta1]))
    DW[(alt > loc)] = (1. -
                       (f_pVoigt(alt[alt > loc],
                                 [height-bkg, loc, fwhm2, eta2]) + bkg))
    return DW

# def f_DW_pv_lmfit(alt, pars, t):
#     height = 1 - pars[7]
#     loc = pars[8] * t
#     fwhm1 = pars[9] * t
#     fwhm2 = pars[10] * t
#     eta1 = pars[11]
#     eta2 = pars[12]
#     bkg = 1 - pars[13]

#     DW = zeros(len(alt))
#     DW[(alt <= loc)] = (1. -
#                         f_pVoigt(alt[alt <= loc], [height, loc, fwhm1, eta1]))
#     DW[(alt > loc)] = (1. -
#                        (f_pVoigt(alt[alt > loc],
#                                  [height-bkg, loc, fwhm2, eta2]) + bkg))
#     return DW

def old2new_DW(alt, dwp, t, new_size, choice):
    dwp_guess = ones(new_size)
    dw_old = f_DW(alt, dwp, t, choice)

    def errfunc(dwp, alt, dw, t): return f_DW(alt, dwp, t, choice) - dw_old
    dwp_new, success = leastsq(errfunc, dwp_guess, args=(alt, dw_old, t))
    return dwp_new

def fit_input_DW(data, size, t, choice):
    def errfunc(dwp, x, y, choice): return f_DW(x, dwp, t, choice) - y

    depth = data[0]
    DW = data[1]

    if choice == 2:
        dwp = p4R.dwp_pv_initial
        t = depth.max()
    else:
        dwp = ones(size)
    height = t - depth

    dwp_fit, success = leastsq(errfunc, dwp, args=(height, DW, choice))
    return dwp_fit

def control_dwp(alt, dwp, t, model):
    Nspline = len(dwp)
    Nslice = len(alt)-1
    # print("Nspline, Nslice", Nspline, Nslice)
    # print("dwp", dwp)
    if model == 0 or model == 5:
        z_dwp =  np.arange(1, Nspline+1)* t / Nspline # generate depth (x axis) for the strain basis function
        z_interp = np.arange(1, (Nspline*Nslice)+1)* t / (Nspline*Nslice)
    if model == 1 or model == 6:
        z_dwp =  np.arange(0, Nspline)* t / (Nspline-1) # generate depth (x axis) for the strain basis function
        z_interp = np.arange(0, (Nspline*Nslice)* t / (Nspline*Nslice-1))
    # print("z_dwp, z_interp", z_dwp, z_interp)
    # print("z_dwp, z_interp", len(z_dwp), len(z_interp))
    dw = f_DW(z_interp, dwp, t, model)
    scaled_dwp = dw[np.in1d(np.around(z_interp, decimals=1),  np.around(z_dwp,decimals=1))]
    st = False
    if len(dwp) == len(scaled_dwp):
        st = True
    # print("dw", dw)
    # print("dw", len(dw))
    # print("z_dwp, scaled_dwp", z_dwp, scaled_dwp)
    return st, z_dwp, scaled_dwp

def shift_dw(alt, sp, t, model, shifted):
    dw_old = f_DW(alt, sp, t, model)
    def errfunc(sp, alt, dw, t, model):
        return f_DW(alt, sp, t, model) - shifted
    sp_new, success = leastsq(errfunc, sp, args=(alt, dw_old, t, model))
    return sp_new

def f_DW(alt, dwp, t, model):
    if model == 0 or model == 5:
        if model == 0:
            tmp_dw = dwp[:]
        else:
            tmp_dw = dwp[-int(dwp[1]):]
        dw = f_DW_spline3_smooth(alt, tmp_dw, t)
    elif model == 1 or model == 6:
        if model == 1:
            tmp_dw = dwp[:]
        else:
            tmp_dw = dwp[-int(dwp[1]):]
        dw = f_DW_spline3_abrupt(alt, tmp_dw, t)
    elif model == 2 or model == 4:
        if model == 2:
            tmp_dw = dwp[:]
        else:
            tmp_dw = dwp[:7]
        dw = f_DW_pv(alt, tmp_dw, t)
    elif model == 3:
        dw = f_DW_histogram(alt, dwp, t)
    return dw

def interp_and_fit_dw(x, y, alt, old_dwp, model):
	# interpolate the dw curve obtained with the control points with a deg3 spline
	# fit a new a new dw curve to this to obtain new Bspline weights
	# old weights are used as a guess
	f = interp1d(x,y, kind = 'cubic', fill_value="extrapolate")
	int_curve = f(alt)
	t = alt.max()

	def errfunc(dwp, alt, int_curve):
		return f_DW(alt, dwp, t, model) - int_curve

	dwp_fit, success = leastsq(errfunc, old_dwp, args=(alt, int_curve))
	return dwp_fit