"""着色器中的漫反射、镜面反射和高光计算"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from scene import Scene

class App(Scene):
    """由BaseScene派生的3D应用程序类"""

    def prepare(self):
        """准备模型数据"""
    
        vshader_src = """
            #version 330 core
 
            in vec4 a_Position;
            in vec3 a_Normal;
            in vec2 a_Texcoord;
            uniform mat4 u_ProjMatrix;
            uniform mat4 u_ViewMatrix;
            uniform mat4 u_ModelMatrix;
            uniform vec3 u_CamPos;
            out vec2 v_Texcoord;
            out vec3 v_Normal;
            out vec3 v_CamDir;
 
            void main() { 
                gl_Position = u_ProjMatrix * u_ViewMatrix * u_ModelMatrix * a_Position; 
                v_Texcoord = a_Texcoord;
 
                mat4 NormalMatrix = transpose(inverse(u_ModelMatrix)); // 法向量矩阵
                v_Normal = normalize(vec3(NormalMatrix * vec4(a_Normal, 1.0))); // 重新计算模型变换后的法向量
                v_CamDir = normalize(u_CamPos - vec3(u_ModelMatrix * a_Position)); // 从当前顶点指向相机的向量
            }
        """
        
        fshader_src = """
            #version 330 core
 
            in vec2 v_Texcoord;
            in vec3 v_Normal;
            in vec3 v_CamDir;
            uniform sampler2D u_Texture;
            uniform vec3 u_LightDir; // 定向光方向
            uniform vec3 u_LightColor; // 定向光颜色
            uniform vec3 u_AmbientColor; // 环境光颜色
            uniform float u_Shiny; // 高光系数，非负数，数值越大高光点越小
            uniform float u_Specular; // 镜面反射系数，0~1之间的浮点数，影响高光亮度
            uniform float u_Diffuse; // 漫反射系数，0~1之间的浮点数，影响表面亮度
            uniform float u_Pellucid; // 透光系数，0~1之间的浮点数，影响背面亮度
 
            void main() { 
                vec3 lightDir = normalize(-u_LightDir); // 光线向量取反后单位化
                vec3 middleDir = normalize(v_CamDir + lightDir); // 视线和光线的中间向量
                vec4 color = texture2D(u_Texture, v_Texcoord);
 
                float diffuseCos = u_Diffuse * max(0.0, dot(lightDir, v_Normal)); // 光线向量和法向量的内积
                float specularCos = u_Specular * max(0.0, dot(middleDir, v_Normal)); // 中间向量和法向量内积
 
                if (!gl_FrontFacing) 
                    diffuseCos *= u_Pellucid; // 背面受透光系数影响
 
                if (diffuseCos == 0.0) 
                    specularCos = 0.0;
                else
                    specularCos = pow(specularCos, u_Shiny);
 
                vec3 scatteredLight = min(u_AmbientColor + u_LightColor * diffuseCos, vec3(1.0)); // 散射光
                vec3 reflectedLight = u_LightColor * specularCos; // 反射光
                vec3 rgb = min(color.rgb * (scatteredLight + reflectedLight), vec3(1.0));
 
                gl_FragColor = vec4(rgb, color.a);
            } 
        """

        # 生成地球的顶点，东西方向和南北方向精度为2°
        rows, cols, r = 90, 180, 1
        gv, gu = np.mgrid[0.5*np.pi:-0.5*np.pi:complex(0,rows), 0:2*np.pi:complex(0,cols)]
        xs = r * np.cos(gv)*np.cos(gu)
        ys = r * np.cos(gv)*np.sin(gu)
        zs = r * np.sin(gv)
        vs = np.dstack((xs, ys, zs)).reshape(-1, 3)
        vs = np.float32(vs)

        # 生成三角面的索引
        idx = np.arange(rows*cols).reshape(rows, cols)
        idx_a, idx_b, idx_c, idx_d = idx[:-1,:-1], idx[1:,:-1], idx[:-1, 1:], idx[1:,1:]
        indices = np.int32(np.dstack((idx_a, idx_b, idx_c, idx_c, idx_b, idx_d)).ravel())

        # 生成法向量
        primitive = vs[indices]
        a = primitive[::3]
        b = primitive[1::3]
        c = primitive[2::3]
        normal = np.repeat(np.cross(b-a, c-a), 3, axis=0)

        idx_arg = np.argsort(indices)
        rise = np.where(np.diff(indices[idx_arg])==1)[0]+1
        rise = np.hstack((0, rise, len(indices)))
 
        tmp = np.zeros((rows*cols, 3), dtype=np.float32)
        for i in range(rows*cols):
            tmp[i] = np.sum(normal[idx_arg[rise[i]:rise[i+1]]], axis=0)

        normal = tmp.reshape(rows,cols,-1)
        normal[:,0] += normal[:,-1]
        normal[:,-1] = normal[:,0]
        normal[0] = normal[0,0]
        normal[-1] = normal[-1,0]
    
        # 生成纹理坐标
        u, v = np.linspace(0, 1, cols), np.linspace(0, 1, rows)
        texcoord = np.float32(np.dstack(np.meshgrid(u, v)).reshape(-1, 2))
        
        # 生成着色器程序
        vshader = shaders.compileShader(vshader_src, GL_VERTEX_SHADER)
        fshader = shaders.compileShader(fshader_src, GL_FRAGMENT_SHADER)
        self.program = shaders.compileProgram(vshader, fshader)

        # 创建VBO和纹理对象
        self.vertices = vbo.VBO(vs)
        self.normal = vbo.VBO(normal)
        self.texcoord = vbo.VBO(texcoord)
        self.indices = vbo.VBO(indices, target=GL_ELEMENT_ARRAY_BUFFER)
        self.n = len(indices)
        # self.texture = self.create_texture_2d('res/earth.jpg')
        self.texture = self.create_texture_2d('res/earth2.jpg')
        # self.texture = self.create_texture_2d('res/earth.png')
    

        # 设置光照参数
        self.light_dir = np.array([-1, 1, 0], dtype=np.float32)     # 光线照射方向
        self.light_color = np.array([1, 1, 1], dtype=np.float32)    # 光线颜色
        self.ambient = np.array([0.2, 0.2, 0.2], dtype=np.float32)  # 环境光颜色
        self.shiny = 50                                             # 高光系数
        self.specular = 1.0                                         # 镜面反射系数
        self.diffuse = 0.7                                          # 漫反射系数
        self.pellucid = 0.5                                         # 透光度

    def draw(self):
        """绘制模型。可在派生类中重写此方法"""

        glUseProgram(self.program)
    
        loc = glGetAttribLocation(self.program, 'a_Position')
        self.vertices.bind()
        glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, 3*4, self.vertices)
        glEnableVertexAttribArray(loc)
        self.vertices.unbind()
     
        loc = glGetAttribLocation(self.program, 'a_Normal')
        self.normal.bind()
        glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, 3*4, self.normal)
        glEnableVertexAttribArray(loc)
        self.normal.unbind()

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

        loc = glGetUniformLocation(self.program, 'u_CamPos')
        glUniform3f(loc, *self.cam)

        loc = glGetUniformLocation(self.program, 'u_Texture')
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniform1i(loc, 0)

        loc = glGetUniformLocation(self.program, 'u_LightDir')
        glUniform3f(loc, *self.light_dir)

        loc = glGetUniformLocation(self.program, 'u_LightColor')
        glUniform3f(loc, *self.light_color)

        loc = glGetUniformLocation(self.program, 'u_AmbientColor')
        glUniform3f(loc, *self.ambient)

        loc = glGetUniformLocation(self.program, 'u_Shiny')
        glUniform1f(loc, self.shiny)

        loc = glGetUniformLocation(self.program, 'u_Specular')
        glUniform1f(loc, self.specular)

        loc = glGetUniformLocation(self.program, 'u_Diffuse')
        glUniform1f(loc, self.diffuse)

        loc = glGetUniformLocation(self.program, 'u_Pellucid')
        glUniform1f(loc, self.pellucid)

        self.indices.bind()
        glDrawElements(GL_TRIANGLES, self.n, GL_UNSIGNED_INT, None)
        self.indices.unbind()

        glUseProgram(0)

    def render(self):
        """重绘事件函数"""

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # 清除屏幕及深度缓存
        self.draw() # 绘制模型
        glutSwapBuffers() # 交换缓冲区

if __name__ == '__main__':
    app = App(haxis='z')
    app.show()
