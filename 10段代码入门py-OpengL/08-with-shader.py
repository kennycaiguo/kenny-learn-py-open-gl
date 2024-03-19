"""最简单的着色器程序"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

PROGRAM = None
VERTICES = None
COLORS = None

def prepare():
    """准备模型数据"""

    global PROGRAM, VERTICES, COLORS

    vshader_src = """
        #version 330 core
        in vec4 a_Position;
        in vec4 a_Color;
        out vec4 v_Color;
        
        void main() { 
            gl_Position = a_Position; // gl_Position是内置变量
            v_Color = a_Color;
        }
    """
    
    fshader_src = """
        #version 330 core
        in vec4 v_Color;
        
        void main() { 
            gl_FragColor = v_Color;  // gl_FragColor是内置变量
        } 
    """

    vshader = shaders.compileShader(vshader_src, GL_VERTEX_SHADER)
    fshader = shaders.compileShader(fshader_src, GL_FRAGMENT_SHADER)
    PROGRAM = shaders.compileProgram(vshader, fshader)
    VERTICES = vbo.VBO(np.array([[0, 1, 0], [-1, -1, 0], [1, -1, 0]], dtype=np.float32))
    COLORS = vbo.VBO(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32))

def draw():
    """绘制模型"""

    glClear(GL_COLOR_BUFFER_BIT)        # 清除缓冲区
    glUseProgram(PROGRAM)

    v_loc = glGetAttribLocation(PROGRAM, 'a_Position')
    VERTICES.bind()
    glVertexAttribPointer(v_loc, 3, GL_FLOAT, GL_FALSE, 3*4, VERTICES)
    glEnableVertexAttribArray(v_loc)
    VERTICES.unbind()
 
    c_loc = glGetAttribLocation(PROGRAM, 'a_Color')
    COLORS.bind()
    glVertexAttribPointer(c_loc, 3, GL_FLOAT, GL_FALSE, 3*4, COLORS)
    glEnableVertexAttribArray(c_loc)
    COLORS.unbind()
 
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glUseProgram(0)
    glFlush() # 执行缓冲区指令

if __name__ == "__main__":
    glutInit()                          # 1. 初始化glut库
    glutCreateWindow('OpenGL Demo')     # 2. 创建glut窗口
    prepare()                           # 3. 生成着色器程序、顶点数据集、颜色数据集
    glutDisplayFunc(draw)               # 4. 绑定模型绘制函数
    glutMainLoop()                      # 5. 进入glut主循环
