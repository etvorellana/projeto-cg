•from OpenGL.GL import *
2
from OpenGL.GLU import *
3
from OpenGL.GLUT import *
4
​
5
#Constantes de Tela
6
SCREEN_WIDTH = 640;
7
SCREEN_HEIGHT = 480;
8
SCREEN_FPS = 60;
9
​
10
#Modos de cor
11
COLOR_MODE_CYAN = 0;
12
COLOR_MODE_MULTI = 1;
13
​
14
#Modo atual de renderização de cor
15
gColorMode = COLOR_MODE_CYAN;
16
​
17
#Scala de projeção
18
gProjectionScale = 1.0; #Tipo: GLfloat
19
​
20
def initGL():
21
        #Inicializando Matriz de Projeção
22
        glMatrixMode(GL_PROJECTION);
23
        glLoadIdentity();
24
        glOrtho(0.0, SCREEN_WIDTH, SCREEN_HEIGHT, 0.0, 1.0, -1.0);
25
​
26
        #Inicializando Matriz de modelo de exibição (Modelview)
27
        glMatrixMode(GL_MODELVIEW);
28
        glLoadIdentity();
29
​
30
        #Inicializando a tela com a cor preta
31
        glClearColor(0,0,0,1);
32
​
33
        #Verificando se há erros
34
        erro = glGetError()
35
        if(erro != GL_NO_ERROR):
36
                print("Error initializing OpenGL! %s\n", gluErrorString(erro))
37
                return False
38
        return True
39
​
40
def update():
41
        pass
42
​
43
def render():
44
        #Limpando o buffer de cor
45
        glClear(GL_COLOR_BUFFER_BIT);
46
​
47
        #Reiniciando a matriz Modelview
48
        glMatrixMode(GL_MODELVIEW);
49
        glLoadIdentity();
