from LVertexData2D import*
from PIL import Image
from PIL.Image import open 

DEFAULT_TEXTURE_WRAP = GL_REPEAT

class LTexture:
	def __init__(self):
		#Inicializando textura ID
		self.mTextureID = 0
		#Inicializando dimensões da textura
		self.mTextureWidth = 0
		self.mTextureHeight = 0
		#Dimensões da imagem
		self.mImageWidth = 0
		self.mImageHeight = 0
		#Pixels atuais
		self.mPixels = None

		#Inicializando VBO(Vertex Buffer Object)
		self.mVBOID = 0
		self.mIBOID = 0
	
	def initVBO(self):
		#Se atextura for carregada e VBO não existe 
		if (self.mTextureID !=0 and self.mVBOID == 0):
			#Dados do vertice
			#vData array(position(x,y), s, t)
			vData = array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], dtype = 'float32')
			iData = array([0,0,0,0], dtype = 'int32')

			#Definindo indices de renderização
			iData[0] = 0
			iData[1] = 1
			iData[2] = 2
			iData[3] = 3

			#Criando VBO
			self.mVBOID = glGenBuffers(1)
			glBindBuffer(GL_ARRAY_BUFFER, self.mVBOID)
			glBufferData(GL_ARRAY_BUFFER,4*(LVertexData2D().__sizeof__()),vData,GL_DYNAMIC_DRAW)

			#Criando IBO 
			self.mIBOID = glGenBuffers(1)
			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.mIBOID)
			glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*(GLuint().__sizeof__()),iData,GL_DYNAMIC_DRAW)

			#Desativando buffer
			glBindBuffer(GL_ARRAY_BUFFER, 0);
			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,0)


	@staticmethod
	def freeTexture(self):
		#Deletando textura
		if(self.mTextureID != 0):
			#glDeleteTextures(1,self.mTextureID)
			self.mTextureID = 0
		#Deletando pixels
		if(self.mPixels != None):
			del self.mPixels
			self.mPixels = None
		self.mTextureWidth = 0
		self.mTextureHeight = 0
		self.mImageHeight = 0
		self.mImageWidth = 0

	def __del__(self):
		#Limpa dados da textura se preciso
		self.freeTexture(self)

		#Liberar o VBO e IBO se preciso 
		self.freeVBO()

	def loadTextureFromPixels32(self,pixels,imgWidth,imgHeight,texWidth,texHeigth):
		#Obtendo dimensoes de imagem
		self.mImageWidth = imgWidth
		self.mImageHeight = imgHeight
		self.mTextureWidth = texWidth
		self.mTextureHeight = texHeigth

		#Gera textura ID
		glGenTextures(1,self.mTextureID)

		#Define a ID da textura
		self.mTextureID = 1

		#Cria textura ID
		glBindTexture(GL_TEXTURE_2D,self.mTextureID)

		#Gera textura
		glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,self.mTextureWidth,self.mTextureHeight,0,GL_RGBA,GL_UNSIGNED_BYTE,pixels)

		#Definindo parâmetros da textura
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, DEFAULT_TEXTURE_WRAP)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, DEFAULT_TEXTURE_WRAP)

		#Liberando textura
		glBindTexture(GL_TEXTURE_2D,0)

		#Procurando erros
		erro = glGetError()
		if(erro != GL_NO_ERROR):
			print("Erro ao carregar textura de %p pixels! %s\n",pixels,gluErrorString(erro))
			return False
		#Gerando VBO
		self.initVBO()
		return True

	def loadTextureFromFile(self,imagem):
		textureLoaded = False

		im = Image.open(imagem).convert("RGBA")
		if(im != None):
			#Inicializando dimensões
			imgWidth = im.width
			imgHeight = im.height

			#Calculando dimensões da textura
			texWidth = self.powerOfTwo(imgWidth)
			texHeigth = self.powerOfTwo(imgHeight)

			imagem = im.tobytes("raw","RGBA",0,-1)
			textureLoaded = self.loadTextureFromPixels32(imagem,imgWidth,imgHeight,texWidth,texHeigth)
		im.close()
		if(textureLoaded == False):
			print("Não foi possível carregar a imagem!")
		return textureLoaded

	def render(self,x,y,clip = None):
		#Se a textura existe
		if(self.mTextureID != 0):
			#Coordenadas de textura
			texTop = 0.0
			texBottom = self.mImageHeight/self.mTextureHeight
			texLeft = 0.0
			texRight = self.mImageWidth/self.mTextureWidth

			#Coordenadas de vértice
			quadWidth = self.mImageWidth
			quadHeight = self.mImageHeight

			if(clip != None):
				#Coordenadas de textura
				texLeft = clip.x / self.mTextureWidth
				texRight = (clip.x + clip.w) / self.mTextureWidth
				texTop = clip.y / self.mTextureHeight
				texBottom = (clip.y + clip.h) / self.mTextureHeight

				#Coordenadas de vertice
				quadWidth = clip.w
				quadHeight = clip.h

			#Movendo para o ponto de renderização
			glTranslatef(x,y,0)

			#Definindo dados do vertice 
			vData = array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], dtype = 'float32')

			#Coordenadas da textura 

			vData[0][2] = texLeft 
			vData[0][3] = texTop 
			vData[1][2] = texRight
			vData[1][3] = texTop
			vData[2][2] = texRight
			vData[2][3] = texBottom
			vData[3][2] = texLeft
			vData[3][3] = texBottom

			#Posições dos vertices 
			vData[0][0] = 0.0
			vData[0][1] = 0.0
			vData[1][0] = quadWidth
			vData[1][1] = 0.0
			vData[2][0] = quadWidth
			vData[2][1] = quadHeight
			vData[3][0] = 0.0
			vData[3][1] = quadHeight

			#Renderizando textura do quadrado
			glBegin(GL_QUADS)
			glTexCoord2f(texLeft,texTop)
			glVertex2f(0,quadHeight)
			glTexCoord2f(texRight,texTop)
			glVertex2f(quadWidth,quadHeight)
			glTexCoord2f(texRight,texBottom)
			glVertex2f(quadWidth,0)
			glTexCoord2f(texLeft,texBottom)
			glVertex2f(0,0)
			glEnd()

			#Definindo textura ID
			glBindTexture(GL_TEXTURE_2D,self.mTextureID)
			
			#Habilitando vertice e coordenada de array de textura 
			glEnableClientState (GL_VERTEX_ARRAY)
			glEnableClientState (GL_TEXTURE_COORD_ARRAY)

			#Ativando buffer do vertice 
			glBindBuffer(GL_ARRAY_BUFFER,self.mVBOID)

			#Atualizando dados do buffer do vertice 
			glBufferSubData(GL_ARRAY_BUFFER,0,4*LVertexData2D().__sizeof__(),vData)

			#Desenhando quadrado usando os dados do vertice e os dados do indice
			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.mIBOID)
			glDrawElements(GL_QUADS,4,GL_UNSIGNED_INT,None)

			#Desabilitando vertices e coordenadas de arrays de vertice
			glDisableClientState(GL_TEXTURE_COORD_ARRAY)
			glDisableClientState(GL_VERTEX_ARRAY)

	def freeVBO(self):
		#Liberando VBO e IBO
		if (self.mVBOID != 0):
			glDeleteBuffers(1,self.mVBOID)		
			glDeleteBuffers(1,self.mIBOID)


	def getPixelData32(self):
		return self.mPixels

	def getTextureID(self):
		return self.mTextureID

	def textureWidth(self):
		return self.mTextureWidth

	def imageWidth(self):
		return self.mImageWidth

	def imageHeight(self):
		return self.mImageHeight

	def textureHeight(self):
		return self.mTextureHeight

	def powerOfTwo(self,num):
		if(num != 0):
			num -= 1
			num = num | (num >> 8)
			num = num | (num >> 16)
			num += 1
		return num