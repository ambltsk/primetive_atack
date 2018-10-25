# -*- coding: utf-8 -*-

import random
from math import *
import pygame as pg
from config import *
import datetime

sides = ("left", "top", "right", "bottom")
types = ("quadro", "triangle", "circle")

class Enemy(pg.sprite.Sprite):
	"""Класс врага народа )))"""
	def __init__(self, main_sc, main_hero, ident):
		"""
		Инициализация нового врага народа
		"""
		pg.sprite.Sprite.__init__(self)
		#Главная поверхность рисования
		self.sc = main_sc
		self.main_hero = main_hero
		self.ident = ident
		#Выбираем случайно тип врага: квадрат, круг и прямоугольник
		#для красоты, принципиальной разницы в форме нет
		self.type = random.choice(types)
		#Флаги убит и мертв
		self.deadth = False
		self.killed = False
		#случайным оброзом определяем с какой стороны появиться
		side = random.choice(sides)
		x = -10
		y = -10
		if side == "left":
			y = random.randint(-10, HEIGHT + 10)
		elif side == "top":
			x = random.randint(-10, WIDTH + 10)
		elif side == "right":
			y = random.randint(-10, HEIGHT + 10)
			x = WIDTH + 10
		else:
			x = random.randint(-10, WIDTH + 10)
			y = HEIGHT +10
		#Вещественные кардинаты положения на экране
		self.x = 1.0 * x
		self.y = 1.0 * y
		#Скорость тоже случайная величина
		self.speed = random.randint(5,10) * cnfg.enemy_speed_factor
		#вычесляем скорости по x и y
		distance = sqrt((WIDTH//2 - self.x) ** 2 + (HEIGHT//2 - self.y) ** 2)
		self.speed_x = ((WIDTH//2 - self.x) * self.speed) / distance
		self.speed_y = ((HEIGHT//2 - self.y) * self.speed) / distance
		#Так же случайно определяем живучесть, сколько даст при поражении очков и цвет
		self.power = random.choice((5,10,15,20,25,30,35,40))
		self.score = random.randint(50,500)
		self.hit_hero = False
		self.color = random.choice((WHITE,
									YELLOW,
									RED,
									BLUE,
									GREEN))
		self.give_score = random.randint(10, 50)
		#Rect врага
		self.rect = pg.rect.Rect((int(self.x) - ENEMY_WIDTH // 2,
									int(self.y) - ENEMY_HEIGHT // 2),
									(ENEMY_WIDTH, ENEMY_HEIGHT))
	
	def __eq__(self, other):
		return self.ident == other.ident
	
	def update(self):
		"""
		Функция обновления свойств врага народа
		"""
		if not self.killed:
			#Если живы идем к намеченной цели
			self.x += self.speed_x
			self.y += self.speed_y
			self.rect.center = (int(self.x), int(self.y))
			#Вот и достигли цели
			if self.main_hero.collide_me(self):
				self.killed = True
				self.hit_hero = True
		else:
			#А если убит (power = 0) то сжимаем в точку
			x = self.rect.centerx
			y = self.rect.centery
			if self.rect.width > 10:
				self.rect.width -= 1
				if self.rect.height > 10:
					self.rect.height -= 1
				self.rect.center = (x, y)	
			else:
				#и считаем мертвым
				self.deadth = True
				cnfg.kill_enemy()
				if not self.hit_hero:
					cnfg.game_score += self.score
	
	def blitme(self):
		"""
		Функция отрисовки врага на главной поверхности
		"""
		#Цвет рамки в три раза тусклее чем цвет врага
		border_color = (self.color[0] // 3,
						self.color[1] // 3,
						self.color[2] // 3)
		#В зависимости от типа рисуем квадрат, круг или треуголтник
		if self.type == "quadro":
			pg.draw.rect(self.sc, self.color, self.rect)
			pg.draw.rect(self.sc, border_color, self.rect, 3)
		elif self.type == "circle":
			pg.draw.circle(self.sc, self.color, self.rect.center, self.rect.width // 2)
			pg.draw.circle(self.sc, border_color, self.rect.center, self.rect.width // 2, 3)
		else:
			poligon = ((self.rect.left, self.rect.bottom),
						(self.rect.right, self.rect.bottom),
						(self.rect.centerx, self.rect.top))
			pg.draw.polygon(self.sc, self.color, poligon)
			pg.draw.polygon(self.sc, border_color, poligon, 3)
		#Если не убит то дополнительно отображаем его мощность
		if not self.killed:
			font = pg.font.Font(None, 20)
			text = font.render("%d" % self.power, 0, BLACK)
			text_rect = text.get_rect(center = self.rect.center)
			if self.type != "triangle":
				#У всех по середке пишем
				self.sc.blit(text, (text_rect.x, text_rect.y))
			else:
				#У треугольника на основании
				self.sc.blit(text, (text_rect.x, text_rect.y +10))
	
	def hit_me(self, value=1):	
		"""
		Функция убивания врага, уменьшает силу врага на value
		"""
		if self.power < 2:
			self.killed = True			
		else:
			self.power -= value
