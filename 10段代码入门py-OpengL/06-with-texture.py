
import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.arrays import vbo
from  baseScene import BaseScene

class App(BaseScene):
    """由BaseScene派生的3D应用程序类"""

    def __init__(self, **kwds):
        """构造函数"""

        BaseScene.__init__(self, **kwds)    # 调用基类构造函数
        self.models = list()                # 模型列表，保存模型的VBO

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
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # 缩小滤波器：线性滤波
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # 放大滤波器：线性滤波
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # S方向铺贴方式：重复
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) # T方向铺贴方式：重复
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        return tid

    def prepare(self):
        """顶点数据预处理""" 

        vertices = np.array([
            [0, 0, -1,  1,  1],   # t0-v0
            [1, 0,  1,  1,  1],   # t1-v1
            [1, 1,  1, -1,  1],   # t2-v2 
            [0, 1, -1, -1,  1],   # t3-v3 
            [1, 0, -1,  1, -1],   # t4-v4 
            [0, 0,  1,  1, -1],   # t5-v5 
        	[0, 1,  1, -1, -1],   # t6-v6 
        	[1, 1, -1, -1, -1]    # t7-v7
        ], dtype=np.float32)

        indices = np.array([
            [0, 3, 2, 1], # v0-v1-v2-v3 (front)
            [5, 6, 7, 4], # v5-v4-v7-v6 (back)
        ], dtype=np.int32)

        vbo_vs = vbo.VBO(vertices)
        vbo_idx = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)
        texture = self.create_texture_2d('res/flower.jpg')
        
        glEnable(GL_TEXTURE_2D)
        self.texture = self.create_texture_2d('res/flower.jpg')

        self.models.append({
            'gltype':   GL_QUADS,           # 图元类型 
            'atype':    GL_T2F_V3F,         # 混合数组类型
            'vbo_vs':   vbo_vs,             # 顶点vbo
            'n_vs':     len(vertices),      # 顶点数量
            'vbo_idx':  vbo_idx,            # 索引vbo
            'texture':  texture,            # 纹理对象
            'ttype':    GL_TEXTURE_2D       # 纹理类型
        })

    def draw(self):
        """绘制模型。可在派生类中重写此方法"""

        for m in self.models:
            if m.get('texture'): # 如果当前模型使用了纹理
                glBindTexture(m['ttype'], m['texture']) # 绑定该纹理

            m['vbo_vs'].bind() # 绑定当前顶点VBO
            glInterleavedArrays(m['atype'], 0, None) # 根据数组类型分离顶点混合数组

            if m['vbo_idx']: # 如果存在索引VBO
                m['vbo_idx'].bind() # 帮顶当前索引VBO
                glDrawElements(m['gltype'], m['vbo_idx'].size//4, GL_UNSIGNED_INT, None)
                m['vbo_idx'].unbind() # 解绑当前索引VBO
            else:
                glDrawArrays(m['gltype'], 0, m['n_vs'])

            m['vbo_vs'].unbind() # 解绑当前顶点VBO
            if m.get('texture'): # 如果当前模型使用了纹理
                glBindTexture(m['ttype'], m['texture']) # 解绑该纹理

if __name__ == '__main__':
    app = App(hax='y')
    app.show()
