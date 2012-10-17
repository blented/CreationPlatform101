
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

import math, random
from PySide import QtGui, QtCore

import FabricEngine.CreationPlatform
from FabricEngine.CreationPlatform.RT.Math import *
from FabricEngine.CreationPlatform.Nodes.Rendering import *
from FabricEngine.CreationPlatform.Nodes.Kinematics import *
from FabricEngine.CreationPlatform.Nodes.Images import *
from FabricEngine.CreationPlatform.Nodes.Manipulation import *
from FabricEngine.CreationPlatform.Nodes.Primitives import *
from FabricEngine.CreationPlatform.Selection import *

from FabricEngine.CreationPlatform.PySide import *

from DiscEmitterImpl import DiscEmitter
from ForceImpl import Force
from SimulatedParticleComponentImpl import SimulatedParticleComponent

class DemoApplication(Basic3DDemoApplication):
  
  def __init__(self):
    
    super(DemoApplication, self).__init__(
      exts={'FabricMath':''},
      setupPersistence = True,
      setupGlobalTimeNode=True,
      setupGrid=True,
      setupSelection = True,
      enableRaycasting=True,
      cameraPosition=Vec3(19.0,13.0,-4.0),
      cameraTarget=Vec3(0.0,2.0,0.0),
      setupUndoRedo=True,
      timeRange=Vec2(0.0,10.0),
      fps = 60
    )

    self.setWindowTitle("Creation Platform Particle System Demo")
   
    # query the constructed components
    scene = self.getScene()

    standardShadersGroup = scene.getNode('StandardShaders')
    overlayShadersGroup = scene.getNode('OverlayShaders')
    time = self.getGlobalTimeNode()
    light = scene.getNode('CameraLight')
    gridSize = 60

    # build the Particle System
    pointCloud = PointCloud(scene)
    pointCloudTransform = Transform(scene)
    emitter = DiscEmitter(scene, pointCount=200, time=time)
    force = Force(scene, direction=Vec3(1,0,0), intensity=0)
    pointCloud.addComponent(SimulatedParticleComponent(time = time, emitter = emitter, force = force))


    Instance(scene,
      geometry=emitter,
      transform=Transform(scene),
      material=Material(scene,
        xmlFile='Points/FlatPoint',
        shaderGroup=standardShadersGroup, 
        prototypeMaterialType='PointMaterial',
        pointSize=2.0 ,
        color=Color(0.43, 0.87, 1.0)
      )
    )

    Instance(scene,
      geometry=pointCloud,
      transform=pointCloudTransform,
      material=Material(scene,
        xmlFile='Points/FlatPoint',
        shaderGroup=standardShadersGroup, 
        prototypeMaterialType='PointMaterial',
        pointSize=2.0 ,
        color=Color(0.43, 0.87, 1.0)
      )
    )

    self.getCameraManipulator().setChildManipulatorNode(emitter.manipulator)
    self.addDockWidget(QtCore.Qt.TopDockWidgetArea, StatisticsDockWidget(scene, {}))

    # create a nodeinspector widget
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, SGNodeInspectorDockWidget({ 'node':pointCloud }))
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, SGNodeInspectorDockWidget({ 'node':force }))        
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, SGNodeInspectorDockWidget({ 'node':emitter }))    
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, SGNodeInspectorDockWidget({ 'node':emitter.circleXform }))    
 
    # resize
    self.resize(1000,600)
    
    # check for errors
    self.constructionCompleted()

    
DemoApplication().exec_()