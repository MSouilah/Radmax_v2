#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

# =============================================================================
# Radmax Calcul module
# =============================================================================

import os
from copy import deepcopy
from scipy import arcsin, sin, multiply
import numpy as np
from numpy import arange

import Parameters as p4R
from Parameters import P4Rm
from Read import ReadFile, SaveFile
from Def_Strain import f_strain, old2new_strain, fit_input_strain, control_sp, interp_and_fit_strain, shift_strain
from Def_DW import f_DW, old2new_DW, fit_input_DW, control_dwp, interp_and_fit_dw, shift_dw
from Def_XRD import f_Refl_fit
import xrayutilities as xu

import logging
logger = logging.getLogger(__name__)
a = P4Rm()
b = ReadFile()
c = SaveFile()

# ------------------------------------------------------------------------------
class Calcul4Radmax():
    def on_init_dictionnaries(self):
        ncolumnParam = len(p4R.Params4Radmax)*[""]
        ncolumnPath = len(p4R.Path4Radmax)*[""]
        ncolumnAllData = len(p4R.Exp_file_all_section)*[""]
        ncolumnFit = len(p4R.FitData)*[0, 0, 0, "", False, "", "", "", None, "", 1]
        P4Rm.AllDataDict = dict(zip(p4R.Exp_file_all_section, ncolumnAllData))
        P4Rm.ParamDict = dict(zip(p4R.Params4Radmax, ncolumnParam))
        P4Rm.PathDict = dict(zip(p4R.Path4Radmax, ncolumnPath))
        P4Rm.FitDict = dict(zip(p4R.FitData, ncolumnFit))

    def on_new_project(self):
        """
        Launch new project with default inital parameters
        all variables are initialized and graph are eventually removed
        """
        self.on_reset_deformation_multiplication()
        self.on_init_dictionnaries()
        P4Rm.res_nearest_dw = []
        P4Rm.xrd_graph_loaded = 0

        P4Rm.initial_parameters = p4R.data_initial
        P4Rm.fitting_parameters = p4R.fitting_initial
        P4Rm.sample_geometry = p4R.geometry_initial
        P4Rm.allparameters = a.initial_parameters + a.fitting_parameters + a.sample_geometry
        i = 0
        for k in p4R.IP_p + p4R.F_p + p4R.SG_p:
            P4Rm.AllDataDict[k] = a.allparameters[i]
            i += 1
        P4Rm.ParamDict['slice_backup'] = a.AllDataDict['number_slices']
        P4Rm.ParamDict['strain_basis_backup'] = a.AllDataDict['strain_basis_func']
        P4Rm.ParamDict['dw_basis_backup'] = a.AllDataDict['dw_basis_func']

        P4Rm.ParamDict['strain_sm_ab_bkp'] = a.AllDataDict['strain_basis_func']
        P4Rm.ParamDict['dw_sm_ab_bkp'] = a.AllDataDict['dw_basis_func']

        P4Rm.ParamDict['damaged_value_backup'] = a.AllDataDict['damaged_depth']
                                                        
        P4Rm.ParamDict['t_l'] = a.AllDataDict['damaged_depth'] / a.AllDataDict['number_slices']
        P4Rm.ParamDict['z'] = arange(a.AllDataDict['number_slices']+1) * a.ParamDict['t_l']
        P4Rm.ParamDict['depth'] = a.AllDataDict['damaged_depth'] - a.ParamDict['z']
        P4Rm.ParamDict['sp'] = int(a.AllDataDict['strain_basis_func'])*[1]
        P4Rm.ParamDict['dwp'] = int(a.AllDataDict['dw_basis_func'])*[1]
        P4Rm.ParamDict['sp_abrupt'] = int(a.AllDataDict['strain_basis_func'])*[1]
        P4Rm.ParamDict['dwp_abrupt'] = int(a.AllDataDict['dw_basis_func'])*[1]
        
        P4Rm.ParamDict['sp_smooth'] = int(a.AllDataDict['strain_basis_func'])*[1]
        P4Rm.ParamDict['dwp_smooth'] = int(a.AllDataDict['dw_basis_func'])*[1]

        function_profile = 2  # pseudo-voigt
        P4Rm.AllDataDict['function_profile'] = function_profile
        P4Rm.ParamDict['func_profile'] = p4R.FitFunction_choice[function_profile]

        self.on_init_sp_dwp()

        P4Rm.spline_strain = 0
        P4Rm.spline_DW = 0

        P4Rm.ParamDictbackup['sp'] = a.ParamDict['sp']
        P4Rm.ParamDict['strain_basis'] = float(a.AllDataDict['strain_basis_func'])
        P4Rm.from_calc_strain = 1
        P4Rm.ParamDictbackup['dwp'] = a.ParamDict['dwp']
        P4Rm.ParamDict['dw_basis'] = float(a.AllDataDict['strain_basis_func'])
        P4Rm.from_calc_DW = 1
        # self.f_strain_DW()

        spline_strain = a.spline_strain
        spline_DW = a.spline_DW
        nb_slice, dw_func = self.OnChangeBasisFunction(
            a.AllDataDict['strain_basis_func'],
            a.AllDataDict['dw_basis_func'],
            spline_strain,
            spline_DW,
            a.AllDataDict['number_slices'],
            "load"
        )
        a.AllDataDict['dw_basis_func'] = dw_func
        a.AllDataDict['number_slices'] = nb_slice
        
        P4Rm.AllDataDict['substrate_name'] = "Al2O3"
        P4Rm.PathDict['substrate_name'] = "Al2O3"

        P4Rm.AllDataDict['exp_offset'] = 0

        self.graph_controller_dwp(1)
        self.graph_controller_sp(1)
        tmp = []
        tmp.append(a.res_nearest_dw[2])
        tmp.append(a.AllDataDict['strain_basis_func'])
        tmp.append(a.AllDataDict['damaged_depth'])
        if a.nearest_dw_change == 1:
            tmp.append(a.res_nearest_dw[0])
        else:
            tmp.append(a.AllDataDict['dw_function'])
        tmp.append(a.AllDataDict['number_slices'])
        P4Rm.ChangeBasisFunction = tmp
        P4Rm.nearest_dw_change = 0

        self.on_copy_default2_alldata()

    def on_load_project(self, paths):
        if paths:
            b.on_read_init_parameters(paths[0], p4R.ExperimentFile)
            datafromini = b.read_result_value()

            self.on_reset_deformation_multiplication()
            self.on_init_dictionnaries()

            P4Rm.res_nearest_dw = []
            P4Rm.ProjectFileData = datafromini['xrd_data']
            P4Rm.AllDataDict['exp_offset'] = 0
            for k, v in a.AllDataDict.items():
                P4Rm.AllDataDict[k] = datafromini[k]
            for k in p4R.Exp_file_all_section:
                if k in p4R.Exp_read_only:
                    P4Rm.AllDataDict[k] = float(a.AllDataDict[k])
                elif k in ['h', 'k', 'l', 'crystal_symmetry']:
                    P4Rm.AllDataDict[k] = int(float(a.AllDataDict[k]))
                else:
                    P4Rm.AllDataDict[k] = a.AllDataDict[k]
            for name in [
                'crystal_name',
                'substrate_name',
                'xrd_data'
            ]:
                P4Rm.PathDict[name] = datafromini[name]

            P4Rm.DefaultDict['project_folder'] = os.path.split(paths[0])[0]
            P4Rm.PathDict['path2ini'] = os.path.dirname(paths[0])
            # P4Rm.PathDict['path2ini'] = os.path.split(paths[0])[0]
            P4Rm.PathDict['path2inicomplete'] = paths[0]
            P4Rm.PathDict['namefromini'] = os.path.splitext(os.path.basename(paths[0]))[0]
            self.on_update_config_file('project_folder')
            if a.ProjectFileData == []:
                print("empty")
            else:
                P4Rm.PathDict['project_name'] = os.path.basename((os.path.dirname(paths[0])))
                # P4Rm.PathDict['project_name'] = os.path.splitext(os.path.basename(paths[0]))[0]
            success = self.on_read_initial_file()
            if success:
                self.on_load_and_read_data(0)

    def on_load_from_Database(self):
        P4Rm.FitDict['New&Load'] = 1
        P4Rm.res_nearest_dw = []
        self.on_reset_deformation_multiplication()
        self.on_calc_from_xrd()

        P4Rm.ParamDictbackup['dwp'] = deepcopy(a.ParamDict['dwp'])
        P4Rm.ParamDictbackup['sp'] = deepcopy(a.ParamDict['sp'])

        P4Rm.ParamDict['sp_abrupt'] = deepcopy(a.ParamDict['sp'])
        P4Rm.ParamDict['dwp_abrupt'] = deepcopy(a.ParamDict['dwp'])

        P4Rm.ParamDict['sp_smooth'] = deepcopy(a.ParamDict['sp'])
        P4Rm.ParamDict['dwp_smooth'] = deepcopy(a.ParamDict['dwp'])

        self.on_load_and_read_data(1)

    def on_load_and_read_data(self, val):
        P4Rm.ParamDict['slice_backup'] = a.AllDataDict['number_slices']
        P4Rm.ParamDict['damaged_value_backup'] = a.AllDataDict['damaged_depth']

        P4Rm.ParamDict['strain_basis_backup'] = a.AllDataDict['strain_basis_func']
        P4Rm.ParamDict['dw_basis_backup'] = a.AllDataDict['dw_basis_func']

        P4Rm.ParamDict['strain_sm_ab_bkp'] = a.AllDataDict['strain_basis_func']
        P4Rm.ParamDict['dw_sm_ab_bkp'] = a.AllDataDict['dw_basis_func']

        func_int = int(a.AllDataDict['function_profile'])
        P4Rm.ParamDict['func_profile'] = p4R.FitFunction_choice[func_int]

        if val == 0:
            if a.PathDict['crystal_name'] in a.crystal_list:
                msg = "Config file successfully loaded"
                logger.log(logging.INFO, msg)
            else:
                msg = "You need to add the proper strcuture to continue"
                logger.log(logging.INFO, msg)

        self.on_retype_data()
        self.on_init_sp_dwp()

        self.on_reset_deformation_multiplication()
        self.on_calcul_parameters("load", 1)

    def on_init_sp_dwp(self):
        P4Rm.ParamDict['sp_pv'] = p4R.sp_pv_initial
        P4Rm.ParamDict['dwp_pv'] = p4R.dwp_pv_initial

        P4Rm.ParamDict['state_sp'] = len(a.ParamDict['sp'])*[True]
        P4Rm.ParamDict['state_dwp'] = len(a.ParamDict['dwp'])*[True]

    def on_copy_default2_alldata(self):
        a = P4Rm()
        for k in p4R.Exp_read_only:
            P4Rm.AllDataDict[k] = a.DefaultDict[k]

    def on_test_substrate(self):
        if a.AllDataDict['film_thick'] < a.AllDataDict['damaged_depth']:
            P4Rm.AllDataDict['film_thick'] = a.AllDataDict['damaged_depth'] + 1
            P4Rm.FitDict['New&Load'] = 1
        if a.AllDataDict['dw_thick'] not in [0, 1]:
            P4Rm.AllDataDict['dw_thick'] = 1
            P4Rm.FitDict['New&Load'] = 1

    def on_update_config_file(self, name_key):
        name = p4R.filename + '.ini'
        c.on_update_config_file(
            os.path.join(p4R.current_dir, name),
            a.DefaultDict[name_key],
            name_key
        )

    def on_launch_calc(self):
        success = self.on_read_initial_file()
        if success:
            self.on_calcul_parameters("update", 1)

    def on_read_initial_file(self):
        dir_list = []
        for x in os.listdir(a.PathDict['path2ini']):
            if x.endswith(".txt"):
                dir_list.append(x)

        cur_file = "DW_coeff.txt"
        if cur_file in dir_list:
            try:
                """READING DW FILE"""
                b.read_dw_file(os.path.join(a.PathDict['path2ini'], cur_file))
            except TypeError:
                logger.log(
                    logging.WARNING,
                    "!Please check your input file!"
                )
                P4Rm.ParamDict['dwp'] = int(a.AllDataDict['dw_basis_func'])*[1]
        else:
            P4Rm.ParamDict['dwp'] = int(a.AllDataDict['dw_basis_func'])*[1]
        
        cur_file = "strain_coeff.txt"
        if cur_file in dir_list:
            try:
                """READING Strain FILE"""
                b.read_strain_file(os.path.join(a.PathDict['path2ini'], cur_file))
            except TypeError:
                logger.log(
                    logging.WARNING,
                    "!Please check your input file!"
                )
                P4Rm.ParamDict['sp'] = int(a.AllDataDict['strain_basis_func'])*[1]
        else:
            P4Rm.ParamDict['sp'] = int(a.AllDataDict['strain_basis_func'])*[1]
        
        P4Rm.ParamDict['sp_abrupt'] = a.ParamDict['sp']
        P4Rm.ParamDict['dwp_abrupt'] = a.ParamDict['dwp']

        P4Rm.ParamDict['sp_smooth'] = a.ParamDict['sp']
        P4Rm.ParamDict['dwp_smooth'] = a.ParamDict['dwp']

        if (os.path.exists(a.PathDict['xrd_data'])) is True:
            try:
                """READING XRD FILE"""
                b.read_xrd_file(a.PathDict['xrd_data'])
                self.on_calc_from_xrd()

            except TypeError:
                logger.log(
                    logging.WARNING,
                    "!Please check your input file!"
                )
            else:
                return True
        else:
            print('error')
            # msg_ = "Please, check that the input files really exists"
            # dlg = GMD.GenericMessageDialog(None, msg_,
            #                                "Attention", agwStyle=wx.OK |
            #                                wx.ICON_INFORMATION)
            # dlg.ShowModal()
            return False

    def on_calc_from_xrd(self):
        P4Rm.ParamDict['Iobs'] = a.ParamDict['data_xrd'][1]
        minval = np.min(a.ParamDict['Iobs'][np.nonzero(a.ParamDict['Iobs'])])
        P4Rm.ParamDict['Iobs'][a.ParamDict['Iobs'] == 0] = minval
        P4Rm.ParamDict['Iobs'] = a.ParamDict['Iobs'] / a.ParamDict['Iobs'].max()
        P4Rm.ParamDict['th'] = (a.ParamDict['data_xrd'][0]) * np.pi/360.
        P4Rm.ParamDict['th4live'] = 2*a.ParamDict['th']*180/np.pi
        P4Rm.ParamDictbackup['Iobs'] = a.ParamDict['Iobs']
        P4Rm.ParamDictbackup['th'] = a.ParamDict['th']
        P4Rm.xrd_graph_loaded = 1
        p4R.limit_graph['xmin_xrd'] = a.ParamDict['th4live'][0]
        p4R.limit_graph['xmax_xrd'] = a.ParamDict['th4live'][-1]

    def on_make_param_func(self):
        func = a.ParamDict['func_profile']
        fwhml = a.AllDataDict['width_left']*np.pi/180
        fwhmr = a.AllDataDict['width_right']*np.pi/180
        etal = a.AllDataDict['shape_left']
        etar = a.AllDataDict['shape_right']
        b_bell = a.AllDataDict['b_bell']
        pos = (a.ParamDict['th'].min() + a.ParamDict['th'].max())/2
        if func.__name__ == "f_Gauss" or func.__name__ == "f_Lorentz":
            param_func = [1, pos, fwhml]
        elif func.__name__ == "f_pVoigt":
            param_func = [1, pos, fwhml, etal]
        elif func.__name__ == "f_gbell":
            param_func = [1, pos, fwhml, b_bell]
        elif func.__name__ == "f_splitpV":
            param_func = [1, pos, fwhml, fwhmr, etal, etar]
        P4Rm.ParamDict['param_func_profile'] = param_func

    def read_cif_file(self):
        # =============================================================================
        # Material Data
        # =============================================================================
        crystal_name = a.AllDataDict['crystal_name'] + '.cif'
        cif_name = os.path.join(p4R.structures_name, crystal_name)
        mater = xu.materials.Crystal.fromCIF(cif_name)

        P4Rm.ParamDict['a'] = mater.lattice.a
        P4Rm.ParamDict['b'] = mater.lattice.b
        P4Rm.ParamDict['c'] = mater.lattice.c
        P4Rm.ParamDict['alpha'] = mater.lattice.alpha
        P4Rm.ParamDict['beta'] = mater.lattice.beta
        P4Rm.ParamDict['gamma'] = mater.lattice.gamma
        P4Rm.ParamDict['Vol'] = mater.lattice.UnitCellVolume()
        P4Rm.ParamDict['d'] = mater.planeDistance(a.AllDataDict['h'], a.AllDataDict['k'], a.AllDataDict['l'])
        P4Rm.ParamDict['FH'] = mater.StructureFactor(
            mater.Q(
                a.AllDataDict['h'],
                a.AllDataDict['k'],
                a.AllDataDict['l']
            ),
            p4R.value4StructureFactor*a.AllDataDict['wavelength']
        )
        P4Rm.ParamDict['FmH'] = mater.StructureFactor(
            mater.Q(
                -1*a.AllDataDict['h'],
                -1*a.AllDataDict['k'],
                -1*a.AllDataDict['l']
            ),
            p4R.value4StructureFactor*a.AllDataDict['wavelength']
        )
        P4Rm.ParamDict['F0'] = mater.StructureFactor(
            mater.Q(0, 0, 0),
            p4R.value4StructureFactor*a.AllDataDict['wavelength']
        )
        # =============================================================================
        # Substrate Data
        # =============================================================================
        substrate_name = a.AllDataDict['substrate_name'] + '.cif'
        cif_name = os.path.join(p4R.structures_name, substrate_name)
        mater = xu.materials.Crystal.fromCIF(cif_name)
        P4Rm.ParamDict['a_s'] = mater.lattice.a
        P4Rm.ParamDict['b_s'] = mater.lattice.b
        P4Rm.ParamDict['c_s'] = mater.lattice.c
        P4Rm.ParamDict['alpha_s'] = mater.lattice.alpha
        P4Rm.ParamDict['beta_s'] = mater.lattice.beta
        P4Rm.ParamDict['gamma_s'] = mater.lattice.gamma
        P4Rm.ParamDict['Vol_s'] = mater.lattice.UnitCellVolume()
        P4Rm.ParamDict['d_s'] = mater.planeDistance(a.AllDataDict['h_s'], a.AllDataDict['k_s'], a.AllDataDict['l_s'])
        P4Rm.ParamDict['FH_s'] = mater.StructureFactor(
            mater.Q(
                a.AllDataDict['h_s'],
                a.AllDataDict['k_s'],
                a.AllDataDict['l_s']
            ),
            p4R.value4StructureFactor*a.AllDataDict['wavelength']
        )
        P4Rm.ParamDict['FmH_s'] = mater.StructureFactor(
            mater.Q(
                -1*a.AllDataDict['h_s'],
                -1*a.AllDataDict['k_s'],
                -1*a.AllDataDict['l_s']
            ),
            p4R.value4StructureFactor*a.AllDataDict['wavelength']
        )
        P4Rm.ParamDict['F0_s'] = mater.StructureFactor(
            mater.Q(0, 0, 0),
            p4R.value4StructureFactor*a.AllDataDict['wavelength']
        )

    def f_strain_DW(self, val=None):
        if val == 1:
            P4Rm.ParamDict['sp'] = a.ParamDict['_fp_min'][:int(a.AllDataDict['strain_basis_func'])]
            P4Rm.ParamDict['dwp'] = a.ParamDict['_fp_min'][-1*int(a.AllDataDict['dw_basis_func']):]
        P4Rm.from_Calc_Strain = 1
        P4Rm.from_Calc_DW = 1

        P4Rm.ParamDict['DW_i'] = f_DW(
            a.ParamDict['z'],
            a.ParamDict['dwp'],
            a.AllDataDict['damaged_depth'],
            a.spline_DW
        )
        P4Rm.ParamDict['strain_i'] = f_strain(
            a.ParamDict['z'],
            a.ParamDict['sp'],
            a.AllDataDict['damaged_depth'],
            a.spline_strain
        )

    def calc_XRD(self, paths):
        """
        Loading and extracting of XRD data file with no default extension,
        but needed a two columns format file
        """
        test_opening = b.read_xrd_file(paths[0])
        if test_opening:
            if len(a.ParamDict['data_xrd']) == 2:
                P4Rm.DefaultDict['XRD_folder'] = os.path.split(paths[0])[0]
                P4Rm.PathDict['xrd_data'] = paths[0]
                self.on_update_config_file('XRD_folder')
                self.on_calc_from_xrd()
                return True
            else:
                return False
        else:
            return False

    def calc_strain(self, paths=None, choice=None):
        """
        Reading and calcul Strain coefficient
        """
        if paths:
            P4Rm.DefaultDict['Strain_folder'] = os.path.split(paths)[0]
            self.on_update_config_file('Strain_folder')
        spline_strain = a.spline_strain

        if choice == 0:
            test_opening = b.read_strain_xy_file(paths)
            if test_opening[0]:
                data = test_opening[1]
                if spline_strain == 2:
                    t = data[0].max()
                    P4Rm.ParamDict['t_l'] = t/a.AllDataDict['number_slices']
                    P4Rm.ParamDict['z'] = (
                        arange(a.AllDataDict['number_slices'] + 1) * a.ParamDict['t_l']
                    )
                    P4Rm.ParamDict['depth'] = t - a.ParamDict['z']
                else:
                    t = a.AllDataDict['damaged_depth']
                P4Rm.ParamDict['sp'] = fit_input_strain(
                    data,
                    a.AllDataDict['strain_basis_func'],
                    a.AllDataDict['damaged_depth'],
                    spline_strain
                )
                P4Rm.ParamDictbackup['sp'] = a.ParamDict['sp']
                P4Rm.ParamDict['strain_basis'] = float(a.AllDataDict['strain_basis_func'])
                P4Rm.from_Calc_Strain = 1
                c.save_deformation('input_strain', 'strain', a.ParamDict['sp'])
                return True
            else:
                return False
        else:
            t = a.AllDataDict['damaged_depth']
            P4Rm.ParamDictbackup['sp'] = a.ParamDict['sp']
            P4Rm.ParamDict['strain_basis'] = float(a.AllDataDict['strain_basis_func'])
            P4Rm.from_Calc_Strain = 1

    def calc_DW(self, paths=None, choice=None):
        """
        Reading and calcul DW coefficient
        """
        if paths:
            P4Rm.DefaultDict['DW_folder'] = os.path.split(paths)[0]
            self.on_update_config_file('DW_folder')
        spline_DW = a.spline_DW
        if choice == 0:
            test_opening = b.read_dw_xy_file(paths)
            if test_opening[0]:
                data = test_opening[1]
                if spline_DW == 2:
                    t = data[0].max()
                    P4Rm.ParamDict['t_l'] = t/a.AllDataDict['number_slices']
                    P4Rm.ParamDict['z'] = (
                        arange(a.AllDataDict['number_slices'] + 1) * a.ParamDict['t_l']
                    )
                    P4Rm.ParamDict['depth'] = t - a.ParamDict['z']
                else:
                    t = a.AllDataDict['damaged_depth']
                # P4Rm.AllDataDict['dw_basis_func'] = len(data[0])
                P4Rm.ParamDict['dwp'] = fit_input_DW(
                    data,
                    a.AllDataDict['dw_basis_func'],
                    a.AllDataDict['damaged_depth'],
                    spline_DW
                )
                P4Rm.ParamDictbackup['dwp'] = a.ParamDict['dwp']
                P4Rm.ParamDict['dw_basis'] = float(a.AllDataDict['strain_basis_func'])
                P4Rm.from_calc_DW = 1
                c.save_deformation('input_dw', 'DW', a.ParamDict['dwp'])
                return True
            else:
                return False
        else:
            t = a.AllDataDict['damaged_depth']
            P4Rm.ParamDictbackup['dwp'] = a.ParamDict['dwp']
            P4Rm.ParamDict['dw_basis'] = float(a.AllDataDict['strain_basis_func'])
            P4Rm.from_calc_DW = 1

    def OnChangeBasisFunction(self, strain, dw, spline_strain, spline_DW, slice_, state):
        strain_change = 0
        dw_change = 0
        slice_change = 0
        if strain != float(a.ParamDict['strain_basis_backup']):
            P4Rm.ParamDict['strain_basis_backup'] = strain
            P4Rm.ParamDict['state_sp'] = int(float(strain))*[True]
            strain_change = 1
        if dw != a.ParamDict['dw_basis_backup']:
            P4Rm.ParamDict['dw_basis_backup'] = dw
            dw_change = 1
        if slice_ != float(a.ParamDict['slice_backup']):
            P4Rm.ParamDict['slice_backup'] = slice_
            slice_change = 1
        if a.change_model == 1:
            slice_change = 1
        # if strain_change == 1 or dw_change == 1 or slice_change == 1:
        # print(strain, dw, spline_strain, spline_DW, slice_, state, "a.change_model", a.change_model)
        # print(a.ParamDict['strain_basis_backup'], a.ParamDict['dw_basis_backup'], a.ParamDict['slice_backup'])
        if strain_change == 1 or slice_change == 1 or dw_change == 1 or a.res_nearest_dw == []:
            if a.res_nearest_dw == []:
                dw_change = 1
            P4Rm.nearest_dw_change = 1
            res_nearest_damaged = self.find_nearest_damaged_depth(
                a.AllDataDict['damaged_depth'],
                a.AllDataDict['number_slices'],
                strain
            )
            P4Rm.AllDataDict['damaged_depth'] = res_nearest_damaged[0]
            P4Rm.AllDataDict['number_slices'] = res_nearest_damaged[1]
            slice_val = res_nearest_damaged[1]
            P4Rm.res_nearest_dw = self.find_nearest_dw(
                a.AllDataDict['number_slices'],
                dw,
                strain,
                strain_change,
                dw_change,
                slice_change
            )
            P4Rm.ParamDict['t_l'] = a.AllDataDict['damaged_depth']/a.AllDataDict['number_slices']
            P4Rm.ParamDict['z'] = arange(a.AllDataDict['number_slices'] + 1) * a.ParamDict['t_l']
            P4Rm.ParamDict['dwp'] = old2new_DW(
                a.ParamDict['z'],
                a.ParamDict['dwp'],
                a.AllDataDict['damaged_depth'],
                a.res_nearest_dw[0],
                int(spline_DW)
            )
            P4Rm.ParamDict['sp'] = old2new_strain(
                a.ParamDict['z'],
                a.ParamDict['sp'],
                a.AllDataDict['damaged_depth'],
                strain,
                int(spline_strain)
            )
            P4Rm.ParamDictbackup['dwp'] = deepcopy(a.ParamDict['dwp'])
            P4Rm.ParamDictbackup['sp'] = deepcopy(a.ParamDict['sp'])
            P4Rm.FitDict['New&Load'] = 0
            P4Rm.FitDict['list4DW'] = a.res_nearest_dw[2]
            P4Rm.ParamDict['state_dwp'] = a.res_nearest_dw[0]*[True]

            if state == "update":
                if a.AllDataDict['model'] == 2:
                    P4Rm.ParamDict['state_sp'] = 7*[True]
                    P4Rm.ParamDict['state_dwp'] = 7*[True]
                else:
                    if a.change_model == 1:
                        P4Rm.AllDataDict['strain_basis_func'] = a.ParamDict['strain_sm_ab_bkp']
                        P4Rm.AllDataDict['dw_basis_func'] = a.ParamDict['dw_sm_ab_bkp']
                    P4Rm.ParamDict['state_sp'] = len(a.ParamDict['sp'])*[True]
                    # P4Rm.ParamDict['state_dwp'] = len(a.ParamDict['dwp'])*[True]

            return a.AllDataDict['number_slices'], a.res_nearest_dw[0]
        else:
            slice_val = int(a.AllDataDict['number_slices'])
            return slice_val, dw

    def find_nearest_damaged_depth(self, damaged, N, Nstrain):
        if a.AllDataDict['model'] == 0:
            if damaged % Nstrain != 0:
                damaged = round(damaged/Nstrain)*Nstrain
            if N/Nstrain != 0:
                N = round(N/Nstrain)*Nstrain
        elif a.AllDataDict['model'] == 1:
            Nstrain = Nstrain - 3
            if damaged % Nstrain != 0:
                damaged = round(damaged/Nstrain)*Nstrain
            if N/Nstrain != 0:
                N = round(N/Nstrain)*Nstrain
        return damaged, N

    def find_nearest(self, ar, value):
        ar_ = [int(a) for a in ar]
        ar_ = np.array(ar_)
        idx = (np.abs(ar_-value)).argmin()
        return idx

    def find_nearest_dw(self, N, Ndw, Nstrain, strain_change, dw_change, slice_change):
        temp = []
        if a.AllDataDict['model'] == 0:
            for i in range(5, Nstrain + 1):
                if N % i == 0:
                    temp.append(str(i))
            if strain_change == 1:
                index = int(self.find_nearest(temp, Nstrain))
                P4Rm.AllDataDict['dw_basis_func'] = Nstrain
                val = int(temp[index])
            elif slice_change == 1:
                index = int(self.find_nearest(temp, Ndw))
                val = int(temp[index])
            elif dw_change == 1:
                index = int(a.AllDataDict['dw_basis_func'])
                val = int(float(index))
        elif a.AllDataDict['model'] == 1:
            val = Nstrain
            temp.append(str(val))
            index = 1
        return val, index, temp

    def on_reset_deformation_multiplication(self):
        P4Rm.ParamDict['DW_multiplication'] = 1.0
        P4Rm.ParamDict['strain_multiplication'] = 1.0

    def on_update(self, data=None):
        res_data = data[0]
        # print(res_data)
        basis_func_state = 1
        if (int(res_data['strain_basis_func']) == a.AllDataDict['strain_basis_func'] and
            int(res_data['dw_basis_func']) == a.AllDataDict['dw_basis_func'] and 
            int(res_data['number_slices']) == a.AllDataDict['number_slices']):
            basis_func_state = 0
        for key in res_data:
            P4Rm.AllDataDict[key] = res_data[key]
        func_int = int(a.AllDataDict['function_profile'])
        P4Rm.ParamDict['func_profile'] = p4R.FitFunction_choice[func_int]
        P4Rm.change_model = res_data['change_model']

        P4Rm.AllDataDict['crystal_name'] = res_data['crystal_choice']
        P4Rm.PathDict['crystal_name'] = res_data['crystal_choice']
        P4Rm.AllDataDict['substrate_name'] = res_data['crystal_choice_s']
        P4Rm.PathDict['substrate_name'] = res_data['crystal_choice_s']
        P4Rm.spline_strain = a.AllDataDict['model']
        P4Rm.spline_DW = a.AllDataDict['model']

        P4Rm.exclude_region = data[2]

        # print("exclude_region", a.exclude_region)
        # print(len(a.exclude_region))
        # if len(a.exclude_region) > 0:
        #     val_start = 0
        #     val_end = 0
        #     for val in a.exclude_region:
        #         val_start = float(val['exclude_start_region'])
        #         val_end = float(val['exclude_end_region'])
        #         print(a.ParamDict['th4live'])
        #         print(val_start)
        #         print(val_end)
        #         difference_array_start = np.absolute(a.ParamDict['th4live']-val_start)
        #         difference_array_end = np.absolute(a.ParamDict['th4live']-val_end)
        #         # find the index of minimum element from the array
        #         index_start = difference_array_start.argmin()
        #         index_end = difference_array_end.argmin()
        #         list_index = np.arange(index_start, index_end, 1)
        #         list_inf = np.full(len(list_index), np.inf)
        #         print("list_index, list_inf", list_index, list_inf)
        #         print("list_index, list_inf", len(list_index), len(list_inf))
        #         iobs_include_region = deepcopy(a.ParamDict['Iobs'])
        #         print(a.ParamDict['Iobs'])
        #         iobs_include_region[list_index] = list_inf
        #         print(iobs_include_region)

        self.on_retype_data()
        if (a.ParamDict['Iobs'] == [] or a.ParamDict['sp'] == [] or a.ParamDict['dwp'] == []):
            return
        else:
            res_test = self.on_calcul_parameters("update", basis_func_state)
            if res_test:
                P4Rm.success4Fit = 0
                return True
            else:
                return False

    def on_retype_data(self):
        joined_list = [*p4R.s_strain_DW, *p4R.s_geometry, *p4R.s_GSA_options]
        for vl in joined_list:
            P4Rm.AllDataDict[vl] = int(float(a.AllDataDict[vl]))

        for vl in p4R.s_experiment:
            if vl == 'function_profile':
                P4Rm.AllDataDict[vl] = int(float(a.AllDataDict[vl]))
            else:
                P4Rm.AllDataDict[vl] = float(a.AllDataDict[vl])

        for vl in ['h', 'k', 'l', 'h_s', 'k_s', 'l_s', 'crystal_symmetry_s']:
            P4Rm.AllDataDict[vl] = float(a.AllDataDict[vl])

    def on_calcul_parameters(self, state, basis_func_state):
        name = a.PathDict['crystal_name']
        self.on_test_substrate()
        self.read_cif_file()

        spline_strain = a.spline_strain
        spline_DW = a.spline_DW

        temp = [spline_strain, spline_DW]
        P4Rm.splinenumber = temp
        if a.AllDataDict['model'] != 2:
            if basis_func_state == 1:
                # print("OnChangeBasisFunction")
                nb_slice, dw_func = self.OnChangeBasisFunction(
                    a.AllDataDict['strain_basis_func'],
                    a.AllDataDict['dw_basis_func'],
                    spline_strain,
                    spline_DW,
                    a.AllDataDict['number_slices'],
                    state
                )
                a.AllDataDict['dw_basis_func'] = dw_func
                a.AllDataDict['number_slices'] = nb_slice
            tmp = []
            tmp.append(a.res_nearest_dw[2])
            tmp.append(a.AllDataDict['strain_basis_func'])
            tmp.append(a.AllDataDict['damaged_depth'])
            if a.nearest_dw_change == 1:
                tmp.append(a.res_nearest_dw[0])
            else:
                tmp.append(a.AllDataDict['dw_function'])
            tmp.append(a.AllDataDict['number_slices'])
            P4Rm.ChangeBasisFunction = tmp
            P4Rm.nearest_dw_change = 0
        else:
            tmp = []
            tmp.append([7])
            tmp.append(a.AllDataDict['strain_basis_func'])
            tmp.append(a.AllDataDict['damaged_depth'])
            tmp.append(a.AllDataDict['dw_function'])
            tmp.append(a.AllDataDict['number_slices'])
            P4Rm.ChangeBasisFunction = tmp
        if name != []:
            self.on_make_param_func()
            P4Rm.ParamDict['par'] = np.concatenate(
                (
                    a.ParamDict['sp'],
                    a.ParamDict['dwp']
                ),
                axis=0
            )
            x_ = a.ParamDict['th']
            param = a.ParamDict['param_func_profile']
            P4Rm.ParamDict['resol'] = a.ParamDict['func_profile'](x_, param)
            P4Rm.ParamDict['t_l'] = a.AllDataDict['damaged_depth'] / a.AllDataDict['number_slices']
            P4Rm.ParamDict['z'] = arange(a.AllDataDict['number_slices']+1) * a.ParamDict['t_l']

            # =============================================================================
            # Material Data
            # =============================================================================
            temp_1 = a.ConstDict['re'] * a.AllDataDict['wavelength'] * a.AllDataDict['wavelength']
            P4Rm.ParamDict['G'] = temp_1 / (np.pi * a.ParamDict['Vol'])
            P4Rm.ParamDict['thB_S'] = arcsin(
                a.AllDataDict['wavelength'] / (2*a.ParamDict['d'])
            )
            P4Rm.ParamDict['g0'] = sin(a.ParamDict['thB_S'] - a.ConstDict['phi'])
            P4Rm.ParamDict['gH'] = -sin(a.ParamDict['thB_S'] + a.ConstDict['phi'])
            P4Rm.ParamDict['b_S'] = a.ParamDict['g0'] / a.ParamDict['gH']

            # =============================================================================
            # Substrate Data
            # =============================================================================

            temp_1 = a.ConstDict['re'] * a.AllDataDict['wavelength'] * a.AllDataDict['wavelength']
            P4Rm.ParamDict['G_s'] = temp_1 / (np.pi * a.ParamDict['Vol_s'])
            P4Rm.ParamDict['thB_S_s'] = arcsin(
                a.AllDataDict['wavelength'] / (2*a.ParamDict['d_s'])
            )
            P4Rm.ParamDict['g0_s'] = sin(a.ParamDict['thB_S_s'] - a.ConstDict['phi_s'])
            P4Rm.ParamDict['gH_s'] = -sin(a.ParamDict['thB_S_s'] + a.ConstDict['phi_s'])
            P4Rm.ParamDict['b_S_s'] = a.ParamDict['g0_s'] / a.ParamDict['gH_s']

            # =============================================================================
            P4Rm.ParamDict['depth'] = a.AllDataDict['damaged_depth'] - a.ParamDict['z']
            test_dwp = self.graph_controller_dwp(1)
            if test_dwp:
                self.graph_controller_sp(1)
                self.calc_f_Refl()
                P4Rm.from_Calc_Strain = 1
                P4Rm.from_Calc_DW = 1
                return True
            else:
                return False
        else:
            msg_ = "check if the structure file really exists"
            logger.log(logging.WARNING, msg_)
            return False

    def on_read_bounds(self):
        roundval = 3
        P4Rm.bounds_parameters = []
        try:
            tmp_state_sp = a.ParamDict['state_sp'].tolist()
            tmp_state_dwp = a.ParamDict['state_dwp'].tolist()
        except (AttributeError):
            tmp_state_sp = a.ParamDict['state_sp']
            tmp_state_dwp = a.ParamDict['state_dwp']

        if a.AllDataDict['model'] == 2:
            for i in range(7):
                name = p4R.asym_pv[i]
                val_sp = str(round(a.ParamDict['sp'][i], roundval))
                val_dwp = str(round(a.ParamDict['dwp'][i], roundval))
                check_sp = a.ParamDict['state_sp'][i]
                check_dwp = a.ParamDict['state_dwp'][i]
                P4Rm.bounds_parameters.append(
                    {
                        "name": name,
                        "x_value": name,
                        "strain": val_sp,
                        "strain_choice": check_sp,
                        "dw": val_dwp, 
                        "dw_choice" : check_dwp
                    }
                )
        else:
            len_sp = len(a.ParamDict['strain_scat_x'])
            len_dwp = len(a.ParamDict['dw_scat_x'])
            if len_sp > len_dwp:
                num = len_sp
            else:
                num = len_dwp
            for i in range(num):
                if i < len_sp:
                    val_sp = str(round(a.ParamDict['strain_scat_y'][i], roundval))
                    check_sp = tmp_state_sp[i]
                    x_sp = a.ParamDict['strain_scat_x'][i]
                else:
                    val_sp = ""
                    check_sp = True
                if i < len_dwp:
                    val_dwp = str(round(a.ParamDict['dw_scat_y'][i], roundval))
                    check_dwp = tmp_state_dwp[i]
                else:
                    val_dwp = ""
                    check_dwp = True
                P4Rm.bounds_parameters.append(
                    {
                        "name": i+1,
                        "x_value": x_sp,
                        "strain": val_sp,
                        "strain_choice": check_sp,
                        "dw": val_dwp, 
                        "dw_choice" : check_dwp
                    }
                )
        return True

    def scale_drx_graph(self, data):
        msg = data[0]
        choice = data[1]
        value = 1 + float(data[2])
        if choice == 0:
            value = 1 - float(data[2])
        if msg == "strain":
            P4Rm.ParamDict['strain_multiplication'] = value
            P4Rm.ParamDict['sp'] = multiply(
                a.ParamDict['sp'],
                a.ParamDict['strain_multiplication']
            )
        if msg == "dw":
            P4Rm.ParamDict['DW_multiplication'] = value
            P4Rm.ParamDict['dwp'] = multiply(
                a.ParamDict['dwp'],
                a.ParamDict['DW_multiplication']
            )
        self.on_read_bounds()
        to_update = [data[3], a.bounds_parameters]
        self.on_update(to_update)

    def read_sp_dwp_from_table(self, data):
        res_bounds = data[1]
        dragPoints = data[2]
        sp_bounds = []
        dwp_bounds = []
        sp_bounds_use = []
        dwp_bounds_use = []
        control_x = []
        if dragPoints:
            data2add = 0
        else:
            max_val = res_bounds[0]['x_value']
            data2add = a.AllDataDict['damaged_depth'] - max_val
            # new_ref = res_bounds[-1]['x_value']
            # data2add = a.AllDataDict['damaged_depth'] - max_val
        for rr in res_bounds:
            sp_bounds.append(float(rr['strain'])/100)
            if rr['dw'] != '':
                dwp_bounds.append(float(rr['dw']))
            sp_bounds_use.append(rr['strain_choice'])
            dwp_bounds_use.append(rr['dw_choice'])
            # print(float(rr['x_value']))
            # print(data2add)
            # print(float(rr['x_value']) + data2add)
            control_x.append(float(rr['x_value']) + data2add)

        P4Rm.ParamDict['state_sp'] = np.array(sp_bounds_use)
        P4Rm.ParamDict['state_dwp'] = np.array(dwp_bounds_use)
        # P4Rm.ParamDict['control_sp_x'] = np.flipud(np.array(control_x))
        # P4Rm.ParamDict['control_dwp_x'] = np.flipud(np.array(control_x))
        # print(np.flipud(np.array(control_x)))

        if data[0] == "DW":
            P4Rm.ParamDict['dwp'] = interp_and_fit_dw(
                a.ParamDict['control_dwp_x'],
                np.array(dwp_bounds),
                a.ParamDict['z'],
                a.ParamDict['dwp'],
                a.AllDataDict['model']
            )
        else:
            P4Rm.ParamDict['sp'] = interp_and_fit_strain(
                a.ParamDict['control_sp_x'],
                np.array(sp_bounds),
                a.ParamDict['z'],
                a.ParamDict['sp'],
                a.AllDataDict['model']
            ) 
        P4Rm.ParamDict['par'] = np.concatenate(
            (
                a.ParamDict['sp'],
                a.ParamDict['dwp']
            ),
            axis=0
        )
        if data[0] == "DW":
            self.graph_controller_dwp(0, np.array(dwp_bounds))
        else:
            self.graph_controller_sp(0, np.array(sp_bounds))

    def update_dw_shift(self, val):
        # create an array twice the initial size to be shifted
        length = int(len(a.ParamDict['dw_line_y']))
        expanded_dw = np.empty(2*length)
        expanded_dw.fill(1)
        expanded_dw[int(length/2):int(3*length/2)] = a.ParamDict['dw_line_y']
        expanded_dw[int(3*length/2):2*length] = a.ParamDict['dw_line_y'][-1]
        # get shift factor from widget and shift curve accordingly
        # print(length, val)
        cut = int(float(val) * length)
        # print(cut)
        P4Rm.shifted_dw = expanded_dw[int(length/2)+cut:int(3*length/2)+cut]
        # print(a.ParamDict['dw_line_y'])
        # print(expanded_dw)
        # print(a.shifted_dw)
        # print(len(a.ParamDict['dw_line_y']))
        # print(len(a.shifted_dw))
        # print(a.ParamDict['control_dwp_x'])
        a.ParamDict['dwp'] = shift_dw(
            a.ParamDict['z'],
            a.ParamDict['dwp'],
            a.AllDataDict['damaged_depth'],
            a.AllDataDict['model'],
            a.shifted_dw
        )
        self.graph_controller_dwp(1)
        self.calc_f_Refl()
        P4Rm.from_Calc_Strain = 1
        P4Rm.from_Calc_DW = 1

    def graph_controller_dwp(self, val, dat=None):
        if val == 1:
            # P4Rm.ParamDict['dwp'] = a.ParamDict['_fp_min'][-1*int(a.AllDataDict['dw_basis_func']):]
            test_len_dwp, P4Rm.ParamDict['control_dwp_x'], P4Rm.ParamDict['dw_scat_y'] = control_dwp(
                a.ParamDict['z'],
                a.ParamDict['dwp'],
                a.AllDataDict['damaged_depth'],
                int(a.AllDataDict['model'])
            )
            if not test_len_dwp:
                return False
            # P4Rm.ParamDict['control_dwp_x'] = a.ParamDict['control_dwp_x']
            P4Rm.ParamDict['dw_scat_y'] = a.ParamDict['dw_scat_y']
        else:
            P4Rm.ParamDict['dw_scat_y'] = dat
        P4Rm.from_Calc_DW = 1
        P4Rm.ParamDict['dw_scat_x'] = a.AllDataDict['damaged_depth'] - a.ParamDict['control_dwp_x']
        P4Rm.ParamDict['dw_line_x'] = a.AllDataDict['damaged_depth'] - a.ParamDict['z']
        # print(a.ParamDict['z'])
        # print(a.ParamDict['dwp'])
        # print(a.AllDataDict['damaged_depth'])
        # print(a.AllDataDict['model'])
        P4Rm.ParamDict['dw_line_y'] = f_DW(
            a.ParamDict['z'],
            a.ParamDict['dwp'],
            a.AllDataDict['damaged_depth'],
            a.AllDataDict['model']
        )
        temp_graph = []
        for vv, tt in zip(a.ParamDict['dw_scat_x'], a.ParamDict['dw_scat_y']):
            tp = {
                "x": vv,
                "y": tt
            }
            temp_graph.append(tp)
        P4Rm.ParamDict['dw_scat'] = temp_graph

        temp_graph = []
        for vv, tt in zip(a.ParamDict['dw_line_x'], a.ParamDict['dw_line_y']):
            tp = {
                "x": vv,
                "y": tt
            }
            temp_graph.append(tp)
        P4Rm.ParamDict['dw_line'] = temp_graph
        p4R.limit_graph['ymin_dw'] = min(a.ParamDict['dw_scat_y']) - min(a.ParamDict['dw_scat_y'])*10/100
        p4R.limit_graph['ymax_dw'] = max(a.ParamDict['dw_scat_y']) + max(a.ParamDict['dw_scat_y'])*20/100
        p4R.limit_graph['xmin_dw'] = a.ParamDict['depth'][-1]
        p4R.limit_graph['xmax_dw'] = a.ParamDict['depth'][0]
        return True

    def update_strain_shift(self, val):
        # create an array twice the initial size to be shifted
        length = int(len(a.ParamDict['strain_line_y']))
        expanded_strain = np.zeros(2*length)
        expanded_strain[int(length/2):int(3*length/2)] = a.ParamDict['strain_line_y']/100
        expanded_strain[int(3*length/2):2*length] = a.ParamDict['strain_line_y'][-1]/100
        # get shift factor from widget and shift curve accordingly
        cut = int(float(val) * length)
        P4Rm.shifted_strain = expanded_strain[int(length/2)+cut:int(3*length/2)+cut]
        a.ParamDict['sp'] = shift_strain(
            a.ParamDict['z'],
            a.ParamDict['sp'],
            a.AllDataDict['damaged_depth'],
            a.AllDataDict['model'],
            a.shifted_strain
        )
        self.graph_controller_sp(1)
        self.calc_f_Refl()
        P4Rm.from_Calc_Strain = 1
        P4Rm.from_Calc_DW = 1
        
    def graph_controller_sp(self, val, dat=None):
        if val == 1:
            # P4Rm.ParamDict['sp'] = a.ParamDict['_fp_min'][:int(a.AllDataDict['strain_basis_func'])]
            P4Rm.ParamDict['control_sp_x'], P4Rm.ParamDict['strain_scat_y'] = control_sp(
                a.ParamDict['z'],
                a.ParamDict['sp'],
                a.AllDataDict['damaged_depth'],
                a.AllDataDict['model']
            )
            # P4Rm.ParamDict['control_sp_x'] = a.ParamDict['control_sp_x']
            P4Rm.ParamDict['strain_scat_y'] = a.ParamDict['strain_scat_y']*100
        else:
            P4Rm.ParamDict['strain_scat_y'] = dat*100
        P4Rm.from_Calc_Strain = 1
        P4Rm.ParamDict['strain_scat_x'] = a.AllDataDict['damaged_depth'] - a.ParamDict['control_sp_x']
        P4Rm.ParamDict['strain_line_x'] = a.AllDataDict['damaged_depth'] - a.ParamDict['z']
        P4Rm.ParamDict['strain_line_y'] = f_strain(
            a.ParamDict['z'],
            a.ParamDict['sp'],
            a.AllDataDict['damaged_depth'],
            a.AllDataDict['model']
        )*100
        temp_graph = []
        for vv, tt in zip(a.ParamDict['strain_scat_x'], a.ParamDict['strain_scat_y']):
            tp = {
                "x": vv,
                "y": tt
            }
            temp_graph.append(tp)
        P4Rm.ParamDict['strain_scat'] = temp_graph

        temp_graph = []
        for vv, tt in zip(a.ParamDict['strain_line_x'], a.ParamDict['strain_line_y']):
            tp = {
                "x": vv,
                "y": tt
            }
            temp_graph.append(tp)
        P4Rm.ParamDict['strain_line'] = temp_graph
        p4R.limit_graph['ymin_strain'] = min(a.ParamDict['strain_scat_y']) - min(a.ParamDict['strain_scat_y'])*10/100
        p4R.limit_graph['ymax_strain'] = max(a.ParamDict['strain_scat_y']) + max(a.ParamDict['strain_scat_y'])*20/100
        p4R.limit_graph['xmin_strain'] = a.ParamDict['depth'][-1]
        p4R.limit_graph['xmax_strain'] = a.ParamDict['depth'][0]
    
    def calc_f_Refl(self):
        const_all = self.dict_4_f_Refl()
        ar = []
        ar.append((a.ParamDict['strain_line_y']/100).astype(np.float64))
        ar.append(a.ParamDict['dw_line_y'].astype(np.float64))
        ar.append(const_all)
        P4Rm.ParamDict['Ical'] = f_Refl_fit(a.AllDataDict['geometry'], ar)
        P4Rm.ParamDict['I_i'] = (a.ParamDict['Ical'] /
                                    a.ParamDict['Ical'].max() +
                                    a.AllDataDict['background'])
        p4R.xrd2graph = []
        for vv, tt in zip(a.ParamDict['th4live'], a.ParamDict['I_i']):
            tp = {
                "x": vv,
                "y": tt
            }
            p4R.xrd2graph.append(tp)

    def on_read_fitting_options(self, data):
        for key in data[1]:
            P4Rm.AllDataDict[key] = float(data[1][key])

    def dict_4_f_Refl(self):
        const_all = {}
        const_all['wl'] = a.AllDataDict['wavelength']
        const_all['t'] = a.AllDataDict['damaged_depth']
        const_all['N'] = a.AllDataDict['number_slices']
        const_all['t_film'] = a.AllDataDict['film_thick']
        const_all['dw_film'] = a.AllDataDict['dw_thick']
        const_all['offset'] = float(a.AllDataDict['exp_offset'])*0.001*np.pi/360
        const_all['phi'] = a.ConstDict['phi']
        const_all['t_l'] = a.ParamDict['t_l']
        const_all['b_S'] = a.ParamDict['b_S']
        const_all['thB_S'] = a.ParamDict['thB_S']
        const_all['G'] = a.ParamDict['G']
        const_all['F0'] = a.ParamDict['F0']
        const_all['FH'] = a.ParamDict['FH']
        const_all['FmH'] = a.ParamDict['FmH']
        const_all['b_S_s'] = a.ParamDict['b_S_s']
        const_all['thB_S_s'] = a.ParamDict['thB_S_s']
        const_all['G_s'] = a.ParamDict['G_s']
        const_all['F0_s'] = a.ParamDict['F0_s']
        const_all['FH_s'] = a.ParamDict['FH_s']
        const_all['FmH_s'] = a.ParamDict['FmH_s']
        const_all['th'] = a.ParamDict['th']
        const_all['len_z'] = len(a.ParamDict['z'])
        const_all['resol'] = a.ParamDict['resol']
        return const_all