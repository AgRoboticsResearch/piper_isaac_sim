# Piper Isaac Sim

This repository contains the necessary files to simulate the Agilex Piper robot in NVIDIA Isaac Sim.

## NOTE: Current model doesn't have color information

## Getting Started

### Launching Isaac Sim

1. Navigate to the Isaac Sim installation directory:
   ```bash
   cd /media/zfei/d/isaac-sim-4.5.0
   ./isaac-sim.selector.sh
   ```

2. You may need to set asset paths using the following arguments:
   ```
   --/persistent/isaac/asset_root/default="/media/zfei/d/isaacsim_assets/Assets/Isaac/4.5"
   ```

### Setting Up the Workspace

1. Create a ROS 2 workspace and clone this repository:
   ```bash
   mkdir -p ./piper_ws/src
   cd ./piper_ws/src
   git clone git@github.com:AgRoboticsResearch/piper_isaac_sim.git
   cd ..
   colcon build
   source install/setup.bash
   ```

### Loading the Simulation

1. Open the Isaac Sim application
2. Load the `piper_isaac.usd` file
3. Use the Physics Inspector to play the simulation (hit the play button)

![Isaac Sim with Piper loaded](path/to/piper_sim_image.png)

4. After loading, you should be able to see the following ROS 2 topics:
   ```
   ros2 topic list
   /clock
   /isaac_joint_commands
   /isaac_joint_states
   /joint_states
   /parameter_events
   /robot_description
   /rosout
   /tf
   /tf_static
   ```

## Setting Up MoveIt

### Initial Configuration

1. Ensure you have all MoveIt2 packages installed
2. Launch the MoveIt Setup Assistant:
   ```bash
   ros2 launch moveit_setup_assistant setup_assistant.launch.py
   ```
3. Follow the configuration steps as described in the [MoveIt tutorial](https://moveit.picknik.ai/main/doc/examples/setup_assistant/setup_assistant_tutorial.html)

![MoveIt Setup Assistant](path/to/moveit_setup_image.png)

### Preparing for Simulation

1. In the generated MoveIt configuration, edit `piper_camera_moveit_config/config/joint_limits.yaml` to convert all integer values to doubles by adding `.0`

![Joint Limits Configuration](path/to/joint_limits_image.png)

### Configuring ROS 2 Control for Isaac Sim

1. Install the topic-based ROS 2 control package:
   ```bash
   sudo apt-get install ros-$ROS_DISTRO-topic-based-ros2-control
   ```

2. Ensure your `piper_description.ros2_control.xacro` contains the following:
   ```xml
   <xacro:macro name="piper_description_ros2_control" params="name initial_positions_file ros2_control_hardware_type:=mock_components">
       <xacro:property name="initial_positions" value="${load_yaml(initial_positions_file)['initial_positions']}"/>

       <ros2_control name="${name}" type="system">
           <hardware>
             <xacro:if value="${ros2_control_hardware_type == 'mock_components'}">
                 <plugin>mock_components/GenericSystem</plugin>
             </xacro:if>
             <xacro:if value="${ros2_control_hardware_type == 'isaac'}">
                 <plugin>topic_based_ros2_control/TopicBasedSystem</plugin>
                 <param name="joint_commands_topic">/isaac_joint_commands</param>
                 <param name="joint_states_topic">/isaac_joint_states</param>
             </xacro:if>
           </hardware>
           <!-- Other configuration... -->
       </ros2_control>
   </xacro:macro>
   ```

3. Make sure your `piper_description.urdf.xacro` is properly configured:
   ```xml
   <?xml version="1.0"?>
   <robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="piper_description">
       <xacro:arg name="initial_positions_file" default="initial_positions.yaml" />
       <xacro:arg name="ros2_control_hardware_type" default="mock_components" />

       <!-- Import piper_description urdf file -->
       <xacro:include filename="$(find piper_description)/urdf/piper_description.urdf" />

       <!-- Import control_xacro -->
       <xacro:include filename="piper_description.ros2_control.xacro" />

       <xacro:piper_description_ros2_control name="FakeSystem" initial_positions_file="$(arg initial_positions_file)" ros2_control_hardware_type="$(arg ros2_control_hardware_type)"/>
   </robot>
   ```

### Launching MoveIt with Isaac Sim

1. Build and source your workspace:
   ```bash
   colcon build
   source install/setup.bash
   ```

2. Launch MoveIt configured for Isaac Sim:
   ```bash
   ros2 launch piper_camera_moveit_config isaac_sim.launch.py ros2_control_hardware_type:=isaac
   ```

## Troubleshooting

If you encounter issues with the simulation, check:
- Asset paths are correctly set
- ROS 2 topics are available
- Joint limits are properly defined as doubles in the configuration

## Contributing

Contributions to improve the simulation are welcome. Please submit pull requests or issues through GitHub.
