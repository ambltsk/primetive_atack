# -*- coding: utf-8 -*-
"""
Файл настроек игры
"""

import pygame as pg

#Частота обновления экрана
FPS = 60
#Размерность экрана
WIDTH = 800
HEIGHT = 800
CAPTION = "THIS IS GAME #1"
#Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SKY = (0, 255, 255)
GRAY = (127, 127, 127)
YELLOW = (255, 255, 0)
FUCSIA = (255, 0, 255)
#Файлы картинок
BACKGROUND = "images/background.bmp"
MAINHERRO = "images/main_hero.png"
SCR_HERO_IMAGE = "images/main_cnt.png"
#Файлы звуков
HIT_ENEMY = "sound/hit_enemy.wav"
HIT_HERO = "sound/hit_hero.wav"
FIRE_BULLET = "sound/fire_bullet.wav"
LEVEL_UP = "sound/next_level.wav"
#Константы управления главным героем
TURN_RIGHT = "Turn RIGHT"
TURN_LEFT = "Turn LEFT"
MOVE_STRAITGHT = "Move straight"
#Константы главного героя
MAIN_HERO_COUNT = 3
MAIN_HERO_BLINK_CNT = 5
MAIN_HERO_BLINK_TICK = FPS // 2
#Константы пуль
BULLET_MAXSPEED = 15
BULLET_MINSPEED = 5
BULLET_COLOR = (SKY, YELLOW, GREEN)
BULLET_CONTUR_COLOR = (BLUE, FUCSIA, RED)
BULLET_ABSORPTION = "absorption"
BULLET_THROUGH = "throgh"
BULLET_MIRROR = "mirror"
BULLET_SIZE = 5
BULLET_DELAY_NORMAL = 10
BULLET_DELAY_FAST = 5
#Константы врагов
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED_FACTOR = 0.01
ENEMY_SPEED_FACTOR_DX = 0.001
ENEMY_DELAY = 3000
ENEMY_DELAY_FACTOR = 250
ENEMY_LEVEL_CNT = 10
#Константы отображения информации на экране
SCR_HEALTH_LEVEL_POS = ("left","bottom")
SCR_HEALTH_LEVEL_WIDTH = 200
SCR_HEALTH_LEVEL_HEIGHT = 20
SCR_HEALTH_LEVEL_BORDER = 2
SCR_HERO_CNT_POS = ("right","bottom")
SCR_HERO_DX = 10
SCR_SCORE_POS = ("left", "top")
SCR_ENEMY_CNT_POS = ("right", "top")
SCR_GAME_OVER_POS = ("center", "center")
SCR_BORDER = 5
 
class Config:
	"""
	Класс конфигурации игры
	"""
	def __init__(self):
		self.game_run = False
		self.reset_config()
	
	def reset_config(self):
		#Параметры игры
		self.score = 0
		self.game_over = False
		self.game_pause = False
		self.level = 1
		#Настройки главного героя
		self.hero_count = MAIN_HERO_COUNT
		#Настройки пуль
		self.bullet_speed = (BULLET_MINSPEED + BULLET_MAXSPEED) // 2
		self.bullet_size = BULLET_SIZE
		self.bullet_delay = BULLET_DELAY_NORMAL
		self.bullet_type = BULLET_ABSORPTION
		self.bullet_fun = False
		#Настройки врагов
		self.enmy_pause = ENEMY_DELAY
		self.enmy_speed_factor = ENEMY_SPEED_FACTOR
		self.enmy_left = self.level * ENEMY_LEVEL_CNT
		self.level_up_flg = True
		self.mute = False

	
	def level_up(self):
		self.level += 1
		self.enmy_left = self.level * ENEMY_LEVEL_CNT
		self.enmy_speed_factor += ENEMY_SPEED_FACTOR_DX
		self.enmy_pause -= ENEMY_DELAY_FACTOR
		self.level_up_flg = True
	
	def reset_level_up_flag(self):
		self.level_up_flg = False
	
	def kill_hero(self):
		self.hero_count -= 1
		if self.hero_count == 0:
			self.game_over = True
	
	def kill_enemy(self):
		self.enmy_left -= 1
		if self.enmy_left < 1:
			self.level_up()
	
	def bullet_speed_ip(self, value=0):
		self.bullet_speed += value
		if self.bullet_speed > BULLET_MAXSPEED:
			self.bullet_speed = BULLET_MAXSPEED
		if self.bullet_speed < BULLET_MINSPEED:
			self.bullet_speed = BULLET_MINSPEED
	
	def bullet_wsize(self):
		self.bullet_size *= 2
	
	def bullet_nsize(self):
		self.bullet_size = BULLET_SIZE
	
	def bullet_hi_pressure(self):
		self.bullet_delay = BULLET_DELAY_FAST
	
	def bullet_normal_pressure(self):
		self.bullet_delay = BULLET_DELAY_NORMAL
	
	def bullet_funs(self):
		self.bullet_fun = True
	
	def bullet_no_funs(self):
		self.bullet_fun = False

	def set_bullet_type(self, blt_type = BULLET_ABSORPTION):
		self.bullet_type = blt_type
	
	def enemy_speed_factor_up(self):
		self.enmy_speed_factor += 0.005
	
	@property
	def main_hero_count(self):
		return self.hero_count
	
	@property
	def blt_speed(self):
		return self.bullet_speed
	
	@property
	def blt_size(self):
		return self.bullet_size
	
	@property
	def blt_type(self):
		return self.bullet_type
	
	@property
	def blt_delay(self):
		return self.bullet_delay
	
	@property
	def is_blt_fun(self):
		return self.bullet_fun
	
	@property
	def enemy_delay(self):
		return self.enmy_pause
	
	@property
	def enemy_speed_factor(self):
		return self.enmy_speed_factor
	
	@property
	def game_score(self):
		return self.score
	
	@property
	def enemy_left(self):
		return self.enmy_left
	
	@property
	def game_level(self):
		return self.level
	
	@property
	def level_up_flag(self):
		return self.level_up_flg
	
	@property
	def is_game_over(self):
		return self.game_over
	
cnfg = Config()
