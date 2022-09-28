#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: A_BOULLE & M_SOUILAH
# Radmax project web

import os
import sys
import argparse
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))
import Parameters as p4R
import Exchange as ExData

try:
    import scipy
    import numpy
    import lmfit
    import sqlite3
    import xrayutilities
    print("***************************************")
    print("             RaDMaX\u00b2")
    print("         Version:%s" % p4R.version)
    print(" Last modification: %s" % p4R.last_modification)
    print("****************************************\n")
    if getattr(sys, 'frozen', False):
        print("Versions of modules compiled for this application:")
    else:
        print("Checking the modules needed to work with RaDMaX\u00b2:")
        print("Version found on this computer:")
    print("Python: %s" % sys.version)
    print("Scipy: %s" % scipy.__version__)
    print("Numpy: %s" % numpy.__version__)
    print("Lmfit: %s" % (lmfit.__version__))
    print("Sqlite3: %s" % (sqlite3.sqlite_version))
    print("Xrayutilities: %s" % (xrayutilities.__version__))
    print('Modules embedded with this application:')
    print("Eel: 0.14.0")
    print()
except ImportError:
    print("Pay attention: scipy and numpy modules are required to run this program")
    sys.exit()

# ---------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example with simple options")
    parser.add_argument(
                        '-b',
                        '-browser',
                        type=int,
                        help="specifying what browser to use (default: chrome)\n1:chrome,\n2:edge,\n3:electron"
                        )

    parser.add_argument(
                        '-l',
                        '-local',
                        action="store_true",
                        default=False,
                        help="in case of no internet connexion, add -local option"
                        )

    args = parser.parse_args()
    net_connected = 0
    browser_choice = 1
    if args.l:
        net_connected = 1
    if args.b != None:
        browser_choice = args.b
    ExData.Main(None, net_connected, browser_choice)


