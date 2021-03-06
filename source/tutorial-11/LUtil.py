from LTexture import *

#Constantes de Tela
SCREEN_WIDTH = 640;
SCREEN_HEIGHT = 480;
SCREEN_FPS = 60;

#Textura de sprite
gStretchedTexture = LTexture();

#Tamanho extendido
gStretchRect = LFRect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

#Filtro de textura
gFiltering = GL_LINEAR

def initGL():
	#Definindo a janela de exibição (Viewport)
	glViewport(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

	#Inicializando Matriz de Projeção
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0.0, SCREEN_WIDTH, SCREEN_HEIGHT, 0.0, 1.0, -1.0);

	#Inicializando Matriz de modelo de exibição (Modelview)
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	#Inicializando a tela com a cor preta
	glClearColor(0,0,0,1);

	#Habilitando textura
	glEnable(GL_TEXTURE_2D)

	#Misturando
	glEnable(GL_BLEND)
	glDisable(GL_DEPTH_TEST)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	#Verificando se há erros
	erro = glGetError()
	if(erro != GL_NO_ERROR):
		print("Erro ao iniciar OpenGL! %s\n", gluErrorString(erro))
		return False
	return True

def loadMedia():
	#Carregando textura com cor ciano
	if(not gStretchedTexture.loadTextureFromFileWithColorKey("mini_opengl.png")):
		print("Não foi possível carregar mini textura!")
		return False
	return True

def update():
	pass

def render():
	#Limpando o buffer de cor
	glClear(GL_COLOR_BUFFER_BIT);

	#Rnderizando imagem
	gStretchedTexture.render(0.0, 0.0, None, gStretchRect)

	#Atualizando tela
	glutSwapBuffers()

def handleKeys(key,x,y):
	#Se q é pressionado
	key = ord(key)
	global gFiltering,gStretchedTexture
	if(key == 113):
		#Disponibiliza textura para modificação
		glBindTexture(GL_TEXTURE_2D, gStretchedTexture.getTextureID())

		#Alteração Linear/Filtragem mais próxima
		if(gFiltering != GL_LINEAR):
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
			gFiltering = GL_LINEAR
		else:
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
			gFiltering = GL_NEAREST
		#Desativando textura
		glBindTexture(GL_TEXTURE_2D, 0)
def runMainLoop(val):
	#Lógica do Frame
	update()
	render()

	#Executando o frame mais uma vez
	glutTimerFunc(1000 // SCREEN_FPS, runMainLoop, val)
