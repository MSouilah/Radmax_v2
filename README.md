RaDMaX<sup>2</sup> is a program that allows to retrieve strain and damage profiles in ion-irradiated materials from the simulation of X-ray diffraction data recorded in symmetric thêta-2thêta geometry.
It is distributed freely under the CeCILL license (see LICENSE.txt and COPYRIGHT.txt).

**If you use this program in academic work, please cite:**
M. Souilah, A. Boulle, A. Debelle, "RaDMaX: a graphical program for the determination of strain and damage profiles in irradiated crystals", _J. Appl.Cryst._ **49**, 311-316 (2016). [Link to article.](http://dx.doi.org/10.1107/S1600576715021019)

RaDMaX<sup>2</sup> is the second version of the original [RaDMaX](https://github.com/aboulle/RaDMaX) program. It comes with a brand new interface and some new features to improve fit treatment.
This new version is still a python program software but the GUI is now in HTML/javascript. To use RaDMaX<sup>2</sup>, we use a little program named [Eel](https://github.com/ChrisKnott/Eel) which managed all the work to communicate between python and javascript (this modules is directly embedded with RaDMaX<sup>2</sup>).
The program will open a browser window (Chrome, or Microsoft Edge on Windows 7-11) as GUI. You can also use [Electron](https://www.electronjs.org/) as GUI (see below for instructions).

# Installation instructions
Download zip file and extract it to your disk.

RaDMaX<sup>2</sup> requires Python 3.x, SciPy, Numpy and LMFIT.
Instructions for Windows and GNU/Linux are given below.
You also need to have install chrome browser on your machine. Edge is also working on windows.
The program works in both connected and offline mode.

## MS Windows
1. For most users, especially on Windows and Mac, the easiest way to install scientific Python is to download **one** of these Python distributions, which includes most of the key packages:
 * [Anaconda](http://continuum.io/downloads) (recommended): A free distribution for the SciPy stack. Supports Linux, Windows and Mac.
 * [WinPython](http://winpython.github.io/) (not tested): A free distribution including the SciPy stack. Windows only. [Download.] (https://sourceforge.net/projects/winpython/files/WinPython_3.8/3.8.12.3/)
2. Alternativaly, you can install the dependencies using the pypi package manager, `pip install scipy lmfit xrayutilities bottle bottle-websocket future pyparsing whichcraft`. Pay attention with Python 3, sometimes you need to use pip3 (if you have python 2.x and 3.x installed on the same machine).
3. Once all the package installed, execute the "Radmax.py" file. Alternatively, open a terminal (press "windows" and "r", type "cmd" [without commas] and press "Enter"). Navigate to the "Radmax_2" folder and type `python Radmax.py`.

## GNU / Linux
1. On most Linux systems the dependencies are available in the software repositories. For debian based systems run (as root): `apt-get install python3-scipy python3-lmfit python3-xrayutilities python3-bottle python3-bottle-websocket python3-future python3-pyparsing python3-whichcraft` or `pip install scipy lmfit xrayutilities bottle bottle-websocket future pyparsing whichcraft`. Numpy is normally installed along Scipy.
2. Because browser have some limitations with opening and saving files, RaDMaX<sup>2</sup> passed through these using Python Tkinter module. Unlike Windows, on most Linux systems Tkinter is not installed with python. For debian based systems run (as root): `apt-get install python3-tk`.
3. In a terminal, run the Radmax.py file with `python Radmax.py`.

For other distributions please visit the [SciPy] (https://scipy.org) or [LMFIT] (https://lmfit.github.io/lmfit-py) websites.

## Mac OSX
1. Mac OS does not come with a package manager. You can use a third party package manager like [Macports](http://www.macports.org/) to install SciPy and LMFIT.
Otherwise, run (as root), for python 3.8 as exemple : `pip install scipy lmfit xrayutilities bottle bottle-websocket future pyparsing whichcraft tk`.
Once all the package installed, in a terminal, navigate to the "Radmax_2" folder and run the Radmax.py file with `python Radmax.py`.

## Development environment
The RaDMaX<sup>2</sup> program has been developed on MS Windows 10 using python 3.8.10, Scipy 1.8.0, Numpy:1.21.5 and Lmfit 1.0.3.
It has been tested on several GNU/Linux distributions.

# Quick test of the program
1. Launch Radmax.py.
2. In the "File" menu select "Load Project".
2. Navigate to the "Radmax_v2/examples/YSZ" or "examples/SiC-3C" folder and load the "config.ini" file.

* Any change in any of the upper panels has to be validated with the "Update" button (or click somewhere in the panel outside a form, or by ctrl-u shortcut) to update the XRD curve.
* The strain and damage profiles can be modified by dragging the control points. The XRD curve is updated in real time.
* Calculated XRD curves can be fitted to experimental data in the "Fitting window" tab.
* Conventional least-squares can be used.
* The fitted curve, the strain and damage profiles are automatically saved (*.txt) in the folder selected above.
* You have the possibility to use database storage, in his case each fit in save.

# Data format
XRD data can be loaded from the "File" menu. The data should be provided as a two-columns (2thêta, intensity) ASCII file in space- (or tab-) separated format. The 2thêta values have to be equally spaced (constant step). For the moment RaDMaX can only handle data recorded in symmetric coplanar geometry (conventional thêta-2thêta scan), as this is the most commonly used geometry in the analysis of irradiated materials.

Guess strain/damage profile can be imported from the "File" menu. The data should be providedas a two-columns ASCII file with the depth below the surface (in Angstroms) as first column.

