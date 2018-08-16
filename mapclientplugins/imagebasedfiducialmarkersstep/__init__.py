
"""
MAP Client Plugin
"""

__version__ = '0.1.0'
__author__ = 'Hugh Sorby'
__stepname__ = 'Image Based Fiducial Markers'
__location__ = 'https://github.com/mapclient-plugins/mapclientplugins.imagebasedfiducialmarkers/archive/master.zip'

# import class that derives itself from the step mountpoint.
from mapclientplugins.imagebasedfiducialmarkersstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
from . import resources_rc