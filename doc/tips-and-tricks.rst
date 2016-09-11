***************
Tips and Tricks
***************

This page lists tips and tricks noted during the workshop.

Deleting Auto-installed Plugin
==============================

Right now, automatically installed plugins must be manually deleted. You may want to do this if you need to install a different version of a plugin.

Automatically install plugins are saved in::

    Users\[user]\AppData\Roaming\MusculoSkeletal\MAPClient\venv_0.13.0\Lib\site-packages

For a particular plugin, you need to delete the ``-nspkg.path`` file, the ``.egg-info`` directory, and the plugin directory in the ``mapclientplugins`` directory (WARNING: not the whole ``mapclientplugins`` directory).

Installing SciPy
================

Scipy should be installed by conda to ensure the dependent linear algebra libraries are also installed. Pip cannot deal with this so ``pip install [gias2.whl]`` will fail to install SciPy.

Bugs
====

-  In an virtual environment's terminal started from the Anaconda explorer GUI, starting a mayaviscenewidget causes an exception: PySide.QtGui.QBoxLayout.addWidget called with wrong argument type QWidget, expected PySide.QtGui.QWidget.

-  The Gait2392 customisation workflow may produce an OpenSim model with a unrealistic knee angle for the right knee.

-  Conditiona via points do not activate on the muscle line segment, causing the muscle path to "snap".