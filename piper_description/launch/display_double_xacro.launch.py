import os
import subprocess
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    package_name = 'piper_description'
    urdf_name = "double_piper_description.xacro"  # Use the double piper xacro file

    ld = LaunchDescription()
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')
    
    # Use subprocess to call xacro command to generate URDF file content
    urdf_content = subprocess.check_output(['xacro', urdf_model_path]).decode('utf-8')
    robot_description = {'robot_description': urdf_content}

    # Use the specified RViz config file path
    specific_rviz_config_path = os.path.join(pkg_share, 'rviz/rviz.rviz')
    print(specific_rviz_config_path)  # Print to ensure the path is correct

    # Declare arguments
    rviz_arg = DeclareLaunchArgument(name='rvizconfig', default_value=str(specific_rviz_config_path),
                                     description='Absolute path to rviz config file')

    # Joint State Publisher GUI Node
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # RViz Node
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    # Add all actions
    ld.add_action(rviz_arg)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(rviz2_node)
    
    return ld