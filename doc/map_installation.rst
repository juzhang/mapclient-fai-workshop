***********************
MAP Client Installation
***********************

MAP Client
==========

Windows - Into an Anaconda Environment
--------------------------------------

Anaconda is an umbrella package of Python packages for scientific computing. It is a convenient way to set up a Python environment with the dependencies for MAP Client and its plugins.

1. Install `Anaconda <https://www.continuum.io/downloads>`_ for Python 2.7

2. Launch the Anaconda Navigator and create a new virtual environment with Python 2.7. A virtual environment is a Python sandbox isolated from the rest of your system in which you can install packages without conflicting with your system or other virtual environments.
    
    2.1 Click the "Environments" tab on the left, then click the "Create" button on the bottom of the list of environments (should only contain "root" for now).

    2.2. In the pop-up dialogue, name the new environment something descriptive like "mapclient-py27". Make sure to select "2.7" in the Python version drop-down list.

    2.3. Click "Create" and wait for the new environment to show up in the environments list.

3. launch a terminal for the new environment (click the "play" button next to your new environment and select "open terminal").

4. Install MAP Client plugin dependencies in the Anaconda environment
    
    4.1. Install Git and Mayavi via the commandline::
        
        conda install mayavi git scipy

    Enter "y" for questions confirming the install, e.g. having to downgrade some packages.

    4.2. Install transforms3d via the commandline using pip::

        pip install transforms3d

    4.3. Download the `latest GIAS2 release <https://bitbucket.org/jangle/gias2/downloads>`_ in the whl format.

    4.4. Install GIAS2 via the commandline prompt::

        pip install path\to\gias2-X.X.X-py2-none-any.whl

    where X.X.X is the version number.

    4.5. Install `OpenSim 3.3 <https://simtk.org/frs/?group_id=91>`_ (if you have not already)

    4.6. In a Anaconda prompt, navigate into the OpenSim python binding folder, e.g. ::

        cd C:\OpenSim 3.3\sdk\python

    There should be a setup.py file in the folder.

    4.7. Install OpenSim Python bindings::

        pip install .

5. Install MAP Client 0.13 Delta in the Anaconda environment.
    
    5.1. Download the `0.13 Delta release <https://github.com/MusculoskeletalAtlasProject/mapclient/releases>`_ in the .zip format.

    5.2. Extract the zip file into some folder and, in a Anaconda prompt, navigate into the src folder e.g. ::

        cd Downloads\mapclient-0.13.0-delta\src

    A setup.py file should be in the folder.

    5.1. Install MAP Client via the commandline prompt::

        pip install . -r requirements.txt

5. Set an environment variable to make sure Mayavi works for visualisation in some mapclient plugins::
    
    set QT_API=pyqt
        
You may or may not need this, depending if you've installed Qt5 at some point. If you do need this command, you will need to run this command whenever you start a new terminal. See `here <https://conda.io/docs/using/envs.html#windows>`_ to set environment variables permanently.

6. Mapclient can be run from your virtual environment's terminal by entering::
    
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