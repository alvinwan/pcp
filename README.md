# Point Cloud Projection

Label KITTI point cloud (3d) drivable area using provided image annotations (2d). Only tested with Python 3.

* includes a new calibration file reader, tailored to KITTI road calibration files
* includes script label point cloud

# How it Works

1. Project point cloud onto the camera, using calibration information.
![scans](https://user-images.githubusercontent.com/2068077/29998238-d66b1546-8fda-11e7-9d54-0716afb7b0c2.jpg)
2. Use image annotations to associate points to labels, `drivable` or otherwise.
![label](https://user-images.githubusercontent.com/2068077/29998236-d446d3fe-8fda-11e7-9c87-ab54634c5239.jpg)
3. Save point cloud with associated labels.
![pc_label](https://user-images.githubusercontent.com/2068077/29998237-d585bdde-8fda-11e7-90b9-2e1b4479eb37.jpg)

# Usage

1. Download the KITTI Road [base kit](http://www.cvlibs.net/download.php?file=data_road.zip) and [velodyne](http://www.cvlibs.net/download.php?file=data_road_velodyne.zip).
2. Save `data_road` and `data_road_velodyne` in the root directory of this repository.
3. Run the main script, to label the velodyne points using the image 2d annotations. Note that the original velodyne binaries contain `nx4` matrices of `x,y,z,intensity`. The new `.npy` files will contain `nx5` matrices of `x,y,z,intensity,drivable`, where `drivable` is a boolean-valued integer.
