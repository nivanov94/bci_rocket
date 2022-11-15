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

        self.setWindowTitle("BCI Rocket")

        # setup UI elements
        for w in widgets.centralwidget.findChildren(QPushButton):
            w.clicked.connect(self.buttonClick)

        widgets.num_trials_lineEdit.setValidator(QIntValidator(3, 3000))

        # for w in widgets.centralwidget.findChildren(QComboBox):
        #     w.currentTextChanged.connect(self.changeSettings)
        # self.settings_valid = True
        # for w in widgets.centralwidget.findChildren(QLineEdit):
        #     w.textChanged.connect(self.changeSettings)
        # self.settings_valid = True

        # setup opengl widget
        widgets.oglWidget = OGLWidget(self)
        widgets.game_frame.layout().addWidget(widgets.oglWidget)

        # setup
        self.settings_lineEdits = [widgets.num_trials_lineEdit, widgets.lsl_marker_outlet_lineEdit, widgets.lsl_prediction_inlet_lineEdit]
        self.settings_lineEdits_labels = [widgets.num_trials_label, widgets.lsl_marker_outlet_label, widgets.lsl_prediction_inlet_label]
        self.settings_comboBoxes = [widgets.task1_comboBox, widgets.task2_comboBox, widgets.task3_comboBox]
        self.settings_comboBoxes_labels = [widgets.task1_label, widgets.task2_label, widgets.task3_label]

        self.show()

        widgets.num_trials_lineEdit.setText('6')

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == 'btn_baseline':
            self.startBaseline()
        elif btnName == 'btn_settings':
            widgets.stackedWidget.setCurrentWidget(widgets.settings_page)
        elif btnName == 'btn_training':
            self.startTraining()
        elif btnName == 'btn_start_game':
            self.startGame()
        elif btnName == 'btn_save_settings':
            self.saveSettings()
        elif btnName == 'btn_back':
            widgets.oglWidget.stop()
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)

    def saveSettings(self):
        self.settings_valid = True
        
        for i in range(len(self.settings_lineEdits)):
            if self.settings_lineEdits[i].text() == '':
                self.settings_lineEdits_labels[i].setStyleSheet('color: red;')
                self.settings_valid = False
            else:
                self.settings_lineEdits_labels[i].setStyleSheet('color: black;')

        comboBox_index = [cb.currentIndex() for cb in self.settings_comboBoxes]
        duplicate_index = {x for x in comboBox_index if comboBox_index.count(x) > 1}
        for i in range(len(self.settings_comboBoxes)):
            if self.settings_comboBoxes[i].currentIndex() in duplicate_index:
                self.settings_comboBoxes_labels[i].setStyleSheet('color: red;')
                self.settings_valid = False
            else:
                self.settings_comboBoxes_labels[i].setStyleSheet('color: black;')

        if self.settings_valid:
            widgets.btn_save_settings.setText('Save')
            widgets.btn_save_settings.setEnabled(True)
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
        else:
            widgets.btn_save_settings.setText('Save - Invalid Settings')
            widgets.btn_save_settings.setEnabled(True)

    def startBaseline(self):
        print('start baseline')
        widgets.stackedWidget.setCurrentWidget(widgets.game_page)
        widgets.oglWidget.startBaseline(self)

    def startTraining(self):
        print('start training')
        widgets.stackedWidget.setCurrentWidget(widgets.game_page)
        widgets.oglWidget.startTraining(self)

    def startGame(self):
        widgets.stackedWidget.setCurrentWidget(widgets.game_page)
        widgets.oglWidget.startGame(self)

    def keyPressEvent(self, event):
        if widgets.stackedWidget.currentWidget() == widgets.game_page:
            if event.key() == Qt.Key_1:
                widgets.oglWidget.selectTask(0)
            if event.key() == Qt.Key_2:
                widgets.oglWidget.selectTask(1)
            if event.key() == Qt.Key_3:
                widgets.oglWidget.selectTask(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("bci_rocket.ico"))
    window = MainWindow()
    sys.exit(app.exec_())