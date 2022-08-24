My project consists in a Python program that simulates the scenario in which a person is trapped in a building that has caught
on fire. The program 'reads' the layout of the building and is able to calculate the shortest and safest route to an exit,
if there is one. The program then outputs the computed route through a graphical interface, which was designed using the Python
module called pygame.


How it works
First, the program reads a layout text file and stores the configuration of the building and the sensors' location, which are
scattered throughout the building, as well as the location of the trapped person. Then, the program simulates the start of a fire
by randomly choosing one sensor and attributing it an intensity and computes the first draft of the route.
The pathfinding algorithm used to compute the route is called 'A* search'.

After that, the program simulates sensor readings by randomly attributing an intensity (values ranging between 0 and 1) to a
certain number (which is a randomly generated integer between 0 and a set constant) of randomly picked sensors and recomputes
the route to fit the new data. This process is repeated every N steps (N is a constant set to 10) the person takes following the
specified route.


The fires are classified into 4 categories, given their intensity:
 - no danger (intensity between 0 and 0.1) - no assigned color;
 - light danger (intensity between 0.1 and 0.3) - colored yellow;
 - medium danger (intensity between 0.3 and 0.6) - colored orange;
 - extreme danger (intensity between 0.6 and 1) - colored red.
The first 3 categories of fires are passable, but the latter is not.

The walls are represented by grey colored rectangles and the clear is represented using white colored rectangles.
The current position of the trapped person is represented by a green colored rectangle.