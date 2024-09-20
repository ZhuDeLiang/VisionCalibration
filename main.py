# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pandas as pd

class EyeInHand:
    def __init__(self, max_shouyan, camera_excel_path, robot_excel_path):
        self.max_shouyan = max_shouyan
        self.camera_excel_path = camera_excel_path
        self.robot_excel_path = robot_excel_path

    def invert_transformation(self, R, t):
        R_inv = R.T
        t_inv = -R_inv @ t
        return R_inv, t_inv

    def load_matrix_from_excel(self, file_path, index):
        """
        从Excel文件中读取4x4矩阵
        :param file_path: Excel文件路径
        :param index: 要读取的矩阵索引（从0开始）
        :return: 4x4矩阵
        """
        df = pd.read_excel(file_path, header=None)
        start_row = index * 4
        matrix_4x4 = df.iloc[start_row:start_row + 4, :].values
        return matrix_4x4

    def collect_data_and_calibrate(self):
        ocr = []
        oct = []
        ebr = []
        ebt = []

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

        for num_shuzu in range(self.max_shouyan):
            # 从Excel文件中读取camera的4x4矩阵
            camera_matrix = self.load_matrix_from_excel(self.camera_excel_path, num_shuzu)
            obj_cam_r = camera_matrix[:3, :3]
            obj_cam_t = camera_matrix[:3, 3].reshape(3, 1)

            # 从Excel文件中读取robot的4x4矩阵
            matrix_4x4 = self.load_matrix_from_excel(self.robot_excel_path, num_shuzu)

            # 提取3x3旋转矩阵和1x3转移矩阵
            end_base_r = matrix_4x4[:3, :3]
            end_base_t = matrix_4x4[:3, 3].reshape(3,1) # 将单位从毫米转换为米

            end_base_r, end_base_t = self.invert_transformation(end_base_r, end_base_t)  # 眼在手外

            ocr.append(obj_cam_r)
            oct.append(obj_cam_t)
            ebr.append(end_base_r)
            ebt.append(end_base_t)

            print(ocr, "\n", oct, "\n", ebr, "\n", ebt)
            print(num_shuzu + 1, "组数据已收集完成")

        A, B = cv2.calibrateHandEye(ebr, ebt, ocr, oct, method=cv2.CALIB_HAND_EYE_TSAI)
        print(A, B)

# 使用实例
camera_excel_path = 'camera.xlsx'  # 相机矩阵的Excel文件路径
robot_excel_path = 'robot.xlsx'    # 机器人矩阵的Excel文件路径
A = EyeInHand(5, camera_excel_path, robot_excel_path)
A.collect_data_and_calibrate()
