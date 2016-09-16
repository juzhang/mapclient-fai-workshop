"""
view_fieldwork_model_elements_script.py
==============================
Author: Ju Zhang
Last Modified: 2016-09-16

Script for viewing element numbers and boundaries on a fieldwork
model.

===============================================================================
This file is part of GIAS2. (https://bitbucket.org/jangle/gias2)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
===============================================================================
"""

_descStr = "Script for viewing element numbers and boundaries on a fieldwork model."

import sys
from gias2.fieldwork.field import geometric_field
import argparse
from argparse import RawTextHelpFormatter

try:
    from gias2.visualisation import fieldvi
except ImportError:
    print('no visualisation available, quitting.')
    sys.exit(1)

def _parse_disc(string):
    return [int(x) for x in string.split('x')]

def main(args):
    element_boundary_discretisation = [10,]
    element_boundary_render_args = {'tube_radius':0.4, 'color':(0.7,0.7,0.7)}
    model_discretisation = _parse_disc(args.disc)

    # load model
    input_model = geometric_field.load_geometric_field(
                    args.geof, args.ens, args.mesh
                    )
    # create a model evaluator
    input_model_evaluator = geometric_field.makeGeometricFieldEvaluatorSparse(
                                input_model, model_discretisation
                                )

    # visualise
    viewer = fieldvi.Fieldvi()
    viewer.GFD = model_discretisation
    model_render_args = {'opacity':float(args.opacity)}
    # viewer.displayGFNodes = False # uncomment to not draw nodes
    viewer.addGeometricField('model', input_model,
                            input_model_evaluator,
                            renderArgs=model_render_args
                            )
    viewer.configure_traits()
    # make sure model is visible
    viewer._drawGeometricField('model')
    # draw element numbers on model
    viewer.drawGeometricFieldElementNumbers(
        'model', textScale=3.0, textColor=(0,0,0)
        )
    # draw element boundaries
    nodes_to_elemtype_map = {3:'line3l', 4:'line4l', 5:'line5l'}    # what type of line element to draw for a given number of edge nodes
    elem_basis_map = {'line3l':'line_L2', 'line4l':'line_L3', 'line5l':'line_L4'}   # what type of 1-d basis function to use with a given element type
    viewer.drawElementBoundaries('model',
                                 element_boundary_discretisation,
                                 geometric_field.makeGeometricFieldEvaluatorSparse,
                                 nodes_to_elemtype_map,
                                 elem_basis_map,
                                 element_boundary_render_args
                                 )

#=============================================================================#
parser = argparse.ArgumentParser(
            description=_descStr,
            formatter_class=RawTextHelpFormatter,
            )
parser.add_argument('geof',
                    help='.geof file path')
parser.add_argument('ens',
                    help='.ens file path')
parser.add_argument('mesh',
                    help='.mesh file path')
parser.add_argument('--disc',
                    action='store',
                    default='8x8',
                    help='mesh discretisation')
parser.add_argument('--opacity',
                    action='store',
                    default='0.8',
                    help='mesh opacity')

#=============================================================================#

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)