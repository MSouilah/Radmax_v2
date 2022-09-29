#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

# =============================================================================
# Radmax Parameters module
# =============================================================================


import os
from os.path import abspath
from Functions import f_Gauss, f_Lorentz, f_pVoigt, f_gbell, f_splitpV

Application_name = "RaDMaX"
filename = "Radmax"
version = "2022.09"
Application_version = " - " + version
last_modification = "28/09/2022"
log_filename = "activity"
ExperimentFile = 'ExperimentFile'
RadmaxFile = 'RadmaxFile'
Database_name = 'RadmaxDB'
Database_sql = 'RadMaxData.sql'

description = "RaDMaX: Radiation Damage in Materials analyzed with X-ray diffraction"
licence = "RaDMaX is distributed freely under the CeCILL license (see LICENSE.txt and COPYRIGHT.txt)."
copyright_ = "(C) IRCER"
website_ = "http://aboulle.github.io/RaDMaX/"


# modification 23/07/2021:
# add fitting panel and improvment for chart.js graph

# modification 30/08/2021:
# create complet web and local package for the application --> indeed, the app is quite long to open when reading files into eel.init('web')
# the local version has to be used only if any connection with internet is available, in this case, time loaded is around 5-6 seconds (depending of your computer configuration)

# modification 13/09/2021:
# add sample geometry and database list tabs

# modification 16/09/2021:
# select and delete data in database

# modification 27/09/2021:
# add shortcuts, better enhencement of sidebar, bugs correction
# next works: cleaning console windows to show only essential datas and informations

# modification 05/10/2021:
# restore previous strain and dwp
# implementation of GSA
# save files and ini projects

# modification 07/10/2021:
# add application theme

# modification 08/10/2021:
# change in strain and deby-weller plot graph

# modification 20/10/2021:
# add change limits input modal window

# modification 05/10/2021:
# change datatables.net by tabulaor for removing jquery -->  test bu not sure if it work at the end

# modification 17/11/2021:
# add tkinter askopenfilename and askopenfilename module to open and save data from web browser != Electron

# modification 26/11/2021:
# corrections diverses bugs:
# - poblem with document.getElementsByName(key) node when several input have the same name, use document.getElementsByName(key).length  and loop through the node
# - poblem wih update following change of the res_data array input order datas
# - add popup on close windows fo electron
# - test prevent update page on classic browser
# - scale not working

# modification 01/12/2021:
# corrections diverses bugs:
# - add scroll to top
# - correction bug imporing data wit header informations
# - correction path and data only in database (data removes from disk)

# modification 02/12/2021:
# corrections diverses bugs:
# - change icon and favicon
# - add examples directory with script to first opening replace <WRITE PATH HERE> by effected path of radmax.py.Works when creating radmax.ini file in modules directory
# - change Readme.md file and update file to push to github

# modification 03/12/2021:
# corrections diverses bugs:
# - migrate all "eel" notation in exchange file to unify the data connexion between javascript and python

# modification 07/12/2021:
# corrections diverses bugs:
# - improve dragdata on starin and DW. With zoom enabled, all points in the zommed window are move by the same amout of displacement.
# - drag curves horizontaly is config but he work is in progress waiting for the function to manage such a mouvement

# modification 17/12/2021:
# corrections diverses bugs:
# - improvment of drag and drop for Strain and DW:
# --> multiple points selection by ctrl+left mouse button or draw ROI by alt+right mouse button, then drag the selected points.
# - begin test of XRD exclude region

# modification 04/01/2022:
# corrections diverses bugs:
# - Include XRD exclude region to be tested
# - color graph, need t color poinbackground

# modification 06/01/2022:
# - B-splines abrupt working at last !!! Add a modal window to invit user to change
# the value of the Strain basis function due to the non-fitting adequation between damaged depth and number of slice
# - Asymetric pv: work in progress
# - begin test horizontaly displacement
# - database to e entirely remain to win size and interactivity
# - remove of GSA (work to do later)


# modification 23/08/2022:
# replace sqlalchemy by sqlite3 to save and read data from/to DB
# remove this large package not useful in our app (too big and useless for what we have to do, very basic read/write sql operation)

# modification 29/08/2022:
# finally succeed to have an offline/connected app
# not able to achieve the jinja2 system to work, I managed a in house solution.
# replace header in the index.html from head_connected.html/head_offline.html
# change the eel.__init__ to add exclude directories option to active or not the reading of the package
# indeed the reading of the 'eel.init('web') is quite long depending the amout of files in the directory and sub-directory

# modification 30/08/2022:
# change config file to config.ini and the two coeff dw and strain files to dw_coeff.txt and strain_coeff.txt
# files are now generic for a serie, just have to change the xrd path to work with

# modification 23/09/2022:
# modifs path and extract files
# change file to fit with new project

# modification 26/09/2022:
# delete data database
# bugs fixes: warning message from export fit if no fit available, warning message if problem in suppression from databse,
# warning message if save/save poject without loading xrd data

# modification 28/09/2022:
# test linux, change path and name of file in UpdateExampleFiles()
# xrayutilities is not embeded anymore, need to install it
# path to local modules eel corrected
# begin test to reactive electron mode:
# --> success to close window app add .destroy
# --> correction call between electron menu and javascript



theme_choice = {
    0: "bootstrap5.1.2.min.css",
    1: "Bootswatch5.1.2_darkly.min.css",
    2: "Bootswatch5.1.2_cyborg.min.css",
    3: "Bootswatch5.1.2_sandstone.min.css",
    4: "Bootswatch5.1.2_sketchy.min.css",
    5: "Bootswatch5.1.2_solar.min.css",
    6: "Bootswatch5.1.2_minty.min.css",
    7: "Bootswatch5.1.2_quartz.min.css"
}

table_theme_choice = {
    0: "tabulator.min.css",
    1: "tabulator_midnight.min.css",
    2: "tabulator_midnight.min.css",
    3: "tabulator_bulma.min.css",
    4: "tabulator_semanticui.min.css",
    5: "tabulator_modern.min.css",
    6: "tabulator_modern.min.css",
    7: "tabulator_modern.min.css"
}

color_modern_choice = {
    5: "bs-yellow",
    6: "bs-pink",
    7: "bs-teal"
}

browser_list = {
    1: "chrome",
    2: "edge"
}

output_name = {
    'out_strain': 'strain_coeff.txt',
    'out_dw': 'DW_coeff.txt',
    'out_strain_profile': 'output_strain.txt',
    'out_dw_profile': 'output_DW.txt',
    'in_strain': 'input_strain_coeff.txt',
    'in_dw': 'input_DW_coeff.txt',
    'out_XRD': 'out_XRD_fit.txt',
    'export_strain': 'export_strain.txt',
    'export_DW': 'export_DW.txt',
    'export_Fit': 'export_XRD_Fit.txt'
}

example_list = [
    "YSZ",
    "SiC_3C",
    # "SiC_pv"
]

# Radmax.py path
application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Modules path (Paramters.py, calcul.py ...)
modules_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(modules_path, filename)
current_dir = os.path.dirname(abspath(config_path))

structures_name = os.path.join(current_dir, 'structures')
struc_factors = os.path.join(current_dir, 'f0f1f2')
log_file_path = os.path.join(current_dir, log_filename + ".log")
music_path = os.path.join(current_dir, 'sounds')
database_path = os.path.join(current_dir, 'database')

"""
Definition of the variables names used in the program
They are called by all modules
"""

value4rounddamaged = int(200)

value4StructureFactor = 12398

database_dict = [
    'engine',
    'session',
    'Name',
    'choice_state',
    'choice_combo',
    'date_1',
    'date_2'
]

headercolumnname = [
    "Date",
    "Exp name",
    "Crystal name",
    "Fit Algo",
    "Fit Success",
    "Residual",
    "Geometry",
    "Model"
]
databasename = [
    "date",
    "exp_name",
    "crys_name",
    "fit_algo",
    "fit_success",
    "residual",
    "geometry",
    "model"
]

asym_pv = [
    'heigt',
    'loc',
    'fwhm_1',
    'fwhm_2',
    'eta_1',
    'eta_2',
    'bkg'
]

FitAlgo_choice = [
    "GSA",
    "leastsq"
]

FitSuccess = [
    "Success",
    "Aborted"

]
FitFunction = [
    "Gaussian",
    "Lorentzian",
    "Pseudo-Voigt",
    "Generalized bell",
    "Split-PV"
]

FitFunction_choice = {
    0: f_Gauss,
    1: f_Lorentz,
    2: f_pVoigt,
    3: f_gbell,
    4: f_splitpV
}

limit_graph = {
    "ymin_strain": 0,
    "ymax_strain": 0,
    "ymin_dw": 0,
    "ymax_dw": 0,
    "xmin_strain": 0,
    "xmax_strain": 0,
    "xmin_dw": 0,
    "xmax_dw": 0,
    "xmin_xrd": 0,
    "xmax_xrd": 0
}

FitFunction_value = {
    'b_func': 2.,
    'resolr': 0.01,
    'shaper': 0.1
}

FitParamDefault = {
    'strain_eta_min': -0.5,
    'strain_eta_max': 1.5,
    'dw_eta_min': -0.5,
    'dw_eta_max': 1.5,
    'dw_height_min': 0.,
    'dw_height_max': 1.,
    'strain_height_min': 0.,
    'strain_height_max': 1.,
    'dw_bkg_min': 0.,
    'dw_bkg_max': 1.,
    'strain_bkg_min': 0.,
    'strain_bkg_max': 1.,
    'strain_min': 0.,
    'strain_max': 1.,
    'dw_min': 0.,
    'dw_max': 1.,
    'qa': 0.99,
    'qv': 2.6,
    'qt': 1.001,
    'xtol': 1.e-7,
    'ftol': 1.e-7,
    'maxfev': 2000,
    'c_strain': '#ffbf80',
    'c_dw': '#00e6ac',
    'c_data': '#3e95cd',
    'c_fit': '#9999ff',
    'c_fit_live': '#ff0000',
    'l_strain': 'dotted',
    'l_dw': 'dashed',
    'l_data': 'solid',
    'l_fit': 'solid',
    'l_fit_live': 'solid',
    'c_graph_background': '#FFFFFF',
    'use_database': 'False',
    'change_path_database': 'False',
    'path_to_database': 'None',
    'open_with_sound': 'True',
    'play_sounds': 'True',
    'theme': 0,
    'version': version,
    'last_modification': last_modification
}

DefaultParam4Radmax = [
    'version',
    'last_modification',
    'project_folder',
    'dw_folder',
    'strain_folder',
    'xrd_folder',
    'save_as_folder',
    'strain_eta_min',
    'strain_eta_max',
    'dw_eta_min',
    'dw_eta_max',
    'strain_height_min',
    'strain_height_max',
    'dw_height_min',
    'dw_height_max',
    'strain_bkg_min',
    'strain_bkg_max',
    'dw_bkg_min',
    'dw_bkg_max',
    'strain_min',
    'strain_max',
    'dw_min',
    'dw_max',
    'qa',
    'qv',
    'qt',
    'xtol',
    'ftol',
    'maxfev',
    'c_strain',
    'c_dw',
    'c_data',
    'c_fit',
    'c_fit_live',
    'l_strain',
    'l_dw',
    'l_data',
    'l_fit',
    'l_fit_live',
    'c_graph_background',
    'use_database',
    'change_path_database',
    'path_to_database',
    'open_with_sound',
    'play_sounds',
    'theme'
]

asym_pv_list = [
    'heigt_strain',
    'loc_strain',
    'fwhm_1_strain',
    'fwhm_2_strain',
    'strain_eta_1',
    'strain_eta_2',
    'bkg_strain',
    'heigt_dw',
    'loc_dw',
    'fwhm_1_dw',
    'fwhm_2_dw',
    'dw_eta_1',
    'dw_eta_2',
    'bkg_dw'
]

GSAp_ = [
    'strain_height_min',
    'strain_height_max',
    'strain_eta_min',
    'strain_eta_max',
    'strain_bkg_min',
    'strain_bkg_max',
    'dw_height_min',
    'dw_height_max',
    'dw_eta_min',
    'dw_eta_max',
    'dw_bkg_min',
    'dw_bkg_max'
]

Params4Radmax = [
    'sp',
    'dwp',
    'sp_pv',
    'dwp_pv',
    'sp_smooth',
    'dwp_smooth',
    'sp_abrupt',
    'dwp_abrupt',
    'data_xrd',
    'x_sp',
    'x_dwp',
    'Iobs',
    'Ical',
    'I_i',
    'I_fit',
    '_fp_min',
    'th',
    'th4live',
    'damaged_value_backup',
    't_l',
    'z',
    'depth',
    'thB_S',
    'g0',
    'gH',
    'b_S',
    'd',
    'G',
    'FH',
    'FmH',
    'F0',
    'Vol',
    'DW_multiplication',
    'strain_multiplication',
    'strain_basis_backup',
    'dw_basis_backup',
    'strain_sm_ab_bkp',
    'dw_sm_ab_bkp',
    'scale_strain',
    'scale_dw',
    'strain_i',
    'strain_shifted',
    'DW_i',
    'DW_shifted',
    'par', 'resol',
    'stain_out',
    'dw_out',
    'thB_S_s',
    'g0_s',
    'gH_s',
    'b_S_s',
    'd_s',
    'G_s',
    'FH_s',
    'FmH_s',
    'F0_s',
    'Vol_s',
    'state_sp',
    'state_dwp',
    'func_profile',
    'param_func_profile',
    'state_sp_backup',
    'state_dwp_backup',
    'strain_scat_x',
    'strain_scat_y',
    'dw_scat_x',
    'dw_scat_y',
    'strain_line_x',
    'strain_line_y',
    'dw_line_x',
    'dw_line_y',
    'control_sp_x',
    'control_dwp_x',
    'model_strain',
    'model_dw',
]

Bsplinesave = [
    "smooth",
    "abrupt",
    "pv"
]
Strain_DW_choice = [
    "B-splines smooth",
    "B-splines abrupt",
    "Asymmetric pv"
]
sample_geometry = [
    "Default",
    "Thin film",
    "Thick film",
    "Thick film + substrate"
]

# Initial Parameters panel
IP_p = [
    'wavelength',
    'background',
    'function_profile',
    'width_left',
    'width_right',
    'shape_left',
    'shape_right',
    'b_bell',
    'h',
    'k',
    'l',
    'crystal_symmetry',
    'exp_offset',
    'exclude_range',
    'model',
    'strain_basis_func',
    'dw_basis_func',
    'damaged_depth',
    'number_slices'
]

# Sample Geometry panel
SG_p = [
    'geometry',
    'film_thick',
    'dw_thick',
    'h_s',
    'k_s',
    'l_s',
    'crystal_symmetry_s'
]

# Fitting panel
F_p = [
    'tmax',
    'nb_cycle_max',
    'nb_palier'
]

# All Path
Path4Radmax = [
    'project_name',
    'path2ini',
    'path2inicomplete',
    'path2drx',
    'namefromini',
    'name4lmfit',
    'crystal_name',
    'substrate_name',
    'input_dw',
    'input_strain',
    'xrd_data'
]

FitData = [
    'checkFittingField',
    'checkGeometryField',
    'checkInitialField',
    'fit_type',
    'lmfit_install',
    'fit_params',
    'spline_strain',
    'spline_DW',
    'worker_live',
    'Leastsq_report',
    'New&Load',
    'list4DW'
]

# =============================================================================
# experimental file.ini section
# =============================================================================
Exp_file_section = [
    'Crystal',
    'Data files',
    'Experiment',
    'Material',
    'Strain and DW',
    'GSA options',
    'Bspline Bounds',
    'PV Bounds',
    'GSA expert',
    'Leastsq parameters',
    'Sample Geometry',
    'Substrate'
]
s_crystal = [
    'crystal_name',
    'substrate_name'
]
s_data_file = [
    'xrd_data'
]

s_experiment = [
    'wavelength',
    'background',
    'function_profile',
    'width_left',
    'width_right',
    'shape_left',
    'shape_right',
    'b_bell'
]

s_material = [
    'h',
    'k',
    'l',
    'crystal_symmetry',
    'exp_offset',
    'exclude_range'
]
s_material_bis = [
    'a',
    'b',
    'c',
    'alpha',
    'beta',
    'gamma',
    'a_s',
    'b_s',
    'c_s',
    'alpha_s',
    'beta_s',
    'gamma_s'
]
s_strain_DW = [
    'model',
    'strain_basis_func',
    'dw_basis_func',
    'damaged_depth',
    'number_slices'
]
s_GSA_options = [
    'tmax',
    'nb_cycle_max',
    'nb_palier'
]
s_bsplines = [
    'strain_min',
    'strain_max',
    'dw_min',
    'dw_max'
]
s_pv = [
    'strain_eta_min',
    'strain_eta_max',
    'dw_eta_min',
    'dw_eta_max',
    'strain_height_min',
    'strain_height_max',
    'dw_height_min',
    'dw_height_max',
    'strain_bkg_min',
    'strain_bkg_max',
    'dw_bkg_min',
    'dw_bkg_max'
]
s_GSA_expert = [
    'qa',
    'qv',
    'qt'
]
s_leastsq = [
    'xtol',
    'ftol',
    'maxfev'
]
s_geometry = [
    'geometry',
    'film_thick',
    'dw_thick'
]
s_substrate = [
    'h_s',
    'k_s',
    'l_s',
    'crystal_symmetry_s'
]

Exp_file_all_section = (
    s_crystal + s_data_file + s_experiment + s_material +
    s_strain_DW + s_GSA_options + s_bsplines + s_pv +
    s_GSA_expert + s_leastsq + s_geometry + s_substrate
)

# read from experiment file without check if value is a number or not
Exp_read_only = s_bsplines + s_pv + s_GSA_expert + s_leastsq

# =============================================================================
# Radmax.ini section
# =============================================================================
Radmax_File_section = [
    'RaDMax',
    'Folder Paths',
    'PV Bounds',
    'Bspline Bounds',
    'GSA expert',
    'Leastsq parameters',
    'Graph Options',
    'Database',
    'Sound',
    'Theme'
]
s_radmax_1 = [
    'version',
    'last_modification'
]
s_radmax_2 = [
    'project_folder',
    'dw_folder',
    'strain_folder',
    'xrd_folder',
    'save_as_folder',
]
s_radmax_3 = [
    'strain_eta_min',
    'strain_eta_max',
    'dw_eta_min',
    'dw_eta_max',
    'strain_height_min',
    'strain_height_max',
    'dw_height_min',
    'dw_height_max',
    'strain_bkg_min',
    'strain_bkg_max',
    'dw_bkg_min',
    'dw_bkg_max'
]
s_radmax_4 = [
    'strain_min',
    'strain_max',
    'dw_min',
    'dw_max'
]
s_radmax_5 = [
    'qa',
    'qv',
    'qt'
]
s_radmax_6 = [
    'xtol',
    'ftol',
    'maxfev'
]
s_radmax_7 = [
    'c_strain',
    'c_dw',
    'c_data',
    'c_fit',
    'c_fit_live',
    'l_strain',
    'l_dw',
    'l_data',
    'l_fit',
    'l_fit_live',
    'c_graph_background'
]
s_radmax_8 = [
    'use_database',
    'change_path_database',
    'path_to_database',
]
s_radmax_9 = [
    'open_with_sound',
    'play_sounds'
]
s_radmax_10 = [
    'theme'
]

Radmax_all_section = (s_radmax_1 + s_radmax_2 + s_radmax_3 + s_radmax_4 +
                      s_radmax_5 + s_radmax_6 + s_radmax_7 + s_radmax_8 +
                      s_radmax_9 + s_radmax_10)

Radmax_new_project = s_experiment + s_material + s_strain_DW + s_geometry + s_substrate + s_GSA_options

data_initial = [
    1.5406,
    5e-6,
    0,
    0.013,
    0.013,
    0.00001,
    0.00001,
    2,
    1,
    1,
    0,
    0,
    1,
    1,
    0,
    10,
    10,
    3500,
    70
]

sp_pv_initial = [
    2,
    0.2,
    0.1,
    0.1,
    0.1,
    0.1,
    0.05
]

dwp_pv_initial = [
    0.5,
    0.2,
    0.1,
    0.1,
    0.1,
    0.1,
    0.85
]

fitting_initial = [
    10,
    1000,
    10
]

geometry_initial = [
    0,
    6001,
    1,
    1,
    0,
    0,
    2,
    0
]


# -----------------------------------------------------------------------------
class P4Rm():
    """
    Parameters4Diff:
    All the variable passed and shared along the different module
    """

    """Parameters Panel"""
    ncolumnParam = len(Params4Radmax)*[""]
    ncolumnPath = len(Path4Radmax)*[""]
    ncolumnDefault = len(DefaultParam4Radmax)*[""]
    ncolumnAllData = len(Exp_file_all_section)*[""]
    ncolumnFit = len(FitData)*[0, 0, 0, "", False, "", "", "", None, "", 1]
    ncolumnDB = len(database_dict)*[None]
    ncolumnNewProject = len(Radmax_new_project)*[""]

    AllDataDict = dict(zip(Exp_file_all_section, ncolumnAllData))
    ParamDict = dict(zip(Params4Radmax, ncolumnParam))
    PathDict = dict(zip(Path4Radmax, ncolumnPath))
    DefaultDict = dict(zip(DefaultParam4Radmax, ncolumnDefault))
    FitDict = dict(zip(FitData, ncolumnFit))
    # NewProjectDict = OrderedDict(zip(Radmax_new_project, ncolumnNewProject))
    NewProjectDict = dict(zip(Radmax_new_project, data_initial + geometry_initial + fitting_initial))

    ConstDict = {
        're': 2.818*10**-5,
        'phi': 0,
        'phi_s': 0,
        'jump_scale': 0.00001
    }

    ParamDict['DW_multiplication'] = 1
    ParamDict['strain_multiplication'] = 1

    ParamDictbackup = dict(zip(Params4Radmax, ncolumnParam))

    Paramwindowtest = {
        'FitParametersPanel': "",
        'PseudoVoigtPanel': "",
        'BsplinePanel': ""
    }

    DBDict = dict(zip(database_dict, ncolumnDB))

    ProjectFileData = []
    initial_parameters = []
    fitting_parameters = []
    sample_geometry = []

    bounds_parameters = []
    database_list = ""
    list4live = []

    checkFittingField = 0
    checkGeometryField = 0
    checkInitialField = 0
    fit_type = ""
    lmfit_install = False
    fit_params = ""

    exclude_region = []

    crystal_list = ""

    spline_strain = ""
    spline_DW = ""

    log_window_status = ""

    gsa_loop = 0
    fitlive = 0
    residual_error = 0

    xrd_graph_loaded = 0
    shifted_strain = 0
    shifted_dw = 0

    zoomOn = 0

    from_Calc_Strain = 0
    from_Calc_DW = 0

    DragDrop_Strain_x = []
    DragDrop_Strain_y = []
    DragDrop_DW_x = []
    DragDrop_DW_y = []

    allparameters = []
    allparameters4save = []

    ChangeBasisFunction = []
    res_nearest_dw = []
    nearest_dw_change = 0
    change_model = 0

    xrd2graph = []

    splinenumber = []
    par_fit = []
    success = []
    resultFit = ""
    success4Fit = 0
    test_fit_aborted = 0
    modelPv = ""
    pathfromDB = 0
    db_nb_line = 100
    colorMenuItem = "#282a36"

    iobs_include_region = 0
