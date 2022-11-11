from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QOpenGLTexture, QImage, QColor, QFont
from OpenGL.GL import *
from OpenGL.GLU import *
import os, copy, math, random

class OGLWidget(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.colors = [QColor(255,0,0), QColor(0,255,0), QColor(0,0,255)]
        self.font = QFont("Arial", 70, QFont.Bold, False)
        self.cue_texts = ['','','']

        self.update_timer = QTimer()
        self.update_timer.setTimerType(Qt.PreciseTimer)
        self.update_timer.setInterval(16)
        self.update_timer.timeout.connect(self.update)

        self.trial_timer = QTimer()
        self.trial_timer.setTimerType(Qt.PreciseTimer)
        self.trial_timer.setInterval(1000)

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

        print(self.image_files)

        # Load all images
        self.images = {}
        for f in self.image_files:
            im = QOpenGLTexture(QImage(os.path.join(self.image_dir, f)).mirrored())
            im.setMinificationFilter(QOpenGLTexture.Linear)
            im.setMagnificationFilter(QOpenGLTexture.Linear)
            im.setWrapMode(QOpenGLTexture.ClampToBorder)
            im.setBorderColor(QColor(0,0,0,0))
            self.images[f.replace('.png', '')] = im

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

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0,0,width,height)

    def paintGL(self):
        for i in range(3):
            self.drawImageCentered(self.pos_hoop[i], [0.9, 0.9], self.images['hoop_%s_bg' % self.color_names[i]])
            self.drawImageCentered(self.pos_ball[i], [0.5, 0.5], self.images['ball_%s' % self.color_names[i]])
            self.drawImageCentered(self.pos_hoop[i], [0.9, 0.9], self.images['hoop_%s_fg' % self.color_names[i]])

            if self.drop_ball[i]:
                self.pos_ball[i][1] -= 0.05

            if self.pos_ball[i][1] < -1.5:
                self.drop_ball[i] = False
                self.pos_ball[i] = copy.deepcopy(self.start_pos_ball[i])

        self.drawText([-1, 0.3, 1, -0.1], self.cue_texts[0], self.colors[0])

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

    def drawText(self, positions, text, color):
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
        self.font.setPointSizeF(abs(pos[3]) * 0.3)
        self.painter.setFont(self.font)
        self.painter.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, text)
        self.painter.end()

    def start(self, parent):
        self.ui = parent.ui
        # generate randomized trials
        num_trials = int(self.ui.num_trials_lineEdit.text())
        self.trials = [0,1,2] * math.ceil(num_trials / 3)
        self.trials = self.trials[:num_trials]
        random.shuffle(self.trials)
        print('trials: ', self.trials)
        # widgets.oglWidget.cue_texts = [widgets.task1_lineEdit.text(), widgets.task2_lineEdit.text(), widgets.task3_lineEdit.text()]

        self.update_timer.start()

    def stop(self):
        self.update_timer.stop()