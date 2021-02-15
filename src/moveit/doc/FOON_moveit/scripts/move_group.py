#!/usr/bin/env python
##########################################################################################################################
#  @Author: Sherif Shousha                                                                                               # 
#  @Supervisor:Pantano Matteo                                                                                            #
#                                                                                                                        #
#  NOTE: This file includes the MoveIt controlling using FOON.                                                           #
#  NOTE: This file is the main file, which calls all other project files.                                                #   
#                                                                                                                        # 
##########################################################################################################################
# BEGIN imports
#
# To use the Python MoveIt interfaces, we will import the "moveit_commander", "moveit_msgs", "geometry_msgs" and "trajectory_msgs.


import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import math

from moveit_msgs.msg import Grasp, PlaceLocation
from trajectory_msgs.msg import JointTrajectoryPoint
from moveit_commander.conversions import pose_to_list
from FOON_structure import buildObjects , FOON_tree, buildGraph
from geometry_msgs.msg import PoseStamped


from tf.transformations import *
## END imports

 
# class moveIt control
class MoveGroup(object):

  """MoveGroup"""
  def __init__(self):
    super(MoveGroup, self).__init__()

    # BEGIN  setup
    # First initialize `moveit_commander`_ and a `rospy`_ node.
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group', anonymous=True)

    # Instantiate a `RobotCommander`_ object. Provides information such as the robot's
    # kinematic model and the robot's current joint states
    robot = moveit_commander.RobotCommander()

    # Instantiate a `PlanningSceneInterface`_ object.  This provides a remote interface
    # for getting, setting, and updating the robot's internal understanding of the surrounding world.
    scene = moveit_commander.PlanningSceneInterface()

    ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
    ## to a planning group (group of joints).
    group_name = "panda_arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    ## Create a `DisplayTrajectory`_ ROS publisher which is used to display trajectories in Rviz.
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)

    
    # Getting Basic Information
    # ^^^^^^^^^^^^^^^^^^^^^^^^^
    # The name of the reference frame for this robot.
    planning_frame = move_group.get_planning_frame()
    print "============ Planning frame: %s" % planning_frame

    # Print the name of the end-effector link for this group.
    eef_link = move_group.get_end_effector_link()
    print "============ End effector link: %s" % eef_link

    # List of all the groups in the robot.
    group_names = robot.get_group_names()
    print "============ Available Planning Groups:", robot.get_group_names()

    # The entire state of the robot.
    print "============ Printing robot state"
    print robot.get_current_state()
    print ""
    

    # variables
    self.box_name = ''
    self.robot = robot
    self.scene = scene
    self.move_group = move_group
    self.display_trajectory_publisher = display_trajectory_publisher
    self.planning_frame = planning_frame
    self.eef_link = eef_link
    self.group_names = group_names
  #enddef

  def start(self):
    
    move_group = self.move_group

    
    # The Panda's zero configuration is at a `singularity`, so the first thing we want to do is move it to a slightly better configuration.
    
    # get the joint values from the group 
    joint_goal = move_group.get_current_joint_values()
    
    #adjust some of the values.
    joint_goal[0] = 0
    joint_goal[1] = -math.pi/4
    joint_goal[2] = 0
    joint_goal[3] = -math.pi/2
    joint_goal[4] = 0
    joint_goal[5] = math.pi/3
    joint_goal[6] = math.pi/4

    # parameters if you have already set the pose or joint target for the group
    move_group.go(joint_goal, wait=True)

    # ensuring that there is no residual movement
    move_group.stop()

  #enddef

  def addColissoinObject(self, Objects_list):
    # Using the FOON to build the required objects.
    print "============ Add objects from FOON objects list"

    # call planning scene to be able to set new objects.
    scene = moveit_commander.PlanningSceneInterface()
    
    # get the information of each object from FOON and add the object in the environment.
    for objColission in Objects_list:
      objectPosition = objColission.getObjectLocation()
      print(objectPosition)
      Size = objColission.getSize()
      objectId = objColission.getObjectId()
      objectName = objColission.getObjectLabel()
      Object = PoseStamped()
      Object.header.frame_id = "panda_link0"
      Object.pose.position.x = objectPosition[0]
      Object.pose.position.y = objectPosition[1]
      Object.pose.position.z = objectPosition[2]
      if objectName == "box":
        print(objectId)
        print(Size)
        scene.add_box(objectId, Object, (Size[0],Size[1],Size[2]))
      elif objectName == "cylinder":
        scene.add_cylinder(objectId, Object, Size[0], Size[1])
      
    rospy.sleep(1)   
    print "============ object should be added"
  #enddef

    
  def control_center(self): 
    
    move_group = self.move_group
    
    # get the FOON tree information.
    FOON_Tree = FOON_tree()
    
    # take the order from the user.
    order = input ("Enter order to the robot : ")
    
    # chick if the user want to use all the functional units in the FOON.
    if FOON_Tree.getTreeGoal() == order:

      print("inside tree")
      # first build a graph for all functional units in FOON.
      state = 0
      buildGraph(FOON_Tree, None, None, None, state)
      FU_number = 0
      
      # get every functional unit in the FOON.
      for Functional_unit in FOON_Tree.getTreeFunctionalUnits():
        FU_number += 1
        
        # check if the current functional unit is the right one.
        if Functional_unit.getFunctionalUnitOrder() == FU_number:
         
          for M in Functional_unit.getMotion():
            
            # use the FOON information to set the required infromation in pick and place functions.
            pickInfo = M.getMotionStartPose()
            pickInfo.append(M.getStartSupportSurface())
            pickInfo.append(M.getLabel())
                    
            placeInfo= M.getMotionEndPose() 
            placeInfo.append(M.getEndSupportSurface())
            placeInfo.append(M.getLabel())
                
            rospy.sleep(5)
            # update the graph with the current position in FOON.
            state = 2
            buildGraph(None, [M.getLabel()], Functional_unit.getMotion(), Functional_unit.getOutputList(), state)
                
            # pick and place the targeted object.    
            self.pick(pickInfo)
            rospy.sleep(1)
            self.start()
            rospy.sleep(2)
            self.place(placeInfo)
            rospy.sleep(1)
            self.start()
            rospy.sleep(4)
          # update the graph that current functional unit is accomplished.
          state = 3 
          buildGraph(None ,[ ], Functional_unit.getMotion(), Functional_unit.getOutputList(), state)
      
      # if all functional units are finished, stop the program.
      rospy.sleep(10)
      move_group.stop()

         

    else:

      # if the user whant to use only one functional unit from the FOON.
      for Functional_unit in FOON_Tree.getTreeFunctionalUnits():
        # filter the functional units to get the functional unit, which is required from the user.
        if Functional_unit.getName() == order:
          print(" ##### inside functional unit: ", Functional_unit.getInputList())
          state = 1
          # draw the targeted functional unit in the graph
          buildGraph(None ,Functional_unit.getInputList(), Functional_unit.getMotion(), Functional_unit.getOutputList(), state)
           # get every motion step inside the functional unit.
          for M in Functional_unit.getMotion():

            # use the FOON information to set the required infromation in pick and place functions.
            pickInfo = M.getMotionStartPose()
            pickInfo.append(M.getStartSupportSurface())
            pickInfo.append(M.getLabel())
            
            placeInfo= M.getMotionEndPose() 
            placeInfo.append(M.getEndSupportSurface())
            placeInfo.append(M.getLabel())
            
            rospy.sleep(5)
            state = 2
            # update the graph with the current position in FOON.
            buildGraph(None, [M.getLabel()], Functional_unit.getMotion(), Functional_unit.getOutputList(), state)
            
            
            self.pick(pickInfo)
            rospy.sleep(1)
            self.start()
            rospy.sleep(2)
            self.place(placeInfo)
            rospy.sleep(1)
            self.start()
            rospy.sleep(4)
          # update the graph that current functional unit is accomplished.  
          state = 3 
          buildGraph(None ,[ ], Functional_unit.getMotion(), Functional_unit.getOutputList(), state)
          rospy.sleep(10)
          move_group.stop()
          #endfor
        #endif
      #endfor
  #enddef  

  
     
  # pick object  
  def pick(self, pose_goal):
    # get the move group name. 
    move_group = self.move_group
    
    # get the move group current position.
    current_position = move_group.get_current_pose()

    # calculate the quanternion from roll, pitch, yaw.
    orientation = quaternion_from_euler(math.radians(
           pose_goal[3]), math.radians(pose_goal[4]), math.radians(pose_goal[5]))
    # call grasp class from moveit_msgs.
    grasps = Grasp()
    # set the object position and orientation.
    grasps.grasp_pose.header.frame_id = "panda_link0"
    grasps.grasp_pose.pose.orientation.x = orientation[0]
    grasps.grasp_pose.pose.orientation.y = orientation[1]
    grasps.grasp_pose.pose.orientation.z = orientation[2]
    grasps.grasp_pose.pose.orientation.w = orientation[3]
    grasps.grasp_pose.pose.position.x = pose_goal[0] 
    grasps.grasp_pose.pose.position.y = pose_goal[1]      
    grasps.grasp_pose.pose.position.z = pose_goal[2]       

    # set information about the arm movement behavior before the pick action.
    grasps.pre_grasp_approach.direction.header.frame_id = "panda_link0"
    grasps.pre_grasp_approach.direction.vector.x= grasps.grasp_pose.pose.position.x - current_position.pose.position.x
    grasps.pre_grasp_approach.direction.vector.y = grasps.grasp_pose.pose.position.y - current_position.pose.position.y
    grasps.pre_grasp_approach.min_distance = 0.05
    grasps.pre_grasp_approach.desired_distance = 2
      
    # arm behavior after the pick action. 
    grasps.post_grasp_retreat.direction.header.frame_id = "panda_link0" 
    grasps.post_grasp_retreat.direction.vector.z = 1.5
    grasps.post_grasp_retreat.min_distance = 0.15
    grasps.post_grasp_retreat.desired_distance = 0.9

    # open and close the gripper.
    self.openGripper(grasps.pre_grasp_posture)
    self.closeGripper(grasps.grasp_posture)
    
    move_group.set_support_surface_name(pose_goal[6])
    move_group.pick(pose_goal[7], grasps)
  #enddef

  
  def place(self, current_goal):
    # get the move group name.
    move_group = self.move_group

    # get the move group current position.
    current_position = move_group.get_current_pose()

    # calculate the quanternion from roll, pitch, yaw.
    orientation = quaternion_from_euler(math.radians(
          current_goal[3]), math.radians(current_goal[4]), math.radians(current_goal[5]))
    
    # call place location class from moveit
    place_location = PlaceLocation() 
    # Setting place location position and orientation
    place_location.place_pose.header.frame_id = "panda_link0"
    place_location.place_pose.pose.orientation.x = orientation[0]
    place_location.place_pose.pose.orientation.y = orientation[1]
    place_location.place_pose.pose.orientation.z = orientation[2]
    place_location.place_pose.pose.orientation.w = orientation[3]
    place_location.place_pose.pose.position.x = current_goal[0]
    place_location.place_pose.pose.position.y = current_goal[1]
    place_location.place_pose.pose.position.z = current_goal[2]
    
    # Setting pre-place approach ##
    place_location.pre_place_approach.direction.header.frame_id = "panda_link0"
    place_location.pre_place_approach.direction.vector.z = place_location.place_pose.pose.position.z - current_position.pose.position.z # Direction is set as negative z axis
    place_location.pre_place_approach.min_distance = 0.02
    place_location.pre_place_approach.desired_distance = 0.3
    
    # Setting post-place retreat
    place_location.post_place_retreat.direction.header.frame_id = "panda_link0"
    place_location.post_place_retreat.direction.vector.y = -1.0  # Direction is set as negative y axis
    place_location.post_place_retreat.direction.vector.z = 0.8
    place_location.post_place_retreat.min_distance = 0.1
    place_location.post_place_retreat.desired_distance = 0.45
    

    self.openGripper(place_location.post_place_posture)

    move_group.set_support_surface_name(current_goal[6])
    move_group.place(current_goal[7], place_location)
  #enddef

  
  def openGripper(self, posture):

    # Add both finger joints of panda robot
    posture.joint_names = [str for i in range(2)]
    posture.joint_names[0] = "panda_finger_joint1"
    posture.joint_names[1] = "panda_finger_joint2"
    
    # Set them as open, wide enough for the object to fit
    posture.points = [JointTrajectoryPoint()]
    posture.points[0].positions = [float for i in range(2)]
    posture.points[0].positions[0] = 0.04
    posture.points[0].positions[1] = 0.04
    posture.points[0].time_from_start = rospy.Duration(0.5)  
  #enddef
  
  
  def closeGripper(self, posture):
    
    # Add both finger joints of panda robot
    posture.joint_names = [str for i in range(2)]
    posture.joint_names[0] = "panda_finger_joint1"
    posture.joint_names[1] = "panda_finger_joint2"
    
    # Set them as closed
    posture.points = [JointTrajectoryPoint()]
    posture.points[0].positions = [float for i in range(2)]
    posture.points[0].positions[0] = 0.00
    posture.points[0].positions[1] = 0.00
    posture.points[0].time_from_start = rospy.Duration(0.5)
  #enddef
#endClass MoveGroup


def main():
  try:
    print ""
    print "----------------------------------------------------------"
    print "######### Welcome to the FOON_MoveIt project #############"
    print "----------------------------------------------------------"
    
    print "============ Press `Enter` to begin the  setup of the robot ..."

    
    raw_input()
    moveit = MoveGroup()
    print "============ Press `Enter` to set objects in FOON"
    raw_input()
    Objects_list = buildObjects()
    print "============ Press `Enter` to add objects"
    raw_input()
    moveit.addColissoinObject(Objects_list)

    print "============ Press `Enter` to execute a movement to the start position."
    raw_input()
    moveit.start()
    print "============ Press `Enter` to execute a movement to the first object"
    raw_input()
    moveit.control_center()
  

   
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()
