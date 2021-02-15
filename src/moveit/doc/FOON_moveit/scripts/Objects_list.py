
##########################################################################################################################
#  @Author: Sherif Shousha                                                                                               # 
#  @Supervisor:Pantano Matteo                                                                                            #
#                                                                                                                        #
#  NOTE: This file includes the list of required objects and their motion.                                               #   
#                                                                                                                        # 
##########################################################################################################################
from collections import namedtuple

def Objects():
    objects = namedtuple("objects", ["id", "state", "order", "name", "pose", "size", "neighbour"])
    beerTable = objects("beer_table", ["fixed"], "order", "box", ( 0.8, 0, 0.2, 1.0), (0.4, 0.6, 0.6), [])
    actionTable = objects("actoin_table", ["fixed"], "order","box", ( 0, 0.8, 0.2, 1.0), (0.6, 0.4, 0.6), [])
    boxTable = objects( "Box_table", ["fixed"], "order","box", ( 0, -0.8, 0.2, 1.0), (0.6, 0.4, 0.6), [])
    # beer
    augustiner = objects("augustiner_bottle", ["unsorted", "sorted"], "sort augustiner","cylinder", (0.7, 0, 0.6, 1.0), (0.2, 0.02), ["augustiner_box"])
    rothaus = objects("rothaus", ["unsorted", "sorted"], "sort rothaus","cylinder", (0.7, -0.2, 0.57, 1.0), (0.15, 0.03), ["rothaus2", "rothaus_box"])
    rothaus2 = objects("rothaus2", ["unsorted", "sorted"], "sort rothaus","cylinder", (0.7, 0.2, 0.57, 1.0), (0.15, 0.03), ["rothaus", "rothaus_box"])
    #boxes
    augustinerBox = objects("augustiner_box", ["empty" , "full"], "sort augustiner","box", (0.2, -0.8, 0.6, 1.0), (0.2, 0.2, 0.2), ["augustiner_bottle"])
    rothausBox = objects("rothaus_box", ["empty", "full"], "sort rothaus","box", (-0.15, -0.8, 0.6, 1.0), (0.3, 0.2, 0.2), ["rothaus", "rothaus2"])
    
    objects_list= [beerTable, actionTable, boxTable, augustiner, rothaus, rothaus2, augustinerBox, rothausBox]
    
    return objects_list
#enddef
def Motions():
    # first build every individual motion
    motions = namedtuple("motions", ["objectId", "motionId", "motionOrder", "startSurface", "endSurface", "startPose", "endPose"])
    augustiner_box = motions("augustiner_box", "sort augustiner", 0, "Box_table", "actoin_table", (0.2, -0.6, 0.6, -90, -45, -180), (-0.2, 0.8, 0.6, 0, 0, 180))
    augustiner_beer = motions("augustiner_bottle", "sort augustiner", 1, "beer_table", "augustiner_box", (0.615, 0, 0.6, -90, -45, -90), (-0.2, 0.77, 0.8 , 0, 0, 90))
    rothaus_box = motions("rothaus_box", "sort rothaus", 0, "Box_table", "actoin_table", (-0.2, -0.6, 0.6, -90, -45, -180), (0.2, 0.8, 0.6, 0, 0, 180))
    rothaus_beer = motions("rothaus", "sort rothaus", 1, "beer_table", "rothaus_box", (0.615, -0.2, 0.6, -90, -45, -90), (0.1, 0.78, 0.77 , 0, 0, 90))
    rothaus_beer2 = motions("rothaus2", "sort rothaus", 2, "beer_table", "rothaus_box", (0.615, 0.2, 0.6, -90, -45, -90), (0.31, 0.72, 0.77 , 0, 0, 60))
    
    motions_list = [augustiner_box, augustiner_beer, rothaus_box, rothaus_beer, rothaus_beer2]
    return motions_list
#enddef