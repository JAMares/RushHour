import pygame, sys

class Button:
	def __init__(self,text,width,height):
		#Buttom 
		self.pressed = False
		self.elevation = 3
		self.movement = 3
		self.y = 250
		self.word = text

		#Top
		self.top_rect = pygame.Rect((200,250),(width,height))
		self.top_color = (0, 140, 51)

		#Bottom 
		self.bottom_rect = pygame.Rect((200,250),(width,height))
		self.bottom_color = (0, 122, 44)
		#Text
		self.text = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic 
		self.top_rect.y = self.y - self.movement
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.movement

		pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
		screen.blit(self.text, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = (0, 86, 31)
			if pygame.mouse.get_pressed()[0]:
				self.movement = 0
				self.pressed = True
			else:
				self.movement = self.elevation
				if self.pressed == True:
				    self.pressed = False
		else:
			self.movement = self.elevation
			self.top_color = (0, 140, 51)

pygame.init()
screen = pygame.display.set_mode((500,500))
gui_font = pygame.font.Font(None,30)

buttonStart = Button('Start',100,30)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('#DCDDD8')
	buttonStart.draw()

	pygame.display.update()
	
