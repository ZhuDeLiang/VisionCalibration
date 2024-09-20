import numpy as np
import cv2
from pyk4a import PyK4A

class shouyan1:
    def __init__(self):
        # 定义 ArUco 标记字典
        self.ARUCO_DICT = {
            # ...（其余字典项）
            "DICT_4X4_50": cv2.aruco.DICT_4X4_50, "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
              "DICT_4X4_250": cv2.aruco.DICT_4X4_250, "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
              "DICT_5X5_50": cv2.aruco.DICT_5X5_50, "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
              "DICT_5X5_250": cv2.aruco.DICT_5X5_250, "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
              "DICT_6X6_50": cv2.aruco.DICT_6X6_50, "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
              "DICT_6X6_250": cv2.aruco.DICT_6X6_250, "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
              "DICT_7X7_50": cv2.aruco.DICT_7X7_50, "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
              "DICT_7X7_250": cv2.aruco.DICT_7X7_250, "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
              "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
              "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
              "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
              "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
              "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
            # ...（其余字典项）
        }

        # 相机内参和畸变系数

        self.dist = np.array([ 3.56499135e-01, -2.38331628e+00 , 1.09357561e-03, -8.55933584e-04,
                      1.37534881e+00,  2.41856128e-01, -2.21700788e+00,  1.30763078e+00])
        self.mtx = np.array(
            [[605.9921875,    0,     638.23809814],# fx  cx  fy  cy
            [0,         605.88006592, 367.54467773],
            [0,  0, 1]])

        # ArUco 相关参数
        self.arucoDict = cv2.aruco.Dictionary_get(self.ARUCO_DICT["DICT_6X6_1000"])
        self.arucoParams = cv2.aruco.DetectorParameters_create()

        # 配置和启动 RealSense 流水线
        # Load camera with the default config
        self.k4a = PyK4A()
        self.k4a.start()


    def zhuanhuan(self, data):  # 转换成3*3的旋转矩阵
        c = data[0, 0, :].copy()
        c = np.diag(c)
        return c

    def process_frames(self):
        rvec, tvec = None, None  # 初始化为 None 或合适的默认值

        while True:
            capture = self.k4a.get_capture()
            color_image = capture.color
            color_image = color_image[:, :, 2::-1]
            color_image = color_image[..., ::-1]
            color_image = np.ascontiguousarray(color_image)  # 确保图像数据是连续的

            corners, ids, rejected = cv2.aruco.detectMarkers(
                color_image, self.arucoDict, parameters=self.arucoParams)

            if len(corners) > 0:
                ids = ids.flatten()
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners, 0.1, self.mtx, self.dist)

                for i in range(len(corners)):
                    cv2.aruco.drawDetectedMarkers(color_image, corners)
                    cv2.drawFrameAxes(color_image, self.mtx, self.dist,
                                      rvec[i, :, :], tvec[i, :, :], 0.03)

            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)

            key = cv2.waitKey(24)

            # 检查是否有有效的 rvec 和 tvec
            if rvec is not None and tvec is not None and key == ord('c'):
                rvec = np.squeeze(rvec).reshape(3, 1)
                print(rvec)
                R_target2cam1, _ = cv2.Rodrigues(rvec)
                # print('旋转矩阵: ', R_target2cam1, '\n转移矩阵: ', tvec[0, 0, :].copy())
                self.k4a.stop()  # 确保停止流水线
                return R_target2cam1, tvec[0, 0, :].copy()  # 确保返回有效值
                break


