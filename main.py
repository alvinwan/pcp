"""Label point clouds using image 2d annotation and calibration files."""

from thirdparty.calib import Calib
import argparse
import os
import cv2
import numpy as np
import sys


def main():
    parser = argparse.ArgumentParser(description='Converter')
    parser.add_argument('--kitti-road', type=str, help='Path to KITTI `data_road`', default='data_road/')
    parser.add_argument('--kitti-road-velodyne', type=str, help='Path to KITTI `data_road_velodyne`', default='data_road_velodyne/')
    parser.add_argument('--cam-idx', type=int, help='Index of the camera being used', default=2)
    parser.add_argument('--dataset', type=str, choices=('training', 'testing'), help='Which dataset to run on', default='training')
    args = parser.parse_args()

    dirpath = os.path.join(args.kitti_road_velodyne, args.dataset, 'velodyne')

    for filename in os.listdir(dirpath):
        if filename.startswith('.'):
            continue
        name = filename.split('.')[0]
        id = name.split('_')[1]
        velo_path = os.path.join(args.kitti_road_velodyne, args.dataset, 'velodyne', filename)
        calib_path = os.path.join(args.kitti_road, args.dataset, 'calib', '%s.txt' % name)
        gt_path = os.path.join(args.kitti_road, args.dataset, 'gt_image_2', 'um_lane_%s.png' % id)

        # n x 4 (x, y, z, intensity)
        velo_data = np.fromfile(velo_path, dtype=np.float32).reshape((-1, 4))
        velo_points = velo_data[:, :3]
        gt = cv2.imread(gt_path, cv2.IMREAD_UNCHANGED)
        if gt is None:
            print('\r%s does not have a ground truth file' % filename)
            continue
        gt_labels = gt[:, :, 0]
        calib = Calib(calib_path)

        img_points = calib.velo2img(velo_points, args.cam_idx).astype(int)
        selector = (img_points[:, 0] < gt.shape[0]) * (img_points[:, 0] > 0) *\
            (img_points[:, 1] < gt.shape[1]) * (img_points[:, 1] > 0)
        img_points = img_points[selector]
        velo_new_data = velo_data[selector]

        velo_labels = []
        for point in img_points:
            velo_labels.append(gt_labels[tuple(point)])
        velo_labels = np.vstack(velo_labels)

        # n x 4 (x, y, z, intensity, drivable) - excludes anything not in cam
        velo_new_data = np.hstack((velo_new_data, velo_labels))
        velo_new_path = os.path.join(args.kitti_road_velodyne, args.dataset, 'gt_velodyne', name)
        os.makedirs(os.path.dirname(velo_new_path), exist_ok=True)
        np.save(velo_new_path, velo_new_data)
        sys.stdout.write("\rConverted %s" % filename)
        sys.stdout.flush()
    print('Done, yay.')


if __name__ == '__main__':
    main()