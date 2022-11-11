import sys
import math, random
from modules import *

widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        # SET AS GLOBAL WIDGETS
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        self.setWindowTitle("BCI Hoops")

        # setup UI elements
        for w in widgets.centralwidget.findChildren(QPushButton):
            w.clicked.connect(self.buttonClick)

        widgets.num_trials_lineEdit.setValidator(QIntValidator(3, 3000))

        for w in widgets.centralwidget.findChildren(QComboBox):
            w.textChanged.connect(self.changeSettings)
        self.settings_valid = True
        for w in widgets.centralwidget.findChildren(QLineEdit):
            w.textChanged.connect(self.changeSettings)
        self.settings_valid = True

        # setup opengl widget
        widgets.oglWidget = OGLWidget(self)
        widgets.game_frame.layout().addWidget(widgets.oglWidget)

        self.show()

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == 'btn_settings':
            widgets.stackedWidget.setCurrentWidget(widgets.settings_page)
        elif btnName == 'btn_training':
            self.startTraining()
        elif btnName == 'btn_start_game':
            self.startGame()
        elif btnName == 'btn_save_settings':
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        elif btnName == 'btn_back':
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            widgets.oglWidget.stop()

    def changeSettings(self):
        self.settings_valid = True
        
        settings_lineEdits = [widgets.num_trials_lineEdit, widgets.lsl_marker_outlet_lineEdit, widgets.lsl_prediction_inlet_lineEdit]
        for w in settings_lineEdits:
            w_name = w.objectName().replace('_lineEdit', '')
            if w.text() == '':
                eval("widgets.%s_label.setStyleSheet('color: red;')" % w_name)
                self.settings_valid = False
            else:
                eval("widgets.%s_label.setStyleSheet('color: black;')" % w_name)

        settings_comboBoxes = [widgets.task1_comboBox, widgets.task2_comboBox, widgets.task3_comboBox]
        # for i in range(len(settings_comboBoxes)):
            # if settings_comboBoxes[i].currentIndex

        if self.settings_valid:
            widgets.btn_save_settings.setText('Save')
            widgets.btn_save_settings.setEnabled(True)
        else:
            widgets.btn_save_settings.setText('Invalid Settings')
            widgets.btn_save_settings.setEnabled(False)

    def startTraining(self):
        print('start training')
        widgets.stackedWidget.setCurrentWidget(widgets.game_page)
        widgets.oglWidget.start(self)

    def startGame(self):
        widgets.stackedWidget.setCurrentWidget(widgets.game_page)
        print('start game')        

    def keyPressEvent(self, event):
        if widgets.stackedWidget.currentWidget() == widgets.game_page:
            if event.key() == Qt.Key_1:
                widgets.oglWidget.drop_ball[0] = True
            if event.key() == Qt.Key_2:
                widgets.oglWidget.drop_ball[1] = True
            if event.key() == Qt.Key_3:
                widgets.oglWidget.drop_ball[2] = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())