#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pygame as pg
import game_function as gf
from pygame.sprite import Group
from config import *
from random import randint
from random import choice
from main_hero import MainHero
from bullet import Bullet
from enemy import Enemy
from screen_info import ScreenInfo
from bonus import Bonus


pg.init()

pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

next_level = pg.mixer.Sound(LEVEL_UP)
hit_enemy = pg.mixer.Sound(HIT_ENEMY)
hit_hero = pg.mixer.Sound(HIT_HERO)
fire_bullet = pg.mixer.Sound(FIRE_BULLET)

def game_run():
	main_sc = pg.display.set_mode((WIDTH, HEIGHT))
	pg.display.set_caption(CAPTION)
	clock = pg.time.Clock()
	#Фоновое изображение
	bg_image = pg.image.load(BACKGROUND)
	
	main_hero = MainHero(main_sc, hit_hero)
	
	bullets = Group()
	add_bullet = False
	bullet_tick = 0
	
	enemys = Group()
	enemy_id = 0
	pg.time.set_timer(pg.USEREVENT, cnfg.enemy_delay)
	
	bonuses = Group()
	
	scr_info = ScreenInfo(main_sc, main_hero)
	
	
	while 1:
		#Прослушивание и обработка событий
		for i in pg.event.get():
			if i.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif i.type == pg.USEREVENT:
				if len(enemys) < cnfg.enemy_left:
					if cnfg.game_run:
						enemy = Enemy(main_sc, main_hero, enemy_id)
						enemys.add(enemy)
						enemy_id += 1
						if enemy_id > 0xFFFFFF:
							enemy_id = 0
			elif i.type == pg.KEYDOWN:
				if i.key == pg.K_LEFT:
					main_hero.turn = TURN_LEFT
				elif i.key == pg.K_RIGHT:
					main_hero.turn = TURN_RIGHT
				elif i.key == pg.K_SPACE or i.key == pg.K_UP:
					add_bullet = True
					bulet_tick = 0
				elif i.key == pg.K_p:
					cnfg.game_pause = not cnfg.game_pause
				elif i.key == pg.K_s:
					if not cnfg.game_run:
						cnfg.reset_config()
						cnfg.game_run = True
				elif i.key == pg.K_m:
					v = pg.mixer.music.get_volume()
					if v == 1:
						pg.mixer.music.set_volume(0)
					else:
						pg.mixer.music.set_volume(1)
				#***** TEST *****
				elif i.key == pg.K_1:
					cnfg.set_bullet_type(BULLET_ABSORPTION)
				elif i.key == pg.K_2:
					cnfg.set_bullet_type(BULLET_MIRROR)
				elif i.key == pg.K_3:
					cnfg.set_bullet_type(BULLET_THROUGH)
				elif i.key == pg.K_4:
					cnfg.bullet_hi_pressure()
				elif i.key == pg.K_5:
					cnfg.bullet_normal_pressure()
				elif i.key == pg.K_6:
					cnfg.is_blt_fun = not cnfg.is_blt_fun
				elif i.key == pg.K_7:
					cnfg.bullet_wsize()
				elif i.key == pg.K_8:
					cnfg.bullet_nsize()
				#***** /TEST *****
			elif i.type == pg.KEYUP:
				if i.key == pg.K_LEFT and main_hero.turn == TURN_LEFT:
					main_hero.turn = MOVE_STRAITGHT
				elif i.key == pg.K_RIGHT and main_hero.turn == TURN_RIGHT:
					main_hero.turn = MOVE_STRAITGHT
				elif i.key == pg.K_SPACE or i.key == pg.K_UP:
					add_bullet = False
				elif i.key == pg.K_DOWN:
					main_hero.angel -= 180
		
		if not cnfg.game_pause:
			
			if cnfg.level_up_flag and cnfg.game_run:
				pg.time.set_timer(pg.USEREVENT, cnfg.enemy_delay)
				if not cnfg.mute:
					next_level.play()
				cnfg.reset_level_up_flag()
			
			#Добавление и обработка пуль
			if add_bullet and bullet_tick <= 0:
				#Пока нажат пробел добавляем пули, но с задержкой в bullet_delay фреймов
				if not cnfg.mute:
					fire_bullet.play()
				gf.bullet_add(main_sc, main_hero, bullets)
				bullet_tick = cnfg.blt_delay
			else:
				bullet_tick -= 1
				
			#Обновление действий персонажей
			main_hero.update()
			#Обновление врагов
			enemys.update()
			#Обновление пуль
			bullets.update()	
			#Проверка колизий     
			gf.collision(bullets, enemys, hit_enemy)
		#Перерисовка фона
		main_sc.blit(bg_image, (0,0))
		#Прорисовка персонажей
		if cnfg.game_run:
			for bullet in bullets:
				bullet.blitme()
			for enemy in enemys:
				enemy.blitme()
			main_hero.blitme()
		scr_info.draw_info()
		#Обновление экрана
		pg.display.update()
		#Временная задержка
		clock.tick(FPS)

def main():
	game_run()

if __name__ == '__main__':
	main()
