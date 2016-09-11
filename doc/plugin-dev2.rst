***************************
Advanced Plugin Development
***************************

This chapter walks through the `Fieldwork Gait2392 Geometry Customisation Step <https://github.com/mapclient-plugins/fieldworkgait2392geomstep>`_ as an example of a more advanced plugin. This plugin uses the `GIAS2 <https://bitbucket.org/jangle/gias2>`_ and OpenSim libraries to customise the Gait2392 model based on input lower limb bone models. Before the walk-through, let's have a brief overview of the GIAS2 library.

GIAS2
=====

`GIAS2 <https://bitbucket.org/jangle/gias2>`_ is a free and open-source Python library used by most MAP Client plugins written by Ju Zhang. It has a wide range of functionalities aimed at musculoskeletal modelling. It's functionalities can be broadly categoried into:

- Geometric transformations
- Rigid and non-rigid Registration
- Image segmentation (active shape models and random forest regression)
- Mesh processing
- Statistical shape models
- Lower-limb bone models

GIAS2 makes heavy use of the SciPy and NumPy. In addition, certain modules depend on PyDicom, Scikit-Learn, Matplotlib, and Mayavi (for 3D visualisation). GIAS2 is licensed under the Mozilla Public License Version 2.0.

GIAS2 has grown with the developement of the MAP Client and its plugins. It has served as library for storing functions and classes commonly used by many plugins and projects of mine outside of MAP. Having grown organically, GIAS2 does suffer from issues such as lack of documentation, in-complete features in some areas, and can probably do with some refactoring. It does have a collection of example scripts which demonstration the usage of some of its features. The MAP Client plugins on which it depends provide some more examples.

The Fieldwork Gait2392 Geometry Customisation Step uses classes and functions from a number of GIAS2 modules::

    from gias2.common import transform3D
    from gias2.fieldwork.field import geometric_field
    from gias2.mesh import vtktools
    from gias2.musculoskeletal import mocap_landmark_preprocess
    from gias2.musculoskeletal.bonemodels import bonemodels
    from gias2.musculoskeletal.bonemodels import lowerlimbatlas
    from gias2.musculoskeletal import osim
    from gias2.musculoskeletal import fw_model_landmarks as fml

The following is a brief summary of each of these modules.

transform3D
-----------

The `transform3D <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/common/transform3D.py?at=master&fileviewer=file-view-default>`_ module contains functions for applying rigid-body, similarity, and affine transformations to lists of point coordinates. Also function for calculating transformation matrices between 2 lists of corresponding points.

geometric_field
---------------

The `geometric_field <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/fieldwork/field/geometric_field.py?at=master&fileviewer=file-view-default>`_ module contains classes and functions for reading, writing, evaluating, and manipulating geometric Fieldwork models (see glossary). Fieldwork models are piece-wise parametric meshes interpolated by Lagrange polynomials. When used to describe geometry, Fieldwork models are instances of the ``GeometricField`` class in the geometric_field module. The bone meshes generated and used by many MAP Plugin plugins are such Fieldwork models.

vtktools
--------

The `vtktools <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/mesh/vtktools.py?at=master&fileviewer=file-view-default>`_ module contains classes and functions for polygon mesh processing using the `VTK library <http://www.vtk.org>`_. Especially useful are the ``Reader`` and ``Writer`` classes for reading and writing surface meshes in a variety of formats.

mocap_landmark_preprocess
-------------------------

The `mocap_landmark_preprocess <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/musculoskeletal/mocap_landmark_preprocess.py?at=master&fileviewer=file-view-default>`_ module contains functions for moving skin-surface marker coordinates to the bone surface using a given soft-tissue thickness and fixed translation vectors.

bonemodels
----------

The `bonemodels <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/musculoskeletal/bonemodels/bonemodels.py?at=master&fileviewer=file-view-default>`_ module contains classes of various bones and multi-bone systems represented by underlying ``GeometricField`` instances (see above). Each bone's class derives from the ``BoneModel`` class and has a anatomical coordinate system establised from anatomical landmarks on the GeometricField instance.

lowerlimbatlas
--------------

The `lowerlimbatlas <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/musculoskeletal/bonemodels/lowerlimbatlas.py?at=master&fileviewer=file-view-default>`_ module contains the ``LowerLimbAtlas`` class which represents the articulated lower-limb shape model. This class exposes all the degrees of freedom of the model.

osim
----

The `osim <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/musculoskeletal/osim.py?at=master&fileviewer=file-view-default>`_ module contains wrapper classes for OpenSim objects. This module provides Pythonic wrappers around commonly used OpenSim Python API Classes including the ``Model``, ``Body``, ``Joint``, and ``Muscle`` classes. These wrapper classes allow the OpenSim objects to be used without the cumbersome ``get`` and ``set`` methods.

fw_model_landmarks
------------------

The `fw_model_landmarks <https://bitbucket.org/jangle/gias2/src/18b11980cc2e742e5a17ecf197f2a4c88d9a672d/src/gias2/musculoskeletal/fw_model_landmarks.py?at=master&fileviewer=file-view-default>`_ module contains functions for evaluating anatomical landmarks from ``GeometricField`` bone meshes.

Fieldwork Gait2392 Geometry Customisation Step
==============================================

Detailed documentation on this plugin can be found on its `Github page <https://github.com/mapclient-plugins/fieldworkgait2392geomstep>`_. 

step.py
-------

The step.py module of this class does not differ greatly from the Plugin Wizard-generated boiler-plate code. The key differences are that there are more configurable parameters::

    self._config = {}
    self._config['identifier'] = ''
    self._config['GUI'] = False
    self._config['scale_other_bodies'] = True
    self._config['in_unit'] = 'mm'
    self._config['out_unit'] = 'm'
    self._config['osim_output_dir'] = ''
    self._config['write_osim_file'] = True
    self._config['subject_mass'] = None
    self._config['preserve_mass_distribution'] = False
    self._config['adj_marker_pairs'] = {}

And one of the step class attributes is an instance of the ``Gait2392GeomCustomiser`` class::

    self._g2392Cust = Gait2392GeomCustomiser(self._config)

which does the main work of this step. Step configurations are directly accessible by ``self._g2392Cust``, and its methods are called on step execution.

Let's look at ``Gait2392GeomCustomiser`` in more detail.

gait2392geomcustomiser.py
-------------------------

This module contains the ``Gait2392GeomCustomiser`` class and helper functions for extracting geometric parameters from lower limb bone mesh and customising the default Gait2392 OpenSim model.

Key Class Attributes
~~~~~~~~~~~~~~~~~~~~

- ``LL`` : the ``LowerLimbAtlas`` instance to be used to customise the Gait2392 model.

- ``osimmodel`` : the osim module-wrapped Gait2392 ``Model`` instance. The raw OpenSim ``Model`` can be accessed at ``self.osimmodel._model``.

- ``config`` : the step config ``dict``.

- ``markerset`` : the Gait2392 markerset as a osim module-wrapped MarkerSet instance.

Key Class Methods
~~~~~~~~~~~~~~~~~

- ``set_lowerlimb_atlas(self, ll)`` : sets the LowerLimbAtlas instance provided as a step input.

- ``set_lowerlimb_gfields(self, gfieldsdict)`` : uses the given ``dict`` of GeometricField instances to replace bone meshes in ``self.LL``. This is called in the Opensim Model Generation example workflow where we provide the fitted bone meshes to the lower limb atlas estimated from mocap markers.

- ``customise(self)`` : the method called on step execution. Key parts of this method are described below.

  ::

        self.prescale_muscles()

  Calls OpenSim's ``prescale`` function on each muscle in the model to save their lengths before bodies are scaled.

  ::

        self.cust_osim_pelvis()
        self.cust_osim_femur_l()
        self.cust_osim_femur_r()
        self.cust_osim_tibiafibula_l()
        self.cust_osim_tibiafibula_r()
        self.cust_osim_ankle_l()
        self.cust_osim_ankle_r()
        self.cust_osim_torso()

  Call class methods to customise the mass, inertial, joint, and visual geometry properties of each body in Gait2392.

  ::

        self.normalise_mass()

  If subject mass is given in the step config, normalise the scaled mass of each body to sum to the subject mass. If ``preserve_mass_distribution`` is true in the config, then the mass of each body is simply scaled by the ratio between the subject mass and the unscaled Gait2392 subject mass.

  ::

        self.postscale_muscles()

  Calls OpenSim's ``postscale`` function on each muscle in the model to calculate their new optimal fibre length and tendon slack length properties after bodies have been scaled.

  ::

        self.add_markerset()

  Scale and add the default Gait2392 markerset to the customised OpenSim model. The marker set will be written in the model .osim file.

  ::

        self.write_cust_osim_model()

  Write the customised Gait2392 model to file.

- ``cust_osim_pelvs(self)`` : customises the Pelvis body in the Gait2392 OpenSim model. Key parts of this method are described below.

  ::

        pelvis = self.LL.models['pelvis']
        osim_pelvis = self.osimmodel.bodies[OSIM_BODY_NAME_MAP['pelvis']]

  Retrieve pointers to the pelvis GIAS2 bone mode and the pelvis opensim Body.

  ::

        sf = self._get_osimbody_scale_factors('pelvis')
        scaler.scale_body_mass_inertia(osim_pelvis, sf)

  Calculate the orthogonal scale factors for the pelvis and use the scale factors to scale pelvis mass and inertia.

  ::

        pelvis_origin = pelvis.acs.o  
        self.osimmodel.joints['ground_pelvis'].locationInParent = \
            pelvis_origin*self._unit_scaling # in ground CS
        self.osimmodel.joints['ground_pelvis'].location = \
            np.array((0,0,0), dtype=float)*self._unit_scaling  # in pelvis CS

  Calculate the ground-pelvis joint coordinates from the pelvis bonemodel.

  ::

        pelvis_ground_joint = self.osimmodel.joints['ground_pelvis']
        if self._hasInputLL:
            tilt, _list, rot = self.LL.pelvis_rigid[3:]
        else:
            tilt, _list, rot = calc_pelvis_ground_angles(pelvis)

        ## tilt
        pelvis_ground_joint.coordSets['pelvis_tilt'].defaultValue = tilt
        ## list
        pelvis_ground_joint.coordSets['pelvis_list'].defaultValue = _list
        ## rotation
        pelvis_ground_joint.coordSets['pelvis_rotation'].defaultValue = rot

  Retrieve a pointer to the ground-pelvis joint, calculate ground-pelvis joint angles, and assign those angles to the joint.

  ::

        lhgf, sacgf, rhgf = _splitPelvisGFs(self.LL.models['pelvis'].gf)

  Split the pelvis GeometricField meshes into the left-hemipelvis, sacrum, and right-hemipelvis meshes.

  ::

        self._check_geom_path()

        ## sacrum.vtp
        sac_vtp_full_path = os.path.join(
            self.config['osim_output_dir'], GEOM_DIR, SACRUM_FILENAME
            )
        sac_vtp_osim_path = os.path.join(GEOM_DIR, SACRUM_FILENAME)
        self._save_vtp(sacgf, sac_vtp_full_path, pelvis.acs.map_local)

        ## pelvis.vtp
        rh_vtp_full_path = os.path.join(
            self.config['osim_output_dir'], GEOM_DIR, HEMIPELVIS_RIGHT_FILENAME
            )
        rh_vtp_osim_path = os.path.join(GEOM_DIR, HEMIPELVIS_RIGHT_FILENAME)
        self._save_vtp(rhgf, rh_vtp_full_path, pelvis.acs.map_local)

        ## l_pelvis.vtp
        lh_vtp_full_path = os.path.join(
            self.config['osim_output_dir'], GEOM_DIR, HEMIPELVIS_LEFT_FILENAME
            )
        lh_vtp_osim_path = os.path.join(GEOM_DIR, HEMIPELVIS_LEFT_FILENAME)
        self._save_vtp(lhgf, lh_vtp_full_path, pelvis.acs.map_local)

        osim_pelvis.setDisplayGeometryFileName(
            [sac_vtp_osim_path, rh_vtp_osim_path, lh_vtp_osim_path]
            )

  Generate triangulated meshes of the three pelvis bones and write out in the VTP format. Record the VTP file paths in the OpenSim model. The coordinates of the mesh vertices are in the pelvis frame.

  The other bones are customised in similar class methods.


