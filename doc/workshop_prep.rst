Workshop Preparation
====================

The upcoming MAP Client workshop will be centered around using the MAP Client and developing MAP Client plugins. We will focus in particular on workflows and plugins relevant to the FAI project.

To maximise productivity during the workshop, there are few things
participants can do in preparation.

1. The MAP Client
----------------------------

Please refer to the `MAP Client Manual <http://map-client.readthedocs.io/en/latest/manual/index.html>`_ for details on using the MAP Client. Note that the installation pages of the manual is currently out of date.

If you intend on writing MAP Client plugins, please read the `MAP Plugin <http://map-client.readthedocs.io/en/latest/manual/MAP-plugin.html>`_ page to familiarise yourself with the MAP Client plugin API.

Try the :doc:`map_installation` guide for Windows. If you do not succeed, don't worry, we will go over installation on day 1.

2. Download FAI case data
-------------------------

We will be running workflows and developing plugins for FAI data.
Therefore, it will be helpful to have a few FAI cases downloaded on your
computer. If you do not have access to FAI data, please talk to David
Saxby.

For each case, we will need its MRI segmentations and its static-trial
TRC file. You may want to set up the following folder structure for each
case::

    FAS-XXX/
        raw_seg/
            [segmented STL files]
        preprocessed_seg/
        mocap/
            static_trial.TRC
        map_output/
            fitted_meshes/
            osim_model/

3. Download the Workshop Data
-----------------------------

The data for this workshop, including the documentation (in reStructured Text format), example workflows, and workflow data can be downloaded from the `workshop Github page <https://github.com/juzhang/mapclient-fai-workshop>`_, or through `this link <https://github.com/juzhang/mapclient-fai-workshop/archive/master.zip>`_.

4. Git and Github
-----------------

MAP Client and its plugins use Git for version control and are hosted on
Github. To be comfortable installing, writing, and modifying plugins,
you may want to familiarise yourself with Git and Github. Feel feel to
browse, fork, and clone the `MAP
Client <https://github.com/MusculoskeletalAtlasProject/mapclient>`__ and
`plugin <https://github.com/mapclient-plugins>`__ repositories on
Github.

5. Python, NumPy, SciPy, and OpenSim
------------------------------------

The MAP Client and its plugins are written in the Python programming
language. The plugins themselves make heavy use of the `SciPy <https://docs.scipy.org/doc/numpy-dev/user/quickstart.html>`__
library for numeric computing (you don't need to install SciPy separately). Since we will be dealing with `OpenSim
models <https://simtk.org/projects/opensim>`__, we will also be using
OpenSim 3.3's Python API. If you intend on developing MAP Client
plugins, you should familiarise yourself with Python and these
libraries.

The :doc:`map_installation` guide covers the installation of these libraries.
