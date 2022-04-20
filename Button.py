import pygame, sys

#Crea los botones
class Button:
	def __init__(self,text,width,height):
		#Buttom 
		self.pressed = False
		self.elevation = 3
		self.movement = 3
		self.y = 475
		self.word = text

		#Top
		self.top_rect = pygame.Rect((670,100),(width,height))
		self.top_color = (0, 140, 51)

		#Bottom 
		self.bottom_rect = pygame.Rect((50,450),(width,height))
		self.bottom_color = (0, 122, 44)
		#Text
		gui_font = pygame.font.Font(None,30)
		self.text = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text.get_rect(center = self.top_rect.center)
