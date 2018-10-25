# -*- coding: utf-8 -*-

import pygame as pg
from config import *

def where_it(pos, width, height):
	x, y = 0, 0
	if pos[0] == "left":
		x = SCR_BORDER
	elif pos[0] == "right":
		x = WIDTH - SCR_BORDER - width
	else:
		x = (WIDTH - width) // 2
	if pos[1] == "top":
		y = SCR_BORDER
	elif pos[1] == "bottom":
		y = HEIGHT - SCR_BORDER - height
	else:
		y = (HEIGHT - height) // 2
	return x, y

class ScreenInfo:
	"""
	Класс отображающий игровую информацию на экране
	"""
	
	def __init__(self, main_sc, hero):
		self.sc = main_sc
		self.hero = hero
		self.hero_cnt_image = pg.image.load(SCR_HERO_IMAGE)
		self.hero_cnt_rect = self.hero_cnt_image.get_rect()
	
	def draw_info(self):
		"""
		Отрисовка информации на экране
		"""
		self.draw_hero_health()
		self.draw_hero_cnt()
		self.draw_text_info()
		if cnfg.is_game_over:
			self.draw_text(SCR_GAME_OVER_POS, "GAME OVER", 80, RED)
		else:
			if not cnfg.game_run:
				self.draw_text(SCR_GAME_OVER_POS, u"Нажмите <S> для старта", 40, WHITE) 
		if cnfg.game_pause:
			self.draw_text(SCR_GAME_OVER_POS, u"ПАУЗА", 40, WHITE)
	
	def draw_hero_health(self):
		"""
		отрисовка шкалы здоровья главного героя
		"""
		#Определяем местоположение
		x, y = where_it(SCR_HEALTH_LEVEL_POS, SCR_HEALTH_LEVEL_WIDTH, SCR_HEALTH_LEVEL_HEIGHT)
		#Рисуем рамку
		rect_border = pg.rect.Rect(x, y, SCR_HEALTH_LEVEL_WIDTH, SCR_HEALTH_LEVEL_HEIGHT)
		pg.draw.rect(self.sc, YELLOW, rect_border)
		#Рисуем фон
		w = SCR_HEALTH_LEVEL_WIDTH - 2 * SCR_HEALTH_LEVEL_BORDER
		h = SCR_HEALTH_LEVEL_HEIGHT - 2 * SCR_HEALTH_LEVEL_BORDER
		rect_bg = pg.rect.Rect(x + SCR_HEALTH_LEVEL_BORDER,
								y + SCR_HEALTH_LEVEL_BORDER, w, h)
		pg.draw.rect(self.sc, BLUE, rect_bg)
		#Рисуем прогресс здоровья
		w = (self.hero.get_health() * w) // 100
		rect_health = pg.rect.Rect(x + SCR_HEALTH_LEVEL_BORDER,
									y + SCR_HEALTH_LEVEL_BORDER, w, h)
		pg.draw.rect(self.sc, RED, rect_health)
 
	def draw_hero_cnt(self):
		"""
		Отрисовка количества жизней героя
		"""
		#Определяем местоположение
		hw = cnfg.main_hero_count * (self.hero_cnt_rect.width + SCR_HERO_DX)
		x, y = where_it(SCR_HERO_CNT_POS, hw, self.hero_cnt_rect.height)
		for i in range(cnfg.main_hero_count):
			self.hero_cnt_rect.x = x + i * (self.hero_cnt_rect.width + SCR_HERO_DX)
			self.hero_cnt_rect.y = y
			self.sc.blit(self.hero_cnt_image, self.hero_cnt_rect)
	
	def draw_text(self, pos, txt="TEST", size=30, color=YELLOW):
		"""
		Отрисовка текста
		"""
		fnt = pg.font.Font(None, size)
		text = fnt.render(txt, 1, color)
		rect = text.get_rect()
		#Определяем местоположение
		x, y = where_it(pos, rect.width, rect.height)
		self.sc.blit(text, (x, y))
	
	def draw_text_info(self):
		self.draw_text(SCR_SCORE_POS, u"Уровень: %d   Прогресс: %d" % (cnfg.game_level, cnfg.game_score))
		self.draw_text(SCR_ENEMY_CNT_POS, u"Врагов осталось: %d" % cnfg.enemy_left, color=GREEN)
