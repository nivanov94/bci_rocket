from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QOpenGLTexture, QImage, QColor, QFont
from OpenGL.GL import *
from OpenGL.GLU import *
import os, copy, math, random
from pylsl import StreamInfo, StreamOutlet

class OGLWidget(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.colors = [QColor(255,0,0), QColor(0,255,0), QColor(0,0,255)]
        self.text_color = QColor(255,255,255);
        self.font = QFont("Arial", 50, QFont.Bold, False)

        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)

        self.update_timer = QTimer()
        self.update_timer.setTimerType(Qt.PreciseTimer)
        self.update_timer.setInterval(16)
        self.update_timer.timeout.connect(self.update)

        self.baseline_cue_duration = 3
        self.baseline_duration = 2
        self.cue_duration = 2
        self.task_duration = 4
        self.break_duration = 2
        self.cue_text = 'cue text'

        # initialize ball positions
        self.pos_hoop = [[-0.6, -0.6],
                         [   0, -0.6],
                         [ 0.6, -0.6]]
        self.start_pos_ball = [[-0.6, 0.7],
                               [   0, 0.7],
                               [ 0.6, 0.7]]
        self.pos_ball = copy.deepcopy(self.start_pos_ball)
        self.drop_ball = [False, False, False]
        self.color_names = ['red', 'green', 'blue']

        self.word_categories = ['Animals', 'Places', 'Vehicles', 'Sport', 'Food']

    def initializeGL(self):
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Find all images
        self.image_dir = 'images'
        self.image_files = []
        for f in os.listdir(self.image_dir):
            fname = os.path.join(self.image_dir, f)
            if os.path.isfile(fname) and fname.endswith('.png'):
                self.image_files.append(f)

        # Load all images
        self.images = {}
        for f in self.image_files:
            im = QOpenGLTexture(QImage(os.path.join(self.image_dir, f)).mirrored())
            im.setMinificationFilter(QOpenGLTexture.Linear)
            im.setMagnificationFilter(QOpenGLTexture.Linear)
            im.setWrapMode(QOpenGLTexture.ClampToBorder)
            im.setBorderColor(QColor(0,0,0,0))
            self.images[f.replace('.png', '')] = im

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0,0,width,height)

    def paintGL(self):
        if self.scene == 'baseline':
            self.baselineScene()
        elif self.scene == 'training':
            self.trainingScene()

    def baselineScene(self):
        if self.stage == 'cue':
            self.drawTextCentered([0,0], [2, 0.5], self.cue_text, self.text_color)
        elif self.stage == 'fixation':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

    def trainingScene(self):
        # Rest
        if self.stage == 'cue_rest':
            self.drawTextCentered([0,0], [2, 0.5], 'Rest', self.text_color)
        elif self.stage == 'rest':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Auditory Imagery
        elif self.stage == 'cue_Auditory Imagery':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['music'])
        elif self.stage == 'Auditory Imagery':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Facial Imagery - Celebrity
        elif self.stage == 'cue_Facial Imagery - Celebrity':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['face_celebrity'])
            self.drawTextCentered([0,0.35], [2, 0.5], 'Celebrity', self.text_color)
        elif self.stage == 'Facial Imagery - Celebrity':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Facial Imagery - Family Member
        elif self.stage == 'cue_Facial Imagery - Family Member':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['face_family'])
            self.drawTextCentered([0,0.35], [2, 0.5], 'Family member', self.text_color)
        elif self.stage == 'Facial Imagery - Family Member':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Motor Imagery - Foot
        elif self.stage == 'cue_Motor Imagery - Foot':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['foot'])
        elif self.stage == 'Motor Imagery - Foot':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Motor Imagery - Left Hand
        elif self.stage == 'cue_Motor Imagery - Left Hand':
            self.drawImageCentered([0,0], [0.8, 0.8], self.images['left_hand'])
        elif self.stage == 'Motor Imagery - Left Hand':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Motor Imagery - Right Hand
        elif self.stage == 'cue_Motor Imagery - Right Hand':
            self.drawImageCentered([0,0], [0.8, 0.8], self.images['right_hand'])
        elif self.stage == 'Motor Imagery - Right Hand':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Motor Imagery - Tongue
        elif self.stage == 'cue_Motor Imagery - Tongue':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['tongue'])
        elif self.stage == 'Motor Imagery - Tongue':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Shape Rotation - Cube
        elif self.stage == 'cue_Shape Rotation - Cube':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['cube'])
        elif self.stage == 'Shape Rotation - Cube':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Shape Rotation - Complex Shape
        elif self.stage == 'cue_Shape Rotation - Complex Shape':
            self.drawImageCentered([0,-0.1], [0.8, 0.8], self.images['complex_shape'])
        elif self.stage == 'Shape Rotation - Complex Shape':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Subtraction - Simple
        elif self.stage == 'cue_Subtraction - Simple':
            num_start = random.randint(51, 100)
            num_subtract = random.randint(3,10)
            self.drawTextCentered([0,0], [2, 0.5], 'Mental Math: %d - %d - %d - %d = ?' % (num_start, num_subtract, num_subtract, num_subtract), self.text_color)
        elif self.stage == 'Subtraction - Simple':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Subtraction - Complex
        elif self.stage == 'cue_Subtraction - Complex':
            num_start = random.randint(100, 200)
            num_subtract = random.randint(3,10)
            self.drawTextCentered([0,0], [2, 0.5], 'Mental Math: %d - %d - %d - %d = ?' % (num_start, num_subtract, num_subtract, num_subtract), self.text_color)
        elif self.stage == 'Subtraction - Complex':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Word Generation
        elif self.stage == 'cue_Word Generation':
            self.drawTextCentered([0,0], [2, 0.5], 'Words: %s' % random.choice(self.word_categories), self.text_color)
        elif self.stage == 'Word Generation':
            self.drawImageCentered([0,0], [0.5, 0.5], self.images['fixation'])

        # Others
        elif self.stage == 'break':
            return
        else:
            self.drawTextCentered([0,0], [2, 0.5], self.stage, self.text_color)

    # def gameScene(self):
    #     if self.stage == 'cue'
        # for i in range(3):
        #     self.drawImageCentered(self.pos_hoop[i], [0.9, 0.9], self.images['hoop_%s_bg' % self.color_names[i]])
        #     self.drawImageCentered(self.pos_ball[i], [0.5, 0.5], self.images['ball_%s' % self.color_names[i]])
        #     self.drawImageCentered(self.pos_hoop[i], [0.9, 0.9], self.images['hoop_%s_fg' % self.color_names[i]])

        #     if self.drop_ball[i]:
        #         self.pos_ball[i][1] -= 0.05

        #     if self.pos_ball[i][1] < -1.5:
        #         self.drop_ball[i] = False
        #         self.pos_ball[i] = copy.deepcopy(self.start_pos_ball[i])

        # self.drawText([-1, 0.3, 1, -0.1], self.cue_text, self.colors[0])

    def drawImageCentered(self, center, size, image):
        # center = [center_x, center_y], size = [size_x, size_y]
        positions = [center[0] - size[0]/2, center[1] - size[1]/2, center[0] + size[0]/2, center[1] + size[1]/2]
        self.drawImage(positions, image)

    def drawImage(self, positions, image):
        # scale positions to maintain image aspect ratio and fit within button
        width = abs(positions[2] - positions[0])
        height = abs(positions[3] - positions[1])
        if width * self.width() <= height * self.height():
            left = positions[0]
            right = positions[2]
            top = (positions[3] + positions[1]) / 2 - (width / image.width() * image.height() / self.height() * self.width()) / 2
            bottom = (positions[3] + positions[1]) / 2 + (width / image.width() * image.height() / self.height() * self.width()) / 2
        else:
            left = (positions[2] + positions[0]) / 2 - (height / image.height() * image.width() / self.width() * self.height()) / 2
            right = (positions[2] + positions[0]) / 2 + (height / image.height() * image.width() / self.width() * self.height()) / 2
            top = positions[1]
            bottom = positions[3]

        # Render image
        # glColor3f(1., 1., 1.)
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, image.textureId())
        glEnable(GL_TEXTURE_2D)

        glBegin(GL_QUADS)
        glTexCoord2f(0,0); glVertex2f(left,top)
        glTexCoord2f(0,1); glVertex2f(left,bottom)
        glTexCoord2f(1,1); glVertex2f(right,bottom)
        glTexCoord2f(1,0); glVertex2f(right,top)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glDepthMask(GL_TRUE)

    def drawTextCentered(self, center, size, text, color, font=None, scale=None):
        positions = [center[0] - size[0]/2, center[1] + size[1]/2, center[0] + size[0]/2, center[1] - size[1]/2]
        self.drawText(positions, text, color, font, scale)

    def drawText(self, positions, text, color, font=None, scale=None):
        if not font:
            font = self.font
        if not scale:
            scale = 0.3
        # convert positions to rect
        pos = []
        pos.append(int((positions[0] + 1.) / 2. * self.width()))
        pos.append(int((1-(positions[1] + 1.) / 2.) * self.height()))
        pos.append(int(((positions[2]-positions[0])) / 2. * self.width()))
        pos.append(int((1-((positions[3]-positions[1]) / 2.) * self.height())))
        rect = QRect(pos[0], pos[1], pos[2], pos[3])

        # draw text at rect
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.TextAntialiasing)
        self.painter.setPen(color)
        font.setPointSizeF(abs(pos[3]) * scale)
        self.painter.setFont(font)
        self.painter.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, text)
        self.painter.end()

    def startBaseline(self, parent):
        self.ui = parent.ui

        self.stream_info = StreamInfo(self.ui.lsl_marker_outlet_lineEdit.text(), 'Markers', 1, 0, 'string', 'bci_hoops')
        self.stream_outlet = StreamOutlet(self.stream_info)
        print("LSL Marker Outlet Stream Initialized")
        for i in range(3):
            self.stream_outlet.push_sample(['initialize baseline'])

        self.scene = 'baseline'
        self.stage = 'cue'
        self.stream_outlet.push_sample(['cue'])
        self.cue_remaining_time = self.baseline_cue_duration
        self.cue_text = 'Starting in %d...' % self.cue_remaining_time
        self.timer.timeout.connect(self.baseline_timer_timeout)
        self.timer.start(1000)

    def baseline_timer_timeout(self):
        self.cue_remaining_time -= 1
        self.cue_text = 'Starting in %d...' % self.cue_remaining_time
        if self.cue_remaining_time == 0:
            self.timer.stop()
            self.timer.timeout.disconnect(self.baseline_timer_timeout)
            self.stream_outlet.push_sample(['baseline'])
            self.stage = 'fixation'
            self.timer.timeout.connect(self.stop)
            self.timer.start(self.baseline_duration * 1000)
        self.update()

    def startTraining(self, parent):
        self.ui = parent.ui

        # get tasks
        self.tasks = [self.ui.task1_comboBox.currentText(), self.ui.task2_comboBox.currentText(), self.ui.task3_comboBox.currentText()]

        # generate randomized trials
        num_trials = int(self.ui.num_trials_lineEdit.text())
        self.trials = [0,1,2] * math.ceil(num_trials / 3)
        self.trials = self.trials[:num_trials]
        random.shuffle(self.trials)
        print('trials: ', self.trials)
        self.current_trial = 0
        self.ui.score_label.setText('Trial: %d / %d' % (self.current_trial + 1, len(self.trials)))

        self.stream_info = StreamInfo(self.ui.lsl_marker_outlet_lineEdit.text(), 'Markers', 1, 0, 'string', 'bci_hoops')
        self.stream_outlet = StreamOutlet(self.stream_info)
        print("LSL Marker Outlet Stream Initialized")
        for i in range(3):
            self.stream_outlet.push_sample(['initialize training'])

        self.scene = 'training'
        self.stage = 'cue_rest'
        self.stream_outlet.push_sample([self.stage])
        self.timer.timeout.connect(self.training_timer_timeout)
        self.timer.start(self.cue_duration * 1000)

    def training_timer_timeout(self):
        self.timer.stop()
        if self.stage == 'cue_rest':
            self.stage = 'rest'
            self.stream_outlet.push_sample([self.stage])
            self.timer.start(self.task_duration * 1000)
        elif self.stage == 'rest':
            self.stage = 'cue_%s' % self.tasks[self.trials[self.current_trial]]
            self.stream_outlet.push_sample([self.stage])
            self.timer.start(self.cue_duration * 1000)
        elif self.stage == 'cue_%s' % self.tasks[self.trials[self.current_trial]]:
            self.stage = self.tasks[self.trials[self.current_trial]]
            self.stream_outlet.push_sample([self.stage])
            self.timer.start(self.task_duration * 1000)
        elif self.stage == self.tasks[self.trials[self.current_trial]]:
            self.stage = 'break'
            self.stream_outlet.push_sample([self.stage])
            self.timer.start(self.break_duration * 1000)
        elif self.stage == 'break':
            self.current_trial += 1
            self.ui.score_label.setText('Trial: %d / %d' % (self.current_trial + 1, len(self.trials)))
            if self.current_trial < len(self.trials):
                self.stage = 'cue_rest'
                self.stream_outlet.push_sample([self.stage])
                self.timer.start(self.cue_duration * 1000)
            else:
                self.stop()
        self.update()

    def stop(self):
        self.timer.stop()
        try:
            self.timer.timeout.disconnect()
        except:
            pass
        self.update_timer.stop()
        try:
            self.update_timer.timeout.disconnect()
        except:
            pass
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)