from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QOpenGLTexture, QImage, QColor
from OpenGL.GL import *
from OpenGL.GLU import *
import os

class OGLWidget(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_AlwaysStackOnTop)

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
        self.start_pos_ball_red    = [-0.6, 0.7]
        self.start_pos_ball_green  = [   0, 0.7]
        self.start_pos_ball_blue   = [ 0.6, 0.7]
        self.pos_ball_red    = self.start_pos_ball_red.copy()
        self.pos_ball_green  = self.start_pos_ball_green.copy()
        self.pos_ball_blue   = self.start_pos_ball_blue.copy()

        # settings
        self.drop_red = False
        self.drop_green = False
        self.drop_blue = False

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0,0,width,height)

    def paintGL(self):
        self.drawImageCentered([-0.6, -0.6], [0.9, 0.9], self.images['hoop_red_bg'])
        self.drawImageCentered([   0, -0.6], [0.9, 0.9], self.images['hoop_green_bg'])
        self.drawImageCentered([ 0.6, -0.6], [0.9, 0.9], self.images['hoop_blue_bg'])

        self.drawImageCentered(self.pos_ball_red,   [0.5, 0.5], self.images['ball_red'])
        self.drawImageCentered(self.pos_ball_green, [0.5, 0.5], self.images['ball_green'])
        self.drawImageCentered(self.pos_ball_blue,  [0.5, 0.5], self.images['ball_blue'])
        
        self.drawImageCentered([-0.6, -0.6], [0.9, 0.9], self.images['hoop_red_fg'])
        self.drawImageCentered([   0, -0.6], [0.9, 0.9], self.images['hoop_green_fg'])
        self.drawImageCentered([ 0.6, -0.6], [0.9, 0.9], self.images['hoop_blue_fg'])

        if self.drop_red:
            self.pos_ball_red[1] -= 0.05
        if self.drop_green:
            self.pos_ball_green[1] -= 0.05
        if self.drop_blue:
            self.pos_ball_blue[1] -= 0.05

        if self.pos_ball_red[1] < -1.5:
            self.drop_red = False
            self.pos_ball_red = self.start_pos_ball_red.copy()
        if self.pos_ball_green[1] < -1.5:
            self.drop_green = False
            self.pos_ball_green = self.start_pos_ball_green.copy()
        if self.pos_ball_blue[1] < -1.5:
            self.drop_blue = False
            self.pos_ball_blue = self.start_pos_ball_blue.copy()

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

    def drawText(self, positions, text):
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
        self.painter.setPen(self.text_color)
        self.font.setPointSizeF(abs(pos[3]) * 0.3)
        self.painter.setFont(self.font)
        self.painter.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, text)
        self.painter.end()