import copy, time
import FabricEngine.Core
import FabricEngine.CreationPlatform
import FabricEngine.CreationPlatform.RT
import FabricEngine.CreationPlatform.RT.Math

from FabricEngine.CreationPlatform.RT.Math.Vec3Impl import Vec3

# This function is needed as we are using Vec3 type in the particle simulation
# You don't really need to understand it for now
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


# All the work to define our dependency graph is really starting here!

particlesNode = FabricCoreClient.DG.createNode('particles')
particlesNode.addMember('pointsCount', 'Size', 100)
particlesNode.addMember('positions', 'Vec3[]')

timerNode = FabricCoreClient.DG.createNode('timer')
timerNode.addMember('frame', 'Integer', 0)
timerNode.addMember('rate', 'Scalar', 60.0)

forcesNode = FabricCoreClient.DG.createNode('forces')
forcesNode.addMember('gravity', 'Vec3', Vec3(0.0, -9.81, 0.0))

particlesNode.setDependency(timerNode, 'timer')
particlesNode.setDependency(forcesNode, 'forces')

# The operator that will create our particles
operator = FabricCoreClient.DG.createOperator(name='ParticleSystem')
operator.setEntryPoint('ParticleSystem')
operator.setSourceCode(open('particlesOperators.kl').read())

# We instanciate a Binding object. It will glue the data with the operator.
binding = FabricCoreClient.DG.createBinding()
binding.setOperator(operator)

binding.setParameterLayout([
  'timer.frame',
  'timer.rate',
  'self.pointsCount',
  'self.positions',
  'forces.gravity'
])

particlesNode.bindings.append(binding)

# The simulation part

for i in range(0, 100):
  timerNode.setData('frame', i)
  particlesNode.evaluate()
  print 'At frame: {0}, first particle position is: {1}'.format(i, particlesNode.getData('positions')[0])
