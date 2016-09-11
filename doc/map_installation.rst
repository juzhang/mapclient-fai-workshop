***********************
MAP Client Installation
***********************

MAP Client
==========

Windows - Into an Anaconda Environment
--------------------------------------

Anaconda is an umbrella package of Python packages for scientific computing. It is a convenient way to set up a Python environment with the dependencies for MAP Client and its plugins.

1. Install `Anaconda <https://www.continuum.io/downloads>`_ for Python 2.7
2. Install MAP Client plugin dependencies in the Anaconda environment
    
    2.1. Open a Anaconda 2 command prompt: Start > All programs > Anaconda2 > Anaconda Prompt
    
    2.2. Install Git and Mayavi via the commandline::
        
        conda install mayavi git

    Enter "y" for questions confirming the install, e.g. having to downgrade some packages.

    2.3. Install transforms3d via the commandline using pip::

        pip install transforms3d

    2.4. Download the `latest GIAS2 release <https://bitbucket.org/jangle/gias2/downloads>`_ in the whl format.

    2.5. Install GIAS2 via the commandline prompt::

        pip install path\to\gias2-X.X.X-py2-none-any.whl

    where X.X.X is the version number.

    2.6. Install `OpenSim 3.3 <https://simtk.org/frs/?group_id=91>`_ (if you have not already)

    2.7. In a Anaconda prompt, navigate into the OpenSim python binding folder, e.g. ::

        cd C:\OpenSim 3.3\sdk\python

    There should be a setup.py file in the folder.

    2.8. Install OpenSim Python bindings::

        pip install .

3. Install MAP Client 0.13 Delta in the Anaconda environment.
    
    3.1. Download the `0.13 Delta release <https://github.com/MusculoskeletalAtlasProject/mapclient/releases>`_ in the .zip format.

    3.2. Extract the zip file into some folder and, in a Anaconda prompt, navigate into the src folder e.g. ::

        cd Downloads\mapclient-0.13.0-delta\src

    A setup.py file should be in the folder.

    3.1. Install MAP Client via the commandline prompt::

        pip install . -r requirements.txt

4. Mapclient can be run from the Anaconda prompt by entering::
    
    mapclient

Windows - MAP Client Standalone
-------------------------------

[EXPERIMENTAL, CANNOT INSTALL ADDITIONAL DEPENDENCIES]

1. Download the `0.13 Beta release <https://github.com/MusculoskeletalAtlasProject/mapclient/releases>`_ in the .exe format.

2. Run the .exe and install into the folder of your choice.

Linux
-----

Coming soon.

MAP Client Plugins
==================

MAP Client plugins can either be installed by the MAP Client automatically on opening of a workflow, or manually by the user. Pure-Python plugins should be easily handled automatically but plugins with non-python components and/or dependencies may need to be installed manually.

Automatically from a Workflow
-----------------------------

1. Open a workflow in MAP Client
2. MAP Client should automatically download any plugins in the workflow not already installed. An error message will appear when plugins are installed [known bug].
3. Restart the MAP Client for the newly installed plugins to be usable.

Manually
--------

1. Create a folder for keeping plugins
2. Open MAP Client, open the Plugin Manager, set the plugins folder
3. Download the latest releases of the desired plugin from the `MAP Client Plugins Github site <https://github.com/mapclient-plugins>`_ and extract into the plugins folder. There should be a folder for each plugin, e.g. ::

    mapclient-plugins\
        trcsourcestep\
        trcframeselectorstep\
        ...

4. Restart the MAP Client for the newly installed plugins to be usable [known bug].

MAP Client Workflows
====================

A MAP Client workflow is saved as a series of files in its own folder. This folder can be anywhere on your file system. The workflow is imported into MAP Client by File>Open and selecting the workflow folder.