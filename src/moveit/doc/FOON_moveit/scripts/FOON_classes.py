##########################################################################################################################
#  @Author: Sherif Shousha																								 #
#  @Supervisor:Pantano Matteo																							 #		
#   																													 #
#  NOTE: This file includes all classes which are required to create a FOON.											 #
#																														 #
##########################################################################################################################


class Thing(object):
	# -- A thing is a general node; it can be either an object or a motion node.
	# -- Thing objects have three (3) elements:
	#	1. an identifier (ID).
	#	2. Label, which tells the user what type of Thing it is.
	#	3. List of other used objects in the same action. (i.e. neighbouring nodes).

	# -- constructor methods for creating Thing object:
	def __init__(self, Id=None, L=None):
		# variables
		self.id = Id	
		self.label = L 
		self.neighbours = []
	#enddef

	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
	#enddef


	def getId(self):
		return self.id
	#enddef
	
	def setId(self, Id):
		self.id = Id
	#enddef

	def getLabel(self):
		return self.label
	#enddef

	def setLabel(self, L):
		self.label = L
	#enddef

	def getNeighbourList(self):
		return self.neighbours
	#enddef

	def addNeighbour(self, N_id, newN):
		self.neighbours[N_id].append(newN)
	#enddef

	def addNeighbours(self, newN):
		self.neighbours.append(newN)
	#enddef

	def countNeighbours(self):
		return len(self.neighbours)
	#enddef

	def equals(self, T):
		return self.id == T.getId()
	#enddef

	def is_motionNode(self):
		return isinstance(self, Motion)
	#enddef

	def is_objectNode(self):
		return not self.is_motionNode()
	#enddef

#endclass Thing

class Object(Thing):
	# NOTE: an Object object is any item that is used in the cooking/manipulation procedure.
	# NOTE: an Object is a Thing inherently, so it must have a type and label as well as a list of its neighbours.

	# NOTE: constructor for Object node objects:
	def __init__(self, OId=None, OL=None):

		super(Object,self).__init__(OId, OL)

		# NOTE: member variables unique to objects: object state, object location, object size, and object possible order.
		self.objectStates = []
		self.objectLocation = []
		self.size = []
		self.objectOrder = ""
	#enddef
	
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
	#enddef

	def getObjectId(self):
		return super(Object,self).getId()
	#enddef

	def setObjectId(self, N):
		super(Object,self).setId(N)
	#enddef

	def getObjectLabel(self):
		return super(Object,self).getLabel()
	#enddef

	def setObjectLabel(self, L):
		super(Object,self).setLabel(L)
	#enddef

	# NOTE: objects can have multiple states, so we are working with a list of states:
	def getStatesList(self):
		return self.objectStates
	#enddef

	def setStatesList(self, S):
		for state in S:
			self.objectStates.append(state)
	#enddef

	def getOrder(self):
		return self.objectOrder
	#enddef

	def setOrder(self, X):
		self.objectOrder = X
	#enddef

	def getObjectLocation(self):
		if self.objectLocation:
			return list(self.objectLocation)
		return None
	#enddef

	def setObjectLocation(self, L):
		self.objectLocation = L
	#enddef	
	
	def getSize(self):
		if self.size:
			return list(self.size)
	
	def setObjectSize(self, S):
		self.size = S
	#enddef

	def isSameStates(self, O):
		count = 0
		self.objectStates.sort(); O.objectStates.sort()
		for S in self.objectStates:
			for SU in O.objectStates:
				if S[0] == SU[0] and S[1] == SU[1] and S[2] == SU[2]:
					count += 1

		if count == len(O.objectStates) and len(self.objectStates) == len(O.objectStates):
			return True
		return False
	#enddef

	def isSameStates_ID_only(self, O):
		count = 0
		self.objectStates.sort(); O.objectStates.sort()
		for S in self.objectStates:
			for SU in O.objectStates:
				if S[0] == SU[0]:
					count += 1

		if count == len(O.objectStates) and len(self.objectStates) == len(O.objectStates):
			return True
		return False
	#enddef

	def isSameLocation(self, O):
		return self.getObjectLocation() == O.getObjectLocation()
	#enddef
# endclass Object



class Motion(Thing):
	# NOTE: A Motion node is the other node that is found in the bipartite FOON graph.
	# NOTE: A Motion node reflects a manipulation or non-manipulation action that is needed to change (some) objects from one state to another

	# NOTE: constructor method for Motion node objects:
	def __init__(self, MId=None, M=None, O=None, S=None, E=None):

		super(Motion,self).__init__(MId, M)
		
		#NOTE: member variables unique to motion: start and end position, start and end surface, motion order.
		self.Motion_Start_Pose = []
		self.Motion_End_Pose = []
		self.Motion_Start_SupportSurface = S
		self.Motion_End_SupportSurface = E
		self.motionOrder = O
	#enddef

	def getMotionId(self):
		return super(Motion,self).getId()
	#enddef

	def setMotionId(self, M):
		super(Motion,self).setId(M)
	#enddef

	def getMotionOrder(self):
		return self.motionOrder
	#enddef

	def setMotionOrder(self, O):
		self.motionOrder = O
	#enddef
	
	def getMotionStartPose(self):
		if self.Motion_Start_Pose:
			return list(self.Motion_Start_Pose)
		return None
	#enddef

	def setMotionStartPose(self, L):
		self.Motion_Start_Pose = L
	#enddef

	def getMotionEndPose(self):
		if self.Motion_End_Pose:
			return list(self.Motion_End_Pose)
		return None
	#enddef

	def setMotionEndPose(self, L):
		self.Motion_End_Pose = L
	#enddef

	def getStartSupportSurface(self):
		return self.Motion_Start_SupportSurface
	#enddef

	def setStartSupportSurface(self, S):
		self.Motion_Start_SupportSurface = S
	#enddef

	def getEndSupportSurface(self):
		return self.Motion_End_SupportSurface
	#enddef

	def setEndSupportSurface(self, S):
		self.Motion_End_SupportSurface = S	
	#enddef

	def getMotionLabel(self):
		return super(Motion,self).getLabel()
	#enddef

	def setMotionLabel(self, M):
		super(Motion,self).setLabel(M)  
	#enddef
#endclass Motion


class FunctionalUnit(object):
	def __init__(self, Name):
		
		# functional uni name.
		self.name = Name
		# list of input and output object nodes (which use the Object class defined above).
		self.inputNodes = []; self.outputNodes = []
		# motion node that belongs to a functional unit instance.
		self.motionNode = None
		# functional unit order.
		self.FU_order = None	
	#enddef
	
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)
	#enddef

	def isEmpty(self):
		# -- quite simply, a functional unit is empty if it has no Motion node or no Input/Output nodes:
		return not self.motionNode or not self.inputNodes or not self.outputNodes
	#enddef

	def addObjectNode(self, O, N):
		if N == 1:
			if O not in self.inputNodes:
				print("inside class")
				print(O)
				print("--------")
				self.inputNodes.append(O)
		elif N == 2:
			if O not in self.outputNodes:
				self.outputNodes.append(O)
		else:
			print(' -- WARNING: incorrect usage of function : ' + "'addObjectNode()' !")
		#endif
	#enddef
	
	def getName(self):
		return self.name
	#enddef

	def setName(self, Name):
		self.name = Name
	#enddef

	def getMotion(self):
		return self.motionNode
	#enddef

	def setMotion(self, M):
		self.motionNode = M
	#enddef

	def getInputList(self):
		return self.inputNodes
	#enddef

	def getOutputList(self):
		return self.outputNodes
	#enddef

	def getNumberOfInputs(self):
		return len(self.inputNodes)
	#enddef

	def setInputList(self, L):
		self.inputNodes = L
	#enddef

	def getNumberOfOutputs(self):
		return len(self.outputNodes)
	#enddef

	def setOutputList(self, L):
		self.outputNodes = L
	#enddef

	def getFunctionalUnitOrder(self):
		return self.FU_order
	#enddef

	def setFunctionalUnitOrder(self, number):
		self.FU_order = number	
	#enddef

#endclass FunctionalUnit

class TreeNode(object):
	# NOTE: TreeNode calss includs all functional units in the FOON.

	def __init__(self, Goal):
	
		# tree Goal name
		self.goal = Goal	
		# point between the functional units to merge between them in the graph
		self.mergePoint	= ""	
		# Functional unit which used to acheive the main gaol
		self.treeFunctionalUnits = []
	#enddef

	def getTreeGoal(self):
		return self.goal
	#enddef

	def setTreeGoal(self, Goal):
		self.goal = Goal
	#enddef

	def getMergePoint(self):
		return self.mergePoint
	#enddef

	def setMergePoint(self, name):
		self.mergePoint = name
	#enddef

	def getTreeFunctionalUnits(self):
		return self.treeFunctionalUnits
	#enddef

	def setTreeFunctionalUnits(self, FUs):
		for FU in FUs:
			self.treeFunctionalUnits.append(FU)
	#enddef

#endclass TreeNode
      
