# Monte Carlo Localization

Assignment designed to implement Monte Carlo Localization using the particle filters.

## Brief Overview  

A robot is placed in the environment without knowing where it is. As it moves, the particles are (in green arrows) updated each time using the particle filter algorithm. After many measurements, the particles converge to a small cluster around the robot. Hence we find the robot's position.

Demo:

![monte_carlo](https://user-images.githubusercontent.com/22216684/42646529-216e0d92-85cf-11e8-964e-8986368a4113.gif)

## Prerequisites

* Ubuntu 16.04
* ROS kinetic: Installation instruction can be found [here](http://wiki.ros.org/kinetic/Installation/Ubuntu).
* Required ROS packages:
    ```
    $ sudo apt-get install ros-kinetic-control-toolbox ros-kinetic-joystick-drivers ros-kineticrealtime-tools ros-kinetic-ros-control ros-kinetic-gazebo-ros-control ros-kinetic-roscontrollers
    ```

## Build

* compile the code
```
$ catkin_make
```

## How to Use

>
```
$ rosbag​ ​play​ ​-r ​ ​0.25​ ​laser_controls_and_odometry.bag
$ roslaunch ​ ​estimation_assignment​ monte_carlo_localization_v2.launch
$ rosrun ​ ​rviz ​ ​rviz
```
When rviz initializes, go to File > OpenConfig and then
load the configuration file in estimation_assignment/resources/comp417.rviz which is going
to start the visualization of laser scan messages, frames of reference, and particles.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
