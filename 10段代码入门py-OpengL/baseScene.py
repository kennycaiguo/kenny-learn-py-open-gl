
"""深度缓冲区和深度测试"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class BaseScene:
    """基于OpenGl.GLUT的三维场景类"""

    def __init__(self, **kwds):
        """构造函数"""

        self.csize = kwds.get('size', (960, 640))       # 画布分辨率
        self.bg = kwds.get('bg', [0.0, 0.0, 0.0])       # 背景色
        self.haxis = kwds.get('haxis', 'y').lower()     # 高度轴
        self.oecs = kwds.get('oecs', [0.0, 0.0, 0.0])   # 视点坐标系ECS原点
        self.near = kwds.get('near', 2.0)               # 相机与视椎体前端面的距离
        self.far = kwds.get('far', 1000.0)              # 相机与视椎体后端面的距离
        self.fovy = kwds.get('fovy', 40.0)              # 相机水平视野角度
        self.dist = kwds.get('dist', 5.0)               # 相机与ECS原点的距离
        self.azim = kwds.get('azim', 0.0)               # 方位角
        self.elev = kwds.get('elev', 0.0)               # 高度角
 
        self.aspect = self.csize[0]/self.csize[1]       # 画布宽高比
        self.cam = None                                 # 相机位置
        self.up = None                                  # 指向相机上方的单位向量
        self._update_cam_and_up()                       # 计算相机位置和指向相机上方的单位向量

        self.left_down = False                          # 左键按下
        self.mouse_pos = (0, 0)                         # 鼠标位置

        # 保存相机初始姿态（视野、方位角、高度角和距离）
        self.home = {'fovy':self.fovy, 'azim':self.azim, 'elev':self.elev, 'dist':self.dist}
 
    def _update_cam_and_up(self, oecs=None, dist=None, azim=None, elev=None):
        """根据当前ECS原点位置、距离、方位角、仰角等参数，重新计算相机位置和up向量"""

        if not oecs is None:
            self.oecs = [*oecs,]
 
        if not dist is None:
            self.dist = dist
 
        if not azim is None:
            self.azim = (azim+180)%360 - 180
 
        if not elev is None:
            self.elev = (elev+180)%360 - 180
 
        up = 1.0 if -90 <= self.elev <= 90 else -1.0
        azim, elev  = np.radians(self.azim), np.radians(self.elev)
        d = self.dist * np.cos(elev)

        if self.haxis == 'z':
            azim -= 0.5 * np.pi
            self.cam = [d*np.cos(azim)+self.oecs[0], d*np.sin(azim)+self.oecs[1], self.dist*np.sin(elev)+self.oecs[2]]
            self.up = [0.0, 0.0, up]
        else:
            self.cam = [d*np.sin(azim)+self.oecs[0], self.dist*np.sin(elev)+self.oecs[1], d*np.cos(azim)+self.oecs[2]]
            self.up = [0.0, up, 0.0]

    def reshape(self, w, h):
        """改变窗口大小事件函数"""
 
        self.csize = (w, h)
        self.aspect = self.csize[0]/self.csize[1] if self.csize[1] > 0 else 1e4
        glViewport(0, 0, self.csize[0], self.csize[1])
 
        glutPostRedisplay()

    def click(self, btn, state, x, y):
        """鼠标按键和滚轮事件函数"""
 
        if btn == 0: # 左键
            if state == 0: # 按下
                self.left_down = True
                self.mouse_pos = (x, y)
            else: # 弹起
                self.left_down = False 
        elif btn == 2 and state ==1: # 右键弹起，恢复相机初始姿态
            self._update_cam_and_up(dist=self.home['dist'], azim=self.home['azim'], elev=self.home['elev'])
            self.fovy = self.home['fovy']
        elif btn == 3 and state == 0: # 滚轮前滚
            self.fovy *= 0.95
        elif btn == 4 and state == 0: # 滚轮后滚
            self.fovy += (180 - self.fovy) / 180
        
        glutPostRedisplay()

    def drag(self, x, y):
        """鼠标拖拽事件函数"""
        
        dx, dy = x - self.mouse_pos[0], y - self.mouse_pos[1]
        self.mouse_pos = (x, y)

        azim = self.azim - (180*dx/self.csize[0]) * (self.up[2] if self.haxis == 'z' else self.up[1])
        elev = self.elev + 90*dy/self.csize[1]
        self._update_cam_and_up(azim=azim, elev=elev)
        
        glutPostRedisplay()

    def prepare(self):
        """GL初始化后、开始绘制前的预处理。可在派生类中重写此方法"""

        pass

    def draw(self):
        """绘制模型。可在派生类中重写此方法"""

        glBegin(GL_TRIANGLES)                   # 开始绘制三角形
        glColor(1.0, 0.0, 0.0)                  # 设置当前颜色为红色
        glVertex(0.0, 1.0, 0.5)                 # 设置顶点
        glColor(0.0, 1.0, 0.0)                  # 设置当前颜色为绿色
        glVertex(-1.0, -1.0, 0.5)               # 设置顶点
        glColor(0.0, 0.0, 1.0)                  # 设置当前颜色为蓝色
        glVertex(1.0, -1.0, 0.5)                # 设置顶点
        glEnd()                                 # 结束绘制三角形
            
        glBegin(GL_TRIANGLES)                   # 开始绘制三角形
        glColor(1.0, 0.0, 0.0)                  # 设置当前颜色为红色
        glVertex(0.0, 1.0, -0.5)                # 设置顶点
        glColor(0.0, 1.0, 0.0)                  # 设置当前颜色为绿色
        glVertex(-1.0, -1.0, -0.5)              # 设置顶点
        glColor(0.0, 0.0, 1.0)                  # 设置当前颜色为蓝色
        glVertex(1.0, -1.0, -0.5)               # 设置顶点
        glEnd()                                 # 结束绘制三角形

    def render(self):
        """重绘事件函数"""

        # 清除屏幕及深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 设置投影矩阵 
        glMatrixMode(GL_PROJECTION) # 操作投影矩阵
        glLoadIdentity() # 将投影矩阵设置为单位矩阵
        gluPerspective(self.fovy, self.aspect, self.near, self.far) # 生成透视投影矩阵
        
        # 设置视点矩阵
        gluLookAt(*self.cam, *self.oecs, *self.up)

        # 设置模型矩阵
        glMatrixMode(GL_MODELVIEW) # 操作模型矩阵
        glLoadIdentity() # 将模型矩阵设置为单位矩阵
        
        # 绘制模型
        self.draw()

        # 交换缓冲区
        glutSwapBuffers()

    def show(self):
        """显示"""

        glutInit() # 初始化glut库

        sw, sh = glutGet(GLUT_SCREEN_WIDTH), glutGet(GLUT_SCREEN_HEIGHT)
        left, top = (sw-self.csize[0])//2, (sh-self.csize[1])//2

        glutInitWindowSize(*self.csize) # 设置窗口大小
        glutInitWindowPosition(left, top) # 设置窗口位置
        glutCreateWindow('Data View Toolkit') # 创建窗口
        
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH) # 设置显示模式
        glClearColor(*self.bg, 1.0) # 设置背景色
        glEnable(GL_DEPTH_TEST) # 开启深度测试
        glDepthFunc(GL_LEQUAL) # 设置深度测试函数的参数

        self.prepare() # GL初始化后、开始绘制前的预处理

        glutDisplayFunc(self.render) # 绑定重绘事件函数
        glutReshapeFunc(self.reshape) # 绑定窗口大小改变事件函数
        glutMouseFunc(self.click) # 绑定鼠标按键和滚轮事件函数
        glutMotionFunc(self.drag) # 绑定鼠标拖拽事件函数
        
        glutMainLoop() # 进入glut主循环


