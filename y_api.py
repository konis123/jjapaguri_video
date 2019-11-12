import cv2
import numpy as np
import json
from flask import Flask, render_template, jsonify

def makeResultFile(list, p1_avgSpeed, p2_avgSpeed, p1_maxSpeed, p2_maxSpeed, winner):

    #각 플레이어 공격 방향 횟수
    a_player_left_attack_num = 0
    b_player_left_attack_num = 0
    a_player_middle_attack_num = 0
    b_player_middle_attack_num = 0
    a_player_right_attack_num = 0
    b_player_right_attack_num = 0

    # 각 플레이어 방어 방향 횟수
    a_player_left_defence_num = 0
    b_player_left_defence_num = 0
    a_player_middle_defence_num = 0
    b_player_middle_defence_num = 0
    a_player_right_defence_num = 0
    b_player_right_defence_num = 0

    a_result = ''
    b_result = ''

    # a_player_total_attack_num = 0
    # b_player_total_attack_num = 0

    i=1
    while i < len(list):
        if list[i][0] == 0:
            FROM = -1
            TO = -1
            if list[i][0] == 0 and i == 0:  #랠리 시작 부분은 공격자만있음.
                if (i+1) < len(list):
                    FROM = list[i+1][0]
                if (i+2) < len(list):
                    TO = list[i+2][0]
                    if TO == 1:
                        b_player_right_attack_num += 1
                    elif TO == 2:
                        b_player_middle_attack_num += 1
                    elif TO == 3:
                        b_player_left_attack_num += 1
                    elif TO == 4:
                        a_player_left_attack_num += 1
                    elif TO == 5:
                        a_player_middle_attack_num += 1
                    elif TO == 6:
                        a_player_right_attack_num += 1

            elif list[i][0] == 0:
                if (i+1) < len(list):
                    FROM = list[i+1][0]
                if (i+2) < len(list):
                    TO = list[i+2][0]
                    if TO == 1:
                        b_player_right_attack_num += 1
                        a_player_left_defence_num += 1
                    elif TO == 2:
                        b_player_middle_attack_num += 1
                        a_player_middle_defence_num += 1
                    elif TO == 3:
                        b_player_left_attack_num += 1
                        a_player_right_defence_num += 1
                    elif TO == 4:
                        a_player_left_attack_num += 1
                        b_player_right_defence_num += 1
                    elif TO == 5:
                        a_player_middle_attack_num += 1
                        b_player_middle_defence_num += 1
                    elif TO == 6:
                        a_player_right_attack_num += 1
                        b_player_left_defence_num += 1


        i+=1

    WINNER = ''
    #랠리가 잘된 된 경우
    if list[len(list)-1][0] == 0:
        #스매싱인경우
        if list[len(list)-2][2] > 4:
            if list[len(list)-2][0] == 1:
                a_result = 'left_smashing_defence_fail'
                b_result = 'right_smashing_attack_success'
                WINNER = 'B'
            elif list[len(list)-2][0] == 2:
                a_result = 'middle_smashing_defence_fail'
                b_result = 'middle_smashing_attack_success'
                WINNER = 'B'
            elif list[len(list)-2][0] == 3:
                a_result = 'right_smashing_defence_fail'
                b_result = 'left_smashing_attack_success'
                WINNER = 'B'
            elif list[len(list)-2][0] == 4:
                a_result = 'left_smashing_attack_success'
                b_result = 'right_smashing_defence_fail'
                WINNER = 'A'
            elif list[len(list)-2][0] == 5:
                a_result = 'middle_smashing_attack_success'
                b_result = 'middle_smashing_defence_fail'
                WINNER = 'A'
            elif list[len(list)-2][0] == 6:
                a_result = 'right_smashing_attack_success'
                b_result = 'left_smashing_defence_fail'
                WINNER = 'A'
        
        #스매싱이 아닌 경우
        else:
            if list[len(list)-2][0] == 1:
                a_result = 'left___defence_fail'
                b_result = 'right___attack_success'
                WINNER = 'B'
            elif list[len(list)-2][0] == 2:
                a_result = 'middle___defence_fail'
                b_result = 'middle___attack_success'
                WINNER = 'B'
            elif list[len(list)-2][0] == 3:
                a_result = 'right___defence_fail'
                b_result = 'left___attack_success'
                WINNER = 'B'
            elif list[len(list)-2][0] == 4:
                a_result = 'left___attack_success'
                b_result = 'right___defence_fail'
                WINNER = 'A'
            elif list[len(list)-2][0] == 5:
                a_result = 'middle___attack_success'
                b_result = 'middle___defence_fail'
                WINNER = 'A'
            elif list[len(list)-2][0] == 6:
                a_result = 'right___attack_success'
                b_result = 'left___defence_fail'
                WINNER = 'A'

    #네트에 걸린 경우
    else:
        if list[len(list)-1][0] == 1:
            a_result = 'left_net'
            b_result = 'right___attack_success'
            WINNER = 'B'
        elif list[len(list)-1][0] == 2:
            a_result = 'middle_net'
            b_result = 'middle___attack_success'
            WINNER = 'B'
        elif list[len(list)-1][0] == 3:
            a_result = 'right_net'
            b_result = 'left___attack_success'
            WINNER = 'B'
        elif list[len(list)-1][0] == 4:
            a_result = 'left___attack_success'
            b_result = 'right_net'
            WINNER = 'A'
        elif list[len(list)-1][0] == 5:
            a_result = 'middle___attack_success'
            b_result = 'middle_net'
            WINNER = 'A'
        elif list[len(list)-1][0] == 6:
            a_result = 'right___attack_success'
            b_result = 'left_net'
            WINNER = 'A'
        else:
            print("-------")

    if WINNER != winner:
        if winner == 'A':
            a_result = 'middle___attack_success'
            b_result = 'middle___defence_fail'
        if winner == 'B':
            a_result = 'middle___defence_fail'
            b_result = 'middle___attack_success'

    data = {
            'A' : {
                'winner' : winner,
                'avg_velocity' : p1_avgSpeed,
                'max_velocity' : p1_maxSpeed,
                'Attack' : {
                    'right' : a_player_right_attack_num,
                    'middle' : a_player_middle_attack_num,
                    'left' : a_player_left_attack_num
                },
                'Defence' : {
                    'right': a_player_right_defence_num,
                    'middle': a_player_middle_defence_num,
                    'left': a_player_left_defence_num
                },
                'result' : a_result
            },
            'B' : {
                'winner': not(winner),
                'avg_velocity': p2_avgSpeed,
                'max_velocity': p2_maxSpeed,
                'Attack': {
                    'right': b_player_right_attack_num,
                    'middle': b_player_middle_attack_num,
                    'left': b_player_left_attack_num
                },
                'Defence': {
                    'right': b_player_right_defence_num,
                    'middle': b_player_middle_defence_num,
                    'left': b_player_left_defence_num
                },
                'result': b_result
            }
    }

    return data



def anal(video):
    # 리스트 생성
    final_list = [[0, 0, 0]]
    p1_list = []
    p2_list = []

    cap = cv2.VideoCapture(video)  # video_path를 설정했으면 0 대신 '파일이름'
    if not cap.isOpened():  # video(cap)이 잘 열렸는지.. 아니면 exit
        print("No video file")
        exit()

    frame = 1
    tracker = cv2.TrackerKCF_create()  # 추적자 생성(CSRT라는 트래커)

    ret, img = cap.read()
    print("이미지 크기(h,w,c) : ", end='')
    print(img.shape)

    # 영상 가로세로 바뀌면 이거 바꿔야 돼!!
    p1_speed = 0
    p1_count = 0
    p2_speed = 0
    p2_count = 0

    def avgSpeed():
        p1_avgSpeed = 0
        p2_avgSpeed = 0

        for i in p1_list:
            p1_avgSpeed = p1_avgSpeed + i

        for i in p2_list:
            p2_avgSpeed = p2_avgSpeed + i

        if p1_count == 0:
            p1_avgSpeed = 0
        else:
            p1_avgSpeed = p1_avgSpeed / p1_count

        if p2_count == 0:
            p2_avgSpeed = 0
        else:
            p2_avgSpeed = p2_avgSpeed / p2_count

        # print("p1 평균 속력 : ", end='')
        # print(p1_avgSpeed)
        # print("p2 평균 속력 : ", end='')
        # print(p2_avgSpeed)

        return p1_avgSpeed, p2_avgSpeed

    def getSpeed(r_box, s_box, arrive, start, player):  #r_box : receive box, s_box : start box
        nonlocal p1_speed
        nonlocal p1_count
        nonlocal p2_speed
        nonlocal p2_count

        if player == 1:
            p1_count = p1_count + 1
            if r_box == 6 and s_box == 1:
                p1_speed = (2.15 / (arrive - start)) * 1000
            elif r_box == 6 and s_box == 2:
                p1_speed = (1.36 / (arrive - start)) * 1000
            elif r_box == 6 and s_box == 3:
                p1_speed = (1.30 / (arrive - start)) * 1000
            elif r_box == 5 and s_box == 1:
                p1_speed = (1.25 / (arrive - start)) * 1000
            elif r_box == 5 and s_box == 2:
                p1_speed = (1.30 / (arrive - start)) * 1000
            elif r_box == 5 and s_box == 3:
                p1_speed = (1.25 / (arrive - start)) * 1000
            elif r_box == 4 and s_box == 1:
                p1_speed = (1.30 / (arrive - start)) * 1000
            elif r_box == 4 and s_box == 2:
                p1_speed = (1.36 / (arrive - start)) * 1000
            elif r_box == 4 and s_box == 3:
                p1_speed = (2.15 / (arrive - start)) * 1000

            p1_list.append(p1_speed)
            return p1_speed

        elif player == 2:
            p2_count = p2_count + 1
            if r_box == 1 and s_box == 4:
                p2_speed = (1.30 / (arrive - start)) * 1000
            elif r_box == 1 and s_box == 5:
                p2_speed = (1.36 / (arrive - start)) * 1000
            elif r_box == 1 and s_box == 6:
                p2_speed = (2.15 / (arrive - start)) * 1000
            elif r_box == 2 and s_box == 4:
                p2_speed = (1.25 / (arrive - start)) * 1000
            elif r_box == 2 and s_box == 5:
                p2_speed = (1.30 / (arrive - start)) * 1000
            elif r_box == 2 and s_box == 6:
                p2_speed = (1.25 / (arrive - start)) * 1000
            elif r_box == 3 and s_box == 4:
                p2_speed = (2.15 / (arrive - start)) * 1000
            elif r_box == 3 and s_box == 5:
                p2_speed = (1.35 / (arrive - start)) * 1000
            elif r_box == 3 and s_box == 6:
                p2_speed = (1.30 / (arrive - start)) * 1000

            p2_list.append(p2_speed)
            return p2_speed

    def addList(num, player):
        trace_list = []

        trace_list.append(num)
        trace_list.append(cap.get(cv2.CAP_PROP_POS_MSEC))

        if num == 0:                #영상 외부로 나간 것은
            trace_list.append(0)    #speed값이 없음!!

        elif num != 0 and player == 0:  #영상 내부 값 중 타격쪽은 시작구간이므로 속도 계산 불가
            trace_list.append(0)

        else:  #영상 내부 값 중 리시브쪽까지 와야 속도 계산 가능
            speed = getSpeed(num, final_list[-1][0], cap.get(cv2.CAP_PROP_POS_MSEC), final_list[-1][1], player)
            trace_list.append(speed)

        final_list.append(trace_list)

    def location(w, h, flag, img):   #공을 찾았는데 없으면 0!!
        print("location(w, h) : ", end='')
        print(w, h)

        h_1 = 0
        h_2 = img.shape[0] / 2
        h_3 = img.shape[0]

        w_1 = img.shape[1] / 3
        w_2 = (img.shape[1] / 3) * 2
        w_3 = img.shape[1]

        last = final_list[-1][0]  # 마지막 값 가져옴
        print("last : ", end='')
        print(last)

        if flag == 0 and last != 0 and final_list[-2][0] != 0:  #공을 찾았는데 없고, 0이 연속되지 않으며, 0사이 숫자값이 하나가 아니도록!
            addList(0, 0)

        else:
            if last == 0:
                if 0 <= w < w_1 and h_1 <= h < h_2:
                    print("새로이 1이 들어갑니다")
                    addList(1, 0)
                elif w_1 <= w < w_2 and h_1 <= h < h_2:
                    print("새로이 2가 들어갑니다")
                    addList(2, 0)
                elif w_2 <= w < w_3 and h_1 <= h < h_2:
                    print("새로이 3이 들어갑니다")
                    addList(3, 0)
                elif 0 <= w < w_1 and h_2 <= h < h_3:
                    print("새로이 4가 들어갑니다")
                    addList(4, 0)
                elif w_1 <= w < w_2 and h_2 <= h < h_3:
                    print("새로이 5가 들어갑니다")
                    addList(5, 0)
                elif w_2 <= w < w_3 and h_2 <= h < h_3:
                    print("새로이 6이 들어갑니다")
                    addList(6, 0)

            elif last == 1:
                if w_1 <= w < w_2 and h_1 <= h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                    print("2가 들어갑니다")
                    final_list.pop()
                    addList(2, 2)
                elif w_2 <= w < w_3 and h_1 <= h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                    print("3이 들어갑니다")
                    final_list.pop()
                    addList(3, 2)
                elif 0 <= w < w_1 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("4가 들어갑니다")
                    addList(4, 1)
                elif w_1 <= w < w_2 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("5가 들어갑니다")
                    addList(5, 1)
                elif w_2 <= w < w_3 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("6이 들어갑니다")
                    addList(6, 1)
                elif 0 <= w < w_1 and h_1 <= h < h_2:
                    print("공이 이전 [1]이랑 같은 공간에 있습니다!!")
                    return False
                else:
                    print("공이 나머지 빈 공간에 있습니다!!")
                    return False

            elif last == 2:
                if 0 <= w < w_1 and h_1 <= h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                    print("1이 들어갑니다")
                    final_list.pop()
                    addList(1, 2)
                elif w_2 <= w < w_3 and h_1 <= h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                    print("3이 들어갑니다")
                    final_list.pop()
                    addList(3, 2)
                elif 0 <= w < w_1 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("4가 들어갑니다")
                    addList(4, 1)
                elif w_1 <= w < w_2 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("5가 들어갑니다")
                    addList(5, 1)
                elif w_2 <= w < w_3 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("6이 들어갑니다")
                    addList(6, 1)
                elif w_1 <= w < w_2 and h_1 <= h < h_2:
                    print("공이 이전 [2]이랑 같은 공간에 있습니다!!")
                    return False
                else:
                    print("공이 나머지 빈 공간에 있습니다!!")
                    return False

            elif last == 3:
                if 0 <= w < w_1 and h_1 <= h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                    print("1이 들어갑니다")
                    final_list.pop()
                    addList(1, 2)
                elif w_1 <= w < w_2 and h_1 <= h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                    print("2가 들어갑니다")
                    final_list.pop()
                    addList(2, 2)
                elif 0 <= w < w_1 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("4가 들어갑니다")
                    addList(4, 1)
                elif w_1 <= w < w_2 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("5가 들어갑니다")
                    addList(5, 1)
                elif w_2 <= w < w_3 and h_2 <= h < h_3 and final_list[-2][0] != 4 and final_list[-2][0] != 5 and final_list[-2][0] != 6:
                    print("6이 들어갑니다")
                    addList(6, 1)
                elif w_2 <= w < w_3 and h_1 <= h < h_2:
                    print("공이 이전 [3]이랑 같은 공간에 있습니다!!")
                    return False
                else:
                    print("공이 나머지 빈 공간에 있습니다!!")
                    return False

            elif last == 4:
                if 0 <= w < w_1 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("1이 들어갑니다")
                    addList(1, 2)
                elif w_1 <= w < w_2 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("2가 들어갑니다")
                    addList(2, 2)
                elif w_2 <= w < w_3 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("3이 들어갑니다")
                    addList(3, 2)
                elif w_1 <= w < w_2 and h_2 <= h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                    print("5가 들어갑니다")
                    final_list.pop()
                    addList(5, 1)
                elif w_2 <= w < w_3 and h_2 <= h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                    print("6이 들어갑니다")
                    final_list.pop()
                    addList(6, 1)
                elif 0 <= w < w_1 and h_2 <= h < h_3:
                    print("공이 이전 [4]이랑 같은 공간에 있습니다!!")
                    return False
                else:
                    print("공이 나머지 빈 공간에 있습니다!!")
                    return False

            elif last == 5:
                if 0 <= w < w_1 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("1이 들어갑니다")
                    addList(1, 2)
                elif w_1 <= w < w_2 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("2가 들어갑니다")
                    addList(2, 2)
                elif w_2 <= w < w_3 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("3이 들어갑니다")
                    addList(3, 2)
                elif 0 <= w < w_1 and h_2 <= h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                    print("4가 들어갑니다")
                    final_list.pop()
                    addList(4, 1)
                elif w_2 <= w < w_3 and h_2 <= h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                    print("6이 들어갑니다")
                    final_list.pop()
                    addList(6, 1)
                elif w_1 <= w < w_2 and h_2 <= h < h_3:
                    print("공이 이전 [5]이랑 같은 공간에 있습니다!!")
                    return False
                else:
                    print("공이 나머지 빈 공간에 있습니다!!")
                    return False

            elif last == 6:
                if 0 <= w < w_1 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("1이 들어갑니다")
                    addList(1, 2)
                elif w_1 <= w < w_2 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("2가 들어갑니다")
                    addList(2, 2)
                elif w_2 <= w < w_3 and h_1 <= h < h_2 and final_list[-2][0] != 1 and final_list[-2][0] != 2 and final_list[-2][0] != 3:
                    print("3이 들어갑니다")
                    addList(3, 2)
                elif 0 <= w < w_1 and h_2 <= h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                    print("4가 들어갑니다")
                    final_list.pop()
                    addList(4, 1)
                elif w_1 <= w < w_2 and h_2 <= h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                    print("5가 들어갑니다")
                    final_list.pop()
                    addList(5, 1)
                elif w_2 <= w < w_3 and h_2 <= h < h_3:
                    print("공이 이전 [6]이랑 같은 공간에 있습니다!!")
                    return False
                else:
                    print("공이 나머지 빈 공간에 있습니다!!")
                    return False

        print(final_list)
        # cv2.waitKey(0)

        return True

    def initTracker(img, flag):  # Tracker가 Update 안 되었을 때만 flag가 1로 와서 동작
        nonlocal tracker
        nonlocal frame

        img_copy = img
        tracker = cv2.TrackerKCF_create()  # 추적자를 (다시) 생성(CSRT or KCF)

        # middle black 이미지 생성
        # sensivity = 20
        # img_black = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        # for i in range(0, img.shape[0]):
        #     for j in range(0, img.shape[1]):
        #         img_black[i, j] = 255
        #         if (img.shape[0] / 2) - sensivity <= i <= (img.shape[0] / 2) + sensivity:
        #             img_black[i, j] = 0
        #         if 0 <= j <= 10 or (img.shape[1] - 10) <= j <= img.shape[1]:
        #             img_black[i, j] = 0

        #img_black = cv2.cvtColor(img_black, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('black', img_black)
        # cv2.waitKey(0)

        # Step1. 주황색 물체 추출(이미지 중 흰색인 것만 남긴 새로운 이미지 생성)
        # sensitivity = 80
        # lower_white = np.array([40, 0, 255 - sensitivity])
        # upper_white = np.array([180, sensitivity, 255])
        # lower_orange = np.array([0, 0, 0])
        # upper_orange = np.array([30, 255, 255]

        str1 = str(frame)
        cv2.putText(img_copy, str1, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))

        # cv2.imshow("First_image", img_copy)
        # cv2.waitKey(0)
        # img = cv2.resize(img, dsize=(0, 0), fx=1, fy=0.9, interpolation=cv2.INTER_LINEAR)

        hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

        # img_mask = cv2.inRange(hsv, lower_white, upper_white)
        # img_white = cv2.bitwise_and(img_copy, img_copy, mask=img_mask)
        # cv2.imshow('img_white', img_white)
        # cv2.waitKey(0)

        # img_white = cv2.cvtColor(img_white, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('img_white2', img_white)
        # cv2.waitKey(0)

        h1, s, v = cv2.split(hsv)
        s = cv2.inRange(s, 51, 80)
        # cv2.imshow('s', s)
        # cv2.waitKey(0)

        ##8, 20 이 hue의 오렌지 영역 블루는 115,125
        h1 = cv2.inRange(h1, 8, 30)
        # cv2.imshow('h1', h1)
        # cv2.waitKey(0)

        color = cv2.bitwise_and(hsv, hsv, mask=h1)
        # cv2.imshow('and', color)
        # color = cv2.bitwise_or(color, hsv, mask=s)
        # cv2.imshow('or', color)
        color = cv2.cvtColor(color, cv2.COLOR_HSV2BGR)
        # cv2.imshow('BGR', color)
        color = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        # print(color)
        # cv2.imshow('GRAY', color)
        # cv2.waitKey(0)
        sensivity = 20
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if (img.shape[0] / 2) - sensivity <= i <= (img.shape[0] / 2) + sensivity:
                    color[i, j] = 0
                if 0 <= j <= 10 or (img.shape[1] - 10) <= j <= img.shape[1]:
                    color[i, j] = 0
        # color = cv2.bitwise_and(color, img_black)
        # cv2.imshow('Final', color)
        # cv2.waitKey(0)

        # inter = cv2.bitwise_and(color, img_white)
        # color = cv2.bitwise_xor(color, inter)
        # cv2.imshow('final', color)
        # cv2.waitKey(0)

        # 180이상인값은 흰색으로 낮은값은 검은색 threshold 245로 했었음
        # ret, color = cv2.threshold(color, 100, 255, cv2.THRESH_BINARY)
        # if not ret:
        #     print('Threshold 오류')
        #     return
        # cv2.imshow('threshold', color)
        # cv2.waitKey(0)

        # kernel = np.ones((2, 2), np.uint8)
        # color = cv2.morphologyEx(color, cv2.MORPH_OPEN, kernel)
        # cv2.imshow('morpho', color)
        # cv2.waitKey(0)

        circles = cv2.HoughCircles(color, cv2.HOUGH_GRADIENT, 1, 1, param1=50, param2=1, minRadius=0, maxRadius=8)

        if circles is not None:  # circles값이 있을 때
            print("circle이 is not None이므로(존재하므로) tracker를 (재)설정합니다")

            side = 10 * int(circles[0][0][2])
            rect = (circles[0][0][0] - (side / 2), circles[0][0][1] - (side / 2), side, side)

            if int(circles[0][0][0]) is not 0:  # circle값이 탐지되었고, 그 값이 0이 아닐 때(오류 검출이 아닐 때)
                tracker.init(img, rect)  # rect라고 설정한 놈을 트래킹해라 라고 초기화!
                print("Rect Initalize : ", end='')
                print(rect)
                cv2.rectangle(img, pt1=(int(circles[0][0][0] - (side / 2)), int(circles[0][0][1] - (side / 2))),
                              pt2=(int(circles[0][0][0] + (side / 2)), int(circles[0][0][1] + (side / 2))),
                              color=(0, 0, 0), thickness=3)
                if flag == 1:
                    location(int(circles[0][0][0]), int(circles[0][0][1]), 1, img)

                # cv2.imshow('Initial Rect', img)
                # cv2.waitKey(0)
                # cv2.destroyWindow('Initial Rect')
            else:
                location(-1, -1, 0, img)
                print("Circle 값이 탐지되었지만, 0값이 나와서 무시하고 진행됩니다.")
        else:
            location(-1, -1, 0, img)
            print("initTracker()가 실행되었지만, circle을 아예 찾지 못하여 무시하고 진행됩니다.")

    initTracker(img, 0)
    t_left = 0
    t_top = 0

    while True:  # 계속 잘 읽어오면
        ret, img = cap.read()  # cap을 1프렘씩 읽어서 img라는 변수에 저장!
        if not ret:  # ret에는 성공 실패 여부가 담김!!(프로그램이 끝날 때 자동으로 종료)
            print(p1_list)
            print(p2_list)
            print("최종 리스트 : ", end='')
            for x, y ,z in final_list:
                print(x)
            print(final_list)
            p1_avgSpeed, p2_avgSpeed = avgSpeed()
            jsonString = json.dumps(final_list)     #final_list를 JSON 파일로 인코딩
            print(jsonString)
            print(type(jsonString))
            print("영상 끝!!")

            if len(p1_list) > 0:
                p1_maxSpeed = max(p1_list)
            else:
                p1_maxSpeed = 0

            if len(p2_list) > 0:
                p2_maxSpeed = max(p2_list)
            else:
                p2_maxSpeed = 0


            return final_list, p1_avgSpeed, p2_avgSpeed, p1_maxSpeed, p2_maxSpeed

        frame = frame + 1
        print("--------------------------------------------------------------")
        print("frame : %i" % frame)
        str2 = str(frame)
        # img = cv2.resize(img, dsize=(0, 0), fx=1, fy=0.8, interpolation=cv2.INTER_LINEAR)

        # update = 매 프레임 읽는 img마다 rect가 따라가도록 만드는 함수
        success, box = tracker.update(img)  # success는 성공 여부, box은 ROI를 설정했을 떄 처럼 rect와 같은 형태의 데이터가 나오게 됨

        if success is True:
            print("Tracker가 사라지지 않고 업데이트 되었습니다!!")
            left, top, w, h = [int(v) for v in box]  # box의 값을 int형태로 변환하여 왼쪽 4개의 변수들에 넣어라

            # 한 곳에 머물러 있는지 확인
            if left == t_left:
                print("BBox의 left 좌표 값이 이전 값과 같습니다. InitTracker를 실행합니다.")
                initTracker(img, 0)     #밑에서 location을 체크하므로 여기선 flag가 0
                success, box = tracker.update(img)
                print(frame, success)
                left, top, w, h = [int(v) for v in box]  # box의 값을 int형태로 변환하여 왼쪽 4개의 변수들에 넣어라

            elif top == t_top:
                print("BBox의 top 좌표 값이 이전 값과 같습니다. InitTracker를 실행합니다.")
                initTracker(img, 0)     #밑에서 location을 체크하므로 여기선 flag가 0
                success, box = tracker.update(img)
                print(frame, success)
                left, top, w, h = [int(v) for v in box]  # box의 값을 int형태로 변환하여 왼쪽 4개의 변수들에 넣어라

            else:
                print("이전 BBox와 겹치지도 않습니다!!")

            t_left = left
            t_top = top

            # left, top, w, h 변수들을 가지고 ROI를 따라다니는 사각형 만들기
            cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255, 255, 255), thickness=3)
            cv2.putText(img, str2, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
            # cv2.imshow('Tracker_True', img)
            # cv2.waitKey(0)
            # cv2.destroyWindow('Tracker_True')

            location(left + (w / 2), top + (h / 2), 1, img)
            if w == 0:
                location(-1, -1, 0, img)
                print("네모가 없어졌어요!!")
                # initTracker(img)
        else:
            print("Tracker Update가 안되서 initTracker() 실행!!")
            cv2.putText(img, str2, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
            # cv2.imshow('Tracker_false', img)
            # cv2.waitKey(0)
            initTracker(img, 1) #공이 없다! 찾아보자!!(1은 완전히 location까지 체크하겠다는 의미, 0은 바깥에 나갔을 경우를 체크)

        cv2.imshow('Play', img)
        # cv2.waitKey(0)
        # if frame == 2:
        #     cv2.waitKey(0)

        # 'q' 누르면 종료
        if cv2.waitKey(1) == ord('q'):  # 1. 실제 화면을 볼 수 있도록 10ms씩 딜레이를 줌  2. 그 중 q를 누르면 종료가 됨
            print("Q키를 눌러 프로그램이 종료됩니다.")
            break





# config = {
#     "DEBUG": True,          # some Flask specific configs
#     "CACHE_TYPE": "simple", # Flask-Caching related configs
#     "CACHE_DEFAULT_TIMEOUT": 30000
# }
app = Flask(__name__)
# app.config.from_mapping(config)
# cache = Cache(app)

@app.route('/')
def api_main():
    print('root manse')
    return 'Hello, World!'

@app.route('/analysis/<videoName>')
def getAnalysisVideo(videoName):
    print(videoName,'come here~~')
    name = 'https://playstyle.s3.ap-northeast-2.amazonaws.com/videos/'+str(videoName)
    final_list, p1_avgSpeed, p2_avgSpeed, p1_maxSpeed, p2_maxSpeed = anal(name)

    splitedName = videoName.split('_')
    # if splitedName[1] == 'A':
    #     value['A']['win'] = True
    #     value['B']['win'] = False
    # else:
    #     value['A']['win'] = False
    #     value['B']['win'] = True

    #매개변수로 공 위치들, A 평균속도, B 평균속도, Winner(A가 이기면 True 지면 False)
    if splitedName[1] == 'A':
        value = makeResultFile(final_list, p1_avgSpeed, p2_avgSpeed, p1_maxSpeed, p2_maxSpeed, True)
    else:
        value = makeResultFile(final_list, p1_avgSpeed, p2_avgSpeed, p1_maxSpeed, p2_maxSpeed, False)


    value['roomId'] = splitedName[0]
    # value['winner'] = splitedName[1]
    value['seqId'] = splitedName[2].split('.')[0]

    return jsonify(value)#render_template('loop.html', values=value)

@app.route('/hello_loop')
def hello_name():
    value_list = ['list1', 'list2', 'list3']
    return render_template('loop.html', values=value_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
