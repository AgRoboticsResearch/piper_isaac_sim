from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch

def generate_launch_description():
    # Command-line arguments
    ros2_control_hardware_type_arg = DeclareLaunchArgument(
        "ros2_control_hardware_type",
        default_value="mock_components",
        description="ROS2 control hardware interface type to use for the launch file",
    )

    # Create the MoveIt configuration with ros2_control_hardware_type set to the launch configuration
    moveit_config = (
        MoveItConfigsBuilder("piper_description", package_name="piper_camera_moveit_config")
        .robot_description(
            file_path="config/piper_description.urdf.xacro",
            mappings={
                "ros2_control_hardware_type": LaunchConfiguration(
                    "ros2_control_hardware_type"
                )
            },
        )
        .to_moveit_configs()
    )

    # Generate and return the launch description
    return LaunchDescription([
        ros2_control_hardware_type_arg,
        generate_demo_launch(moveit_config)
    ])