# -*- coding: utf-8 -*-

import pygame as pg
from config import *

class MainHero(pg.sprite.Sprite):
	""" Класс главного героя игры"""
	def __init__(self, main_sc, sound):
		"""
		Инициализация главного героя, входные данные главная поверхность рисования
		"""
		pg.sprite.Sprite.__init__(self)
		#Главная поверхность рисования
		self.sc = main_sc
		#Изображение  и главный рект главного героя
		self.image = pg.image.load(MAINHERRO)
		#Главный герой в центре экрана
		self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
		#Изображение для модификации и вывода на эркран
		self.screen_image = self.image.copy()
		#Rect модифицированного изображения, центрируется по главному Rect
		self.screen_rect = self.screen_image.get_rect(center = self.rect.center)
		#Флаг разворота влево - прямо - вправо, при инициализации прямо
		self.turn = MOVE_STRAITGHT
		#Угол поворота главного героя относительно положения вверх
		self.angel = 0
		#Здоровье главного героя
		self.health = 100
		self.death = False
		#Флаг мигания при появлении героя
		self.blink = True
		self.blink_cnt = MAIN_HERO_BLINK_CNT
		self.blink_tick = MAIN_HERO_BLINK_TICK
		self.sound = sound
	
	def blitme(self):
		"""
		Функция отрисовки главного героя на главной поверхности
		"""
		#Разворачиваем главное изображение на угол angel и копируем новое изображение screen_image
		self.screen_image = pg.transform.rotate(self.image, self.angel)
		#Центруем Rect отображения относительно центра экрана
		self.screen_rect = self.screen_image.get_rect(center = self.rect.center)
		#Рисуем главного героя на главной поверхности
		if not self.blink:
			self.sc.blit(self.screen_image, self.screen_rect)
		else:
			if self.blink_tick == 5:
				self.sc.blit(self.screen_image, self.screen_rect)
			self.blink_tick -=1
			if self.blink_tick == 0:
				self.blink_tick = 5
				self.blink_cnt -= 1
				if self.blink_cnt == 0:
					self.blink = False
	
	def update(self):
		"""
		Функция изменения текущего состояния главного героя в процессе игры
		"""
		if self.turn <> MOVE_STRAITGHT:
			if self.turn == TURN_LEFT:
				self.angel +=1
			else:
				self.angel -=1
	
	def hit_me(self, value = 1):
		"""
		Функция убивания главного героя, уменьшает 
		уровень здоровья на value
		"""
		self.health -= value
		if self.health <= 0:
			self.death = True
	
	@property
	def is_death(self):
		"""
		Есть ли здесь кто нибудь живой?
		"""
		return self.death
	
	def get_health(self):
		return self.health
	
	def collide_me(self, enemy):
		if self.screen_rect.colliderect(enemy.rect):
			self.health -= enemy.power
			if not cnfg.mute:
				self.sound.play()
			if self.health < 1:
				self.health = 100
				self.blink = True
				self.blink_cnt = MAIN_HERO_BLINK_CNT
				self.blink_tick = MAIN_HERO_BLINK_TICK
				cnfg.main_hero_count -= 1
				if cnfg.main_hero_count == 0:
					cnfg.is_game_over = True
					cnfg.game_run = False
			return True
		else:
			return False			


