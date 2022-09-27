#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

# =============================================================================
# Radmax read module
# =============================================================================

import os
from sys import exit
from sys import platform as _platform

import Parameters as p4R
from Parameters import P4Rm

try:
    from ConfigParser import SafeConfigParser, MissingSectionHeaderError
except (ImportError):
    from configparser import SafeConfigParser, MissingSectionHeaderError

from numpy import savetxt, loadtxt, column_stack, pi

import logging
logger = logging.getLogger(__name__)

read_ini_files = {}
lecture_fichier = []
result_values = []

a = P4Rm()

# -----------------------------------------------------------------------------
class ReadFile():
    """
    Reading '.ini' project
    Test if the config file has the waiting structure
    if not, the project can't be launch, and a warning is write in the log file
    """
    def __init__(self):
        self.section_name = []
        self.structure_section = []
        self.read_ini_files = {}

    def on_read_init_parameters(self, filename, choice):
        self.read_ini_files = {}
        if choice == 'RadmaxFile':
            self.section_name = p4R.Radmax_all_section
            self.structure_section = p4R.Radmax_File_section
        elif choice == 'ExperimentFile':
            self.section_name = p4R.Exp_file_all_section
            self.structure_section = p4R.Exp_file_section
        if not os.path.exists(filename):
            _msg = "! Pay attention, the config file does not exist: "
            logger.log(logging.WARNING, _msg + str(filename))
            if choice == 'RadmaxFile':
                _msg = "Making of the config file with initial parameters"
                logger.log(logging.WARNING, _msg + str(filename))
                d = SaveFile()
                d.on_makingof_config_file(filename)
                return True
        else:
            result_values[:] = []
            _msg = "Trying to load the following config file: "
            logger.log(logging.INFO, _msg + str(filename))
            # if choice == 'ExperimentFile':
                # self.test_data_file(filename)
            self.test_existence_section(filename)
            return False

    def test_existence_section(self, filename):
        test_true_false = []
        parser = SafeConfigParser(allow_no_value=True)
        try:
            parser.read(filename)
        except MissingSectionHeaderError:
            print(
                "\n! Config file structure is not correct," +
                "please check your config file !!"
            )
            exit(1)
        for nameofsection in self.structure_section:
            var = parser.has_section(nameofsection)
            test_true_false.append(var)
        indices_section = self.all_indices(False, test_true_false)
        if indices_section != []:
            print(
                "\n! Check your config file! " +
                "The following sections are not being present:"
            )
            for char in indices_section:
                print(self.structure_section[char])
        else:
            self.test_existence_option(filename, self.section_name)

    def test_existence_option(self, filename, section_name):
        test_true_false = []
        parser = SafeConfigParser(allow_no_value=True)
        parser.read(filename)
        lecture_fichier[:] = []
        for nameofsection in self.structure_section:
            for name, value in parser.items(nameofsection):
                var = name
                test_true_false.append(var)
        difference = self.diff(section_name, test_true_false)
        result =  all(elem in difference  for elem in p4R.s_material_bis)
        tt = False
        if difference == []:
            tt = True
        elif result:
            tt = True
        if tt:
            for nameofsection in parser.sections():
                for name, value in parser.items(nameofsection):
                    var = parser.get(nameofsection, name)
                    self.read_ini_files[name] = 0
                    lecture_fichier.append(var)
            self.test_existence_value(filename, section_name)
        else:
            print(
                "\n! Check your config file! " +
                "The following options are not being present:"
            )
            for chare in difference:
                print(chare)

    def test_existence_value(self, filename, section_name):
        parser = SafeConfigParser(allow_no_value=True)
        parser.read(filename)
        nulle = self.all_indices('', lecture_fichier)
        if nulle == []:
            for nameofsection in parser.sections():
                for name, value in parser.items(nameofsection):
                    var = parser.get(nameofsection, name)
                    self.read_ini_files[name] = var
                    result_values.append(var)
        else:
            print(
                "\n! Check your config file!" +
                "The following values are not being present:"
            )
            logger.log(logging.WARNING, "Check your config file!")
            logger.log(logging.WARNING, "Value of option section are" +
                       "not being present:")
            for chare in nulle:
                print (section_name[chare])
                logger.log(
                    logging.ERROR, "Missing data from: " + str(section_name[chare])
                )

    def read_result_value(self):
        if result_values != []:
            return self.read_ini_files

    def all_indices(self, value, qlist):
        """
        return indice of list containing identical value
        """
        indices = []
        idx = -1
        while True:
            try:
                idx = qlist.index(value, idx+1)
                indices.append(idx)
            except ValueError:
                break
        return indices

    def diff(self, a, b):
        """
        return difference between 2 list
        """
        b = set(b)
        return [aa for aa in a if aa not in b]

    def test_data_file(self, name):
        with open(name, 'r') as f:
            skip_line = 11
            [next(f) for x in range(skip_line)]
            header = next(f)
            mline = ""
            for i in header:
                mline += i
            ll = mline.split()
            if ll == []:
                self.convert_Data_File(name)
            else:
                if ll[0] == 'background':
                    return 0
                else:
                    self.convert_Data_File(name)

    def nonblank_lines(self, f):
        for l in f:
            line = l.rstrip()
            if line:
                yield line

    def convert_Data_File(self, name):
        print('tteasssst')
        ll_0 = []
        ll_1 = []
        a = P4Rm()
        with open(name, 'r') as f:
            for line in self.nonblank_lines(f):
                if line[0] != '[':
                    ll = line.split(' = ')
                    ll_0.append(ll[0])
                    ll_1.append(ll[1])
        i = 0
        P4Rm.AllDataDict['model'] = 0.0
        P4Rm.AllDataDict['function_profile'] = 2.0
        for k in ll_0:
            P4Rm.AllDataDict[k] = ll_1[i]
            i += 1
        P4Rm.AllDataDict['substrate_name'] = a.AllDataDict['crystal_name']
        for k in p4R.s_radmax_3 + p4R.s_radmax_4 + p4R.s_radmax_5:
            P4Rm.AllDataDict[k] = p4R.FitParamDefault[k]
        data_path = os.path.split(name)[0]
        data_file_name = os.path.splitext(os.path.basename(name))[0]
        data_name = os.path.join(data_path, data_file_name + '.ini')
        P4Rm.PathDict['path2inicomplete'] = data_name
        b = SaveFile()
        b.save_project(1)
        return 0

# -----------------------------------------------------------------------------
    """
    Read method for XRD, Strain and DW files
    """
    def read_dw_file(self, filename):
        """
        Opening file containing the experimental data
        """
        logger.log(
            logging.INFO,
            "Reading experimental data file: " + filename
        )
        try:
            tmp_loading = loadtxt(filename, unpack=True)
            if len(tmp_loading) == 2:
                P4Rm.ParamDict['dwp'] = tmp_loading[0]
                P4Rm.ParamDict['state_dwp'] = [True if val == 1.0 else False for val in tmp_loading[1]]
            else:
                P4Rm.ParamDict['dwp'] = tmp_loading
                P4Rm.ParamDict['state_dwp'] = len(tmp_loading)*[True]
            return 0
        except (IOError):
            logger.log(
                logging.ERROR,
                "!!! .txt data file is not present !!!"
            )
        except (IndexError):
            logger.log(
                logging.ERROR,
                "!!! The number of columns in the file is not correct !!!"
            )

    def read_strain_file(self, filename):
        """
        Opening file containing the experimental data
        """
        logger.log(
            logging.INFO,
            "Reading experimental data file: " + filename
        )
        try:
            tmp_loading = loadtxt(filename, unpack=True)
            if len(tmp_loading) == 2:
                P4Rm.ParamDict['sp'] = tmp_loading[0]
                P4Rm.ParamDict['state_sp'] = [True if val == 1.0 else False for val in tmp_loading[1]]
            else:
                P4Rm.ParamDict['sp'] = tmp_loading
                P4Rm.ParamDict['state_sp'] = len(tmp_loading)*[True]
            return 0
        except (IOError):
            logger.log(
                logging.ERROR,
                "!!! .txt data file is not present !!!"
            )
        except (IndexError):
            logger.log(
                logging.ERROR,
                "!!! The number of columns in the file is not correct !!!"
            )

    def read_dw_xy_file(self, filename):
        """
        Opening file containing the experimental data
        """
        logger.log(
            logging.INFO,
            "Reading experimental data file: " + filename
        )
        try:
            data = loadtxt(filename, unpack=True)
            return [True, data]
        except (IOError):
            logger.log(
                logging.ERROR,
                "!!! .txt data file is not present !!!"
            )
            return [False]
        except (IndexError, ValueError):
            logger.log(
                logging.ERROR,
                "!!! The number of columns in the file is not correct !!!"
            )
            return [False]

    def read_strain_xy_file(self, filename):
        """
        Opening file containing the experimental data
        """
        logger.log(
            logging.INFO,
            "Reading experimental data file: " + filename
        )
        try:
            data = loadtxt(filename, unpack=True)
            return [True, data]
        except (IOError):
            logger.log(
                logging.ERROR,
                "!!! .txt data file is not present !!!"
            )
            return [False]
        except (IndexError, ValueError):
            logger.log(
                logging.ERROR,
                "!!! The number of columns in the file is not correct !!!"
            )
            return [False]

    def read_xrd_file(self, filename):
        """
        Opening file containing the experimental data
        """
        logger.log(
            logging.INFO,
            "Reading experimental data file: " + filename
        )
        try:
            P4Rm.ParamDict['data_xrd'] = loadtxt(filename, unpack=True)
            return True
        except (IOError):
            logger.log(
                logging.ERROR,
                "!!! .txt data file is not present !!!"
            )
            return False
        except (IndexError, ValueError):
            logger.log(
                logging.ERROR,
                "!!! The number of columns in the file is not correct !!!"
            )
            return False


# -----------------------------------------------------------------------------
class SaveFile():
    """
    Save the project in a '.ini' file
    several method are available, create a new file, update an existing file
    or making the 'RaDMax.ini' config file
    """

    def save_project(self, case):
        nunberofdatapersection = [
            0, 
            len(p4R.s_crystal),
            len(p4R.s_data_file),
            len(p4R.s_experiment),
            len(p4R.s_material),
            len(p4R.s_strain_DW),
            len(p4R.s_GSA_options),
            len(p4R.s_bsplines),
            len(p4R.s_pv),
            len(p4R.s_GSA_expert),
            len(p4R.s_leastsq),
            len(p4R.s_geometry),
            len(p4R.s_substrate)
        ]
        filename = a.PathDict['path2inicomplete']
        parser = SafeConfigParser()
        if case == 0:
            parser.read(filename)
        new_section_name = p4R.Exp_file_all_section
        for i in range(len(p4R.Exp_file_section)):
            if case == 1:
                parser.add_section(p4R.Exp_file_section[i])
            k = nunberofdatapersection[i]
            r = nunberofdatapersection[i+1]
            new_section_name = new_section_name[k:]
            for l in range(r):
                parser.set(
                    p4R.Exp_file_section[i],
                    new_section_name[l],
                    str(a.AllDataDict[new_section_name[l]])
                )
        parser.write(open(filename, 'w'))

    def on_update_config_file(self, filename, data, sequence):
        parser = SafeConfigParser()
        parser.read(filename)
        if sequence == 'project_folder':
            parser.set(
                p4R.Radmax_File_section[1],
                p4R.s_radmax_2[0],
                data
            )
        elif sequence == 'dw_folder':
            parser.set(
                p4R.Radmax_File_section[1],
                p4R.s_radmax_2[1],
                data
            )
        elif sequence == 'strain_folder':
            parser.set(
                p4R.Radmax_File_section[1],
                p4R.s_radmax_2[2],
                data
            )
        elif sequence == 'xrd_folder':
            parser.set(
                p4R.Radmax_File_section[1],
                p4R.s_radmax_2[3],
                data
            )
        elif sequence == 'save_as_folder':
            parser.set(
                p4R.Radmax_File_section[1],
                p4R.s_radmax_2[4],
                data
            )
        parser.write(open(filename, 'w'))

    def on_makingof_config_file(self, filename):
        nunberofdatapersection = [
            0, 
            len(p4R.s_radmax_1),
            len(p4R.s_radmax_2),
            len(p4R.s_radmax_3),
            len(p4R.s_radmax_4),
            len(p4R.s_radmax_5),
            len(p4R.s_radmax_6),
            len(p4R.s_radmax_7),
            len(p4R.s_radmax_8),
            len(p4R.s_radmax_9),
            len(p4R.s_radmax_10)
        ]
        pathini = [os.path.split(filename)[0]]*5
        data2ini = [p4R.version, p4R.last_modification] + pathini
        parser = SafeConfigParser()
        new_section_name = p4R.Radmax_all_section
        Initial_data = dict(zip(p4R.Radmax_all_section, data2ini))
        Initial_data.update(p4R.FitParamDefault)
        for i in range(len(p4R.Radmax_File_section)):
            parser.add_section(p4R.Radmax_File_section[i])
            k = nunberofdatapersection[i]
            r = nunberofdatapersection[i+1]
            new_section_name = new_section_name[k:]
            for l in range(r):
                parser.set(
                    p4R.Radmax_File_section[i],
                    new_section_name[l],
                    str(Initial_data[new_section_name[l]])
                )
        parser.write(open(filename, 'w'))
        b = ReadFile()
        b.on_read_init_parameters(
            os.path.join(p4R.current_dir, filename),
            p4R.RadmaxFile
        )

    def on_update_config_file_parameters(self):
        filename = os.path.join(p4R.modules_path, 'Radmax.ini')
        parser = SafeConfigParser()
        parser.read(filename)
        for name in p4R.s_radmax_3:
            parser.set(
                p4R.Radmax_File_section[2],
                name,
                str(a.DefaultDict[name])
            )
        for name in p4R.s_radmax_4:
            parser.set(
                p4R.Radmax_File_section[3],
                name,
                str(a.DefaultDict[name])
            )
        for name in p4R.s_radmax_5:
            parser.set(
                p4R.Radmax_File_section[4],
                name,
                str(a.DefaultDict[name])
            )
        for name in p4R.s_radmax_6:
            parser.set(
                p4R.Radmax_File_section[5],
                name,
                str(a.DefaultDict[name])
            )
        for name in p4R.s_radmax_7:
            parser.set(
                p4R.Radmax_File_section[6],
                name,
                str(a.DefaultDict[name])
            )
        for name in p4R.s_radmax_8:
            parser.set(
                p4R.Radmax_File_section[7],
                name,
                str(a.DefaultDict[name])
            )
        for name in p4R.s_radmax_9:
            parser.set(
                p4R.Radmax_File_section[8],
                name,
                str(a.DefaultDict[name])
            )
        for name in p4R.s_radmax_10:
            parser.set(
                p4R.Radmax_File_section[9],
                name,
                str(a.DefaultDict[name])
            )
        parser.write(open(filename, 'w'))

    def save_deformation(self, case, name, data, supp=None):
        if a.PathDict['project_name'] == "":
            name_ = name + '_coeff.txt'
            path = os.path.join(a.PathDict['path2ini'], name_)
        else:
            name_ = name + '_coeff.txt'
            path = os.path.join(a.PathDict['path2ini'], name_)
            if supp == 1:
                name_ = name + '_coeff.txt'
                path2remove = os.path.join(a.PathDict['path2ini'], name_)
                if os.path.isfile(path2remove):
                    os.remove(path2remove)
        savetxt(path, data, fmt='%10.8f')

    def save_drx(self, case):
        name = a.PathDict['project_name'] + '.txt'
        path = os.path.join(a.DefaultDict['save_as_folder'], name)
        data = column_stack(
            (2*a.ParamDict['th']*180/pi, a.ParamDict['Iobs'])
        )
        savetxt(path, data, fmt='%10.8f')

    def on_save_project(self, case, path=None):
        """
        Saving project, save or save as depending of the action
        """
        if a.PathDict['input_dw'] != "" or a.PathDict['input_strain'] != "" or a.PathDict['xrd_data'] != "":
            if case == 1:
                save_path = os.path.split(path)[0]
                basename_file = "config.ini"
                # basename_file = os.path.splitext(os.path.basename(path))[0]
                P4Rm.DefaultDict['project_folder'] = path
                P4Rm.DefaultDict['save_as_folder'] = save_path
                self.on_update_config_file(
                    os.path.join(
                        p4R.current_dir,
                        p4R.filename + '.ini'
                    ),
                    save_path,
                    'save_as_folder'
                )
                P4Rm.PathDict['path2ini'] = path
                # if _platform == "linux" or _platform == "linux2":
                #     P4Rm.PathDict['path2inicomplete'] = os.path.join(save_path, basename_file)
                # elif _platform == "win32":
                #     P4Rm.PathDict['path2inicomplete'] = path
                P4Rm.PathDict['path2inicomplete'] = os.path.join(path, basename_file)
                P4Rm.PathDict['namefromini'] = basename_file
            else:
                basename_file = a.PathDict['namefromini']

            isFile = os.path.isdir(a.PathDict['path2ini'])
            if isFile:
                P4Rm.PathDict['project_name'] = os.path.splitext(os.path.basename(path))[0]
                # P4Rm.PathDict['project_name'] = a.PathDict['namefromini']
                self.save_deformation(
                    'input_strain',
                    'strain',
                    a.ParamDict['sp'],
                    1
                )
                self.save_deformation(
                    'input_dw',
                    'DW',
                    a.ParamDict['dwp'],
                    1
                )
                if a.pathfromDB == 1:
                    self.save_drx('xrd_data')

                P4Rm.AllDataDict['crystal_name'] = a.PathDict['crystal_name']
                P4Rm.AllDataDict['substrate_name'] = a.PathDict['substrate_name']
                P4Rm.AllDataDict['input_dw'] = a.PathDict['input_dw']
                P4Rm.AllDataDict['input_strain'] = a.PathDict['input_strain']
                P4Rm.AllDataDict['xrd_data'] = a.PathDict['xrd_data']
                self.save_project(case)

                msg = "Data have been saved to " + a.PathDict['namefromini']
                logger.log(
                    logging.INFO,
                    msg
                )

                return os.path.splitext(os.path.basename(a.PathDict['path2ini']))[0]
            else:
                return False

    def on_save_from_fit(self):
        if a.PathDict['path2ini'] != '':
            path = a.PathDict['path2ini']
        else:
            path = a.PathDict['path2drx']
        try:
            header = ["2theta", "Iobs", "Icalc"]
            line = u'{:^12} {:^24} {:^12}'.format(*header)

            # -----------------------------------------------------------------
            name_ = p4R.output_name['out_strain_profile']
            # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['out_strain_profile']
            data_ = column_stack(
                (
                    a.ParamDict['depth'],
                    a.ParamDict['strain_i']
                )
            )
            savetxt(
                os.path.join(path, name_),
                data_,
                fmt='%10.8f'
            )
            # -----------------------------------------------------------------
            name_ = p4R.output_name['out_dw_profile']
            # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['out_dw_profile']
            data_ = column_stack(
                (
                    a.ParamDict['depth'],
                    a.ParamDict['DW_i']
                )
            )
            savetxt(
                os.path.join(path, name_),
                data_,
                fmt='%10.8f'
            )
            # -----------------------------------------------------------------
            if a.par_fit == []:
                # -------------------------------------------------------------
                name_ = p4R.output_name['out_strain']
                # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['out_strain']
                data_ = a.ParamDict['sp']
                savetxt(
                    os.path.join(path, name_), 
                    data_,
                    fmt='%10.8f'
                )
                # -------------------------------------------------------------
                name_ = p4R.output_name['out_dw']
                # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['out_dw']
                data_ = a.ParamDict['dwp']
                savetxt(
                    os.path.join(path, name_),
                    data_,
                    fmt='%10.8f'
                )
            else:
                # -------------------------------------------------------------
                name_ = p4R.output_name['in_strain']
                # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['in_strain']
                # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['out_strain']
                data_ = a.par_fit[:int(a.AllDataDict['strain_basis_func'])]
                savetxt(
                    os.path.join(path, name_),
                    data_,
                    fmt='%10.8f'
                )
                # -------------------------------------------------------------
                name_ = p4R.output_name['in_dw']
                # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['in_dw']
                # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['out_dw']
                data_ = a.par_fit[-1*int(a.AllDataDict['dw_basis_func']):]
                savetxt(
                    os.path.join(path, name_),
                    data_,
                    fmt='%10.8f'
                )
            # -----------------------------------------------------------------
            try:
                name_ = p4R.output_name['out_XRD']
                # name_ = a.PathDict['namefromini'] + '_' + p4R.output_name['out_XRD']
                data_ = column_stack(
                    (
                        a.ParamDict['th4live'],
                        a.ParamDict['Iobs'],
                        a.ParamDict['I_fit']
                    )
                )
                savetxt(
                    os.path.join(path, name_),
                    data_,
                    header=line,
                    fmt='{:^12}'.format('%3.8f')
                )
                # -----------------------------------------------------------------
                logger.log(
                    logging.INFO,
                    "Data have been saved successfully"
                )
            except (ValueError):
                msg = "Some problems occurs during fitting data, please do not abort the fit to soon"
                logger.log(
                    logging.WARNING,
                    msg
                )                
                msg = "Data can not be saved to file, please relaunch fit "
                logger.log(
                    logging.WARNING,
                    msg
                )                
        except (IOError):
            msg = "Some problems occurs during saving data, please check your path !!"
            logger.log(
                logging.WARNING,
                msg
            )

    def on_export_data(self):
        """
        Manual export data to file containing Strain, Dw and XRD fit
        """
        if a.PathDict['project_name'] == "":
            return
        else:
            if a.PathDict['path2ini'] != '':
                path = a.PathDict['path2ini']
            else:
                path = a.PathDict['path2drx']
            try:
                header = ["2theta", "Iobs", "Icalc"]
                line = u'{:^12} {:^24} {:^12}'.format(*header)
                
                # -----------------------------------------------------------------
                name_ = p4R.output_name['out_strain_profile']
                data_ = column_stack(
                    (
                        a.ParamDict['depth'],
                        a.ParamDict['strain_i']
                    )
                )
                savetxt(
                    os.path.join(path, name_),
                    data_,
                    fmt='%10.8f'
                )
                
                # -----------------------------------------------------------------
                name_ = p4R.output_name['out_dw_profile']
                data_ = column_stack(
                    (
                        a.ParamDict['depth'],
                        a.ParamDict['DW_i']
                    )
                )
                savetxt(
                    os.path.join(path, name_),
                    data_,
                    fmt='%10.8f'
                )

                # -----------------------------------------------------------------
                name_ = p4R.output_name['out_XRD']
                data_ = column_stack(
                    (
                        a.ParamDict['th4live'],
                        a.ParamDict['Iobs'],
                        a.ParamDict['I_i']
                    )
                )
                savetxt(
                    os.path.join(path, name_),
                    data_,
                    header=line,
                    fmt='{:^12}'.format('%3.8f')
                )
                # -----------------------------------------------------------------
                logger.log(
                    logging.INFO,
                    "Data have been exported successfully"
                )
            except (IOError):
                msg = "Some problems occurs during exporting data, please check your path !!"
                logger.log(
                    logging.WARNING,
                    msg
                )
