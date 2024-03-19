from OpenGL.GL import *                 # 导入核心库GL，该库所有函数均以gl为前缀
from OpenGL.GLUT import *               # 导入工具库GLUT，该库所有函数均以glut为前缀

def draw():
    """绘制模型"""

    glClear(GL_COLOR_BUFFER_BIT)        # 清除缓冲区

    glBegin(GL_TRIANGLES)               # 开始绘制三角形
    glColor(1.0, 0.0, 0.0)              # 设置当前颜色为红色
    glVertex(0.0, 1.0, 0.0)             # 设置第1个顶点
    glColor(0.0, 1.0, 0.0)              # 设置当前颜色为绿色
    glVertex(-1.0, -1.0, 0.0)           # 设置第2个顶点
    glColor(0.0, 0.0, 1.0)              # 设置当前颜色为蓝色
    glVertex(1.0, -1.0, 0.0)            # 设置第3个顶点
    glEnd()                             # 结束绘制三角形

    glFlush()                           # 输出缓冲区

if __name__ == "__main__":
    glutInit()                          # 1. 初始化glut库
    glutCreateWindow('OpenGL Demo')     # 2. 创建glut窗口
    glutDisplayFunc(draw)               # 3. 绑定模型绘制函数
    glutMainLoop()       
