##########################################################################################################################
#  @Author: Sherif Shousha                                                                                               # 
#  @Supervisor:Pantano Matteo                                                                                            #
#                                                                                                                        #
#  NOTE: This file includes the main structure of FOON and the draw function to visualize the FOON.                      #          
#                                                                                                                        # 
##########################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import FOON_classes as FOON
from Objects_list import Objects ,Motions


# global values

# NOTE: list of input nodes used for each functional unit
nodes_FU1 = []; nodes_FU2 = []
# NOTE: list of all input nodes used for all functional units 
input_nodes_FU = []
 
# NOTE: list of motion sequence node in each functional unit:
motion_to_FU1= []; motion_to_FU2 = []
# NOTE: list of all motions used for all functional units
motions_FU = []

# NOTE: list of functional units names
functionalUnitsNames = []
# NOTE: list of functional units. We save hier all functional unit after build them
functionalUnits = []

# NOTE: this variables are used to draw the graoh
G = nx.DiGraph()
fig = plt.figure(figsize=(35, 15))


def buildObjects():

    # get objects from the list
    objects_list = Objects()

    # NOTE: fixed objects which are the support surfaces like tables
    fixed_objects = []
    # NOTE: all objects in the sorrunding environment
    objects_info = []
    
    # create object calss for every object in the list
    for obj in objects_list:
       

        newObject = FOON.Object( obj.id, obj.name)
        newObject.setObjectLocation(obj.pose)
        newObject.setObjectSize(obj.size)
        newObject.setStatesList(obj.state)
        newObject.setOrder(obj.order)
        for neighbour in obj.neighbour:
            if len(obj.neighbour):
                newObject.addNeighbours( neighbour)
        if obj.state[0] == "fixed":
            fixed_objects.append(newObject)
        # TODO: that can be done dynamically (using sort algorithm for the list)
        if obj.order == "sort augustiner":
            nodes_FU1.append(newObject)
        if obj.order == "sort rothaus":
            nodes_FU2.append(newObject)

        objects_info.append(newObject)
        
    
    #endfor
    input_nodes_FU.append(nodes_FU1)
    input_nodes_FU.append(nodes_FU2)
    # start build motion classes after finish the object classes.
    buildMotion()

    print("+++++++++++++++++ input nodes +++++++++++++++++++++++++++++++++")
    print(input_nodes_FU)
    
    return objects_info
#enddef

def buildMotion():
    # get the motions from the list
    motion_list = Motions()

    # create a Motion class for every motion in the list
    for M in motion_list:
        newMotion = FOON.Motion(M.motionId, M.objectId, M.motionOrder, M.startSurface, M.endSurface)
        newMotion.setMotionStartPose(M.startPose)
        newMotion.setMotionEndPose(M.endPose)
        # TODO: that can be done dynamically (using sort algorithm for the list)
        if M.motionId == "sort augustiner":
            if M.motionId not in functionalUnitsNames:
                functionalUnitsNames.append(M.motionId)
            
            motion_to_FU1.append(newMotion)
        if M.motionId == "sort rothaus":
            if M.motionId not in functionalUnitsNames:
                functionalUnitsNames.append(M.motionId)
            motion_to_FU2.append(newMotion)
    #endfor

    # save all motion nodes. 
    motions_FU.append(motion_to_FU1)
    motions_FU.append(motion_to_FU2)
    print("################# all motion nodes in the FOON ################################")
    print(motions_FU)
#enddef


def buildFunctionalUnit():

    # counter to know the number of the functional unit in the FOON.
    functionalUnitNumber = 0

    # build a functional unit class for every required functional unit.
    for functionalUnitName in functionalUnitsNames:
        # NOTE: prepare the input nodes, motion nodes and output nodes.
        # NOTE: the output node(s) information is found here such as the state changing and node name.
        new_FU_inputs = []
        new_FU_motion = []
        new_FU_output_Id = []
        new_FU_output_label = []
        new_FU_output_state = []
        

        # get the input nodes
        for input_nodes in input_nodes_FU:
            if input_nodes[0].getOrder() == functionalUnitName:
                new_FU_inputs = input_nodes
            #endif
        #endfor
        
        # get the motion node
        for motion_FU in motions_FU:
            if motion_FU[0].getMotionId() == functionalUnitName:
                new_FU_motion = motion_FU
            #endif
        #endfor

        # NOTE: build the output object after the motion
        for new_FU_input in new_FU_inputs:
            

            if len(new_FU_output_Id)  < (len(new_FU_inputs) - 1):
                obj_id = new_FU_input.getId() + " and "
            else:
                obj_id = new_FU_input.getId() 

            if len(new_FU_output_label) < (len(new_FU_inputs) - 1):
                obj_label = new_FU_input.getLabel() + " and "
            else:
                obj_label = new_FU_input.getLabel()
            

            if len(new_FU_output_state) < (len(new_FU_inputs) - 1):
                obj_output_state = new_FU_input.getStatesList()[1] + ", "
            else:
                obj_output_state = new_FU_input.getStatesList()[1] + ". "
        


            new_FU_output_Id.append(obj_id)
            new_FU_output_label.append(obj_label)
            new_FU_output_state.append(obj_output_state)
        #endfor

        Id = "".join (str(x) for x in new_FU_output_Id) 
        label = "".join(str(x) for x in new_FU_output_label )
        state = "".join(str(x) for x in new_FU_output_state)
        new_FU_output = FOON.Object(Id , label)
        new_FU_output.setStatesList([state])



        # NOTE: set the calculated information in the functional unit class
        # build a new FOON for every name
        newFU = FOON.FunctionalUnit(functionalUnitName)
        functionalUnitNumber += 1

        # build input nodes
        for N in new_FU_inputs:
            newFU.addObjectNode(N, 1)
        
        # build motion node
        newFU.setMotion(new_FU_motion)

        # build output node
        newFU.addObjectNode(new_FU_output, 2)

        # set the functional unit order in the tree
        newFU.setFunctionalUnitOrder(functionalUnitNumber)

        # save the fucntional unit
        functionalUnits.append(newFU)

    print("--------------------------new functional unit---------------------------------------")
    print(functionalUnits[0].getFunctionalUnitOrder())
    return functionalUnits
#enddef

         
# save all functional units in the TreeNode
def FOON_tree():

    # build the treeNode with end goal
    newTree = FOON.TreeNode("sort beer")
    functionalunitList = buildFunctionalUnit()
    newTree.setTreeFunctionalUnits(functionalunitList)
    newTree.setMergePoint("search for the next FU")
    print(newTree)

    return newTree
#enddef


# NOTE: Draw graph for the FOON structure and synchorize it with the robot movement.
def buildGraph(FOON_tree= None, inputNodes = None, motionNode = None, outputNodes = None, state = None):
    print ( "###################### Draw FOON graph ##########################")
  
    # this state is to build all the functional units inside the FOON
    if state == 0:
        # Get the infromation from the FOON_tree

        functionalUnits = FOON_tree.getTreeFunctionalUnits()
        mergepoint = FOON_tree.getMergePoint()
        
        # variables to make the graph dynamic and symmetric.
        numberOfFunctionalUnits = 0
        freeSpace_between_FU = 0
        inputNodeNumber = []
        maxInputNodesNumber = 0
        # get the max number of input point in all graph to find the draw symmetry
        for FU in functionalUnits:
            inputNodes = FU.getInputList()
            inputNodeNumber.append(len(inputNodes))
        #endfor    
        maxInputNodesNumber = np.amax(inputNodeNumber)

        # Build the graph nodes.
        for FU in functionalUnits:
            
            numberOfFunctionalUnits += 1
            
            
            # calculcate the postion of the motion and output node based on the position of the input nodes in the middle.
            inputNodes = FU.getInputList()
            motionNode = FU.getMotion()
            outputNodes = FU.getOutputList()
            FU_order = FU.getFunctionalUnitOrder()

            # calculate dynamic position for every node
            pos_Y = (( maxInputNodesNumber -1) * 4) / 2
            pos_X = FU_order + freeSpace_between_FU
            freeSpace_between_FU += 1
            refrence_x = pos_X  * 4

            # draw nodes and edges
            G.add_node(motionNode[0].getId(),color ='#e65050' ,pos =(( refrence_x + 2 , pos_Y)))
            G.add_node(outputNodes[0].getId(), color = '#00b4d9', pos=( refrence_x + 4 , pos_Y))
    
            counter = 0
            for N in inputNodes:
                G.add_node( N.getId(),color='#4ff077' ,pos=( refrence_x , 4 * counter))

                if len(inputNodes) < maxInputNodesNumber:
                    counter += maxInputNodesNumber - 1
                else:
                    counter += 1
                
                G.add_edge( N.getId(), motionNode[0].getId(), Color ='black', width = 3, weight =N.getStatesList()[0])

            G.add_edge(motionNode[0].getId(), outputNodes[0].getId(), Color ='black', width = 3, weight = outputNodes[0].getStatesList()[0])

            # add the merge point between different functional units.
            if numberOfFunctionalUnits < len(functionalUnits):
                G.add_node( mergepoint ,color ='#8a36f7' ,pos =(( refrence_x + 6 , pos_Y)))
                G.add_edge(outputNodes[0].getId(), mergepoint,  Color ='black', width = 3, weight = "merge_point" )
            else:
                for N in inputNodes:
                    G.add_edge(mergepoint, N.getId() ,Color ='black', width = 3, weight = "merge_point")
                print("should be the last loop")
    #endIf state
    

    # This state to draw only one specific functional unit.
    if state == 1:
        
    
        # calculcate the postion of the motion and output node based on the position of the input nodes in the middle.
        pos_Y = (( len(inputNodes) -1) * 4) / 2
        
        # draw nodes and edges
        G.add_node(motionNode[0].getId(),color ='#e65050' ,pos =((6, pos_Y)))
        G.add_node(outputNodes[0].getId(), color = '#00b4d9', pos=(8, pos_Y))
        counter = 0
        for N in inputNodes:
            print(N.getId())
            G.add_node( N.getId(),color='#4ff077' ,pos=(4 , 4 * counter))
            counter += 1
            G.add_edge( N.getId(), motionNode[0].getId(), Color ='black', width = 3, weight =N.getStatesList()[0])

        G.add_edge(motionNode[0].getId(), outputNodes[0].getId(), Color ='black', width = 3, weight = outputNodes[0].getStatesList()[0])
    #endIf state
    
    # This state is used to update the edge color depending on the robot movement in the FOON.
    if state == 2:
 
        for E in G.edges.data():
            E[2]["Color"] = "black"

            if E[0] == inputNodes[0] and E[1] == motionNode[0].getId():
                E[2]["Color"] = "b"
    #endIf state    
    
    # This state is used when the current functional unit is finished.
    if state == 3:
        for E in G.edges.data():
            E[2]["Color"] = "black"
            if E[0] == motionNode[0].getId() and E[1] == outputNodes[0].getId():
                E[2]["Color"] = "b"
    #endIf state




    # get nodes attributes
    pos = nx.get_node_attributes(G, "pos")
    node_colors = []
    for N in G.nodes.data():
        node_colors.append(N[1]["color"])


    # get edges attributes 
    edges = G.edges()
    edge_colors =[]
    egde_width= []
    edges_weight= nx.get_edge_attributes(G, "weight")
    for E in G.edges.data():
        edge_colors.append(E[2]["Color"])
        egde_width.append(E[2]["width"])
    


    # start draw the graph
    plt.clf()
    nx.draw(G, pos, edges =edges, edge_color= edge_colors, width = egde_width ,node_color = node_colors, font_size=10,node_size=30000, with_labels = True)
    nx.draw_networkx_edge_labels(G, pos, font_size = 10,edge_labels= edges_weight)
    plt.axis("off")
    plt.draw()
    plt.pause(0.01)
#enddef    
