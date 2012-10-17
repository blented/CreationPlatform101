import copy, time
import FabricEngine.Core
import FabricEngine.CreationPlatform
import FabricEngine.CreationPlatform.RT
import FabricEngine.CreationPlatform.RT.Math

from FabricEngine.CreationPlatform.RT.Math.Vec3Impl import Vec3

def registerType(name, desc):
  """Registers a new data type by a given name and description dictionary."""
  # we make a deep copy here because we will remove members from the desc during registration.
  desc = copy.deepcopy(desc)
  constructor = desc['constructor']
  if desc.has_key('klBindings'):
    klCode = desc['klBindings']
    if klCode.has_key('fileName'):
      klCode['sourceCode'] = open(klCode['fileName']).read()
      klCode['filename'] = klCode['fileName']
      del klCode['fileName']
    if klCode.has_key('sourceCode') and klCode.has_key('preProcessorDefinitions'):
      for defName in klCode['preProcessorDefinitions']:
        klCode['sourceCode'] = klCode['sourceCode'].replace(defName, klCode['preProcessorDefinitions'][defName])
      del klCode['preProcessorDefinitions']
  
  FabricCoreClient.RegisteredTypesManager.registerType( name, copy.deepcopy(desc) )
  return constructor

# FabricCoreClient is the object that let you communicate with the core
FabricCoreClient = FabricEngine.Core.createClient()

# We register Creation Platform types to be able to use Vec3.
for regType in FabricEngine.CreationPlatform.RT.getRegisteredTypes():
  registerType(regType['name'], regType['desc'] )


particleGeoNode = FabricCoreClient.DG.createNode('particleGeom')
particleGeoNode.addMember('position', 'Vec3')

# We use an other node for the points count as we will resize the particleGeoNode to the number of points 
particleUniformNode  = FabricCoreClient.DG.createNode('particleUniform')
particleUniformNode.addMember(memberName='pointsCount', memberType='Size', defaultValue=10)

timerNode = FabricCoreClient.DG.createNode('timer')
timerNode.addMember('frame', 'Integer', 0)

particleGeoNode.setDependency(dependencyNode=particleUniformNode, dependencyName='particleUniform')
particleGeoNode.setDependency(dependencyNode=timerNode, dependencyName='timer')

forcesNode = FabricCoreClient.DG.createNode('forces')
forcesNode.addMember('gravity', 'Vec3', Vec3(0.0, -9.81, 0.0))

particleGeoNode.setDependency(forcesNode, 'forces')

# The operator that will create our particles
operator = FabricCoreClient.DG.createOperator('SlicedParticleSystem')
operator.setEntryPoint('SlicedParticleSystem')
operator.setSourceCode('None', sourceCode = open('particlesOperatorSlices.kl').read())

# We instanciate a Binding object. It will glue the data with the operator.
binding = FabricCoreClient.DG.createBinding()
binding.setOperator(operator)

binding.setParameterLayout([
  'timer.frame',
  'particleUniform.pointsCount',
  'self', # self is used in the KL code to resize the number of sliced of the operator owner
  'self.index', # index is a reserved name. It tells that the parameter will be index of the current slice for which the operator is being executed
  'self.position<>', # <> token tells the core to compute over an array of data in parallel
  'forces.gravity'
])

particleGeoNode.bindings.append(binding)

for i in range(0, 100):
  print 'At frame:', i
  timerNode.setData('frame', i)
  particleGeoNode.evaluate()

