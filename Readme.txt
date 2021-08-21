#Knowledge representation of human centred automated manufacturing processes for Industry 4.0 and beyond

## Demo video
https://drive.google.com/file/d/18OtsCAhw5006IOYaI7NiXDFCOsyLYY5K/view?usp=sharing

##Implementation
The goal of the implementation was to make the robot acting human-like by using the FOON graph to extract the needed object to achieve a specific goal.
When the robot received a command, it had to know the input object and its state and it had to plan the motion sequence, which led to the change in the object state to complete the task successfully.
In our implementation, we created an environment that includes two kinds of beer, “augustiner” beer and “rothaus” beer.
Each beer has its own beer box. The environment begins with the beer bottles located on a table and the boxes located on another table.
The robot should use a input command like “sort beer” to build a sequence of actions using the FOON to sort every kind of beer in its own box. Furthermore, the robot should be able to sort any kind of beer to its box from the input command.
For instance, when the robot gets the command “sort augustiner”, the robot should be able to recognize the needed objects and look for the augustiner beer bottle and
the augustiner box. The robot should then get that the state of the beer bottle is “unsorted” and the state of the box is “empty”. After that, the robot generates manipulation motion sequences
from the FOON to put the beer in its box. The output from this sorting task is the beer bottle with the state “sorted” and the box with the state “full”.
The robot should gather all existing beer bottles from the same kind in its own box before changing the state of the box from “empty” to “full”. The robot arms use “pick” and “place”
functions with different input information unique to every object in the processes, which means that all motion nodes in the FOON are consisted of these two manipulation functions, but the
sequence of this motion, the targeted positions, and orientation are not the same within every manipulation problem.

![motion](https://user-images.githubusercontent.com/43730514/130330813-d7936e59-6211-4b97-9d99-508ea6396d59.png)

To achieve that, rospy and its build system “catkin” environment were needed. The implementation started in two parallel parts. The MoveIt part and FOON part. 
The MoveIt part included the robot arm structure, the joints number, and the joints movement limit. Moreover, the MoveIt implementation included the movement planning and needed move function like pick
and place behavior, which should be human-like. The FOON part can be referred to as the “robot brain”, since this part included all existing objects in the environment, and planning and
creating the sequence of action to achieve the desired goal.


