# quadruped_ros2

sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
 
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

sudo apt-get update
sudo apt-get install libgz-transport15-dev
sudo apt install libgz-msgs12-dev

sudo apt update
sudo apt install libzmq3-dev
sudo apt install cppzmq-dev

## Usage

ros2 launch anymal_bringup bringup_complete.launch.py

ros2 launch anymal_bringup bringup_complete.launch.py world_sim:=electrical_station.world



