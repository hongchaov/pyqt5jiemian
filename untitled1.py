"可以显示矩形区域"
from collections import  deque
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import *
import numpy as np
#import imutils
import cv2
import sys
import time
import threading
#设定蓝色阈值，HSV空间
blueLower = np.array([100, 100, 100])
blueUpper = np.array([120, 255, 255])
#初始化追踪点的列表
mybuffer = 64
pts = deque(maxlen=mybuffer)
#打开摄像头
camera = cv2.VideoCapture(0)
#等待两秒
time.sleep(2)
#遍历每一帧，检测蓝色瓶盖

class MyTemperatureThread(QThread):
    def __init__(self, parent=None):  # 线程初始化
        super().__init__(parent)

    breakSignal = pyqtSignal(int, int)

    def run(self):
        while True:
            # 读取帧
            (ret, frame) = camera.read()
            frame = cv2.flip(frame, 1, dst=None)  # 水平镜像
            # 判断是否成功打开摄像头
            if not ret:
                print('No Camera')
                break
            # frame = imutils.resize(frame, width=600)
            # 转到HSV空间
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # 根据阈值构建掩膜
            mask = cv2.inRange(hsv, blueLower, blueUpper)
            # 腐蚀操作
            mask = cv2.erode(mask, None, iterations=2)
            # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
            mask = cv2.dilate(mask, None, iterations=2)
            # 轮廓检测
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            # 初始化瓶盖圆形轮廓质心
            center = None
            # 如果存在轮廓
            if len(cnts) > 0:
                # 找到面积最大的轮廓
                c = max(cnts, key=cv2.contourArea)
                # 确定面积最大的轮廓的矩形
                x, y, w, h = cv2.boundingRect(c)
                # 计算轮廓的矩
                M = cv2.moments(c)
                # 计算质心
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # 只有当半径大于10时，才执行画图
                a = int(M["m10"] / M["m00"])
                b = int(M["m01"] / M["m00"])
                print("x：", a)
                print("y: ", b)
                self.breakSignal.emit(a, b)
                # print(center)#显示中心点坐标
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 显示矩形框
                cv2.circle(frame, center, 1, (0, 0, 255), -1)  # 显示圆心
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
            # 摄像头释放



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(645, 483)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 483, 483))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../jre/cheku.jpg"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(420, 90, 32, 21))
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../jre/luvse.jpg"))
        self.label_2.setObjectName("label_2")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
def chuli(a,b):
    ui.label_2.move(a, b)
if __name__ == '__main__':

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    cv2.waitKey(1000)

    T = MyTemperatureThread()
    #T.run()
    T.breakSignal.connect(chuli)
    T.start()
   # a=10
   # b=10
    sys.exit(app.exec_())
    #销毁所有窗口
    cv2.destroyAllWindows()

