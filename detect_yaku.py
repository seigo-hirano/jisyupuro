#!/usr/bin/env python
# -*- coding: utf-8 -*-


def detect_yaku(getcards, score):
    # 返り値はリスト[[五光，四光，雨入り四光，三光，花見で一杯，月見で一杯，[猪鹿蝶，タネ枚数]，[赤短，タン枚数]，[青短，タン枚数]，[タネ，タネ枚数]，[タン，タン枚数]，[カス，カス枚数]], こいこい]
    yaku_list = [[0, 0, 0, 0, 0, 0, [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], 0]
    
    hikari = []
    tane = []
    tan = []
    kasu = []
    
    for card in getcards:
        if card in [11, 31, 81, 111, 121]:
            hikari.append(card)
        elif card in [21, 41, 51, 61, 71, 82, 91, 101, 112]:
            tane.append(card)
        elif card in [12, 22, 32, 42, 52, 62, 72, 92, 102, 113]:
            tan.append(card)
        elif card in [13, 14, 23, 24, 33, 34, 43, 44, 53, 54, 63, 64, 73, 74, 83, 84, 91, 93, 94, 103, 104, 114, 122, 123, 124]:
            kasu.append(card)
    
    # 役判定        
    # 三光
    if (len(hikari) == 3) & (111 not in hikari):
        yaku_list[0][3] = 1
    
    # 雨入り四光
    if (len(hikari) == 4) & (111 in hikari):
        yaku_list[0][3] = 0
        yaku_list[0][2] = 1
    
    # 四光
    if (len(hikari) == 4) & (111 not in hikari):
        yaku_list[0][3] = 0
        yaku_list[0][2] = 0
        yaku_list[0][1] = 1
    
    # 五光
    if len(hikari) == 5:
        yaku_list[0][3] = 0
        yaku_list[0][2] = 0
        yaku_list[0][1] = 0
        yaku_list[0][0] = 1
    
    # 花見で一杯
    if (31 in getcards) & (91 in getcards):
        yaku_list[0][4] = 1
    
    # 月見で一杯
    if (81 in getcards) & (91 in getcards):
        yaku_list[0][5] = 1
        
    # 猪鹿蝶
    if (61 in getcards) & (71 in getcards) & (101 in getcards):
        yaku_list[0][6][0] = 1
        yaku_list[0][6][1] = len(tane)
    
    # 赤短
    if (12 in getcards) & (22 in getcards) & (32 in getcards):
        yaku_list[0][7][0] = 1
        yaku_list[0][7][1] = len(tan)
    
    # 青短
    if (62 in getcards) & (92 in getcards) & (102 in getcards):
        yaku_list[0][8][0] = 1
        yaku_list[0][8][1] = len(tan)
    
    # タネ
    if len(tane) >= 5:
        yaku_list[0][9][0] = 1
    yaku_list[0][9][1] = len(tane)
    
    # タン
    if len(tan) >= 5:
        yaku_list[0][10][0] = 1
    yaku_list[0][10][1] = len(tan)
    
    # カス
    if len(kasu) >= 10:
        yaku_list[0][11][0] = 1
    yaku_list[0][11][1] = len(kasu)
    
    
    
    # 得点計算
    new_score = 0
    
    # 五光
    if yaku_list[0][0] == 1:
        new_score += 10
    # 四光
    if yaku_list[0][1] == 1:
        new_score += 8
    # 雨入り四光
    if yaku_list[0][2] == 1:
        new_score += 7
    # 三光
    if yaku_list[0][3] == 1:
        new_score += 5
    # 花見で一杯
    if yaku_list[0][4] == 1:
        new_score += 5
    # 月見で一杯
    if yaku_list[0][5] == 1:
        new_score += 5
    # 猪鹿蝶
    if yaku_list[0][6][0] == 1:
        new_score += 5 + (yaku_list[0][6][1] - 3)
    # 赤短・青短の重複
    if (yaku_list[0][7][0] == 1) & (yaku_list[0][8][0] == 1):
        new_score += 10 + (yaku_list[0][7][1] - 6)
    else:
        # 赤短
        if yaku_list[0][7][0] == 1:
            new_score += 5 + (yaku_list[0][7][1] - 3)
        # 青短
        if yaku_list[0][8][0] == 1:
            new_score += 5 + (yaku_list[0][8][1] - 3)
    # タネ
    if yaku_list[0][9][0] == 1:
        new_score += 1 + (yaku_list[0][9][1] - 5)
    # タン
    if yaku_list[0][10][0] == 1:
        new_score += 1 + (yaku_list[0][10][1] - 5)
    # カス
    if yaku_list[0][11][0] == 1:
        new_score += 1 + (yaku_list[0][11][1] - 10)
    
    # 7点以上なら得点2倍
    if new_score >= 7:
        new_score = new_score * 2
        
        
    
    # 得点が上がった場合
    # こいこいステータス0ならこいこいするかを聞く → するなら1，しないなら2
    # こいこいステータス1 → 2に変更
    if new_score > score:
        if yaku_list[1] == 0:
            while True:
                key = int(input("DO KOIKOI?  Yes: 1  No: 0   :"))
                if key == 1:
                    yaku_list[1] = 1
                    break
                elif key == 0:
                    yaku_list[1] = 2
                    break
                else:
                    print("type only 0 or 1")
        elif yaku_list[1] == 1:
            yaku_list[1] = 2
        
    
    
    return yaku_list, new_score


if __name__ == '__main__':
    cards = list(map(int, input().split()))
    print(cards)
    yaku, score = detect_yaku(cards, 0)
    print(yaku)
    print(score)