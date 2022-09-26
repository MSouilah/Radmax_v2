#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project

# =============================================================================
# Tkinter Module
# =============================================================================

# permetd'afficher une fentere de dialog de sauvegarde ou douverture de fichiers en python
# --> uniquement dans le cas de l'uilisation de l'application dans une fenetre web et pas dans electron !!!

from tkinter import filedialog as fd

# def show_dialog(t, window_title, dir_path):
#     if t =="open":
#         return open_select_file(window_title, dir_path)
#     root.destroy()

def open_selected_file(window_title, dir_path):
    if window_title == "Load project":
        f_name = 'ini files'
        f_type = '*.ini'

        file2open = (
            (f_name, f_type)
        )
        filetypes = [
            file2open
        ]
    elif window_title == "Load XRD file":
        file2open = (
            ('Binary files', '*.uxd'),
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        filetypes = (
            file2open
        )
    else:
        window_title = window_title +  " - Attention, not coefficients file"
        file2open = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        filetypes = (
            file2open
        )

    filename = fd.askopenfilename(
        title = window_title,
        initialdir = dir_path,
        filetypes = filetypes
    )
    
    return filename

def save_project_file(window_title, dir_path):
    f_name = 'ini files'
    f_type = '*.ini'

    filetypes = [
        (f_name, f_type)
    ]

    # filename = fd.asksaveasfilename(
    #     title = window_title,
    #     initialdir = dir_path,
    #     filetypes = filetypes
    # )

    filename = fd.askdirectory(
        title = window_title,
        initialdir = dir_path
    )
    
    
    return filename