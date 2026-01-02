cmake_minimum_required(VERSION 3.8)
project(quadruped_gz_sim)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  config
  launch
  worlds
  models
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)

endif()

# Register hooks
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/quadruped_gz_sim.sh.in")

ament_package()
