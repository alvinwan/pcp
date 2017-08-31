# Point Cloud Projection

Label KITTI point cloud (3d) drivable area using provided image annotations (2d). Only tested with Python 3.

* includes a new calibration file reader, tailored to KITTI road calibration files
* includes script label point cloud

# How it Works

1. Project point cloud onto the camera, using calibration information.
2. Use image annotations to associate points to labels, `drivable` or otherwise.
3. Save point cloud with associated labels.

# Usage

1. Download the KITTI Road [base kit](http://www.cvlibs.net/download.php?file=data_road.zip) and [velodyne](http://www.cvlibs.net/download.php?file=data_road_velodyne.zip).
2. Save `data_road` and `data_road_velodyne` in the root directory of this repository.
3. Run the main script, to label the velodyne points using the image 2d annotations. Note that the original velodyne binaries contain `nx4` matrices of `x,y,z,intensity`. The new `.npy` files will contain `nx5` matrices of `x,y,z,intensity,drivable`, where `drivable` is a boolean-valued integer.
