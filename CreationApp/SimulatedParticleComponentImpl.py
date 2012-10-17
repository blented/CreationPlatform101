
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#


from FabricEngine.CreationPlatform.RT.Math import *
from FabricEngine.CreationPlatform.Nodes import Component
from FabricEngine.CreationPlatform.Nodes.Animation.BaseTimeImpl import BaseTime
from BaseParticleEmitterImpl import BaseParticleEmitter
from ForceImpl import Force

class SimulatedParticleComponent(Component):

  def __init__(self, **options):
    super(SimulatedParticleComponent, self).__init__(**options)

  def apply(self, pointCloud):
    super(SimulatedParticleComponent, self).apply(pointCloud)

    pointCloud.addAttribute('velocities', 3, genVBO=True)
    pointCloud.addValue('gravity', 'Vec3', Vec3(0.0, -9.81, 0.0), True)

    pointCloud.addReferenceInterface(name='Time', cls=BaseTime, isList=False, changeCallback=self.__onChangeTimeCallback, callbackData=pointCloud)
    pointCloud.setTimeNode(self._getOption('time'))

    pointCloud.addReferenceInterface(name='Emitter', cls=BaseParticleEmitter, isList=False, changeCallback=self.__onChangeEmitterCallback, callbackData=pointCloud)
    pointCloud.setEmitterNode(self._getOption('emitter'))

    pointCloud.addReferenceInterface(name='Force', cls=Force, isList=False, changeCallback=self.__onChangeForceCallback, callbackData=pointCloud)
    pointCloud.setForceNode(self._getOption('force'))

    # Operators bindings
    pointCloud.bindDGOperator(pointCloud.getGeometryDGNode().bindings,
          name = 'SimulatedParticleOp', 
          fileName = FabricEngine.CreationPlatform.buildAbsolutePath('SimulatedParticleComponent.kl'), 
          layout = [
            'self.attributes',
            'self.generation',
            'time.time',
            'time.timeStep',
            'emitter.attributes',
            'self.gravity',
            'force.direction',
            'force.intensity'
    ])

  def __onChangeTimeCallback(self, data):
    pointCloud = data['callbackData']
    timeController = data['node']
    pointCloud.getGeometryDGNode().setDependency( timeController.getDGNode(), 'time')

  def __onChangeEmitterCallback(self, data):
    pointCloud = data['callbackData']
    emitter = data['node']
    pointCloud.getGeometryDGNode().setDependency( emitter.getGeometryDGNode(), 'emitter')

  def __onChangeForceCallback(self, data):
    pointCloud = data['callbackData']
    force = data['node']
    pointCloud.getGeometryDGNode().setDependency( force.getDGNode(), 'force')


SimulatedParticleComponent.registerComponentClass('SimulatedParticleComponent')
