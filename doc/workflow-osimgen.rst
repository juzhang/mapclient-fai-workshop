*********************************
OpenSim Model Generation Workflow
*********************************

This document describes how to build and run a MAP Client workflow for
customising the Gait2392 OpenSim model to fit patient-specific bone
meshes generated from FAI project data.

Background
==========

The `Gait2392 OpenSim
model <http://simtk-confluence.stanford.edu:8080/display/OpenSim/Gait+2392+and+2354+Models>`__
is a rigid-body model of the lower limbs widely for gait kinematics,
inverse-dynamics, and muscle control studies. The models is composed of
Bodies connected by Joints and line-segment Muscles. The parameters of
the model (e.g. Body masses, joint coordinates) can be customised to
match the anatomy of a particular subject, allowing the model to better
represent the function of that subject.

This workflow customises the reference Gait2392 using patient-specific
model parameters calculated from the bone meshes generated from the Bone
Mesh Generation Workflow. The output Gait2392 model has customised: -
body masses and inertial properties, - joint positions, - knee joint
trajectory based on femur and tibia shape, - muscle via points, - muscle
tendon slack length and optimal fibre length, - model markers, and -
Display meshes for each bone

Each of the parameters above are customised to varying levels of subject
specificity. Please refer to the readme files of the **Fieldwork
Gait2392 Geometry Customisation** step and **Fieldwork Gait2392 Muscle
HMF** for details.

Inputs Data
===========

-  The fitted bone meshes for the pelvis, femurs, patellas, and
   tibia/fibulas from the Bone Mesh Generation Workflow.
-  TRC file of mocap static-trial

Output Data
===========

-  A OpenSim Gait2392 model and geometry meshes customised using the
   input bone meshes.

Building the Workflow
=====================

1. Start a new workflow: *File>New>Workflow* and create a new folder for
   the workflow and click *Open* inside that folder.
2. Add the **TRC Source** step to the workspace. Configure it with the
   case's static-trial TRC file.
3. Add the **TRC Frame Selector** step to the workspace. Connect the
   output port of **TRC Source Step** to the first port of **TRC Frame
   Selector Step**. Configure the step to read particular frame.
4. Add the **Fieldwork Lower Limb (2 sides) Generation** step to the
   workspace. Connect the output port of **TRC Frame Selector Step** to
   the input port. Configure the step:

   -  PCs to Fit: 1
   -  Mahalanobis Weight: 0.1
   -  Landmarks:

      -  femur-HC-l : LHJC
      -  femur-HC-r : RHJC
      -  femur-LEC-l : LLFC
      -  femur-LEC-r : RLFC
      -  femur-MEC-l : LMFC
      -  femur-MEC-r : RMFC
      -  pelvis-LASIS : LASI
      -  pelvis-LPSIS : LPSI
      -  pelvis-RASIS : RASI
      -  pelvis-RPSIS : RPSI
      -  tibiafibula-LM-l : LLMAL
      -  tibiafibula-LM-r : RLMAL
      -  tibiafibula-MM-l : LMMAL
      -  tibiafibula-MM-r : RMMAL

   -  Marker Radius: 5 (or whatever the marker radius was, unit is mm)
   -  Skin Padding : 5 (or whatever the patient soft-tisse was roughly,
      unit is mm)
   -  Knee Options : check Abd. DOF
   -  GUI : check

5. Add the **Fieldwork Model Dict Source** to the workflow. Configure it
   with the path of the INI file containing the file paths of the fitted
   mesh files. Please refer to the step's readme file for creating a
   valid INI file.
6. Add the **Fieldwork Gait2392 Geometry Customisation** step to the
   workflow. Connect the second output port of the **Fieldwork Lower
   Limb (2 sides) Generation** step to the first input port. Connect the
   output port of the **TRC Frame Selector** step to the second input
   port. Connect the output port of the **Fieldwork Model Dict Source**
   to the third input port. Configure the step:

   -  Output Directory: the folder where the customised OpenSim will be
      written.
   -  Input Unit: mm
   -  Output Unit: m
   -  Output .osim file: check
   -  Scale other bodies: check
   -  Subject Mass: the subject mass in kilograms.
   -  Preserve Mass Distribution: check if Subject Mass is specified and
      you wish to preserve the original Gait2392 mass distribution.
   -  Adjustable Marker: specify any Gait2392 markers that should be
      moved to an input landmark.

7. Add the **Fieldwork Gait2392 Muscle HMF** step to the workflow.
   Connect the first output of the **Fieldwork Gait2392 Geometry
   Customisation** step to the second input port. Connect the second
   output of the **Fieldwork Gait2392 Geometry Customisation** step to
   the first input port. Configure the step:

   -  Input Unit: mm
   -  OUtput Unit: m
   -  Write Osim File: check
   -  Update Knee Spline: uncheck
   -  Static Vastus: uncheck
   -  Output folder: the folder where the customised OpenSim will be
      written.

Running the Workflow
====================

When the workflow is executed, the workflow steps are executed from
start to finish. The steps are explain below. Most steps are automatic
and do not have user interaction. They are denoted by [AUTO]. The
operation of the other steps are explain below. For more details on each
step's operation, please refer to their respective readme files.

1. [AUTO] The **TRC Source** step read in the case's static-trial marker
   data.
2. [AUTO] The **TRC Frame Selector** step extracts the marker names and
   locations at a specified frame.
3. The **Fieldwork Lower Limb Generation** step registers the lower-limb
   shape model to the specified markers, thereby generating
   approximately patient-specific meshes for each lower limb bone. When
   the GUI of this step appears, the lower limb model will be shown in
   its un-registered position away from the green markers. The step is
   preconfigured so simply click the *Register* button in the
   *Registration* tab. Registration will take around 2 minutes after
   which the model will be registered with the markers. The registration
   can be refined by increasing the *PCs to Fit* value to 5 and clicking
   *Register* again. Model parameters can be manually adjusted in the
   *Manual Registration* tab. Click *Accept* to move onto the next step.
4. [AUTO] The **Fieldwork Model Dict Source** step read in the set of
   previously generated meshes as defined in its INI file.
5. [AUTO] The **Fieldwork Gait2392 Geometry Customisation** step
   combines the bone meshes from (4) with the lower-limb kinematics from
   (5) to create an updated lower-limb model. From this updated
   lower-limb model it then extracts body, joint, marker, and display
   geometry data and writes them into the OpenSim Gait2392 model.
6. [AUTO] The **Fieldwork Gait2392 Muscle HMF** takes the updated
   lower-limb model and the customised Gait2392 model from (5) and
   further customises the Gait2392 muscle parameters before writing the
   model to file.

When the workflow is complete, MAP Client will return to the workspace
view.
