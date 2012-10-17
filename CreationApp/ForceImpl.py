
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

import FabricEngine.CreationPlatform
from FabricEngine.CreationPlatform.RT.Math import *
from FabricEngine.CreationPlatform.Nodes.SceneGraphNodeImpl import SceneGraphNode

class Force(SceneGraphNode):
  """ A simple Directional Force Class """
  def __init__(self, scene, **options):
    super(Force, self).__init__(scene, **options)

    self.constructDGNode()
    self.getDGNode().addMember('direction', 'Vec3', options.setdefault('direction', Vec3(0, 1, 0)))
    self._addMemberInterface(self.getDGNode(), 'direction', defineSetter = True)
    self.getDGNode().addMember('intensity', 'Scalar', options.setdefault('intensity',10))    
    self._addMemberInterface(self.getDGNode(), 'intensity', defineSetter = True)





