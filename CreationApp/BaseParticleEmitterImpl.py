
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

import FabricEngine.CreationPlatform
from FabricEngine.CreationPlatform.RT.Math import *
from FabricEngine.CreationPlatform.Nodes.Animation.BaseTimeImpl import BaseTime
from FabricEngine.CreationPlatform.Nodes.SceneGraphNodeImpl import SceneGraphNode
from FabricEngine.CreationPlatform.Nodes.Geometry.PointCloudImpl import PointCloud


class BaseParticleEmitter(PointCloud):
  """ A simple Particle Emitter system """
  def __init__(self, scene, **options):
  # call the baseclass constructor

    # ensure that base class is never instantiated
    if self.__class__.__name__ == 'BaseParticleEmitter':
      raise FabricEngine.CreationPlatform.SceneGraphException('You cannot instantiate the BaseParticleEmitter node directly.')

    super(BaseParticleEmitter, self).__init__(scene, **options)

    self.addValue('points_count', 'Size', options.setdefault('pointCount', 100), addGetterSetterInterface=True)
    self.addValue('initial_velocity', 'Vec3', Vec3(0,10,0), addGetterSetterInterface=True)
    self.addValue('initial_velocity_variance', 'Vec3', Vec3(1.0, 0.0, 1.0), addGetterSetterInterface=True)
    self.addAttribute('velocities', 3, genVBO=True)

    def __setTimeNode(data):
      timeController = data['node'] 
      self.getGeometryDGNode().setDependency( timeController.getDGNode(), 'time')
    self.addReferenceInterface(name='Time', cls=BaseTime, isList=False, changeCallback=__setTimeNode)

    if options.setdefault('time', None) is not None:
      self.setTimeNode(options['time'])

    # the Time class doesn't store the fps in its DG node. It is a standard python attribute that we set into the emitter node 
    fps = self.getTimeNode().getFPS()
    self.addValue('fps', 'Scalar', fps)



