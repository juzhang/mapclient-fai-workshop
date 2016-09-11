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