Advanced Plugin Development
===========================

This section looks at more advanced plugin development for FAI model generation. We will walk through the `Fieldwork Gait2392 Geometry Customisation Step <https://github.com/mapclient-plugins/fieldworkgait2392geomstep>`_ and see how it uses the :doc:`gias2` and OpenSim libraries to customise the OpenSim Gait2392 model.

GIAS2
-----

`GIAS2 <https://bitbucket.org/jangle/gias2>`_ is a free and open-source Python library used by most MAP Client plugins written by Ju Zhang. It has a wide range of functionalities aimed at musculoskeletal modelling. It's functionalities can be broadly categoried into:

- Geometric transformations
- Rigid and non-rigid Registration
- Image segmentation (active shape models and random forest regression)
- Mesh processing
- Statistical shape models
- Lower-limb bone models

The Fieldwork Gait2392 Geometry Customisation Step uses classes and functions from a number of GIAS2 modules::

    from gias2.common import transform3D
    from gias2.fieldwork.field import geometric_field
    from gias2.mesh import vtktools
    from gias2.musculoskeletal import mocap_landmark_preprocess
    from gias2.musculoskeletal.bonemodels import bonemodels
    from gias2.musculoskeletal.bonemodels import lowerlimbatlas
    from gias2.musculoskeletal import osim
    from gias2.musculoskeletal import fw_model_landmarks as fml

Here is a brief summary of each of these modules

transform3D
~~~~~~~~~~~

geometric_field
~~~~~~~~~~~~~~~

vtktools
~~~~~~~~

mocap_landmark_preprocess
~~~~~~~~~~~~~~~~~~~~~~~~~

bonemodels
~~~~~~~~~~

lowerlimbatlas
~~~~~~~~~~~~~~

osim
~~~~

fw_model_landmarks
~~~~~~~~~~~~~~~~~~


Fieldwork Gait2392 Geometry Customisation Step
----------------------------------------------

Detailed documentation on this plugin can be found on its Github page (see link above). 

step.py
~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the ``Gait2392GeomCustomiser`` class and helper functions for extracting geometric parameters from lower limb bone mesh and customisin the default Gait2392 OpenSim model.

