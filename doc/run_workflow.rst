Run a Workflow
==============

Let's run a pre-built workflow. This workflow takes a set of fitted meshes of lower limb bones and generates a customised OpenSim Gait2392 model (see :doc:`workflow-osimgen` for details).

Instructions
------------
1. If you have not already, download the workshop data pack `here <https://github.com/juzhang/mapclient-fai-workshop/archive/master.zip>`_. This contains the workshop documentation, example workflows, and example workflow data. Extract into a folder of your choice. We will call this the workshop folder.

2. Start MAP Client (open an Anaconda prompt, type mapclient, press enter).

3. File>Open, go to the workflow folder, go into the workshop_workflows folder, select the gait2392_cust folder. This will import the workflow and download the plugins it requires. Give it a few minutes for the plugins to download and install in the background.

    3.1. [KNOWN BUG] When the plugins have finished installing, a error message will pop up about a invalid workflow. Close the error message and restart MAP Client and open the workflow again. If the plugins have installed successfully, you will see the workflow in the workspace. If not, let me know.

4. We need to configure some of the plugins to read inputs and write outputs to and from the right places.

    4.1. Click the configure icon (gear) on the left-most *trcsource* step and set the *location* to::

        [workflow folder]\wfdata\FAS-906\mocap\StaticCalibration.trc

    4.2. Click the configure icon (gear) on the *mocap_2392_geom* step and set the *Output Directory* to::

        [workflow folder]\wfdata\FAS-906\map_output\osim_model

    4.3. Click the configure icon (gear) on the right-most *g2392_muscle_cust* step and set the *Output Folder* to::

        [workflow folder]\wfdata\FAS-906\map_output\osim_model

5. Save the workflow (ctrl+s or File>Save), and click *Execute* in the lower right-hand corner to run the workflow. Refer to the "Running the Workflow" section in :doc:`workflow-osimgen` for step-by-step instructions.