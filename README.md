# BlueBoat RVIZ Model

ROS workspace for the BlueBoat project, containing the packages and robot description files needed to work with the BlueBoat platform.

## Overview

This repository contains the BlueBoat ROS workspace, including the robot description and 3D mesh models.

The main package currently visible in this repository is:

- **`blueboat_description`** — contains the BlueBoat robot description and 3D mesh files used to represent the robot in ROS tools and visualization environments.

The workspace is intended to be built and used in a ROS environment.

## Requirements

Before getting started, make sure you have:

- A Linux system compatible with your installed ROS distribution.
- ROS 2 installed.
- `git` installed.
- `git-lfs` installed to download the 3D mesh models.
- `colcon` installed to build the workspace.
- `rosdep` installed to resolve package dependencies.

> **Note:** Use the ROS distribution for which this workspace was developed. Confirm the required distribution before building.

## 1. Clone the repository

Install Git LFS if it is not already installed:

```bash
sudo apt update
sudo apt install git git-lfs
git lfs install
```

Clone the repository:

```bash
git clone https://github.com/losandriana/BlueBoat-Rviz-Model-.git
cd blueboat_ws
```

Check that the mesh files have been downloaded:

```bash
git lfs ls-files
```

If a mesh file contains Git LFS pointer text instead of the actual model, run:

```bash
git lfs pull
```

## 2. Source ROS 2

Replace `<ros_distro>` with your installed ROS 2 distribution, such as `humble` or `jazzy` or `foxy`.

```bash
source /opt/ros/<ros_distro>/setup.bash
```

For example, if you use ROS 2 Foxy:

```bash
source /opt/ros/foxy/setup.bash
```

## 3. Install dependencies

From the workspace root, run:

```bash
sudo apt install python3-rosdep python3-colcon-common-extensions
```

Initialize `rosdep` if it has not already been initialized on your system:

```bash
sudo rosdep init
rosdep update
```

If `rosdep` is already initialized, skip `sudo rosdep init`.

Install the dependencies declared by the workspace packages:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

## 4. Build the workspace

From the root of `blueboat_ws`, build the workspace:

```bash
colcon build --symlink-install
```

When the build completes successfully, source the workspace:

```bash
source install/setup.bash
```

You should run this command in each new terminal where you want to use the workspace, after sourcing the appropriate ROS installation.

## 5. Inspect the available packages

To list the ROS packages in the workspace:

```bash
colcon list
```

To locate launch files:

```bash
find src -type f \( -name "*.launch.py" -o -name "*.launch.xml" -o -name "*.launch" \)
```

To locate robot description files:

```bash
find src/blueboat_description -type f
```

These commands help identify the available launch files and robot description resources.

## 6. Launch or visualize the BlueBoat

The exact launch command depends on the launch files provided by the packages.

After building and sourcing the workspace, use the launch file you identified in the previous step:

```bash
ros2 launch <package_name> <launch_file>
```

Replace `<package_name>` and `<launch_file>` with the actual package name and launch file.

If a compatible RViz configuration or robot visualization launch file is provided, it can be used to visualize the BlueBoat model.

## 7. Workspace structure

A typical ROS 2 workspace has the following structure:

```text
blueboat_ws/
├── src/
│   └── blueboat_description/
│       ├── meshes/
│       │   ├── blueboat.stl
│       │   └── blueboat_small.stl
│       └── ...
├── .gitattributes
├── .gitignore
├── README.md
└── LICENSE
```

The exact contents may change as additional packages are added.

### Important directories

- **`src/`** — source packages maintained in Git.
- **`blueboat_description/meshes/`** — 3D mesh assets used by the robot description.
- **`build/`** — generated build files.
- **`install/`** — generated installation and setup files.
- **`log/`** — build and test logs.

The `build/`, `install/`, and `log/` directories are generated locally and are excluded from version control.

## 8. Git LFS and 3D models

The BlueBoat mesh files are managed using [Git Large File Storage (Git LFS)](https://git-lfs.com/) because 3D models can exceed GitHub's standard file-size limit.

When cloning this repository on a new machine, install Git LFS before cloning so the actual mesh assets can be retrieved.

If a model is missing, try:

```bash
git lfs install
git lfs pull
```

## 9. Troubleshooting

### `colcon: command not found`

Install the colcon extensions:

```bash
sudo apt install python3-colcon-common-extensions
```

### ROS packages or commands are not found

Source ROS and the workspace again:

```bash
source /opt/ros/<ros_distro>/setup.bash
source install/setup.bash
```

### Mesh files are missing or cannot be opened

Check Git LFS:

```bash
git lfs ls-files
git lfs pull
```

### Build fails because of missing dependencies

Run:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

Then retry:

```bash
colcon build --symlink-install
```

## License

This project includes an Apache-2.0 license. See the [`LICENSE`](LICENSE) file for details.

## Repository

GitHub: https://github.com/losandriana/blueboat_ws
