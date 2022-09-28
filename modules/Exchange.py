#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project web

import os
import sys
from random import randint
import shutil
import tkinter as tk

import Parameters as p4R
from Parameters import P4Rm
from Calcul import Calcul4Radmax
from Read import ReadFile, SaveFile
from Settings import Sound_Launcher, UpdateExampleFiles
from DataBase import DataBaseUse
from Fitting import Fitting4Radmax
import Tk_module as tkm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eel

a = P4Rm()
b = Calcul4Radmax()
c = DataBaseUse()
d = SaveFile()
f = ReadFile()
g = Fitting4Radmax()
h = UpdateExampleFiles()

# =============================================================================
# Definition of eel functions (needed to communicate with javascript files)
# =============================================================================

@eel.expose
def change_theme(val, change):
    manage_css_theme_files(int(val), change)

@eel.expose
def change_options_working(val):
    P4Rm.DefaultDict['use_database'] = val[0]
    P4Rm.DefaultDict['open_with_sound'] = val[1]
    P4Rm.DefaultDict['play_sounds'] = val[2]
    d.on_update_config_file_parameters()

@eel.expose
def handle_exit(ar1,ar2):
	sys.exit(0)

def close_callback(route, websockets):
    if not websockets:
        sys.exit()

@eel.expose
def scale_manual(data):
    b.scale_drx_graph(data)
    update_data_format()

def live_data_from_fit(data):
    if data:
        res = data[0]
        if res == "fit_running":
            # b.f_strain_DW(1)
            b.graph_controller_dwp(1)
            b.graph_controller_sp(1)
            tmp = ["update_strain_graph", a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
            tmp = ["update_dw_graph", a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
            p4R.xrd2graph = []
            for vv, tt in zip(a.ParamDict['th4live'], data[1]):
                tp = {
                    "x": vv,
                    "y": tt
                }
                p4R.xrd2graph.append(tp)
            tmp = ["update_xrd_fit", a.ParamDict['th4live'].tolist(), data[1].tolist(), p4R.xrd2graph]
            eel.data_graph_py(tmp)
            if len(data) == 6:
                tmp = ["gsa_running", data[5].tolist()]
                eel.update_gsa_counter(tmp)
                eel.update_gsa_counter(tmp)
        elif res == "fit_finished":
            fit_ended(data)

def fit_ended(data):
    g.on_fit_ending()
    finish_type = "fit_success"
    finish_type_num = 0
    if data[1] == 1:
        finish_type = "fit_aborted"
        finish_type_num = 1
    Sound_Launcher(finish_type_num, randint(0, 200))
    error = round(a.residual_error, 4)
    b.on_read_bounds()
    tmp = [finish_type, error, a.bounds_parameters]
    eel.result_from_fit(tmp)
    if a.DefaultDict['use_database']:
        c.on_fill_database_and_list(finish_type_num)
        tmp = ["Update_database", P4Rm.database_list, P4Rm.DBDict]
        eel.dataPyDB(tmp)
    d.on_save_from_fit()
    if a.pathfromDB == 1:
        P4Rm.pathfromDB = 0

@eel.expose                         # Expose this function to Javascript
def launch_worker():
    test = g.on_launch_thread(live_data_from_fit)
    if test == 0:
        eel.change_limit_input()
    elif test == 2:
        eel.save_project_js()

@eel.expose                         # Expose this function to Javascript
def stop_worker():
    g.on_stop_fit()

@eel.expose 
def update_change_limits(data):
    if data != "None":
        g.on_modify_deformation_limits(data)
        test = g.on_launch_thread(live_data_from_fit)
        if test == 0:
            eel.fit_goes_wrong()

@eel.expose                         # Expose this function to Javascript
def read_db_data(id):
    c.on_item_selected(id)
    b.on_load_from_Database()
    b.on_read_bounds()
    msg = "load_project_from_database"
    load_data_format(msg)

@eel.expose                         # Expose this function to Javascript
def delete_db_data(id):
    res = c.on_delete_selected(id)
    eel.res_from_delete(res)

@eel.expose
def load_DB_initialization():
    tmp = ["Loading_database", a.database_list, a.DBDict]
    eel.dataPyDB(tmp)

@eel.expose
def update_fitting_options(data):
    b.on_read_fitting_options(data)

@eel.expose
def drag_horizontaly(value, graph):
    # print(value, graph)
    if graph == "strain":
        b.update_strain_shift(value)
    else:
        b.update_dw_shift(value)
    b.on_read_bounds()
    update_data_format()

@eel.expose
def update_project(data):
    # print('##################################################')
    # print('Update')
    # print(data)
    # print('##################################################')
    if a.PathDict['xrd_data'] != '':
        res = b.on_update(data)
        if res:
            b.on_read_bounds()
            update_data_format()
        else:
            eel.change_basis_functions(1)

def update_data_format():
    tmp = ["update", a.crystal_list, a.DefaultDict, a.AllDataDict, a.ChangeBasisFunction, a.bounds_parameters]
    # print(tmp)
    eel.data_from_py(tmp)
    tmp = ["update_xrd", a.ParamDict['th4live'].tolist(), a.ParamDict['I_i'].tolist(), p4R.xrd2graph, p4R.limit_graph]
    eel.data_graph_py(tmp)
    tmp = ["update_strain_graph", a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
    eel.data_graph_py(tmp)
    tmp = ["update_dw_graph", a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
    eel.data_graph_py(tmp)
    # tmp = ["update_strain_graph", a.ParamDict['x_sp'].tolist(), a.ParamDict['strain_shifted'].tolist(), p4R.limit_graph]
    # eel.data_graph_py(tmp)
    # tmp = ["update_dw_graph", a.ParamDict['x_dwp'].tolist(), a.ParamDict['DW_shifted'].tolist(), p4R.limit_graph]
    # eel.data_graph_py(tmp)

@eel.expose
def update_sp_dwp_table(data):
    b.read_sp_dwp_from_table(data)
    b.calc_f_Refl()
    b.on_read_bounds()
    tmp = ["update_xrd", a.ParamDict['th4live'].tolist(), a.ParamDict['I_i'].tolist(), p4R.xrd2graph, p4R.limit_graph]
    eel.data_graph_py(tmp)
    tmp = ["update_bounds_table", a.bounds_parameters]
    eel.update_bounds_table(tmp)
    if data[0] == "DW":
        tmp = ["update_dw_graph", a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
        eel.data_graph_py(tmp)
    else:
        tmp = ["update_strain_graph", a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
        eel.data_graph_py(tmp)

@eel.expose
def load_project(msg, path):
    if msg == "load_project_from_main":
        b.on_load_project(path)
        b.on_read_bounds()
        load_data_format("load_project")
    elif msg == "load_project_web":
        root = tk.Tk()
        path = tkm.open_selected_file("Load project", a.DefaultDict['project_folder'])
        root.update()
        root.destroy()
        if path != "":
            b.on_load_project([path])
            b.on_read_bounds()
            load_data_format("load_project")

def load_data_format(msg):
    # load data to interface
    tmp = [msg, a.crystal_list, a.DefaultDict, a.AllDataDict, a.ChangeBasisFunction, a.bounds_parameters, a.PathDict['project_name']]
    eel.data_from_py(tmp)
    tmp = [os.path.splitext(os.path.basename(a.PathDict['project_name']))[0], os.path.dirname(a.PathDict['path2inicomplete'])]
    # tmp = [os.path.splitext(os.path.basename(a.DefaultDict['project_folder']))[0], os.path.dirname(a.DefaultDict['project_folder'])]
    eel.change_api_title(tmp)
    # load xrd graph
    p4R.xrd2graph = []
    for vv, tt in zip(a.ParamDict['th4live'], a.ParamDict['Iobs']):
        tp = {
            "x": vv,
            "y": tt
        }
        p4R.xrd2graph.append(tp)
    tmp = ["load_xrd", a.ParamDict['th4live'].tolist(), a.ParamDict['Iobs'].tolist(), p4R.xrd2graph, p4R.limit_graph]
    eel.data_graph_py(tmp)
    # load strain graph
    tmp = ["load_strain_from_main", a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
    eel.data_graph_py(tmp)
    # load DW graph
    tmp = ["load_dw_from_main", a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
    eel.data_graph_py(tmp)
    # print("a.ParamDict", a.ParamDict)
    # print("a.DefaultDict", a.DefaultDict)
    # print("a.AllDataDict", a.AllDataDict)
    # print("a.PathDict", a.PathDict)

@eel.expose
def data_ask(msg):
    if msg == "initialization":
        tmp = [msg, a.crystal_list, a.DefaultDict, a.NewProjectDict, a.ChangeBasisFunction, a.bounds_parameters]
        eel.data_from_py(tmp)()
    elif msg == "new_project":
        b.on_new_project()
        b.on_read_bounds()
        tmp = [msg, a.crystal_list, a.DefaultDict, a.NewProjectDict, a.ChangeBasisFunction, a.bounds_parameters]
        # eel.data_from_py(tmp)()
        eel.data_from_py(tmp)
        # load strain graph
        tmp = ["load_strain_from_main", a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
        eel.data_graph_py(tmp)
        # load DW graph
        tmp = ["load_dw_from_main", a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
        eel.data_graph_py(tmp)

@eel.expose
def load_graph(msg, path):
    if msg == "load_xrd_from_main":
        test = b.calc_XRD(path)
        if test:
            p4R.xrd2graph = []
            for vv, tt in zip(a.ParamDict['th4live'], a.ParamDict['Iobs']):
                tp = {
                    "x": vv,
                    "y": tt
                }
                p4R.xrd2graph.append(tp)
            tmp = [msg, a.ParamDict['th4live'].tolist(), a.ParamDict['Iobs'].tolist(), p4R.xrd2graph, p4R.limit_graph]
            eel.data_graph_py(tmp)
        else:
            eel.check_input_file()
    elif msg == "load_xrd_web":
        root = tk.Tk()
        path = tkm.open_selected_file("Load XRD file", a.DefaultDict['project_folder'])
        root.update()
        root.destroy()
        test = b.calc_XRD([path])
        if test:
            p4R.xrd2graph = []
            for vv, tt in zip(a.ParamDict['th4live'], a.ParamDict['Iobs']):
                tp = {
                    "x": vv,
                    "y": tt
                }
                p4R.xrd2graph.append(tp)
            tmp = ["load_xrd", a.ParamDict['th4live'].tolist(), a.ParamDict['Iobs'].tolist(), p4R.xrd2graph, p4R.limit_graph]
            eel.data_graph_py(tmp)
        else:
            eel.check_input_file()

    elif msg == "load_strain_from_main":
        test = b.calc_strain(path, 0)
        if test:
            tmp = [msg, a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
        else:
            eel.check_input_file()
    elif msg == "load_strain_web":
        root = tk.Tk()
        path = tkm.open_selected_file("Load Strain file", a.DefaultDict['project_folder'])
        root.update()
        root.destroy()
        test = b.calc_strain(path, 0)
        if test:
            tmp = [msg, a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
        else:
            eel.check_input_file()

    elif msg == "load_dw_from_main":
        test = b.calc_DW(path, 0)
        if test:
            tmp = [msg, a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
        else:
            eel.check_input_file()
    elif msg == "load_dw_web":
        root = tk.Tk()
        path = tkm.open_selected_file("Load DW file", a.DefaultDict['project_folder'])
        root.update()
        root.destroy()
        test = b.calc_DW(path, 0)
        if test:
            tmp = ["load_dw_from_main", a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
        else:
            eel.check_input_file()


# Expose this function to Javascript
@eel.expose
def save_project(case, path):
    if a.PathDict['xrd_data'] != '':
        if a.PathDict['path2ini'] == '':
            case = 1
            path = 0
        if case == 1:
            if path == 0:
                root = tk.Tk()
                path = tkm.save_project_file("Save project", a.DefaultDict['project_folder'])
                root.update()
                root.destroy()
                # print(path)
                if path != "":
                    new_dir_name = d.on_save_project(case, path)
            else:
                new_dir_name = d.on_save_project(case, path)
            tmp = [new_dir_name, a.DefaultDict['project_folder']]
            # tmp = [new_dir_name, os.path.dirname(a.DefaultDict['project_folder'])]
            eel.change_api_title(tmp)
        else:
            new_dir_name = d.on_save_project(case, path)
            if not new_dir_name:
                eel.directory_no_longer_exist(a.PathDict['path2ini'])
            else:
                eel.change_api_title(new_dir_name)
                tmp = [new_dir_name, a.DefaultDict['project_folder']]
                # tmp = [new_dir_name, os.path.dirname(a.DefaultDict['project_folder'])]
                eel.change_api_title(tmp)
    else:
        eel.load_xrd_before_save_project()


# Expose this function to Javascript
@eel.expose
def on_export_data():
    if (a.ParamDict['strain_i'] == "" or
            a.ParamDict['DW_i'] == "" or
                a.ParamDict['I_i'] == ""):
        eel.export_fit_not_working()
    else:
        d.on_export_data()

# Expose this function to Javascript
@eel.expose
def update_graph_colors(val, data):
    if val == 0:
        for key in data.keys():
            a.DefaultDict[key] = data[key]
            d.on_update_config_file_parameters()
    else:
        for key in data.keys():
            a.DefaultDict[key] = p4R.FitParamDefault[key]
            d.on_update_config_file_parameters()
    update_data_format()

def manage_index_html_header(connexion):
    import re
    current_file = p4R.application_path
    current_path = os.path.join(current_file, 'web', 'index.html')
    with open(current_path, 'r') as file :
        indexHeader = file.read()
    indexHeaderExtract = re.findall(r'<head>([\s\S]+?)</head>', indexHeader)[0]
    if connexion == 0:
        connected_path = os.path.join(current_file, 'web', 'head_connected.html')
        with open(connected_path, 'r') as fileConnected :
            FileHeader = fileConnected.read()
    else:
        offline_path = os.path.join(current_file, 'web', 'head_offline.html')
        with open(offline_path, 'r') as fileOffline :
            FileHeader = fileOffline.read()
    FileHeaderExtract = re.findall(r'<head>([\s\S]+?)</head>', FileHeader)[0]
    # replace
    Replace = indexHeader.replace(indexHeaderExtract, FileHeaderExtract)
    with open(current_path, 'w') as file :
        file.write(Replace)

def manage_css_theme_files(theme, change):
    current_file = p4R.application_path
    choice_path = p4R.theme_choice[theme]
    old_name = os.path.join(current_file, 'web/css/', choice_path)
    new_name = os.path.join(current_file, 'web/css/boostrap.min.css')
    shutil.copy(old_name, new_name)

    choice_path = p4R.table_theme_choice[theme]
    old_name = os.path.join(current_file, 'web/modules/plug_in/tabulator/css/', choice_path)
    new_name = os.path.join(current_file, 'web/modules/plug_in/tabulator/css/tabulator_read.min.css')
    if theme > 4:
        with open(old_name, 'r') as file :
            filedata = file.read()
        newdata = filedata.replace("text-color", p4R.color_modern_choice[theme])
        with open(new_name, 'w') as file:
            file.write(newdata)
    else:
        shutil.copy(old_name, new_name)
    
    P4Rm.DefaultDict['theme'] = theme
    if change == 1:
        d.on_update_config_file_parameters()


def connect(host='http://google.com'):
    import urllib.request
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False


####################################################################################################################################################
# --------------------------------------------------------------------------------------------------------------------------------------------------
class Main():
    def __init__(self, parent, net_connected, browser_choice):
        self.net_connected = net_connected
        self.browser_choice = browser_choice

        if not connect():
            self.net_connected = 1
        manage_index_html_header(self.net_connected)

        if self.net_connected == 0:
            eel.init(
                'web',
                excludes_dir=['package']
            )
        else:
            eel.init('web')
        # self.read_init_file()
        eel.spawn(self.read_init_file())
        if self.browser_choice != 4:
            if self.browser_choice == 3:
                eel.start(
                    'main.js',
                    mode='custom',
                    cmdline_args=['C:/Users/souilp01/node_modules/electron/dist/electron.exe', '.'],
                    port=8000
                )
            else:
                browser = p4R.browser_list[self.browser_choice]
                eel.start(
                    'index.html',
                    mode=browser,
                    port=8000,
                    # cmdline_args=[
                    #     # '--start-fullscreen',
                    # ]
                )
        else:
            sys.exit()

    def read_init_file(self):
        P4Rm.lmfit_install = True
        test_ini = f.on_read_init_parameters(
            os.path.join(
                p4R.current_dir,
                p4R.filename + '.ini'
            ),
            p4R.RadmaxFile
        )
        if test_ini:
            h.on_update_example(p4R.application_path)
            eel.sleep(0.5)
            self.read_init_file()
        else:
            config_File_extraction = f.read_result_value()
            for k, v in a.DefaultDict.items():
                P4Rm.DefaultDict[k] = config_File_extraction[k]
            for k, v in p4R.FitParamDefault.items():
                if k == 'maxfev' or k == 'theme':
                    P4Rm.DefaultDict[k] = int(float(a.DefaultDict[k]))
                elif k in p4R.s_radmax_7:
                    P4Rm.DefaultDict[k] = a.DefaultDict[k]
                elif k in p4R.s_radmax_8 or k in p4R.s_radmax_9:
                    if a.DefaultDict[k] == 'True':
                        P4Rm.DefaultDict[k] = True
                    else:
                        P4Rm.DefaultDict[k] = False
                elif k == 'version':
                    P4Rm.DefaultDict[k] = p4R.version
                elif k == 'last_modification':
                    P4Rm.DefaultDict[k] = p4R.last_modification
                else:
                    P4Rm.DefaultDict[k] = float(a.DefaultDict[k])
            tmp = ["browser_choice", self.browser_choice]
            eel.browser(tmp)

            manage_css_theme_files(a.DefaultDict['theme'], 0)
            eel.manage_database_using(a.DefaultDict['use_database'])

            P4Rm.PathDict['path_to_database'] = config_File_extraction['path_to_database']

            if os.listdir(p4R.structures_name):
                tmp = [os.path.splitext(filename)[0] for filename in os.listdir(p4R.structures_name)]
                P4Rm.crystal_list = sorted(tmp)
            if P4Rm.DefaultDict['open_with_sound']:
                load_random_voice = randint(0, 3)
                Sound_Launcher(2, load_random_voice)
            b.on_init_dictionnaries()
            b.on_new_project()
            b.on_read_bounds()
            res_from_db = c.initialize_database()
            c.on_read_part_DB()

            # print('before_eel ', end - start)
            # eel.browser(self.browser_choice)
            tmp = ["initialization", a.crystal_list, a.DefaultDict, a.NewProjectDict, a.ChangeBasisFunction, a.bounds_parameters]
            eel.data_from_py(tmp)
            tmp = ["load_strain_from_main", a.ParamDict['strain_scat'], a.ParamDict['strain_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
            tmp = ["load_dw_from_main", a.ParamDict['dw_scat'], a.ParamDict['dw_line'], p4R.limit_graph]
            eel.data_graph_py(tmp)
            tmp = ["Loading_database", a.database_list, a.DBDict]
            eel.dataPyDB(tmp)

            # if not res_from_db:
            #     change_path_db_choice()

