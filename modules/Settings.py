#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

# =============================================================================
# Settings module
# =============================================================================


import os
from sys import platform as _platform
import Parameters as p4R
from threading import Thread

import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)

LEVELS = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]

# -----------------------------------------------------------------------------
class LogSaver():
    """
    class used all along the modules to record the information available
    """
    # création de l'objet logger qui va nous servir à écrire dans les logs
    logger = logging.getLogger()
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s ::' +
                                  '%(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler(p4R.log_file_path, 'a', 1000000, 1)
    # on lui met le niveau sur DEBUG,
    #        on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# -----------------------------------------------------------------------------
class Sound_Launcher(Thread):
    def __init__(self, case, random_music):
        Thread.__init__(self)
        self.case = case
        self.random_music = random_music
        self.start()

    def run(self):
        l_1 = [2, 18, 106, 107]
        l_2 = [99, 199]
        load_voice = [
            'Radmax_emma',
            'Radmax_harry',
            'Radmax_All_emma',
            'Radmax_All_harry'
        ]
#       1=owin31, 2=Icq, 3=The_End
        if self.case == 0:
            if self.random_music in l_1:
                path2music = os.path.join(p4R.music_path, 'song_3.wav')
            elif self.random_music in l_2:
                path2music = os.path.join(p4R.music_path, 'song_1.wav')
            else:
                path2music = os.path.join(p4R.music_path, 'song_2.wav')
        elif self.case == 1:
            return
        elif self.case == 2:
            path2music = os.path.join(p4R.music_path,
                                      load_voice[self.random_music] + '.wav')

        if _platform == "linux" or _platform == "linux2":
            import subprocess
            subprocess.Popen(
                ['aplay', path2music],
                stdin=None,
                stdout=None,
                stderr=None
            )
        elif _platform == 'darwin':
            import subprocess
            subprocess.Popen(
                ['afplay', path2music],
                stdin=None,
                stdout=None,
                stderr=None
            )
        else:
            from Playsound import playsound
            playsound(path2music, block=False)


# -----------------------------------------------------------------------------
class UpdateExampleFiles():
    def on_update_example(self, data):
        example_path = os.path.join(data, "examples")
        for d in p4R.example_list:
            filename = d + '.ini'
            example_dir = os.path.join(example_path, d, filename)
            replaced_content = ""
            with open(example_dir, 'r', encoding='utf-8') as fp:
                while True:
                    line = fp.readline()
                    if "<WRITE PATH HERE>" in line:
                        if _platform == 'win32':
                            newline = line.replace("/", "\\")
                        newline = newline.replace("<WRITE PATH HERE>", data)
                        replaced_content += newline
                    else:
                        replaced_content += line
                    if not line:
                        break
            with open(example_dir, 'w', encoding='utf-8') as fp:
                fp.write(replaced_content)

            