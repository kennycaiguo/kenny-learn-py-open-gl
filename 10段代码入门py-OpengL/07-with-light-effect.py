import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from  baseScene import BaseScene

class App(BaseScene):
    """由BaseScene派生的3D应用程序类"""

    def __init__(self, **kwds):
        """构造函数"""

        BaseScene.__init__(self, **kwds)    # 调用基类构造函数
        self.models = list()                # 模型列表，保存模型的VBO

    def prepare(self):
        """初始化灯光"""

        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.8,1.0,0.8,1.0))                 # 光源中的环境光
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8,0.8,0.8,1.0))                 # 光源中的散射光
        glLightfv(GL_LIGHT0, GL_SPECULAR, (0.2,0.2,0.2,1.0))                # 光源中的反射光
        glLightfv(GL_LIGHT0, GL_POSITION, (2.0,-20.0,5.0,1.0))              # 光源位置
        
        glLightfv(GL_LIGHT1, GL_AMBIENT, (0.5,0.5,0.5,1.0))                 # 光源中的环境光
        glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.3,0.3,0.3,1.0))                 # 光源中的散射光
        glLightfv(GL_LIGHT1, GL_SPECULAR, (0.2,0.2,0.2,1.0))                # 光源中的反射光
        glLightfv(GL_LIGHT1, GL_POSITION, (-2.0,20.0,-1.0,1.0))             # 光源位置

    def draw(self):
        """绘制模型。可在派生类中重写此方法"""

        glPushAttrib(GL_ALL_ATTRIB_BITS) # 保存当前全部环境设置
        glEnable(GL_LIGHTING) # 启用光照
        glEnable(GL_LIGHT0) # 开启的灯光0：光线偏绿色，从下向上照射
        glPushMatrix() # 保存当前矩阵
        glTranslate(-1, 0, 0) # 平移
        glutSolidSphere(1, 180, 90) # 绘制球
        glPopMatrix() # 恢复保存的矩阵
        glPopAttrib() # 恢复当前全部环境设置

        glPushAttrib(GL_ALL_ATTRIB_BITS) # 保存当前全部环境设置
        glEnable(GL_LIGHTING) # 启用光照
        glEnable(GL_LIGHT1) # 开启的灯光1：稍暗淡，从上向下照射
        glPushMatrix() # 保存当前矩阵
        glTranslate(1, 0, 0) # 平移
        glutSolidCube(1) # 绘制六面体
        glPopMatrix() # 恢复保存的矩阵
        glPopAttrib() # 恢复当前全部环境设置

if __name__ == '__main__':
    app = App(hax='y')
    app.show()
