
import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo
from  baseScene import BaseScene

class App(BaseScene):
    """由BaseScene派生的3D应用程序类"""

    def __init__(self, **kwds):
        """构造函数"""

        BaseScene.__init__(self, **kwds)    # 调用基类构造函数
        self.models = list()                # 模型列表，保存模型的VBO

    def prepare(self):
        """顶点数据预处理"""

        # 三角形颜色、顶点数组
        vertices_triangle = np.array([
            [1.0, 0.0, 0.0,  0.0,  1.2, 0.0],   # c0-v0
            [0.0, 1.0, 0.0, -1.2, -1.2, 0.0],   # c1-v1
            [0.0, 0.0, 1.0,  1.2, -1.2, 0.0],   # c2-v2 
        ], dtype=np.float32)

        # 六面体颜色顶点数组
        vertices_cube = np.array([
            [0.0, 0.5, 1.0, -1, 1, 1],   # c0-v0
            [0.5, 1.0, 0.0, 1, 1, 1],    # c1-v1
            [1.0, 0.0, 0.5, 1, -1, 1],   # c2-v2 
            [0.0, 1.0, 0.5, -1, -1, 1],  # c3-v3 
            [0.5, 0.0, 1.0, -1, 1, -1],  # c4-v4 
            [1.0, 0.5, 0.0, 1, 1, -1],   # c5-v5 
       	    [0.0, 1.0, 1.0, 1, -1, -1],  # c6-v6 
       	    [1.0, 1.0, 0.0, -1, -1, -1]  # c7-v7
        ], dtype=np.float32)

        # 六面体索引数组
        indices_cube = np.array([
            [0, 3, 2, 1], # v0-v1-v2-v3 (front)
            [4, 0, 1, 5], # v4-v5-v1-v0 (top)
            [3, 7, 6, 2], # v3-v2-v6-v7 (bottom)
            [7, 4, 5, 6], # v5-v4-v7-v6 (back)
            [1, 2, 6, 5], # v1-v5-v6-v2 (right)
            [4, 7, 3, 0]  # v4-v0-v3-v7 (left)
        ], dtype=np.int32)

        vs_triangle = vbo.VBO(vertices_triangle)
        vs_cube = vbo.VBO(vertices_cube)
        idx_cube = vbo.VBO(indices_cube, target=GL_ELEMENT_ARRAY_BUFFER)

        self.models.append({
            'gltype':   GL_TRIANGLES,       # 图元类型 
            'atype':    GL_C3F_V3F,         # 混合数组类型
            'vbo_vs':   vs_triangle,        # 顶点vbo
            'n_vs':     len(vs_triangle),   # 顶点数量
            'vbo_idx':  None,               # 索引vbo
            'n_idx':    None                # 索引长度
        })

        self.models.append({
            'gltype':   GL_QUADS,           # 图元类型 
            'atype':    GL_C3F_V3F,         # 混合数组类型
            'vbo_vs':   vs_cube,            # 顶点vbo
            'n_vs':     len(vs_cube),       # 顶点数量
            'vbo_idx':  idx_cube,           # 索引vbo
            'n_idx':    indices_cube.size   # 索引长度
        })

    def draw(self):
        """绘制模型。可在派生类中重写此方法"""

        for m in self.models:
            m['vbo_vs'].bind() # 绑定当前顶点VBO
            glInterleavedArrays(m['atype'], 0, None) # 根据数组类型分离顶点混合数组
            if m['vbo_idx']: # 如果存在索引VBO
                m['vbo_idx'].bind() # 帮顶当前索引VBO
                glDrawElements(m['gltype'], m['n_idx'], GL_UNSIGNED_INT, None)
                m['vbo_idx'].unbind() # 解绑当前索引VBO
            else:
                glDrawArrays(m['gltype'], 0, m['n_vs'])
            m['vbo_vs'].unbind() # 解绑当前顶点VBO

if __name__ == '__main__':
    app = App(hax='y', azim=-30, elev=10)
    app.show()
