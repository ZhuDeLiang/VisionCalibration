# VisionCalibration
neican.py :Get neican of Kinect DK
object_base_camera.py:Get 相机坐标系 和 标定板之间的转换矩阵
test.py：手动输入机器人末端坐标系到机器人基坐标系之间的转换矩阵
main.py：通过excel读取获取相机坐标系和标定板之间的转换矩阵  &&   手动输入机器人末端坐标系到机器人基坐标系之间的转换矩阵

使用方法1：
执行 neican.py 得到后复制到 object_base_camera.py
执行test.py 手动输入机器人末端坐标系到机器人基坐标系之间的转换矩阵，相机坐标系和标定板之间的转换矩阵 通过调用 object_base_camera.py得到

使用方法2：
执行main.py
前提是已经得到了多组对应的  机器人末端坐标系到机器人基坐标系之间的转换矩阵  和  相机坐标系和标定板之间的转换矩阵

###########################################
Extra code：
chess.py 用来检测角点
check.py 执行图片标定
