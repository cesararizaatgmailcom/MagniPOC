# MAGNI POC
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/aa4f2c91-4ecf-4997-8ca8-5e0579111072" />

The purpose of this project is to create a custom implementation of the controllers for MAGNI platfomr created by ubiquity robotics (https://www.ubiquityrobotics.com/). The objective is to stablish a ROS2 project that allows to control the MAGNI Robot and perform SLAM, navigation, image recognition enabling the platform for future more complex tasks.

## Summary

- **magni_description**: Adapted ubiquity's URDFs files and using with ROS2 launch file
- **magni_webots**: this package spawn MAGNI robot in Webots and simulate camera lidar sensors
- **video_recorder**: this package is intended to perform video recording of robot cameras

As part of the purpose of this project we want to study how to leverage docker for better development and deployment experiece so we are using devcontainers for development evironemnt setup and github actions for package creation and deployment. 

<img width="3794" height="1042" alt="image" src="https://github.com/user-attachments/assets/cbeafbb2-b91e-4081-80f5-4d45f17b1604" />



## Quick start ✅

Follow these steps to get a development environment running with the provided Dev Containers:

1. **Clone the repository (including submodules)**

   ```bash
   git clone --recurse-submodules <repository-url>
   # or if you already cloned:
   git submodule update --init --recursive
   ```

2. **Install Docker**

   Follow Docker's official install guide: https://docs.docker.com/engine/install/ubuntu/

3. **Install NVIDIA Container Toolkit** (if you plan to use GPU acceleration)

   Installation instructions: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

4. **Install the Visual Studio Code "Dev Containers" extension**

   Extension docs: https://code.visualstudio.com/docs/remote/containers

5. **Open the repository in VS Code and reopen in a Dev Container**

   - Open the Command Palette (Ctrl+Shift+P) → **Remote-Containers: Reopen in Container**
   - Choose the preferred configuration: **GPU** (`.devcontainer/gpu-simulation`) or **CPU** (`.devcontainer/cpu-simulation`).

6. **Verify the workspace folder is `/home/ws` in the container**

   The devcontainer configuration uses `"workspaceFolder": "/home/ws"`, so new terminals will start in `/home/ws` (this is the ROS 2 workspace).

7. **Build the ROS 2 workspace with colcon**

   Build submodules first

   See the ubiquity_motor_ros2 submodule README for submodule-specific build instructions: https://github.com/JAndresBP/ubiquity_motor_ros2

   ```bash
   # inside the devcontainer, from /home/ws
   source /opt/ros/<ros-distro>/setup.bash
   colcon build --symlink-install
   source install/setup.bash
   ```

8. **Run the simulation**

   ```bash
   ./scripts/launch-webots-simulation.sh
   ```

9. **Open a second terminal and run the keyboard teleop**

   ```bash
   ./scripts/run-teleop-keyboard.sh
   ```

---

**Notes & tips**

- The devcontainer `postCreateCommand` runs `rosdep update` and installs package dependencies automatically.
- If you select the GPU container, ensure the NVIDIA Container Toolkit is installed on the host and the container has access to GPUs (see step 3).
- If any package in `src/` has additional build requirements, follow the package or submodule README for additional steps.


