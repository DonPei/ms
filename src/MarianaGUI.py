
import os, sys, time
from pathlib import Path
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QStyleFactory, QFileDialog, QDesktopWidget, QErrorMessage, QMessageBox, QSizePolicy, QToolBar, QStatusBar, QDockWidget, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QSize, QRect, QThreadPool
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


from MarianaMenu import MarianaMenu

from telemetrix import telemetrix
from config import Config, UserPreference
from MarianaThreadPool import Worker

from pathlib import Path


class MarianaGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.path_root = Path(os.path.abspath(__file__)).parents[0]
        self.path_parent = Path(os.path.abspath(__file__)).parents[1]
        self.path_images = os.path.join(self.path_root, 'images')
        self.path_examples = os.path.join(self.path_parent, 'examples')
        self.path_resources = os.path.join(self.path_parent, 'resources')
        self.config = Config(os.path.join(self.path_root, 'config.ini'))

        home = Path.home()
        dirname = home / '.mariana'
        if not dirname.exists():
            os.mkdir(dirname)
            
        filename = Path("user_preference.ini")
        filename.touch(exist_ok= True)
        self.userPreference = UserPreference(filename)

        try:
            self.board = telemetrix.Telemetrix()
        except Exception as e:
            self.board = None
            print(e)
        
        self.available_cameras = QCameraInfo.availableCameras() 
        if not self.available_cameras: 
            sys.exit()
        
        self.initializeAndShow()
        
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        if self.board:
            self.initMotors()

    def initMotors(self):
        print("starting to Init Motor")
        worker = Worker(self.connectMotors, 1, actionId=1)
        worker.signals.result.connect(self.setMotors)
        worker.signals.finished.connect(self.initMotorsComplete)
        self.threadpool.start(worker)

    def connectMotors(self, *args, **kwargs):
        motors = []
        names = ["motor1", "motor2", "motor3"]
        for name in names:
            stepPin = int(self.config.get(name, "stepPin"))
            dirPin = int(self.config.get(name, "dirPin"))
            print(f'{name} stepPin={stepPin} dirPin={dirPin}')
            motor = self.board.set_pin_mode_stepper(interface=1, pin1=stepPin, pin2=dirPin)
            self.board.stepper_set_max_speed(motor, 400)
            time.sleep(.5)
            self.board.stepper_set_acceleration(motor, 800)
            time.sleep(.5)
            self.board.stepper_set_speed(motor, 400)
            time.sleep(.5)
            motors.append(motor)
        return motors

    def setMotors(self, motors):
        self.motors = motors
    def initMotorsComplete(self):
        print("Init Motor completed")

    def closeEvent(self, event):
        print('Window closed')
        if self.board:
            self.board.shutdown()
        self.config.save()
        sys.exit(0)

    def closeEvent1(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
            #self.threadpool.cancel()
            #self.threadpool.waitForDone()
            sys.exit(0)
        else:
            event.ignore()

    def initializeAndShow(self):
        #self.setFixedSize(650, 650)
        self.setWindowIcon(QIcon(os.path.join(self.path_images, 'marianaLogo_greenCircle.png')))
        self.setWindowTitle('MARIANA')
        self.centerMainWindow()
        self.createToolsDockWidget()

        #self.createMenu()
        menu_bar = self.menuBar()
        self.maMenu = MarianaMenu(self)
        self.maMenu.createMenu(menu_bar)
        self.statusBar = QStatusBar(self)
        self.statusBar.setStyleSheet("background : white;")
        self.setStatusBar(self.statusBar)

        #self.createToolBar()
        if self.available_cameras: 
            self.cameraWidget()
        else:
            self.photoEditorWidgets()
        self.show()

    def createToolBar(self):
        """
        Create toolbar for photo editor GUI
        """
        tool_bar = QToolBar("Photo Editor Toolbar")
        tool_bar.setIconSize(QSize(24,24))
        self.addToolBar(tool_bar)

        # add actions to toolbar
        tool_bar.addAction(self.open_act)
        tool_bar.addAction(self.save_act)
        tool_bar.addAction(self.print_act)
        tool_bar.addAction(self.clear_act)
        tool_bar.addSeparator()
        tool_bar.addAction(self.exit_act)

    def createToolsDockWidget(self):
        """
        Use View -> Edit Image Tools menu and click the dock widget on or off.
        Tools dock can be placed on the left or right of the main window. 
        """
        # set up QDockWidget
        self.dock_tools_view = QDockWidget()
        self.dock_tools_view.setWindowTitle("Edit Image Tools")
        self.dock_tools_view.setAllowedAreas(Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea)

        # create container QWidget to hold all widgets inside dock widget
        self.tools_contents = QWidget()

        # create tool push buttons 
        self.rotate90 = QPushButton("Rotate 90º")
        self.rotate90.setMinimumSize(QSize(130, 40))
        self.rotate90.setStatusTip('Rotate image 90º clockwise')
        self.rotate90.clicked.connect(self.rotateImage90)

        self.rotate180 = QPushButton("Rotate 180º")
        self.rotate180.setMinimumSize(QSize(130, 40))
        self.rotate180.setStatusTip('Rotate image 180º clockwise')
        self.rotate180.clicked.connect(self.rotateImage180)

        self.flip_horizontal = QPushButton("Flip Horizontal")
        self.flip_horizontal.setMinimumSize(QSize(130, 40))
        self.flip_horizontal.setStatusTip('Flip image across horizontal axis')
        self.flip_horizontal.clicked.connect(self.flipImageHorizontal)

        self.flip_vertical = QPushButton("Flip Vertical")
        self.flip_vertical.setMinimumSize(QSize(130, 40))
        self.flip_vertical.setStatusTip('Flip image across vertical axis')
        self.flip_vertical.clicked.connect(self.flipImageVertical)

        self.resize_half = QPushButton("Resize Half")
        self.resize_half.setMinimumSize(QSize(130, 40))
        self.resize_half.setStatusTip('Resize image to half the original size')
        self.resize_half.clicked.connect(self.resizeImageHalf)

        # set up vertical layout to contain all the push buttons 
        dock_v_box = QVBoxLayout()
        dock_v_box.addWidget(self.rotate90)
        dock_v_box.addWidget(self.rotate180)
        dock_v_box.addStretch(1)
        dock_v_box.addWidget(self.flip_horizontal)
        dock_v_box.addWidget(self.flip_vertical)
        dock_v_box.addStretch(1)
        dock_v_box.addWidget(self.resize_half)
        dock_v_box.addStretch(6)

        # set the main layout for the QWidget, tools_contents,
        # then set the main widget of the dock widget
        self.tools_contents.setLayout(dock_v_box)
        self.dock_tools_view.setWidget(self.tools_contents)
        
        # set initial location of dock widget
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_tools_view)

        # handles the visibility of the dock widget
        self.toggle_dock_tools_act = self.dock_tools_view.toggleViewAction()

    def photoEditorWidgets(self):
        self.image = QPixmap()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.setCentralWidget(self.image_label)

    def cameraWidget(self):
        self.save_path = ""
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show() 
        self.setCentralWidget(self.viewfinder)
        self.select_camera(1)
    
    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()
        
        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda error_msg, error, msg: self.alert(msg))
        self.capture.imageCaptured.connect(lambda d, i: self.status.showMessage("Image captured : "+ str(self.save_seq))) 
        
        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0
    
    # method to take photo
    def click_photo(self):
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.save_path,"%s-%04d-%s.jpg" % (self.current_camera_name, self.save_seq, timestamp)))
        self.save_seq += 1

    def change_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Picture Location", "") 
        if path:
            self.save_path = path
            self.save_seq = 0

    def alert(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)
                
    def rotateImage90(self):
        """
        Rotate image 90º clockwise
        """
        if self.image.isNull() == False:
            transform90 = QTransform().rotate(90)
            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform90, mode=Qt.SmoothTransformation)

            self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(rotated) 
            self.image_label.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def rotateImage180(self):
        """
        Rotate image 180º clockwise
        """
        if self.image.isNull() == False:
            transform180 = QTransform().rotate(180)
            pixmap = QPixmap(self.image)

            rotated = pixmap.transformed(transform180, mode=Qt.SmoothTransformation)

            self.image_label.setPixmap(rotated.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # .......... To keep being allowed to rotate the image
            self.image = QPixmap(rotated) 
            self.image_label.repaint() # repaint the child widget
        else:
            # No image to rotate
            pass

    def flipImageHorizontal(self):
        """
        Mirror the image across the horizontal axis
        """
        if self.image.isNull() == False:
            flip_h = QTransform().scale(-1, 1)
            pixmap = QPixmap(self.image)

            flipped = pixmap.transformed(flip_h)

            self.image_label.setPixmap(flipped.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(flipped)
            self.image_label.repaint()
        else:
            # No image to flip
            pass

    def flipImageVertical(self):
        """
        Mirror the image across the vertical axis
        """
        if self.image.isNull() == False:
            flip_v = QTransform().scale(1, -1)
            pixmap = QPixmap(self.image)

            flipped = pixmap.transformed(flip_v)

            self.image_label.setPixmap(flipped.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(flipped)
            self.image_label.repaint()
        else:
            # No image to flip
            pass

    def resizeImageHalf(self):
        """
        Resize the image to half its current size.
        """
        if self.image.isNull() == False:
            resize = QTransform().scale(0.5, 0.5)
            pixmap = QPixmap(self.image)

            resized = pixmap.transformed(resize)

            self.image_label.setPixmap(resized.scaled(self.image_label.size(), 
                Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QPixmap(resized)
            self.image_label.repaint()
        else:
            # No image to resize
            pass

    def centerMainWindow(self):
        app = QApplication.instance()
        screen = app.screenAt(self.pos())
        geometry = screen.availableGeometry()
        screen_width = geometry.width()
        screen_height = geometry.height()
        self.setFixedSize(int(screen_width * 0.6), int(screen_height * 0.8))
        #desktop = QDesktopWidget().screenGeometry()
        self.move(int((screen_width - self.width()) / 2), int((screen_height - self.height()) / 2))

    def on_about_to_quit(self):
        print("Application is about to quit")
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def screen_resolutions(self):
        for displayNr in range(QtWidgets.QDesktopWidget().screenCount()):
            sizeObject = QtWidgets.QDesktopWidget().screenGeometry(displayNr)
            print("Display: " + str(displayNr) + " Screen size : " + str(sizeObject.height()) + "x" + str(sizeObject.width()))

   
# Run program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(QStyleFactory.keys())
    app.setStyle("Windows")
    #QCoreApplication.aboutToQuit.connect(on_about_to_quit)
    #app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    ex = MarianaGUI()
    sys.exit(app.exec_())
