"""着色器中的MVP矩阵"""

import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from  baseScene import BaseScene

class Scene(BaseScene):
    """由BaseScene派生的三维场景类"""

    def __init__(self, **kwds):
        """构造函数"""

        BaseScene.__init__(self, **kwds)            # 调用基类构造函数
 
        self.mmat = np.eye(4, dtype=np.float32)     # 模型矩阵
        self.vmat = np.eye(4, dtype=np.float32)     # 视点矩阵
        self.pmat = np.eye(4, dtype=np.float32)     # 投影矩阵

    def get_vmat(self):
        """返回视点矩阵"""
 
        camX, camY, camZ = self.cam
        oecsX, oecsY, oecsZ = self.oecs
        upX, upY, upZ = self.up
 
        f = np.array([oecsX-camX, oecsY-camY, oecsZ-camZ], dtype=np.float64)
        f /= np.linalg.norm(f)
        s = np.array([f[1]*upZ - f[2]*upY, f[2]*upX - f[0]*upZ, f[0]*upY - f[1]*upX], dtype=np.float64)
        s /= np.linalg.norm(s)
        u = np.cross(s, f)
 
        return np.array([
            [s[0], u[0], -f[0], 0],
            [s[1], u[1], -f[1], 0],
            [s[2], u[2], -f[2], 0],
            [- s[0]*camX - s[1]*camY - s[2]*camZ, 
            - u[0]*camX - u[1]*camY - u[2]*camZ, 
            f[0]*camX + f[1]*camY + f[2]*camZ, 1]
        ], dtype=np.float32)

    def get_pmat(self):
        """返回投影矩阵"""
 
        right = np.tan(np.radians(self.fovy/2)) * self.near
        left = -right
        top = right/self.aspect
        bottom = left/self.aspect
        rw, rh, rd = 1/(right-left), 1/(top-bottom), 1/(self.far-self.near)
 
        return np.array([
            [2 * self.near * rw, 0, 0, 0],
            [0, 2 * self.near * rh, 0, 0],
            [(right+left) * rw, (top+bottom) * rh, -(self.far+self.near) * rd, -1],
            [0, 0, -2 * self.near * self.far * rd, 0]
        ], dtype=np.float32)

    def create_texture_2d(self, texture_file):
        """创建纹理对象"""

        im = np.array(Image.open(texture_file))
        im_h, im_w = im.shape[:2]
        im_mode = GL_LUMINANCE if im.ndim == 2 else (GL_RGB, GL_RGBA)[im.shape[-1]-3]

        tid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tid)

        if (im.size/im_h)%4 == 0:
            glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        else:
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        
        glTexImage2D(GL_TEXTURE_2D, 0, im_mode, im_w, im_h, 0, im_mode, GL_UNSIGNED_BYTE, im)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        return tid

    def prepare(self):
        """准备模型数据"""
    
        vshader_src = """
            #version 330 core
 
            in vec4 a_Position;
            in vec2 a_Texcoord;
            uniform mat4 u_ProjMatrix;
            uniform mat4 u_ViewMatrix;
            uniform mat4 u_ModelMatrix;
            out vec2 v_Texcoord;
 
            void main() { 
                gl_Position = u_ProjMatrix * u_ViewMatrix * u_ModelMatrix * a_Position; 
                v_Texcoord = a_Texcoord;
            }
        """
        
        fshader_src = """
            #version 330 core
 
            in vec2 v_Texcoord;
            uniform sampler2D u_Texture;
 
            void main() { 
                gl_FragColor = texture2D(u_Texture, v_Texcoord);
            } 
        """

        vs = np.array([
            [-1,  1,  1], [ 1,  1,  1], [ 1, -1,  1], [-1, -1,  1], 
            [-1,  1, -1], [ 1,  1, -1], [ 1, -1, -1], [-1, -1, -1]
        ], dtype=np.float32)

        indices = np.array([
            0, 3, 2, 1, # v0-v1-v2-v3 (front)
            4, 0, 1, 5, # v4-v5-v1-v0 (top)
            3, 7, 6, 2, # v3-v2-v6-v7 (bottom)
            7, 4, 5, 6, # v5-v4-v7-v6 (back)
            1, 2, 6, 5, # v1-v5-v6-v2 (right)
            4, 7, 3, 0  # v4-v0-v3-v7 (left)
        ], dtype=np.int32)

        vertices = vs[indices]

        texcoord = np.array([
            [0,0], [0,1], [1,1], [1,0], [0,0], [0,1], [1,1], [1,0], [0,0], [0,1], [1,1], [1,0],   
            [0,0], [0,1], [1,1], [1,0], [0,0], [0,1], [1,1], [1,0], [0,0], [0,1], [1,1], [1,0]
        ], dtype=np.float32)

        vshader = shaders.compileShader(vshader_src, GL_VERTEX_SHADER)
        fshader = shaders.compileShader(fshader_src, GL_FRAGMENT_SHADER)
        self.program = shaders.compileProgram(vshader, fshader)

        self.vertices = vbo.VBO(vertices)
        self.texcoord = vbo.VBO(texcoord)
        self.texture = self.create_texture_2d('res/flower.jpg')
 
    def draw(self):
        """绘制模型。可在派生类中重写此方法"""

        glUseProgram(self.program)
    
        loc = glGetAttribLocation(self.program, 'a_Position')
        self.vertices.bind()
        glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, 3*4, self.vertices)
        glEnableVertexAttribArray(loc)
        self.vertices.unbind()
     
        loc = glGetAttribLocation(self.program, 'a_Texcoord')
        self.texcoord.bind()
        glVertexAttribPointer(loc, 2, GL_FLOAT, GL_FALSE, 2*4, self.texcoord)
        glEnableVertexAttribArray(loc)
        self.texcoord.unbind()

        loc = glGetUniformLocation(self.program, 'u_ProjMatrix')
        glUniformMatrix4fv(loc, 1, GL_FALSE, self.get_pmat(), None)

        loc = glGetUniformLocation(self.program, 'u_ViewMatrix')
        glUniformMatrix4fv(loc, 1, GL_FALSE, self.get_vmat(), None)

        loc = glGetUniformLocation(self.program, 'u_ModelMatrix')
        glUniformMatrix4fv(loc, 1, GL_FALSE, self.mmat, None)
 
        loc = glGetUniformLocation(self.program, 'u_Texture')
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(loc, 0)

        glDrawArrays(GL_QUADS, 0, 24)
        glUseProgram(0)

    def render(self):
        """重绘事件函数"""

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # 清除屏幕及深度缓存
        self.draw() # 绘制模型
        glutSwapBuffers() # 交换缓冲区

