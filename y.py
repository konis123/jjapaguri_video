import cv2
import numpy as np
import json
# from flask import Flask, request, jsonify

def makeResultFile(list):
    f = open(r"C:\Users\clock\PycharmProjects\jjapaguri\result.txt", 'w')

    #각 플레이어 공격 방향 횟수
    a_player_left_num = 0
    b_player_left_num = 0

    a_player_middle_num = 0
    b_player_middle_num = 0

    a_player_right_num = 0
    b_player_right_num = 0

    a_player_total_attack_num = 0
    b_player_total_attack_num = 0


    i=1
    while i < len(list):
        if list[i][0] == 0:
            FROM = -1
            TO = -1
            if list[i][0]==0:
                if (i+1) < len(list):
                    FROM = list[i+1][0]
                if (i+2) < len(list):
                    TO = list[i+2][0]
                    if TO == 1:
                        b_player_right_num += 1
                        b_player_total_attack_num += 1
                    elif TO == 2:
                        b_player_middle_num += 1
                        b_player_total_attack_num += 1
                    elif TO == 3:
                        b_player_left_num += 1
                        b_player_total_attack_num += 1
                    elif TO == 4:
                        a_player_left_num += 1
                        a_player_total_attack_num += 1
                    elif TO == 5:
                        a_player_middle_num += 1
                        a_player_total_attack_num += 1
                    elif TO == 6:
                        a_player_right_num += 1
                        a_player_total_attack_num += 1

            #네트에 걸렸을경우
            if TO == -1:
                if FROM == 1:
                    f.write('네트: 좌측에 걸렸습니다.\n')
                elif FROM == 2:
                    f.write('네트: 중앙에 걸렸습니다.\n')
                elif FROM == 3:
                    f.write('네트: 우측에 걸렸습니다.\n')
                elif FROM == 4:
                    f.write('네트: 우측에 걸렸습니다.\n')
                elif FROM == 5:
                    f.write('네트: 중앙에 걸렸습니다.\n')
                elif FROM == 6:
                    f.write('네트: 좌측에 걸렸습니다.\n')

                break

            #랠리 잘 된 경우
            f.write('%d -> %d    속력: %0.2f\n' % (FROM, TO, list) )

        i+=1


    f.write("A플레이어 좌측 공격 비율: %0.2f\n" % (a_player_left_num/a_player_total_attack_num))
    f.write("A플레이어 중앙 공격 비율: %0.2f\n" % (a_player_middle_num/a_player_total_attack_num))
    f.write("A플레이어 우측 공격 비율: %0.2f\n" % (a_player_right_num/a_player_total_attack_num))
    f.write("B플레이어 좌측 공격 비율: %0.2f\n" % (b_player_left_num/b_player_total_attack_num))
    f.write("B플레이어 중앙 공격 비율: %0.2f\n" % (b_player_middle_num/b_player_total_attack_num))
    f.write("B플레이어 우측 공격 비율: %0.2f\n" % (b_player_right_num/b_player_total_attack_num))




# 리스트 생성
final_list = [[0, 0, 0]]
p1_list = []
p2_list = []

video_path = '2_6.mp4'
cap = cv2.VideoCapture(video_path)  # video_path를 설정했으면 0 대신 '파일이름'

if not cap.isOpened():  # video(cap)이 잘 열렸는지.. 아니면 exit
    print("No video file")
    exit()

frame = 1
tracker = cv2.TrackerKCF_create()  # 추적자 생성(CSRT라는 트래커)

ret, img = cap.read()
print("이미지 크기(h,w,c) : ", end='')
print(img.shape)

# 영상 가로세로 바뀌면 이거 바꿔야 돼!!
h_1 = 0
h_2 = img.shape[0] / 2
h_3 = img.shape[0]

w_1 = img.shape[1] / 3
w_2 = (img.shape[1] / 3) * 2
w_3 = img.shape[1]

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

    p1_avgSpeed = p1_avgSpeed / p1_count
    p2_avgSpeed = p2_avgSpeed / p2_count

    # print(p1_list)
    # print(p2_list)
    # print(p1_count)
    # print(p2_count)
    print("p1 평균 속력 : ", end='')
    print(p1_avgSpeed)
    print("p2 평균 속력 : ", end='')
    print(p2_avgSpeed)

def getSpeed(arrive, start, player):
    global p1_speed
    global p1_count
    global p2_speed
    global p2_count

    if player == 1:
        p1_count = p1_count + 1
        p1_speed = (1.35 / (arrive - start)) * 1000
        p1_list.append(p1_speed)

        return p1_speed

    elif player == 2:
        p2_count = p2_count + 1
        p2_speed = (1.35 / (arrive - start)) * 1000
        p2_list.append(p2_speed)

        return p2_speed

def addList(num, player):
    trace_list = []

    trace_list.append(num)
    trace_list.append(cap.get(cv2.CAP_PROP_POS_MSEC))

    if num == 0:                #영상 외부로 나간 것은
        trace_list.append(0)    #speed값이 없음!!

    else :                      #영상 내부의 값은 스피드 계산 가능
        speed = getSpeed(cap.get(cv2.CAP_PROP_POS_MSEC), final_list[-1][1], player)
        trace_list.append(speed)

    final_list.append(trace_list)

def location(w, h, flag):   #공을 찾았는데 없으면 0!!
    print(w, h)

    last = final_list[-1][0]  # 마지막 값 가져옴
    print("last : ", end='')
    print(last)

    if flag == 0 and last != 0:
        addList(0, 0)

    else:
        if last == 0:
            if 0 < w < w_1 and h_1 < h < h_2:
                print("1이 들어갑니다")
                addList(1, 2)
            elif w_1 < w < w_2 and h_1 < h < h_2:
                print("2가 들어갑니다")
                addList(2, 2)
            elif w_2 < w < w_3 and h_1 < h < h_2:
                print("3이 들어갑니다")
                addList(3, 2)
            elif 0 < w < w_1 and h_2 < h < h_3:
                print("4가 들어갑니다")
                addList(4, 1)
            elif w_1 < w < w_2 and h_2 < h < h_3:
                print("5가 들어갑니다")
                addList(5, 1)
            elif w_2 < w < w_3 and h_2 < h < h_3:
                print("6이 들어갑니다")
                addList(6, 1)

        elif last == 1:
            if w_1 < w < w_2 and h_1 < h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                print("2가 들어갑니다")
                final_list.pop()
                addList(2, 2)
            elif w_2 < w < w_3 and h_1 < h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                print("3이 들어갑니다")
                final_list.pop()
                addList(3, 2)
            elif 0 < w < w_1 and h_2 < h < h_3:
                print("4가 들어갑니다")
                addList(4, 1)
            elif w_1 < w < w_2 and h_2 < h < h_3:
                print("5가 들어갑니다")
                addList(5, 1)
            elif w_2 < w < w_3 and h_2 < h < h_3:
                print("6이 들어갑니다")
                addList(6, 1)
            elif 0 < w < w_1 and h_1 < h < h_2:
                print("공이 이전 [1]이랑 같은 공간에 있습니다!!")
                return False
            else:
                print("공이 나머지 빈 공간에 있습니다!!")
                return False

        elif last == 2:
            if 0 < w < w_1 and h_1 < h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                print("1이 들어갑니다")
                final_list.pop()
                addList(1, 2)
            elif w_2 < w < w_3 and h_1 < h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                print("3이 들어갑니다")
                final_list.pop()
                addList(3, 2)
            elif 0 < w < w_1 and h_2 < h < h_3:
                print("4가 들어갑니다")
                addList(4, 1)
            elif w_1 < w < w_2 and h_2 < h < h_3:
                print("5가 들어갑니다")
                addList(5, 1)
            elif w_2 < w < w_3 and h_2 < h < h_3:
                print("6이 들어갑니다")
                addList(6, 1)
            elif w_1 < w < w_2 and h_1 < h < h_2:
                print("공이 이전 [2]이랑 같은 공간에 있습니다!!")
                return False
            else:
                print("공이 나머지 빈 공간에 있습니다!!")
                return False

        elif last == 3:
            if 0 < w < w_1 and h_1 < h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                print("1이 들어갑니다")
                final_list.pop()
                addList(1, 2)
            elif w_1 < w < w_2 and h_1 < h < h_2 and (final_list[-2][0] == 4 or final_list[-2][0] == 5 or final_list[-2][0] == 6):
                print("2가 들어갑니다")
                final_list.pop()
                addList(22, 2)
            elif 0 < w < w_1 and h_2 < h < h_3:
                print("4가 들어갑니다")
                addList(4, 1)
            elif w_1 < w < w_2 and h_2 < h < h_3:
                print("5가 들어갑니다")
                addList(5, 1)
            elif w_2 < w < w_3 and h_2 < h < h_3:
                print("6이 들어갑니다")
                addList(6, 1)
            elif w_2 < w < w_3 and h_1 < h < h_2:
                print("공이 이전 [3]이랑 같은 공간에 있습니다!!")
                return False
            else:
                print("공이 나머지 빈 공간에 있습니다!!")
                return False

        elif last == 4:
            if 0 < w < w_1 and h_1 < h < h_2:
                print("1이 들어갑니다")
                addList(1, 2)
            elif w_1 < w < w_2 and h_1 < h < h_2:
                print("2가 들어갑니다")
                addList(2, 2)
            elif w_2 < w < w_3 and h_1 < h < h_2:
                print("3이 들어갑니다")
                addList(3, 2)
            elif w_1 < w < w_2 and h_2 < h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                print("5가 들어갑니다")
                final_list.pop()
                addList(5, 1)
            elif w_2 < w < w_3 and h_2 < h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                print("6이 들어갑니다")
                final_list.pop()
                addList(6, 1)
            elif 0 < w < w_1 and h_2 < h < h_3:
                print("공이 이전 [4]이랑 같은 공간에 있습니다!!")
                return False
            else:
                print("공이 나머지 빈 공간에 있습니다!!")
                return False

        elif last == 5:
            if 0 < w < w_1 and h_1 < h < h_2:
                print("1이 들어갑니다")
                addList(1, 2)
            elif w_1 < w < w_2 and h_1 < h < h_2:
                print("2가 들어갑니다")
                addList(2, 2)
            elif w_2 < w < w_3 and h_1 < h < h_2:
                print("3이 들어갑니다")
                addList(3, 2)
            elif 0 < w < w_1 and h_2 < h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                print("4가 들어갑니다")
                final_list.pop()
                addList(4, 1)
            elif w_2 < w < w_3 and h_2 < h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                print("6이 들어갑니다")
                final_list.pop()
                addList(6, 1)
            elif w_1 < w < w_2 and h_2 < h < h_3:
                print("공이 이전 [5]이랑 같은 공간에 있습니다!!")
                return False
            else:
                print("공이 나머지 빈 공간에 있습니다!!")
                return False

        elif last == 6:
            if 0 < w < w_1 and h_1 < h < h_2:
                print("1이 들어갑니다")
                addList(1, 2)
            elif w_1 < w < w_2 and h_1 < h < h_2:
                print("2가 들어갑니다")
                addList(2, 2)
            elif w_2 < w < w_3 and h_1 < h < h_2:
                print("3이 들어갑니다")
                addList(3, 2)
            elif 0 < w < w_1 and h_2 < h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                print("4가 들어갑니다")
                final_list.pop()
                addList(4, 1)
            elif w_1 < w < w_2 and h_2 < h < h_3 and (final_list[-2][0] == 1 or final_list[-2][0] == 2 or final_list[-2][0] == 3):
                print("5가 들어갑니다")
                final_list.pop()
                addList(5, 1)
            elif w_2 < w < w_3 and h_2 < h < h_3:
                print("공이 이전 [6]이랑 같은 공간에 있습니다!!")
                return False
            else:
                print("공이 나머지 빈 공간에 있습니다!!")
                return False

    print("trace_list 중간 점검")
    print(final_list)
    # cv2.waitKey(0)
    return True

def initTracker(img, flag):  # Tracker가 Update 안 되었을 때만 flag가 1로 와서 동작
    global tracker
    global frame
    img_copy = img
    tracker = cv2.TrackerKCF_create()  # 추적자를 (다시) 생성(CSRT or KCF)

    # Step1. 주황색 물체 추출(이미지 중 흰색인 것만 남긴 새로운 이미지 생성)
    lower_orange = np.array([0, 0, 0])
    upper_orange = np.array([30, 255, 255])

    str1 = str(frame)
    cv2.putText(img_copy, str1, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
    # cv2.imshow("First_image", img_copy)
    # cv2.waitKey(0)
    # img = cv2.resize(img, dsize=(0, 0), fx=1, fy=0.9, interpolation=cv2.INTER_LINEAR)
    img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

    # 주황색 픽셀 값 추출
    img_mask = cv2.inRange(img_hsv, lower_orange, upper_orange)
    img_orange = cv2.bitwise_and(img_copy, img_copy, mask=img_mask)

    cv2.putText(img_orange, str1, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
    # cv2.imshow("img_orange", img_orange)
    # cv2.waitKey(0)

    # Step2. 새로운 이미지에서, 원형 객체 추출
    # n = 5
    # for i in range(1, n):
    #     img_orange = cv2.medianBlur(img_orange, 5)
    img_orange = cv2.cvtColor(img_orange, cv2.COLOR_BGR2GRAY)

    cv2.putText(img_orange, str1, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
    # cv2.imshow('circle', img_orange)
    # cv2.waitKey(0)

    cv2.destroyWindow('First_image')
    cv2.destroyWindow('img_orange')
    cv2.destroyWindow('circle')
    cv2.destroyWindow('Tracker_false')

    circles = cv2.HoughCircles(img_orange, cv2.HOUGH_GRADIENT, 1, 1, param1=50, param2=1, minRadius=0, maxRadius=10)

    if circles is not None:  # circles값이 있을 때
        print("circle이 is not none이므로(존재하므로) tracker를 (재)설정합니다")

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
                locate = location(int(circles[0][0][0]), int(circles[0][0][1]), 1)
                if locate is False:
                    print("False라닛!!!!!!")
            # cv2.imshow('Initial Rect', img)
            # cv2.waitKey(0)
            # cv2.destroyWindow('Initial Rect')
        else:
            print("Circle 값이 탐지되었지만, 0값이 나와서 무시하고 진행됩니다.")
    else:
        location(0, 0, 0)
        print("initTracker()가 실행되었지만, circle을 아예 찾지 못하여 무시하고 진행됩니다.")

initTracker(img, 0)
t_left = 0
t_top = 0

while True:  # 계속 잘 읽어오면
    ret, img = cap.read()  # cap을 1프렘씩 읽어서 img라는 변수에 저장!
    if not ret:  # ret에는 성공 실패 여부가 담김!!(프로그램이 끝날 때 자동으로 종료)
        print(final_list)
        avgSpeed()
        print("영상 끝!!")
        jsonString = json.dumps(final_list)
        print(jsonString)
        print(type(jsonString))
        makeResultFile(final_list)

        exit()

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
            print("left : %i" % left)
            print("t_left : %i" % t_left)
            print("BBox의 left 좌표 값이 이전 값과 같습니다. InitTracker를 실행합니다.")
            initTracker(img, 0)
            success, box = tracker.update(img)
            left, top, w, h = [int(v) for v in box]  # box의 값을 int형태로 변환하여 왼쪽 4개의 변수들에 넣어라

        elif top == t_top:
            print("top : %i" % top)
            print("t_top : %i" % t_top)
            print("BBox의 top 좌표 값이 이전 값과 같습니다. InitTracker를 실행합니다.")
            initTracker(img, 0)
            success, box = tracker.update(img)
            left, top, w, h = [int(v) for v in box]  # box의 값을 int형태로 변환하여 왼쪽 4개의 변수들에 넣어라

        else:
            print("이전 BBox와 겹치지도 않습니다!!")
            # print("left : %i" % left)
            # print("t_left : %i" % t_left)
            # print("top : %i" % top)
            # print("t_top : %i" % t_top)

        t_left = left
        t_top = top

        # left, top, w, h 변수들을 가지고 ROI를 따라다니는 사각형 만들기
        cv2.rectangle(img, pt1=(left, top), pt2=(left + w, top + h), color=(255, 255, 255), thickness=3)
        cv2.putText(img, str2, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
        # cv2.imshow('Tracker_True', img)
        # cv2.waitKey(0)
        # cv2.destroyWindow('Tracker_True')

        locate = location(left + (w / 2), top + (h / 2), 1)
        if locate is False:
            print("False라닛!?")

        if w == 0:
            print("네모가 없어졌어요!!")
            # initTracker(img)
    else:
        print("Tracker Update가 안되서 initTracker() 실행!!")
        cv2.putText(img, str2, (0, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0))
        # cv2.imshow('Tracker_false', img)
        # cv2.waitKey(0)
        initTracker(img, 1) #공이 없다! 찾아보자!

    cv2.imshow('Play', img)
    if frame == 2:
        cv2.waitKey(0)

    # 'q' 누르면 종료
    if cv2.waitKey(10) == ord('q'):  # 1. 실제 화면을 볼 수 있도록 10ms씩 딜레이를 줌  2. 그 중 q를 누르면 종료가 됨
        print("Q키를 눌러 프로그램이 종료됩니다.")
        break

