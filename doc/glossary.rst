********
Glossary
********

-  **Fieldwork Model/Mesh** : A Fieldwork model or mesh is a piece-wise
   parametric mesh used by the GIAS2 library. Most bone meshes used by
   current MAP Client plugins are Fieldwork models. A Fieldwork mesh is
   composed of an ensemble of elements interpolated by Lagrange
   polynomials controlled by the coordinates of nodes within each
   element.

   A Fieldwork model has 3 main components: 1) its nodal coordinates
   which define the meshes geometry, 2) the type of Lagrange polynomials
   used to interpolate each element, 3) and the connectivity and shapes
   of the element. As such, a Fieldwork model is serialised into 3
   files:

   -  **.geof** : a GeometricField file that contains the nodal
      coordinates, and therefore the geometry of the mesh;
   -  **.ens** : an Ensemble file that contains information about the
      polynomial functions of the mesh's elements.;
   -  **.mesh** : a Mesh file that contains the connectivity of mesh
      elements and the shape of each element.

   Fieldwork meshes can share the same .ens and .mesh files if they have
   the same mesh topology and polynomial functions. Therefore, it is not
   alway necessary to write out the .ens and .mesh files. For example,
   if a workflow reads in an existing Fieldwork mesh (see Fieldwork
   Model Source Step), fits it to some pointcloud, then writes the mesh
   to file, only the .geof file needs to be written since the mesh
   topology and polynomial functions have not changed, only its
   geometry.
