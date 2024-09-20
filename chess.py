import numpy as np
import cv2
from pyk4a import PyK4A

class shouyan1:
    def __init__(self):
        # 定义 ArUco 标记字典（保留原代码，可能在别的地方需要用到）
        self.ARUCO_DICT = {
            "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
            "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
            # ...（其他字典项可按需添加）
        }

        # 相机内参和畸变系数（保留原代码）
        self.dist = np.array([3.56499135e-01, -2.38331628e+00, 1.09357561e-03, -8.55933584e-04,
                              1.37534881e+00, 2.41856128e-01, -2.21700788e+00, 1.30763078e+00])
        self.mtx = np.array([[605.9921875, 0, 638.23809814],
                             [0, 605.88006592, 367.54467773],
                             [0, 0, 1]])

        # 配置和启动 Kinect DK
        self.k4a = PyK4A()
        self.k4a.start()

    def detect_chessboard_corners(self, chessboard_size=(9, 6)):
        while True:
            # 从 Kinect DK 捕获一帧图像
            capture = self.k4a.get_capture()
            color_image = capture.color
            color_image = color_image[:, :, 2::-1]
            color_image = np.ascontiguousarray(color_image)  # 确保图像数据是连续的

            # 转换为灰度图像
            gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

            # 检测棋盘格角点
            ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

            # 如果找到角点，进一步精确化角点位置
            if ret:
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                # 绘制角点
                cv2.drawChessboardCorners(color_image, chessboard_size, corners, ret)

            # 显示图像
            cv2.namedWindow('Kinect DK - Chessboard Detection', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Kinect DK - Chessboard Detection', color_image)

            # 按下 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放资源
        cv2.destroyAllWindows()
        self.k4a.stop()

# 使用示例
if __name__ == "__main__":
    camera = shouyan1()
    camera.detect_chessboard_corners()
