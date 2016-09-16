"""
surface_to_surface_distance.py
==============================
Author: Ju Zhang
Last Modified: 2016-09-16

Script for calculating the distances between 2 surfaces.

===============================================================================
This file is part of GIAS2. (https://bitbucket.org/jangle/gias2)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
===============================================================================
"""

_descStr = """Script for calculating the distances between 2 surfaces.
Author: Ju Zhang
Last Modified: 2016-09-16

This script takes 2 surfaces (groundtruth and test) and calculates the Jaccard
index and the 2-way surface to surface distances. The 2-way distance means for
each vertex on the groundtruth find the closest vertex on the test and then
vice versa. Thus a total of m+n distances are calculated, where m and n are the
number of vertices on the groundtruth and test surfaces respectively. The max,
mean, and rms of these distances and the Jaccard index are printed to terminal
or file.

Things to note
--------------
- Surface vertex density definitely matters since only vertex-to-vertex
  distances are calculated. Sparser the points, less accurate the results
  represent the true surface to surface distance.

- Units dimension is expected to be in mm. If not, units for the groundtruth
  and test surface coordinates can be defined by the --groundtruth-unit and
  --test-unit options.

- The format of the surface files can be stl, ply, obj, vrml, or vtp.

- The results are printed to the terminal (and to file if the -o option is
  specified), e.g.:

    dmax: 18.0328460848
    dmean: 1.15626509502
    drms: 1.69911836126
    jaccard: 0.915674848409
"""

from os import path
import sys
from scipy.spatial.distance import jaccard
from scipy.spatial import cKDTree
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
import vtk

from gias2.mesh import vtktools

try:
    from gias2.visualisation import fieldvi
    can_visual = True
except ImportError:
    print('no visualisation available')
    can_visual = False

def dim_unit_scaling(in_unit, out_unit):
    """
    Calculate the scaling factor to convert from the input unit (in_unit) to
    the output unit (out_unit). in_unit and out_unit must be a string and one
    of ['nm', 'um', 'mm', 'cm', 'm', 'km']. 

    inputs
    ======
    in_unit : str
        Input unit
    out_unit :str
        Output unit

    returns
    =======
    scaling_factor : float
    """

    unit_vals = {
        'nm': 1e-9,
        'um': 1e-6,
        'mm': 1e-3,
        'cm': 1e-2,
        'm':  1.0,
        'km': 1e3,
        }

    if in_unit not in unit_vals:
        raise ValueError(
            'Invalid input unit {}. Must be one of {}'.format(
                in_unit, list(unit_vals.keys())
                )
            )
    if out_unit not in unit_vals:
        raise ValueError(
            'Invalid input unit {}. Must be one of {}'.format(
                in_unit, list(unit_vals.keys())
                )
            )

    return unit_vals[in_unit]/unit_vals[out_unit]

def triSurface2BinaryMask(v, t, imageShape, voxelOrigin=None, voxelSpacing=None, bg=0):

    imgDtype = np.int16
    if voxelOrigin is None:
        voxelOrigin = [0.0,0.0,0.0]
    if voxelSpacing is None:
        voxelSpacing = [1.0,1.0,1.0]

    # make into vtkPolydata
    gfPoly = vtktools.tri2Polydata(v, t)

    # create mask vtkImage
    maskImageArray = np.ones(imageShape, dtype=imgDtype)
    maskVTKImage = vtktools.array2vtkImage(maskImageArray, imgDtype, flipDim=False)

    # create stencil from polydata
    stencilMaker = vtk.vtkPolyDataToImageStencil()
    stencilMaker.SetInput(gfPoly)
    stencilMaker.SetOutputOrigin(voxelOrigin)
    stencilMaker.SetOutputSpacing(voxelSpacing)
    stencilMaker.SetOutputWholeExtent(maskVTKImage.GetExtent())

    stencil = vtk.vtkImageStencil()
    stencil.SetInput(maskVTKImage)
    stencil.SetStencil(stencilMaker.GetOutput())
    stencil.SetBackgroundValue(bg)
    stencil.ReverseStencilOff()
    stencil.Update()

    maskImageArray = vtktools.vtkImage2Array(stencil.GetOutput(), imgDtype, flipDim=True )
    return maskImageArray, gfPoly

def _rms(x):
    return np.sqrt((x*x).mean())

def loadMesh(filename):
    r = vtktools.Reader()
    r.read(filename)
    return r.getSimplemesh()

def calcJaccard(s1, s2, orig, shape, spacing):
    I1 = triSurface2BinaryMask(
            s1.v, s1.f, shape, orig, spacing
            )[0].astype(int)
    I2 = triSurface2BinaryMask(
            s2.v, s2.f, shape, orig, spacing
            )[0].astype(int)
    j = 1.0 - jaccard(I1.ravel(), I2.ravel())
    return j, I1, I2

def calcDistance(s1, s2):
    tree1 = cKDTree(s1.v)
    tree2 = cKDTree(s2.v)
    d21, d21i = tree1.query(s2.v,k=1)
    d12, d12i = tree2.query(s1.v,k=1)

    # dmax = max([max(d21), max(d12)])
    # drmsmean = np.mean([_rms(d21), _rms(d12)])
    # dmeanmean = np.mean([d21.mean(), d12.mean()])

    dmax = np.hstack([d21, d12]).max()
    drms = _rms(np.hstack([d21, d12]))
    dmean = np.hstack([d21, d12]).mean()

    return dmax, drms, dmean, (d12, d21)

def calcSegmentationErrors(meshFileTest, meshFileGT, jacImgSpacing, gtScaling, testScaling):
    # load ground truth segmentation (tri-mesh)
    surfGT = loadMesh(meshFileGT)
    surfGT.v*=gtScaling

    # load test segmentation (tri-mesh)
    surfTest = loadMesh(meshFileTest)
    surfTest.v*=testScaling

    # work out volume size
    volMin = np.min([surfGT.v.min(0), surfTest.v.min(0)], axis=0)
    volMax = np.max([surfGT.v.max(0), surfTest.v.max(0)], axis=0)
    imgOrig = volMin-10.0
    imgShape = np.ceil(((volMax+10.0)-imgOrig)/jacImgSpacing)

    # calc jaccard coeff
    j, imgGT, imgTest = calcJaccard(surfGT, surfTest, imgOrig, imgShape, jacImgSpacing)

    # calc surface to surface distance
    dmax, drms, dmean, (d12, d21) = calcDistance(surfGT, surfTest)

    results = {'jaccard': j,
               'dmax': dmax,
               'drms': drms,
               'dmean': dmean,
              }

    return results, surfTest, surfGT, imgTest, imgGT

def visualise(V, surfTest, surfGT, imgTest, imgGT):
        V.addTri('test surface', surfTest, renderArgs={'color':(0.4,0.4,0.4)})
        V.updateTriSurface('test surface')
        V.addTri('ground truth surface', surfGT, renderArgs={'color':(0.84705882, 0.8, 0.49803922)})
        V.updateTriSurface('ground truth surface')
        V.addImageVolume(imgGT.astype(float), 'groundtruth')
        V.addImageVolume(imgTest.astype(float), 'test')

def writeResults(filepath, testname, gtname, res):
    text = 'groundtruth: {}, test: {}, rmsd: {:9.6f}, meand: {:9.6f}, maxd: {:9.6f}, jaccard{:9.6f}\n'
    with open(filepath, 'a') as f:
        f.write(
            text.format(
                gtname,
                testname,
                res['drms'],
                res['dmean'],
                res['dmax'],
                res['jaccard'],
                )
            )

#=============================================================================#
imgSpacing = np.array([0.5,]*3, dtype=float)
unitChoices = ('nm', 'um', 'mm', 'cm', 'm', 'km')
defaultUnit = 'mm'
#=============================================================================#
parser = argparse.ArgumentParser(
            description=_descStr,
            formatter_class=RawTextHelpFormatter,
            )
parser.add_argument('gTruthPath',
                    help='ground truth surface path')
parser.add_argument('testPath',
                    help='test surface path')
parser.add_argument('-o', '--outpath',
                    help='results output path. Results are append to text file')
parser.add_argument('-d', '--display',
                    action='store_true',
                    help='visualise results')
parser.add_argument('--groundtruth-unit',
                    action='store',
                    default='mm',
                    choices=unitChoices,
                    help='unit of ground truth coordinates')
parser.add_argument('--test-unit',
                    action='store',
                    default='mm',
                    choices=unitChoices,
                    help='unit of test coordinates')

if __name__ == '__main__':
    args = parser.parse_args()
    gtUnitScaling = dim_unit_scaling(args.groundtruth_unit, defaultUnit)
    testUnitScaling = dim_unit_scaling(args.test_unit, defaultUnit)
    results, surfTest, surfGT, imgTest, imgGT = calcSegmentationErrors(
                                    args.testPath,
                                    args.gTruthPath,
                                    imgSpacing,
                                    gtUnitScaling,
                                    testUnitScaling
                                    )
    for k, v in results.items():
        print '{}: {}'.format(k, v)

    if args.outpath is not None:
        testName = path.splitext(path.split(args.testPath)[1])[0]
        gtName = path.splitext(path.split(args.gTruthPath)[1])[0]
        writeResults(args.outpath, testName, gtName, results)
    
    if args.display and can_visual:
        V = fieldvi.Fieldvi()
        V.configure_traits()
        V.scene.background=(0,0,0)
        visualise(V, surfTest, surfGT, imgTest, imgGT)