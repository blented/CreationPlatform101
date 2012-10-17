
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#
from FabricEngine.CreationPlatform.RT.Math import *
from FabricEngine.CreationPlatform.Nodes.Kinematics.TransformImpl import Transform
from FabricEngine.CreationPlatform.Nodes.Primitives.CircleImpl import Circle
from FabricEngine.CreationPlatform.Nodes.Rendering.MaterialImpl import Material
from FabricEngine.CreationPlatform.Nodes.Rendering.InstanceImpl import Instance
from FabricEngine.CreationPlatform.Nodes.Manipulation.ManipulatorImpl import Manipulator
from FabricEngine.CreationPlatform.Nodes.Manipulation.BaseGizmoInstanceImpl import BaseGizmoInstance
from FabricEngine.CreationPlatform.Nodes.Manipulation.GizmoManipulatorImpl import GizmoManipulator
from FabricEngine.CreationPlatform.Nodes.Manipulation.SelectionGizmoInstanceImpl import SelectionGizmoInstance

from BaseParticleEmitterImpl import BaseParticleEmitter


class DiscEmitter(BaseParticleEmitter):
  def __init__(self, scene, **options):
  # call the baseclass constructor
    super(DiscEmitter, self).__init__(scene, **options)

    self.addValue('seed', 'Integer', 123, addGetterSetterInterface = True)

    # add a manipulator
    self.circle = Circle(scene, radius=1.0)
    self.circleXform = Transform(scene, globalXfo=Xfo(Vec3(0.0,0.0,0.0)))
    self.circleMaterial = Material(scene, xmlFile='Standard/Flat', shaderGroup=scene.getNode('StandardShaders'), color=Color(0.35,0.75,0.95))
    self.circleInstance = Instance(scene,
      geometry=self.circle,
      transform=self.circleXform,
      material=self.circleMaterial,
    )

    # create the manipulator
    self.manipulator = GizmoManipulator(scene)
    selectionGizmoInstance = SelectionGizmoInstance(scene, shaderGroup=scene.getNode('OverlayShaders'))
    self.manipulator.addGizmoNode(selectionGizmoInstance)
    selectionGizmoInstance.addManipulationTargetNode(self.circleInstance)
    
    def __setXformNode(data):
      xform = data['node'] 
      self.getGeometryDGNode().setDependency( xform.getDGNode(), 'transform')

    self.addReferenceInterface('Transform', Transform, False, __setXformNode)
    self.setTransformNode(options.setdefault('emitterXform',   self.circleXform     ))

    self.bindDGOperator(self.getGeometryDGNode().bindings,
      name = 'DiscEmitterGenerator', 
      fileName = FabricEngine.CreationPlatform.buildAbsolutePath('ParticleEmitters.kl'), 
      layout = [
        'self.attributes',
        'time.time',
        'self.fps',
        'self.points_count',
        'self.seed',
        'self.initial_velocity',
        'self.initial_velocity_variance',
        'transform.localXfo',
        'self.generation'
      ], 
    )
