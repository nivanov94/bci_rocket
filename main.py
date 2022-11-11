import sys

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

        for w in widgets.centralwidget.findChildren(QLineEdit):
            w.textChanged.connect(self.changeSettings)
        self.settings_valid = True

        # setup graphics view
        widgets.scene = QGraphicsScene()
        widgets.graphicsView.setScene(widgets.scene)

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

    def changeSettings(self):
        settings_lineEdits = [widgets.task1_lineEdit, widgets.task2_lineEdit, widgets.task3_lineEdit, widgets.num_trials_lineEdit, widgets.lsl_marker_outlet_lineEdit, widgets.lsl_prediction_inlet_lineEdit]
        
        self.settings_valid = True

        for w in settings_lineEdits:
            w_name = w.objectName().replace('_lineEdit', '')
            if w.text() == '':
                eval("widgets.%s_label.setStyleSheet('color: red;')" % w_name)
                self.settings_valid = False
            else:
                eval("widgets.%s_label.setStyleSheet('color: black;')" % w_name)

        if self.settings_valid:
            widgets.btn_save_settings.setText('Save')
            widgets.btn_save_settings.setEnabled(True)
        else:
            widgets.btn_save_settings.setText('Invalid Settings')
            widgets.btn_save_settings.setEnabled(False)

    def startTraining(self):
        widgets.stackedWidget.setCurrentWidget(widgets.game_page)
        print('start training')
        widgets.scene.clear()
        widgets.scene.addText('TRAINING')

    def startGame(self):
        widgets.stackedWidget.setCurrentWidget(widgets.game_page)
        print('start game')
        widgets.scene.clear()
        widgets.scene.addText('GAME')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())