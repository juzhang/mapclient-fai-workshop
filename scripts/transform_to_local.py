"""
Example script for transforming a cloud of points into the local coordinate
system of a map bone.

This could be the basis of a plugin that transforms a cartilage mesh into
the local coordinate system of a femur.

Note that this script cannot actually be run. It is simply an example
of the code required to perfrom the transform.
"""

import numpy as np
from gias2.musculoskeletal.bonemodels import bonemodels

def _update_femur_opensim_acs(femur_model):
    """
    function to evaluate the femur local CS based on
    how opensim does it, and set it for the input
    femur_model
    """
    femur_model.acs.update(
        *bonemodels.model_alignment.createFemurACSOpenSim(
            femur_model.landmarks['femur-HC'],
            femur_model.landmarks['femur-MEC'],
            femur_model.landmarks['femur-LEC'],
            side=femur_model.side
            )
        )

# points to be transformed (plugin input)
# should be a nx3 array
input_points = np.zeros((100,3))

# fieldwork model of the bone
# should be a geometric_field instance
femur_gfield = None

# create a MAP bone model from the gfield
femur = bonemodels.FemurModel('femur', femur_gfield, side='left')

# change the local CS to the opensim one
update_femur_opensim_acs(femur)

# transform input points to local CS
output_points = femur.acs.map_local(input_points)

