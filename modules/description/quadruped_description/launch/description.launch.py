from launch_ros.actions import Node
from launch import LaunchDescription
from launch_ros.descriptions import ParameterValue
from launch.substitutions import LaunchConfiguration, Command, FindExecutable, PathJoinSubstitution
from launch.actions import GroupAction
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    use_sim = LaunchConfiguration("use_sim")
    robot_model = LaunchConfiguration("robot_model")
    robot_xacro = LaunchConfiguration("robot_xacro", default="anymal_d.urdf.xacro")
    
    rviz_config_path = PathJoinSubstitution([
        FindPackageShare('quadruped_description'),
        'config/rviz.rviz'
    ])

    quadruped_description_pkg = PathJoinSubstitution([
        [robot_model, '_description']
    ])

    robot_xacro_path = PathJoinSubstitution([
        FindPackageShare(quadruped_description_pkg),
        'robots',
        robot_xacro
    ])

    robot_description_content = Command(
        [
            FindExecutable(name='xacro'),
            ' ',
            robot_xacro_path,
            ' ',
            'use_sim:=',
            use_sim
        ]
    )

    robot_description = ParameterValue(robot_description_content, value_type=str)

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[
            {
              'use_tf_static' : True, # CHECK
              'robot_description': robot_description,
              'publish_frequency': 100.0,
              'use_sim_time': use_sim
            }
        ],
        remappings=[
            ('robot_description' , 'robot_description'),
            ('joint_states' , 'joint_states')
        ]
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        parameters=[
            {
                'use_gui' : True,
                'rate' : 100,
            }
        ],
        remappings=[
            ('robot_description' , 'robot_description'),
            ('joint_states' , 'joint_states')
        ]
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )


    group = GroupAction([
        robot_state_publisher,
        #joint_state_publisher_gui,
        #rviz
    ])

    return LaunchDescription([group])