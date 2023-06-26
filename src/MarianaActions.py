
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
import os

class MarianaActions(QAction):
    def __init__(self, parent, actionName):
        super().__init__("", parent)
        self.parent = parent
        self.actionName = actionName
    
    def createSubMenu(self, actionName, actionId, tips, shortcut=None, iconFileName=None):
        self.setText(actionName)
        self.triggered.connect(lambda: self.handle_action(actionId))
        self.setStatusTip(tips)
        if shortcut:
            self.setShortcut(shortcut)
        if iconFileName:
            self.setIcon(QIcon(os.path.join(self.parent.path_images, iconFileName)))


    def handle_action(self, actionId):
        pass
        
    def close(self, parent):
        parent.close()

