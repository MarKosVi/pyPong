import pygame, sys, random

class Block(pygame.sprite.Sprite):
	def __init__(self,path,x_pos,y_pos):
		super().__init__()
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Player(Block):
	def __init__(self,path,x_pos,y_pos,speed):
		super().__init__(path,x_pos,y_pos)
		self.speed = speed
		self.movement = 0

	def screen_constrain(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= screen_height:
			self.rect.bottom = screen_height

	def update(self,ball_group):
		self.rect.y += self.movement
		self.screen_constrain()

class Ball(Block):
	def __init__(self,path,x_pos,y_pos,speed_x,speed_y,paddles):
		super().__init__(path,x_pos,y_pos)
		self.speed_x = speed_x * random.choice((-1,1))
		self.speed_y = speed_y * random.choice((-1,1))
		self.paddles = paddles
		self.active = False
		self.score_time = 0

	def update(self):
		if self.active:
			self.rect.x += self.speed_x
			self.rect.y += self.speed_y
			self.collisions()
		else:
			self.reiniciarPontuacao()
		
	def collisions(self):
		if self.rect.top <= 0 or self.rect.bottom >= screen_height:
			pygame.mixer.Sound.play(plob_sound)
			self.speed_y *= -1

		if pygame.sprite.spritecollide(self,self.paddles,False):
			pygame.mixer.Sound.play(plob_sound)
			collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
			if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
				self.speed_x *= -1
			if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
				self.speed_x *= -1
			if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
				self.rect.top = collision_paddle.bottom
				self.speed_y *= -1
			if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
				self.rect.bottom = collision_paddle.top
				self.speed_y *= -1

	def resetBall(self):
		self.active = False
		self.speed_x *= random.choice((-1,1))
		self.speed_y *= random.choice((-1,1))
		self.score_time = pygame.time.get_ticks()
		self.rect.center = (screen_width/2,screen_height/2)
		pygame.mixer.Sound.play(score_sound)

	def reiniciarPontuacao(self):
		current_time = pygame.time.get_ticks()
		countdown_number = 3

		if current_time - self.score_time <= 700:
			countdown_number = 3
		if 700 < current_time - self.score_time <= 1400:
			countdown_number = 2
			pygame.mixer.Sound.play(apito)
		if 1400 < current_time - self.score_time <= 2100:
			countdown_number = 1
		if current_time - self.score_time >= 2100:
			self.active = True

		time_counter = basic_font.render(str(countdown_number),True,accent_color)
		time_counter_rect = time_counter.get_rect(center = (screen_width/2,screen_height/2 + 30))
		pygame.draw.rect(screen,bg_color,time_counter_rect)
		screen.blit(time_counter,time_counter_rect)

class adversario(Block):
	def __init__(self,path,x_pos,y_pos,speed):
		super().__init__(path,x_pos,y_pos)
		self.speed = speed

	def update(self,ball_group):
		if self.rect.top < ball_group.sprite.rect.y:
			self.rect.y += self.speed
		if self.rect.bottom > ball_group.sprite.rect.y:
			self.rect.y -= self.speed
		self.constrain()

	def constrain(self):
		if self.rect.top <= 0: self.rect.top = 0
		if self.rect.bottom >= screen_height: self.rect.bottom = screen_height

class GameManager:
	def __init__(self,ball_group,paddle_group):
		self.player_score = 0
		self.adversario_score = 0
		self.ball_group = ball_group
		self.paddle_group = paddle_group
		op = self.adversario_score
		ps = self.player_score

	def run_game(self):
		# Drawing the game objects
		self.paddle_group.draw(screen)
		self.ball_group.draw(screen)

		# Updating the game objects
		self.paddle_group.update(self.ball_group)
		self.ball_group.update()
		self.resetBall()
		self.draw_score()


	def resetBall(self):
		if self.ball_group.sprite.rect.right >= screen_width:
			pygame.mixer.Sound.play(player_score_sond)
			self.adversario_score += 1	
			self.ball_group.sprite.resetBall()
			
		if self.ball_group.sprite.rect.left <= 0:
			pygame.mixer.Sound.play(score_sound)
			self.player_score += 1
			self.ball_group.sprite.resetBall()
		
	def draw_score(self):
		player_score = basic_font.render(str(self.player_score),True,accent_color)
		adversario_score = basic_font.render(str(self.adversario_score),True,accent_color)

		player_score_rect = player_score.get_rect(midleft = (screen_width / 2 + 40,screen_height/2))
		adversario_score_rect = adversario_score.get_rect(midright = (screen_width / 2 - 40,screen_height/2))

		screen.blit(player_score,player_score_rect)
		screen.blit(adversario_score,adversario_score_rect)

# Configurações
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.joystick.init() #Função com joystick
clock = pygame.time.Clock()

# Tela
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Marcos, Diórgenes, Guilherme - PONG')

#Sons e cores
bg_color = pygame.Color('#000000')
accent_color = ('#FFFFFF')
basic_font = pygame.font.Font('freesansbold.ttf', 32)
plob_sound = pygame.mixer.Sound("sonds/Pong.wav")
apito = pygame.mixer.Sound("sonds/Apito.wav")
score_sound = pygame.mixer.Sound("sonds/score.ogg")
player_score_sond = pygame.mixer.Sound("sonds/sucess.wav")
middle_strip = pygame.Rect(screen_width/2 - 2,0,4,screen_height)

# Jogador e Oponente
player = Player('images/PaddlePlayer.png',20,screen_width/2,5)
adversario = adversario('images/Paddle.png',screen_width - 20,screen_height/2,5)
paddle_group = pygame.sprite.Group()
paddle_group.add(adversario)
paddle_group.add(player)

#Adicionarndo sprite de bola ao objeto
ball = Ball('images/Ball.png',screen_width/2,screen_height/2,2,4,paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

#Apresenta a mensagem de fim de jogo
def draw_mensage():
	font = pygame.font.SysFont("comicsansms", 72)
	text = font.render("Fim de Jogo", True, (255, 255, 255))
	pygame.draw.rect(screen, '#000000', pygame.Rect(100, 150, 400, 100))
	pygame.draw.rect(screen, '#000000', pygame.Rect(280, 250, 40, 100))
	pygame.draw.rect(screen, '#ffffff', pygame.Rect(100, 150, 400, 5))
	pygame.draw.rect(screen, '#ffffff', pygame.Rect(100, 350, 400, 5))
	pygame.draw.rect(screen, '#ffffff', pygame.Rect(100, 150, 5, 200))
	pygame.draw.rect(screen, '#ffffff', pygame.Rect(500, 150, 5, 200))
	screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
	pygame.display.flip()
	clock.tick(0.4)

game_manager = GameManager(ball_sprite,paddle_group)
#Comandos com teclado
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			draw_mensage()
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player.movement -= player.speed
			if event.key == pygame.K_DOWN:
				player.movement += player.speed
			if event.key == pygame.K_ESCAPE:
				draw_mensage()
				pygame.quit()
				sys.exit()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player.movement += player.speed
			if event.key == pygame.K_DOWN:
				player.movement -= player.speed
	


	joystick_count = pygame.joystick.get_count()
 
	# Comando com joystick:
	for i in range(joystick_count):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()

		
		hats = joystick.get_numhats()
		print(screen, "Number of hats: {}".format(hats))

		for i in range(hats):
			hat = joystick.get_hat(i)
			if (str(hat[1])) == '1':
				player.movement -= player.speed/4
			if (str(hat[1])) == '-1':
				player.movement += player.speed/4

	pygame.display.flip()










	# Background Stuff
	screen.fill(bg_color)
	pygame.draw.rect(screen,accent_color,middle_strip)
	
	# Run the game
	game_manager.run_game()

	# Rendering
	pygame.display.flip()
	clock.tick(120)