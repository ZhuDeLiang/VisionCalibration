# -*- coding: utf-8 -*-

import object_base_camera as shouyan1
import cv2
import numpy as np

class EyeInHand:
    def __init__(self, max_shouyan):

        self.max_shouyan  = max_shouyan

    def invert_transformation(self, R, t):
        """
        Invert a transformation given a rotation matrix R and translation vector t.
        This converts the transformation from frame A to frame B, into frame B to frame A.

        :param R: A 3x3 rotation matrix.
        :param t: A 3x1 translation vector.
        :return: A tuple (R_inv, t_inv) where R_inv is the inverted rotation matrix and t_inv is the inverted translation vector.
        """
        # Inverting the rotation matrix
        R_inv = R.T  # or np.linalg.inv(R), since for rotation matrices transpose is the inverse

        # Inverting the translation vector
        t_inv = -R_inv @ t  # or -np.dot(R_inv, t)

        return R_inv, t_inv

    def collect_data_and_calibrate(self):
        ABS = 0
        INCR = 1
        Enable = True
        Disable = False

        num_shuzu = 1
        ocr = []
        oct = []
        ebr = []
        ebt = []

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

        while num_shuzu <= self.max_shouyan:
            # 获得物体到相机坐标系之间旋转矩阵和转移矩阵
            obj_cam = shouyan1.shouyan1()
            obj_cam_r, obj_cam_t = obj_cam.process_frames()
            print("r :")
            print(obj_cam_r)

            print("t:")
            print(obj_cam_t)
            obj_cam_t = np.array(obj_cam_t).reshape((3, 1))


            # 获得末端执行器到基座的坐标参数



            # 从用户输入中接收十六个数字
            input_data = input("请输入旋转矩阵和转移矩阵：")

            # 将输入的字符串分割成浮点数列表
            numbers = list(map(float, input_data.split()))

            # 确保输入的数据数量正确
            if len(numbers) != 16:
                print("输入的数字数量不正确，请输入十六个数字。")
            else:
                # 将列表转换成4x4矩阵
                matrix_4x4 = np.array(numbers).reshape(4, 4)
                print("4x4矩阵：")
                print(matrix_4x4)

                # 提取前面的3x3矩阵
                end_base_r = matrix_4x4[:3, :3]
                print("\n3x3矩阵：")
                print(end_base_r)

                # 提取1x3矩阵（第1、2、3行的第4列）
                end_base_t = matrix_4x4[:3, 3].reshape(1, 3)
                end_base_t = end_base_t.flatten() / 1000  # 将单位从毫米转换为米

                print("\n1x3矩阵：")
                print(end_base_t)

            end_base_r, end_base_t = self.invert_transformation(end_base_r, end_base_t)  # 眼在手外



            if num_shuzu == 1:
                ocr = [obj_cam_r]
                oct = [obj_cam_t]
                ebr = [end_base_r]
                ebt = [end_base_t]
            else:
                ocr.append(obj_cam_r)
                oct.append(obj_cam_t)
                ebr.append(end_base_r)
                ebt.append(end_base_t)

            num_shuzu += 1
            print(ocr, "\n", oct, "\n", ebr, "\n", ebt)
            print(num_shuzu - 1, "组数据已收集完成")


        A, B = cv2.calibrateHandEye(ebr, ebt, ocr, oct, method=cv2.CALIB_HAND_EYE_TSAI)
        print(A, B)



A = EyeInHand(5)
A.collect_data_and_calibrate()
# 使用实例

