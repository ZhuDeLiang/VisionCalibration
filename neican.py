# -*- coding: utf-8 -*-

from pyk4a import PyK4A, Config, ColorResolution, DepthMode, CalibrationType

def get_camera_intrinsics_and_distortions():
    # 初始化 Kinect 相机并设置颜色分辨率和深度模式
    k4a = PyK4A(Config(color_resolution=ColorResolution.RES_720P, depth_mode=DepthMode.NFOV_UNBINNED))
    k4a.start()

    # 获取校准数据
    calibration = k4a.calibration

    # 获取颜色和深度相机的内参数矩阵
    color_camera_matrix = calibration.get_camera_matrix(CalibrationType.COLOR)
    depth_camera_matrix = calibration.get_camera_matrix(CalibrationType.DEPTH)

    # 获取颜色和深度相机的畸变系数
    color_distortion_coefficients = calibration.get_distortion_coefficients(CalibrationType.COLOR)
    depth_distortion_coefficients = calibration.get_distortion_coefficients(CalibrationType.DEPTH)

    # 打印颜色和深度相机的内参数矩阵及畸变系数
    print("Color Camera Matrix:")
    print(color_camera_matrix)
    print("Color Distortion Coefficients:")
    print(color_distortion_coefficients)

    print("\nDepth Camera Matrix:")
    print(depth_camera_matrix)
    print("Depth Distortion Coefficients:")
    print(depth_distortion_coefficients)


    # 停止相机
    k4a.stop()

# 调用函数以获取并打印相机内参数和畸变系数
get_camera_intrinsics_and_distortions()
