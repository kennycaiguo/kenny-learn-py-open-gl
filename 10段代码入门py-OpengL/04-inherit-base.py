from OpenGL.GL import *
from OpenGL.GLUT import *
from  baseScene import BaseScene

class App(BaseScene):
    """由BaseScene派生的3D应用程序类"""
 
    def draw(self):
        """绘制模型"""

        glBegin(GL_LINES)                   # 开始绘制线段
        glColor(1.0, 0.0, 0.0)              # 设置当前颜色为红色
        glVertex(-1.0, 0.0, 0.0)            # 设置线段顶点（x轴负方向）
        glVertex(0.8, 0.0, 0.0)             # 设置线段顶点（x轴正方向）
        glColor(0.0, 1.0, 0.0)              # 设置当前颜色为绿色
        glVertex(0.0, -1.0, 0.0)            # 设置线段顶点（y轴负方向）
        glVertex(0.0, 0.8, 0.0)             # 设置线段顶点（y轴正方向）
        glColor(0.0, 0.0, 1.0)              # 设置当前颜色为蓝色
        glVertex(0.0, 0.0, -1.0)            # 设置线段顶点（z轴负方向）
        glVertex(0.0, 0.0, 0.8)             # 设置线段顶点（z轴正方向）
        glEnd()                             # 结束绘制线段

        glColor(1.0, 1.0, 1.0)              # 设置当前颜色为白色
        glutWireCone(0.3, 0.6, 10, 5)       # 绘制圆锥（线框）

        glPushMatrix()                      # 保存当前矩阵
        glRotate(90, 0, 1, 0)               # 绕向量(0,1,0)即y轴旋转90度
        glTranslate(0, 0, 0.8)              # x轴变z轴，向z轴正方向平移
        glColor(1.0, 0.0, 0.0)              # 设置当前颜色为红色
        glutSolidCone(0.02, 0.2, 30, 30)    # 绘制圆锥（实体）
        glPopMatrix()                       # 恢复保存的矩阵

        glPushMatrix()                      # 保存当前矩阵
        glRotate(-90, 1, 0, 0)              # 绕向量(1,0,0)即x轴旋转-90度
        glTranslate(0, 0, 0.8)              # y轴变z轴，向z轴正方向平移
        glColor(0.0, 1.0, 0.0)              # 设置当前颜色为绿色
        glutSolidCone(0.02, 0.2, 30, 30)    # 绘制圆锥（实体）
        glPopMatrix()                       # 恢复保存的矩阵

        glPushMatrix()                      # 保存当前矩阵
        glTranslate(0, 0, 0.8)              # 向z轴正方向平移
        glColor(0.0, 0.0, 1.0)              # 设置当前颜色为蓝色
        glutSolidCone(0.02, 0.2, 30, 30)    # 绘制圆锥（实体）
        glPopMatrix()                       # 恢复保存的矩阵

if __name__ == '__main__':
    app = App(hax='y')
    app.show()


