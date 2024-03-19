"""视点系统和投影矩阵"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

dist = 5.0                      # 全局变量：相机与坐标原点之间的距离
azim = 0.0                      # 全局变量：方位角
elev = 0.0                      # 全局变量：高度角
fovy = 40.0                     # 全局变量：水平视野角度
near = 2.0                      # 全局变量：最近对焦距离
far = 1000.0                    # 全局变量：最远对焦距离
cam = (0.0, 0.0, 5.0)           # 全局变量：相机位置
csize = (800, 600)              # 全局变量：窗口大小
aspect = csize[0]/csize[1]      # 全局变量：窗口宽高比
mouse_pos = (0,0)               # 全局变量：鼠标位置

def click(btn,state,x,y):
    """鼠标按键和滚轮事件函数"""
    global mouse_pos
    if(btn==1)or(btn==2) and state == 0:
        mouse_pos = (x,y)
    glutPostRedisplay() 

def drag(x,y):
    """拖动事件"""
    global mouse_pos, azim, elev, cam
    #计算鼠标拖拽距离
    dx = x - mouse_pos[0] 
    dy = y- mouse_pos[1] 
    #更新鼠标坐标
    mouse_pos = (x,y)
    # 计算方位角
    azim = azim - 180*dx/csize[0]
    #计算高度角
    elev = elev + 90*dy/csize[1]
    #计算相机的三个轴坐标
    d = dist * np.cos(np.radians(elev))
    x_cam = d * np.sin(np.radians(azim))
    y_cam = d * np.sin(np.radians(elev))
    z_cam = d * np.cos(np.radians(azim))
    # 更新相机位置
    cam = [x_cam,y_cam,z_cam]
    # 更新显示
    glutPostRedisplay()

def reshape(w,h):
    """改变窗口大小"""
    global csize,aspect
    csize=(w,h)
    aspect = w/h if h>0 else 1e4
    # 设置视口
    glViewport(0,0,w,h)
    glutPostRedisplay()

def draw():
    """绘制函数"""
    # 清理屏幕
    glClear(GL_COLOR_BUFFER_BIT)
    # 操作投影矩阵
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # 生成透视投影矩阵
    gluPerspective(fovy,aspect,near,far)
    # 设置视点矩阵
    gluLookAt(*cam,*[0,0,0],*[0,1,0])
    
    # 开始绘制三角形
    glBegin(GL_TRIANGLES)               # 开始绘制三角形
    glColor(1.0, 0.0, 0.0)              # 设置当前颜色为红色
    glVertex(0.0, 1.0, 0.0)             # 设置第1个顶点
    glColor(0.0, 1.0, 0.0)              # 设置当前颜色为绿色
    glVertex(-1.0, -1.0, 0.0)           # 设置第2个顶点
    glColor(0.0, 0.0, 1.0)              # 设置当前颜色为蓝色
    glVertex(1.0, -1.0, 0.0)            # 设置第3个顶点
    glEnd()                             # 结束绘制三角形

    # 绘制一条直线
    glBegin(GL_LINES)               # 开始绘制三角形
    glColor(1.0, 0.0, 01.0)              # 设置当前颜色为紫色
    glVertex(0.0, 0.0, -1.0)             # 设置第1个点
    glColor(0.0, 0.0, 1.0)              # 设置当前颜色为蓝色
    glVertex(0.0, 0.0, 1.0)           # 设置第2个点
    glEnd()  

    glFlush()

if __name__ == '__main__':
    glutInit()    
    glutCreateWindow("cam look up")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMouseFunc(click)
    glutMotionFunc(drag)
    glutReshapeFunc(reshape)
    glutMainLoop()

    




    