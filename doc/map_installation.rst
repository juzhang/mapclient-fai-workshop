MAP Client Installation
=======================

MAP Client
----------

Windows - Into an Anaconda Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[WIP STEPS NOT FINALISED]

Anaconda is an umbrella package of Python packages for scientific computing. It is a convenient way to set up a Python environment with the dependencies for MAP Client and its plugins.

1. Install `Anaconda <https://www.continuum.io/downloads>`_ for Python 2.7
2. Install MAP Client and plugin dependencies in the Anaconda environment
    
    2.1. Open a Anaconda 2 command prompt: Start > All programs > Anaconda2 > Anaconda Prompt
    
    2.2. Install Git, PySide and Mayavi via the commandline (PySide only support python 2.7 and 3.3)::
        
        conda install pyside mayavi git

    Enter "y" for questions confirming the install, e.g. having to downgrade some packages.

    2.3. Install transforms3d via the commandline::

        pip install transforms3d

    2.4. Download the `latest GIAS2 release <https://bitbucket.org/jangle/gias2/downloads>`_ in the whl format.

    2.5. Install GIAS2 via the commandline prompt::

        pip install path\to\gias2-X.X.X-py2-none-any.whl

    where X.X.X is the version number.

3. Install MAP Client 0.13 Beta in the Anaconda environment. [WIP, steps not finalised]
    
    3.1. Download the `0.13 Beta release <https://github.com/MusculoskeletalAtlasProject/mapclient/releases>`_ in the .zip format.

    3.2. Extract the zip file into some folder and navigate into the src folder. A setup.py file should be in the folder, e.g. ::

        cd Downloads\mapclient-0.13.0-beta\src

    3.1. Install MAP Client via the commandline prompt::

        pip install .
        pip install -r requirements.txt

4. Mapclient can be run from the Anaconda prompt by entering::
    
    mapclient

Windows - MAP Client Standalone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[EXPERIMENTAL, CANNOT INSTALL ADDITIONAL DEPENDENCIES]

1. Download the `0.13 Beta release <https://github.com/MusculoskeletalAtlasProject/mapclient/releases>`_ in the .exe format.

2. Run the .exe and install into the folder of your choice.

Linux
~~~~~

MAP Client Plugins
------------------

Automatically from a Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Create a folder for keeping plugins
2. Open MAP Client, open the Plugin Manager, set the plugins folder
3. Save a workflow to disk
4. Open the workflow in MAP Client
5. MAP Client should automatically download any plugins in the workflow not already installed.

Manually
~~~~~~~~
1. Create a folder for keeping plugins
2. Open MAP Client, open the Plugin Manager, set the plugins folder
3. Download the latest releases of the desired plugin from the `MAP Client Plugins Github site <https://github.com/mapclient-plugins>`_ and extract into the plugins folder. There should be a folder for each plugin, e.g. ::

    mapclient-plugins\
        trcsourcestep\
        trcframeselectorstep\
        ...

4. Restart MAP Client 

MAP Client Workflows
--------------------
