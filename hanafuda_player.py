#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import datetime
import gc
import os
import cv2
from detect_yaku import *
from write_log import *
from enemy_move import *
from draw import *


class Hanafuda():

    def __init__(self):
        self.ResetParam()

        self.my_total_score = 0
        self.your_total_score = 0
        self.score_record = []        


    def ResetParam(self):
        self.cards = [11,12,13,14,21,22,23,24,31,32,33,34,41,42,43,44,51,52,53,54,61,62,63,64,
                      71,72,73,74,81,82,83,84,91,92,93,94,101,102,103,104,111,112,113,114,121,122,123,124]
        
        self.my_cards = []
        self.my_getcard = []
        self.my_score = 0
        self.my_koikoi_flag = 0

        self.your_cards = []
        self.your_getcard = []
        self.your_score = 0
        self.your_koikoi_flag = 0

        self.field_cards = []
        self.yamafuda = []

        self.end_flag = False
        self.winner = "HIKIWAKE"

        self.EnemyAlgorithm = EnemyMove()

        self.stage = draw_init()
        cv2.imshow("stage", self.stage)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()


    
    def EndMonthProcess(self):
        self.f.write('------------------\n')

        self.f.write('end of month {}\n'.format(self.month))
        self.f.write('winner : {}\n'.format(self.winner))
        self.f.write('my_score: {}, your_score: {}\n'.format(self.my_score, self.your_score))

        print("\n ----------")
        print("end of month {}".format(self.month))
        print("score  enemy: {}, you: {}".format(self.my_score, self.your_score))

        if self.winner == "Me":
            print("winner Enemy")
            print("kakutoku score  enemy: {}, you: {}".format(self.my_score, 0))
            self.my_total_score += self.my_score
        elif self.winner == "You":
            print("winner : {}".format(self.winner))
            print("kakutoku score  enemy: {}, you: {}".format(0, self.your_score))
            self.your_total_score += self.your_score
        else:
            print("HIKIWAKE")
            print("kakutoku score  enemy: {}, you: {}".format(0, 0))

        self.f.write('my_total_score: {}, your_total_score: {}\n'.format(self.my_total_score, self.your_total_score))
        
        print("total score  enemy: {}, you: {}".format(self.my_total_score, self.your_total_score))
        print("----------\n")

        self.f.write('------------------\n\n')

        self.stage = draw_play_tefuda(self.stage, self.your_cards, self.your_getcard, self.my_cards, self.my_getcard, self.field_cards, displaymode=1)
        cv2.imshow("stage", self.stage)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()

        self.score_record.append((self.my_total_score, self.your_total_score))

    

    def EndGameProcess(self):
        if self.my_total_score > self.your_total_score:
            winner = "Me"
            winner_display = "Enemy"
        elif self.my_total_score < self.your_total_score:
            winner = "You"
            winner_display = "You"
        elif self.my_total_score == self.your_total_score:
            winner = "HIKIWAKE"
            winner_display = "HIKIWAKE"

        self.f.write('\n\n------------------\n')

        self.f.write('end of game\n')
        self.f.write('winner : {}\n'.format(winner))
        self.f.write('my_total_score: {}, your_total_score: {}\n'.format(self.my_total_score, self.your_total_score))
        
        self.f.write('------------------\n\n')

        print("\n----------")
        print("end game")
        print("winner : {}".format(winner_display))
        print("total_score   enemy : {}, you : {}".format(self.my_total_score, self.your_total_score))
        print("----------\n")

        for i in range(len(self.score_record)):
            self.f.write('{} {} {}\n'.format(i, self.score_record[i][0], self.score_record[i][1]))






    def ShiteKuttukiJudge(self):
        my_cards_month_dict = {}
        your_cards_month_dict = {}
        
        for i in range(8):
            my_card_month = self.my_cards[i] // 10
            if my_card_month not in my_cards_month_dict.keys():
                my_cards_month_dict[my_card_month] = 1
            else:
                my_cards_month_dict[my_card_month] += 1
            your_card_month = self.your_cards[i] // 10
            if your_card_month not in your_cards_month_dict.keys():
                your_cards_month_dict[your_card_month] = 1
            else:
                your_cards_month_dict[your_card_month] += 1

        my_site_flag = False
        your_site_flag = False
        my_kuttuki = []
        your_kuttuki = []
        for value in my_cards_month_dict.values():
            if value == 4:
                my_site_flag = True
            if value == 2:
                my_kuttuki.append(1)
            else:
                my_kuttuki.append(0)
        for value in your_cards_month_dict.values():
            if value == 4:
                your_site_flag = True
            if value == 2:
                your_kuttuki.append(1)
            else:
                your_kuttuki.append(0)
        
        my_kuttuki_flag = True
        your_kuttuki_flag = True
        for i in range(len(my_kuttuki)):
            if my_kuttuki[i] == 0:
                my_kuttuki_flag = False
                break
        for i in range(len(your_kuttuki)):
            if your_kuttuki[i] == 0:
                your_kuttuki_flag = False
                break
        
        # 四手・くっつきが同時に起こった場合
        if my_site_flag & your_kuttuki_flag:
            print("\nComputer is SITE and you are KUTTUKI")
            self.f.write('------------------\n')
            self.f.write('You are SHITE and enemy is KUTTUKI\n')
            self.f.write('------------------\n')
            self.end_flag = True
        elif my_kuttuki_flag & your_site_flag:
            print("\nComputer is KUTTUKI and you are SHITE")
            self.f.write('------------------\n')
            self.f.write('You are KUTTUKI and enemy is SHITE\n')
            self.f.write('------------------\n')
            self.end_flag = True
        
        # 四手のみ
        if my_site_flag & your_site_flag:
            print("\nComputer and you are SHITE")
            self.f.write('------------------\n')
            self.f.write('You are SHITE and enemy is SHITE\n')
            self.f.write('------------------\n')
            self.end_flag = True
        elif my_site_flag & ~your_site_flag:
            print("\nComputer is SHITE")
            self.f.write('------------------\n')
            self.f.write('You are SHITE\n')
            self.f.write('------------------\n')
            self.my_score = 6
            self.winner = "Me"
            self.end_flag = True
        elif ~my_site_flag & your_site_flag:
            print("\nYou are SHITE")
            self.f.write('------------------\n')
            self.f.write('Enemy is SHITE\n')
            self.f.write('------------------\n')
            self.your_score = 6
            self.winner = "You"
            self.end_flag = True

        # くっつきのみ
        if my_kuttuki_flag & your_kuttuki_flag:
            print("\nComputer and you are KUTTUKI")
            self.f.write('------------------\n')
            self.f.write('You are KUTTUKI and enemy is KUTTUKI\n')
            self.f.write('------------------\n')
            self.end_flag = True
        elif my_kuttuki_flag & ~your_kuttuki_flag:
            print("\nComputer is KUTTUKI")
            self.f.write('------------------\n')
            self.f.write('You are KUTTUKI\n')
            self.f.write('------------------\n')
            self.my_score = 6
            self.winner = "Me"
            self.end_flag = True
        elif ~my_kuttuki_flag & your_kuttuki_flag:
            print("\nYou are KUTTUKI")
            self.f.write('------------------\n')
            self.f.write('Enemy is KUTTUKI\n')
            self.f.write('------------------\n')
            self.your_score = 6
            self.winner = "You"
            self.end_flag = True





    def FieldMatchingProcess(self, card, player):
        card_month = card // 10

        field_month = []
        for i in range(len(self.field_cards)):
            field_month.append(self.field_cards[i] // 10)
        
        flush_card_list = []

        # 選んだカードと同じ月のカードが場に何枚あるかで場合分け
        # 0枚
        if field_month.count(card_month) == 0:
            self.field_cards.append(card)
        
        # 1枚
        elif field_month.count(card_month) == 1:
            tmp_index = field_month.index(card_month)
            get_card_from_field = self.field_cards[tmp_index]
            
            self.field_cards.remove(get_card_from_field)
            if player == "Me":
                self.my_getcard.append(card)
                self.my_getcard.append(get_card_from_field)
            elif player == "You":
                self.your_getcard.append(card)
                self.your_getcard.append(get_card_from_field)
            
            flush_card_list.append(get_card_from_field)
        
        # 3枚
        elif field_month.count(card_month) == 3:
            get_cards_from_field = []
            for field_card in self.field_cards:
                if field_card // 10 == card_month:
                    get_cards_from_field.append(field_card)

            if player == "Me":
                self.my_getcard.append(card)
            elif player == "You":
                self.your_getcard.append(card)
            
            for i in range(3):
                self.field_cards.remove(get_cards_from_field[i])
                if player == "Me":
                    self.my_getcard.append(get_cards_from_field[i])
                elif player == "You":
                    self.your_getcard.append(get_cards_from_field[i])
                
                flush_card_list.append(get_cards_from_field[i])
        
        # 2枚
        elif field_month.count(card_month) == 2:
            get_kouho_from_field = []
            for field_card in self.field_cards:
                if field_card // 10 == card_month:
                    get_kouho_from_field.append(field_card)
            
            if player == "Me":
                # enemy_move.ChooseCard使用
                select_from_kouho = self.EnemyAlgorithm.ChooseCard(player, 1, card, get_kouho_from_field)
                self.field_cards.remove(select_from_kouho)
                self.my_getcard.append(card)
                self.my_getcard.append(select_from_kouho)

            elif player == "You":
                while True:
                    try:
                        select_from_kouho = int(input("Choose from {} : ".format(get_kouho_from_field)))
                        if select_from_kouho in get_kouho_from_field:
                            break
                        else:
                            print("{} is not field_kouho_cards".format(select_from_kouho))
                    except:
                        print("Type integer only")

                # select_from_kouho = get_kouho_from_field[random.randrange(2)]
                self.field_cards.remove(select_from_kouho)
                self.your_getcard.append(card)
                self.your_getcard.append(select_from_kouho)
            
            flush_card_list.append(select_from_kouho)

        return flush_card_list
        


    def Tefuda(self, player):
        self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
        
        if player == "Me":
            # enemy_move.ChooseCard使用
            select_card = self.EnemyAlgorithm.ChooseCard(player, 0, 0, 0)         
            
            self.my_cards.remove(select_card)

        elif player == "You":
            print("your tefuda : {}".format(self.your_cards))
            print("field_cards : {}".format(self.field_cards))
            
            while True:
                try:
                    select_card = int(input(" select card : "))
                    if select_card in self.your_cards:
                        break
                    else:
                        print("{} is not your tefuda_cards".format(select_card))
                except:
                    print("Type integer only")
                
            # your_cards_month = []
            # for your_card in self.your_cards:
            #     your_cards_month.append(your_card // 10)
            # field_cards_month = []
            # for field_card in self.field_cards:
            #     field_cards_month.append(field_card // 10)
            
            # select_card = 0
            # for i in range(len(self.your_cards)):
            #     if your_cards_month[i] in field_cards_month:
            #         select_card = self.your_cards[i]
            #         break
            #     select_card = self.your_cards[0]
            
            self.your_cards.remove(select_card)
        
        flush_card_list = self.FieldMatchingProcess(select_card, player)
        flush_card_list.append(select_card)

        self.stage = draw_play_tefuda(self.stage, self.your_cards, self.your_getcard, self.my_cards, self.my_getcard, self.field_cards, displaymode)
        self.stage = flush(self.stage, flush_card_list)
        cv2.imshow("stage", self.stage)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()
    
        

    def Draw(self, player):
        self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)

        draw_card = self.yamafuda.pop(0)

        self.stage = draw_play_yamafuda(self.stage, self.your_cards, self.your_getcard, self.my_cards, self.my_getcard, self.field_cards, draw_card, displaymode, timing=0)
        cv2.imshow("stage", self.stage)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()

        flush_card_list = self.FieldMatchingProcess(draw_card, player)
        flush_card_list.append(draw_card)

        self.stage = draw_play_yamafuda(self.stage, self.your_cards, self.your_getcard, self.my_cards, self.my_getcard, self.field_cards, draw_card, displaymode, timing=1)
        self.stage = flush(self.stage, flush_card_list)
        cv2.imshow("stage", self.stage)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()


    
    def Score(self, player, turn, repetition):
        if player == "Me":
            tmp_score = self.my_score
            self.my_yaku, self.my_score = detect_yaku(self.my_getcard)
            if self.my_score > tmp_score:
                if self.my_koikoi_flag == 1:  # 自分がすてにこいこいしていた場合，自分の勝利で終了
                    self.my_koikoi_flag = 2
                    self.winner = "Me"
                    self.end_flag = True
                elif self.my_koikoi_flag == 0:  # 自分がまだこいこいしていなかった場合
                    if self.your_koikoi_flag == 1:  # 相手がこいこいしていたら，自分の勝利で終了
                        self.my_koikoi_flag = 2
                        self.my_score *= 2
                        self.winner = "Me"
                        self.end_flag = True
                    elif self.your_koikoi_flag == 0:  # 相手がこいこいしていなかったら，こいこいするかどうかを判断する
                        self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                        koikoi_judge = self.EnemyAlgorithm.KoikoiJudge(player, self.month, turn, repetition)

                        if koikoi_judge:  # こいこいする場合
                            self.my_koikoi_flag = 1
                            self.f.write('------------------\n')
                            self.f.write('DO KOIKOI\n')
                            self.f.write('my_koikoi_flag: {}, your_koikoi_flag: {}, my_score: {}, your_score: {}\n'.format(self.my_koikoi_flag, self.your_koikoi_flag, self.my_score, self.your_score))
                            self.f.write('------------------\n')
                            print("\ntokuten  enemy: {}, you: {}".format(self.my_score, self.your_score))
                            print("goukei tokuten  enemy: {}, you: {}".format(self.my_total_score, self.your_total_score))
                            print("\n**********")
                            print("KOIKOI")
                            print("**********\n")
                        else:  # こいこいしない場合
                            self.my_koikoi_flag = 2
                            self.winner = "Me"
                            self.end_flag = True
                            print("\ntokuten  enemy: {}, you: {}".format(self.my_score, self.your_score))
                            print("goukei tokuten  enemy: {}, you: {}".format(self.my_total_score, self.your_total_score))
                            print("\n**********")
                            print("NOT KOIKOI")
                            print("**********\n")
        
        elif player == "You":
            tmp_score = self.your_score
            self.your_yaku, self.your_score = detect_yaku(self.your_getcard)
            if self.your_score > tmp_score:
                if self.your_koikoi_flag == 1:
                    self.your_koikoi_flag = 2
                    self.winner = "You"
                    self.end_flag = True
                elif self.your_koikoi_flag == 0:
                    if self.my_koikoi_flag == 1:
                        self.your_koikoi_flag = 2
                        self.your_score *= 2
                        self.winner = "You"
                        self.end_flag = True
                    elif self.my_koikoi_flag == 0:
                        print("tokuten  enemy: {}, you: {}".format(self.my_score, self.your_score))
                        print("goukei tokuten  enemy: {}, you: {}".format(self.my_total_score, self.your_total_score))

                        while True:
                            try:
                                self.your_koikoi_flag = int(input("KOIKOI?  yes:1 no:2 : "))
                                if self.your_koikoi_flag in [1, 2]:
                                    break
                                else:
                                    print("Type only 1 or 2")
                            except:
                                print("Type integer only")
                        
                        if self.your_koikoi_flag == 1:
                            self.f.write('------------------\n')
                            self.f.write('DO KOIKOI\n')
                            self.f.write('my_koikoi_flag: {}, your_koikoi_flag: {}, my_score: {}, your_score: {}\n'.format(self.my_koikoi_flag, self.your_koikoi_flag, self.my_score, self.your_score))
                            self.f.write('------------------\n')
                            print("\n**********")
                            print("KOIKOI")
                            print("**********\n")
                        elif self.your_koikoi_flag == 2:
                            self.winner = "You"
                            self.end_flag = True
                            print("\n**********")
                            print("NOT KOIKOI")
                            print("**********\n")

                        self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                        koikoi_judge = self.EnemyAlgorithm.KoikoiJudge(player, self.month, turn, repetition)
                        print(koikoi_judge)



    def OyaDecision(self):
        print("\n Oya decision")
        repetition = 100

        while True:
            for i in range(random.randint(1,10)):
                random.shuffle(self.cards)

            # player 選択
            while True:
                try:
                    your_key = int(input("Type number from 1 to 48 : "))
                    if your_key in range(1,49):
                        break
                    else:
                        print("Type number from 1 to 48")
                except:
                    print("Type integer only")
            your_card = self.cards[your_key - 1]

            # computer 乱数選択
            while True:
                my_key = random.randint(0, 47)
                if my_key != your_key:
                    break
            my_card = self.cards[my_key - 1]

            self.stage = draw_oya_decision(self.stage, my_card, your_card)
            cv2.imshow("stage", self.stage)
            cv2.waitKey(0)
            # cv2.destroyAllWindows()

            my_month = my_card // 10
            your_month = your_card // 10
            if (my_card // 10) != (your_card // 10):
                print("Oya decision : enemy's month: {}, your month: {}".format(my_month, your_month))
                break
            else:
                print("Oya decision : enemy's month: {}, your month: {}".format(my_month, your_month))
                print("Draw, rechoice number")

        if my_month < your_month:
            repetition = 1
        elif my_month > your_month:
            repetition = 2

        return repetition




    def Play(self, repetition, displaymode):
        dt_now = datetime.datetime.now()
        
        repetition = self.OyaDecision()

        # /Users/hiranoseigo/Documents/3A授業ファイル/b_演習/11_自主プロ/jisyupuro/log
        dir_path_player = "/Users/hiranoseigo/Documents/3A授業ファイル/b_演習/11_自主プロ/jisyupuro/log/"
        log_player_file_num = 0
        filelist = os.listdir(dir_path_player)
        for file_name in filelist:
            if file_name[:5] == "log-p":
                log_player_file_num += 1

        file_name = dir_path_player + "/log-player-" + str(log_player_file_num) + ".txt"
        self.f = open(file_name, 'w')
        self.f.write(dt_now.strftime('%Y-%m-%d %H:%M:%S.%f') + '\n\n')
        self.f.write("")  ############ TODO log

        
        for self.month in range(1, 13):
            self.ResetParam()

            for i in range(random.randint(1,10)):
                random.shuffle(self.cards)

            if (repetition + self.month) % 2 == 0:
                print("MONTH {} : Enemy is Oya".format(self.month))
                for i in range(4):
                    self.my_cards.append(self.cards[0+i*6])
                    self.my_cards.append(self.cards[1+i*6])
                    self.field_cards.append(self.cards[2+i*6])
                    self.field_cards.append(self.cards[3+i*6])
                    self.your_cards.append(self.cards[4+i*6])
                    self.your_cards.append(self.cards[5+i*6])
            elif (repetition + self.month) % 2 == 1:
                print("MONTH {} : You are Oya".format(self.month))
                for i in range(4):
                    self.your_cards.append(self.cards[0+i*6])
                    self.your_cards.append(self.cards[1+i*6])
                    self.field_cards.append(self.cards[2+i*6])
                    self.field_cards.append(self.cards[3+i*6])
                    self.my_cards.append(self.cards[4+i*6])
                    self.my_cards.append(self.cards[5+i*6])
            self.yamafuda = self.cards[24:]
            
            print(self.EnemyAlgorithm.neural_network_judge(0, self.my_cards, self.my_getcard, self.your_getcard, self.field_cards))

            self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
            self.stage = draw_play_init(self.stage, self.your_cards, self.my_cards, self.field_cards, displaymode)
            cv2.imshow("stage", self.stage)
            cv2.waitKey(0)

            self.f.write('------------------\n')
            self.f.write('initial condition\n')
            self.f = write_log_init(self.f, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
            self.f.write('------------------\n')

            # 四手・くっつき判定
            self.ShiteKuttukiJudge()
            if self.end_flag:
                self.EndMonthProcess()
                continue
            

            # 最大で8回手札を出したら終了
            for i in range(8):
                if (repetition + self.month) % 2 == 0:
                    print("\n\n\n----- Computer's turn : Tefuda -----\n")
                    self.Tefuda("Me")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('my turn : Tefuda\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    
                    print("\n----- Computer's turn : Draw -----\n")
                    self.Draw("Me")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('my turn : Draw\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    
                    self.Score("Me", i, repetition)
                    if self.end_flag:
                        self.EndMonthProcess()
                        break
                    
                    
                    print("\n\n\n----- Your turn : Tefuda -----\n")
                    self.Tefuda("You")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('your turn : Tefuda\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    
                    print("\n----- Your turn : Draw -----\n")
                    self.Draw("You")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('your turn : Draw\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    
                    self.Score("You", i, repetition)
                    if self.end_flag:
                        self.EndMonthProcess()
                        break

                elif (repetition + self.month) % 2 == 1:
                    print("\n\n\n----- Your turn : Tefuda -----\n")
                    self.Tefuda("You")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('your turn : Tefuda\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')

                    print("\n----- Your turn : Draw -----\n")
                    self.Draw("You")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('your turn : Draw\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    
                    self.Score("You", i, repetition)
                    if self.end_flag:
                        self.EndMonthProcess()
                        break
                    

                    print("\n\n\n----- Computer's turn : Tefuda -----\n")
                    self.Tefuda("Me")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('my turn : Tefuda\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')

                    print("\n----- Computer's turn : Draw -----\n")
                    self.Draw("Me")
                    self.EnemyAlgorithm.UpdateParam(self.field_cards, self.yamafuda, self.my_cards, self.my_getcard, self.your_cards, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    self.f.write('my turn : Draw\n')
                    self.f = write_log(self.f, self.month, i, self.field_cards, self.yamafuda, self.my_cards, self.your_cards, self.my_getcard, self.your_getcard, self.my_score, self.your_score, self.my_total_score, self.your_total_score, self.my_koikoi_flag, self.your_koikoi_flag)
                    self.f.write('------------------\n')
                    
                    self.Score("Me", i, repetition)
                    if self.end_flag:
                        self.EndMonthProcess()
                        break

            # どちらも役ができない or こいこいしたが役ができない 場合
            else:
                if self.my_koikoi_flag == 1:
                    self.winner = "Me"
                elif self.your_koikoi_flag == 1:
                    self.winner = "You"
                self.EndMonthProcess()

        # end of game        
        self.EndGameProcess()
        cv2.waitKey(0)
        
        self.stage = draw_play_tefuda(self.stage, self.your_cards, self.your_getcard, self.my_cards, self.my_getcard, self.field_cards, 1)
        cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # メモリ解放？
        del self.EnemyAlgorithm




if __name__ == '__main__':
    start = 1
    
    while True:
        try:
            displaymode = int(input("Type displaymode : not display enemy's tefuda: 0, display: 1 : "))
            if displaymode in [0, 1]:
                break
            else:
                print("Type only 0 or 1")
        except:
            print("Type integer only")
    
    
    for i in range(start):
        print("{} : {}".format(i, datetime.datetime.now().strftime('%Y%m%d-%H%M%S.%f')))
        hanafuda = Hanafuda()
        hanafuda.Play(i, displaymode)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # メモリ解放？
        del hanafuda
        gc.collect()


# draw関数はmy_がプレイヤ，your_が敵だと思って作ってあるが，
# このプログラムの実装ではmy_が敵，your_がプレイヤなので，drawに渡す引数はmyとyourを全て入れ替えて表示する必要がある