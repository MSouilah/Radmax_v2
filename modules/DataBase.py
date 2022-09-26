#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

# =============================================================================
# Radmax Database panel module
# =============================================================================

import os
import sqlite3

import Parameters as p4R
from Parameters import P4Rm

from time import strftime, localtime
import pickle
import logging
logger = logging.getLogger(__name__)

select_data_all = """
SELECT *
FROM RadMaxData
"""
select_data_exp_name = """
SELECT DISTINCT exp_name
FROM RadMaxData
ORDER BY id DESC
"""

select_data_by_id = """
SELECT *
FROM RadMaxData
WHERE id=?
"""

insert_data = """
INSERT INTO RadMaxData (date, exp_name,
crys_name, fit_algo, fit_success, residual, geometry,
model, alldata, spdata, dwpdata, pathDict, xrd_data)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

delete_data_by_id = """
DELETE FROM RadMaxData
WHERE id=?
"""

a = P4Rm()

# -----------------------------------------------------------------------------
# noinspection PyRedundantParentheses
class DataBaseUse():
    def __init__(self):
        """
        Constructor
        """
        self.con = None

    def create_connection(self, path):
        """ create a database connection to a SQLite database """
        con = None
        try:
            con = sqlite3.connect(path, check_same_thread=False)
            con.row_factory = sqlite3.Row
            print("Database successfully connected.")
            return con
        except sqlite3.Error as e:
            print("Error while connecting to sqlite", e)

    def connect_db(self, path):
        con = self.create_connection(path)
        P4Rm.DBDict['con'] = con
        P4Rm.DBDict['cursor'] = con.cursor()

    def initialize_database(self):
        """
        Create an engine that stores data in the local directory's
        sqlalchemy_example.db file.
        """
        a = P4Rm()
        logger.log(logging.WARNING, 'Loading or creates database')

        cursor = None
        if not os.path.isdir(p4R.database_path):
            msg = p4R.database_path + " is not present, creates one !"
            logger.log(logging.WARNING, msg)
            os.makedirs(p4R.database_path)
        path = os.path.join(p4R.database_path, p4R.Database_name + '.db')
        if not os.path.isfile(path):
            msg = p4R.Database_name + " is not present, creates one !"
            logger.log(logging.WARNING, msg)

        self.connect_db(path)
        # !!! changer la suite !!!

        file_stats = os.stat(path)
        MB_size = file_stats.st_size / (1024 * 1024)

        # print(file_stats)
        # print(f'File Size in Bytes is {file_stats.st_size}')
        # print(f'File Size in MegaBytes is {MB_size}')
        
        if MB_size > 500:
            print ("Size of the Database file is too high: ",
                    '%s' % (MB_size))
            print ("Making of backup file")
            old_name = os.path.join(
                p4R.database_path,
                p4R.Database_name + '.db'
                )
            new_name = os.path.join(
                p4R.database_path,
                p4R.Database_name + '_backup.db'
                )
            msg = ("Size of the Database file is too high, " +
                    "create a backup file")
            logger.log(logging.WARNING, msg)
            os.rename(old_name, new_name)
            self.connect_db(path)

        cursor = a.DBDict['cursor']
        cursor.execute(
            select_data_all
        )
        res = cursor.fetchall()
        res = [dict(row) for row in res]
        if res:
            if len(res) > 0:
                self.on_read_database_and_fill_list(res)

    @staticmethod
    def on_read_database_and_fill_list(data):
        list_temp = []
        for instance in data:
            tmp = {
                "id": instance['id'],
                "filter_select": 0,
                "date": instance['date'],
                "exp_name": instance['exp_name'],
                "crys_name": instance['crys_name'],
                "fit_algo": instance['fit_algo'],
                "fit_success": instance['fit_success'],
                "residual": instance['residual'],
                "geometry": instance['geometry'],
                "model": instance['model'],
            }
            list_temp.append(tmp)
        P4Rm.database_list = list_temp

    def on_fill_database_and_list(self, success):
        a = P4Rm()
        current_time = localtime()
        date = strftime('%Y-%m-%d %H:%M:%S', current_time)

        # print(a.PathDict)
        exp_name = a.PathDict['project_name']
        crys_name = a.AllDataDict['crystal_name']
        fit_algo = p4R.FitAlgo_choice[int(a.AllDataDict['fitting_choice'])]
        fit_success = p4R.FitSuccess[success]
        residual = round(a.residual_error, 4)
        geometry = p4R.sample_geometry[int(a.AllDataDict['geometry'])]
        model = p4R.Strain_DW_choice[int(a.AllDataDict['model'])]

        alldata = pickle.dumps(a.AllDataDict, protocol=2)
        spdata = pickle.dumps(a.ParamDict['sp'], protocol=2)
        dwpdata = pickle.dumps(a.ParamDict['dwp'], protocol=2)
        pathDict = pickle.dumps(a.PathDict, protocol=2)
        xrd_data = pickle.dumps(a.ParamDict['data_xrd'], protocol=2)

        cursor = a.DBDict['cursor']
        cnx = a.DBDict['con']
        cursor.execute(
            insert_data,
            [
                date,
                exp_name,
                crys_name,
                fit_algo,
                fit_success,
                residual,
                geometry,
                model,
                alldata,
                spdata,
                dwpdata,
                pathDict,
                xrd_data
            ]
        )
        cnx.commit()

        cursor.execute(
            select_data_all
        )
        res = cursor.fetchall()
        res = [dict(row) for row in res]
        if res:
            self.on_read_database_and_fill_list(res)


    @staticmethod
    def on_item_selected(id):
        cursor = a.DBDict['cursor']
        cursor.execute(
            select_data_by_id,
            [
                id
            ]
        )
        res = cursor.fetchall()
        res = [dict(row) for row in res]
        if res:
            P4Rm.AllDataDict = pickle.loads(res[0]['alldata'])
            P4Rm.ParamDict['sp'] = pickle.loads(res[0]['spdata'])
            P4Rm.ParamDict['dwp'] = pickle.loads(res[0]['dwpdata'])
            P4Rm.PathDict = pickle.loads(res[0]['pathDict'])
        try:
            P4Rm.ParamDict['data_xrd'] = pickle.loads(res[0]['xrd_data'], encoding='latin1')
        #            encoding pour python 3 afin de lire les données enregistrees en python 2
        except (TypeError):
            P4Rm.ParamDict['data_xrd'] = pickle.loads(res[0]['xrd_data'])
        path_ini = a.PathDict['path2inicomplete']
        if not os.path.isfile(path_ini):
            P4Rm.pathfromDB = 1
        else:
            P4Rm.pathfromDB = 0

    @staticmethod
    def on_read_part_DB():
        cursor = a.DBDict['cursor']
        cursor.execute(
            select_data_exp_name
        )
        res = cursor.fetchall()
        res = [dict(row) for row in res]
        if res:
            P4Rm.DBDict['name'] = res

    # def on_search_in_DB(self):
    #     a = P4Rm()
    #     temp = []
    #     test = []
    #     test = [
    #         RadMaxData.exp_name,
    #         RadMaxData.crys_name,
    #         RadMaxData.geometry,
    #         RadMaxData.model,
    #         RadMaxData.date
    #     ]
    #     for i in range(len(a.DBDict['choice_combo'])):
    #         if not a.DBDict['choice_combo'][i] is None:
    #             if a.DBDict['choice_combo'][i] == 'equal':
    #                 the_day = datetime.strptime(a.DBDict['date_1'],
    #                                             "%Y-%m-%d %H:%M:%S")
    #                 next_day = the_day + timedelta(days=1)
    #                 next_day = '{:%Y-%m-%d %H:%M:%S}'.format(next_day)
    #                 temp.append(test[i] >= a.DBDict['date_1'])
    #                 temp.append(test[i] <= next_day)
    #             elif a.DBDict['choice_combo'][i] == '=<':
    #                 temp.append(test[i] <= a.DBDict['date_1'])
    #             elif a.DBDict['choice_combo'][i] == '>=':
    #                 temp.append(test[i] >= a.DBDict['date_1'])
    #             elif a.DBDict['choice_combo'][i] == 'between':
    #                 temp.append(test[i] >= a.DBDict['date_1'])
    #                 temp.append(test[i] <= a.DBDict['date_2'])
    #             else:
    #                 temp.append(test[i] == a.DBDict['choice_combo'][i])

    #     s = a.DBDict['session'].query(RadMaxData).filter(*temp).all()
    #     if a.DBDict['choice_state']:
    #         self.on_read_database_and_fill_list(s)
    #     else:
    #         [a.DBDict['session'].delete(x) for x in s]

    @staticmethod
    def on_delete_selected(id):
        try:
            cursor = a.DBDict['cursor']
            cursor.execute(
                delete_data_by_id,
                [
                    id
                ]
            )
            cnx = a.DBDict['con']
            cnx.commit()
            return True
        except:
            return False