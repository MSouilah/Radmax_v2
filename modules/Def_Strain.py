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

def f_strain_spline3_smooth(alt, sp, t):
    w_strain_free = sp
    w_strain = array([0.0, 0.0, 0.0])
    w_strain = append(w_strain, w_strain_free)
    N_abscisses = len(w_strain) - 3.
    z = alt * N_abscisses / t
    index = 0
    strain = ones(len(z))
    for i in z:
        strain[index] = cubicSpline(i, w_strain) / 100. ## LES POIDS SONT EN %
        index = index + 1
    return strain

def f_strain_spline3_abrupt(alt, sp, t):
    w_strain = sp
    N_abscisses = len(w_strain) - 3.
    z = alt * N_abscisses / t
    index = 0
    strain = ones(len(z))
    for i in z:
        strain[index] = cubicSpline(i, w_strain) / 100. ## LES POIDS SONT EN %
        index = index + 1
    return strain

def f_strain_histogram(alt, sp, t):
    w_strain = sp[:]
    N_abscisses = len(w_strain)
    z = alt * N_abscisses / t
    index = 0
    strain = ones(len(z))
    for i in z:
        strain[index] = constantSpline(i, w_strain) / 100.
        index = index + 1
    return strain

def f_strain_pv(alt, pv_p, t):
    height = pv_p[0]
    loc = pv_p[1] * t
    fwhm1 = pv_p[2] * t
    fwhm2 = pv_p[3] * t
    eta1 = pv_p[4]
    eta2 = pv_p[5]
    bkg = pv_p[6]
    strain = zeros(len(alt))
    strain[(alt <= loc)] = f_pVoigt(alt[alt <= loc],
                                    [height, loc, fwhm1, eta1]) / 100
    strain[(alt > loc)] = (f_pVoigt(alt[alt > loc],
                           [height-bkg, loc, fwhm2, eta2]) + bkg) / 100
    return strain

def old2new_strain(alt, sp, t, new_size, choice):
    sp_guess = ones(int(new_size))
    strain_old = f_strain(alt, sp, t, choice)

    def errfunc(sp, alt, strain, t):
        return f_strain(alt, sp, t, choice) - strain_old
    sp_new, success = leastsq(errfunc, sp_guess, args=(alt, strain_old, t))
    return sp_new

def fit_input_strain(data, size, t, choice):
    def errfunc(sp, x, y, choice):
        return f_strain(x, sp, t, choice) - y

    depth = data[0]
    strain = data[1]

    if choice == 2:
        sp = p4R.sp_pv_initial
        t = depth.max()
    else:
        sp = ones(size)
    height = t - depth
    sp_fit, success = leastsq(errfunc, sp, args=(height, strain, choice))
    return sp_fit

def control_sp(alt, sp, t, model):
	Nspline = len(sp)
	Nslice = len(alt)-1

	if model == 0 or model == 5:
		z_sp =  np.arange(1, Nspline+1)* t / Nspline # generate depth (x axis) for the strain basis function
		z_interp = np.arange(1, (Nspline*Nslice)+1)* t / (Nspline*Nslice)
	if model == 1 or model == 6:
		z_sp =  np.arange(0, Nspline)* t / (Nspline-1) # generate depth (x axis) for the strain basis function
		z_interp = np.arange(0, (Nspline*Nslice)* t / (Nspline*Nslice-1))

	strain = f_strain(z_interp, sp, t, model)
	#finds the value of strain at values z close to z_sp
	scaled_sp = strain[np.in1d(np.around(z_interp, decimals=1),  np.around(z_sp,decimals=1))]
	return z_sp, scaled_sp

def shift_strain(alt, sp, t, model, shifted_strain):
    strain_old = f_strain(alt, sp, t, model)
    def errfunc(sp, alt, strain, t, model):
        return f_strain(alt, sp, t, model) - shifted_strain
    sp_new, success = leastsq(errfunc, sp, args=(alt, strain_old, t, model))
    return sp_new
    
def f_strain(alt, sp, t, model):
    if model == 0 or model == 5:
        if model == 0:
            tmp_sp = sp[:]
        else:
            tmp_sp = sp[2:int(sp[0])+2]
        strain = f_strain_spline3_smooth(alt, tmp_sp, t)
    elif model == 1 or model == 6:
        if model == 1:
            tmp_sp = sp[:]
        else:
            tmp_sp = sp[2:int(sp[0])+2]
        strain = f_strain_spline3_abrupt(alt, tmp_sp, t)
    elif model == 2 or model == 4:
        strain = f_strain_pv(alt, sp, t)
    elif model == 3:
        strain = f_strain_histogram(alt, sp, t)
    return strain

def interp_and_fit_strain(x, y, alt, old_sp, model):
	# interpolate the strain curve obtained with the control points with a degree3 spline
	f = interp1d(x, y, kind = 'cubic', fill_value="extrapolate")
	int_curve = f(alt)
	# fit a new a new strain curve to this to obtain the new Bspline weights
	# old weights are used as a guess
	t = alt.max()
	def errfunc(sp, alt, int_curve):
		return f_strain(alt, sp, t, model) - int_curve

	sp_fit, success = leastsq(errfunc, old_sp, args=(alt, int_curve))
	return sp_fit