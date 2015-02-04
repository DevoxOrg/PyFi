# About: #

This is a personal finance package I started to try and automate my own financial analysis and cut out any human error from doing it manually.

Originally this project was intended to be a Python/VBA mashup so that most of the analysis could be done in Excel after Python compiled the CSVs into a unified format. 

As is the nature of projects, the direction of this one has become ever changing. Currently the main aim is to create a comprehensive pure python program that will allow most of the basic analysis to be done automagically.

This will produce financial reports on demand and provide simple flexibility to see the data you want to see, how you want to see it. Lastly it will make available Pythons more advanced mathematical libraries, including NumPy, allowing powerful complex analysis and modelling of the data.

# How to use: #

This code is not ready or suitable for public use, there are several bugs that need to be fixed first and several features that at the time of writing are non-functioning.

If you are still intent on using it, the programme can be used by downloading the lib folder and placing it where you feel is suitable, running `main.py` for the first time will create the necessary sub-folders.

For a command line app which converts OFX and QIF files, as well as a couple select CSV formats, into CSV files ready for excel manipulation, see the last command line based commit:

https://github.com/NDevox/PyFi/tree/6a2bf8e2462c0c3d5985a00d5849d252b740175c

Bare in mind a lot has changed since the last command line based commit, including the back-end systems which are still being streamlined.

## Dependencies: ##

- Python 3.x (this was written in 3.4)
- PySide (and Qt which PySide is dependent on)
- NumPy and MatPlotLib (and their related dependencies)
