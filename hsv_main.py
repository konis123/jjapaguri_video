# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
import sys

# 0~5 구역 사각형으로 표시
def drawRectangle(frame, x, y):

    #A_state
    cv2.rectangle(frame, (int(y/4),0), (int(y/2),int(x/3)), (255,255,255), 1)
    #B_state
    cv2.rectangle(frame, (int(y/4),int(x/3)), (int(y/2),int(x*2/3)), (255,255,255), 1)
    #C_state
    cv2.rectangle(frame, (int(y/4),int(x*2/3)), (int(y/2),int(x)), (255,255,255), 1)
    #D_state
    cv2.rectangle(frame, (int(y/2),0), (int(y*3/4),int(x/3)), (255,255,255), 1)
    #E_state
    cv2.rectangle(frame, (int(y/2),0), (int(y*3/4),int(x*2/3)), (255,255,255), 1)
    #F_state
    cv2.rectangle(frame, (int(y/2),0), (int(y*3/4),int(x)), (255,255,255), 1)


#차례대로 거리 시간
def getSpeed(d, t):

    v = d/t

    return v

#디렉토리에 새로운 영상이 생겼는지 확인
execList = []   #앞으로 실행될 영상들
fileList = []   #현재 폴더에 있는 파일들
def dirSearch():
    tempList = glob.glob('*_*.mp4')
    for fileName in fileList:
        tempList.remove(fileName)


    for file in tempList:
        execList.append(file)

    print(tempList)



    return 0;


#오렌지 색만 추출
def cvtAndExtract(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s=cv2.inRange(s,40,70)
    cv2.imshow('s',s)
    # cv2.imshow('v',v)
    ##8, 20 이 hue의 오렌지 영역 블루는 115,125
    h = cv2.inRange(h, 0, 25)
    color = cv2.bitwise_and(hsv, hsv, mask=h)
    color = cv2.bitwise_or(color, hsv, mask=s)
    color = cv2.cvtColor(color, cv2.COLOR_HSV2BGR)

    # cv2.imshow('thresholding 전 영상', color)

    #180이상인값은 흰색으로 낮은값은 검은색 threshold 245로 했었음
    ret, frame = cv2.threshold(color, 100, 255, cv2.THRESH_BINARY)
    if not ret:
        print('Threshold 오류')
        return

    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

    return frame

def showVideo(name):
    try:
        video = cv2.VideoCapture(name)
    except:
        print('영상 읽기 실패')
        return

    # frameNum = video.get(cv2.CAP_PROP_FPS)

    ret, vid = video.read()
    if not ret:
        print('비디오 읽기 오류')
        return

    #영상 변환 및 추출
    frame = cvtAndExtract(vid)

    x = frame.shape[0]
    y = frame.shape[1]

    list = []   #리스트에는 (위치, 시간, 속도) 튜플이 저장됨.
    # timeStamp = []
    # velocity = []

    # list.append(-1)
    # timeStamp.append(-1)
    list.append((-1,-1,-1))

    init_a_state = 0#frame[0:int(x / 3), int(y / 4):int(y / 2)].sum()
    init_b_state = 0#frame[int(x / 3):int(x * 2 / 3), int(y / 4):int(y / 2)].sum()
    init_c_state = 0#frame[int(x * 2 / 3):x, int(y / 4):int(y / 2)].sum()
    init_d_state = 0#frame[0:int(x / 3), int(y / 2):int(y * 3 / 4)].sum()
    init_e_state = 0#frame[int(x / 3):int(x * 2 / 3), int(y / 2):int(y * 3 / 4)].sum()
    init_f_state = 0#frame[int(x * 2 / 3):int(x), int(y / 2):int(y * 3 / 4)].sum()

    drawRectangle(frame, x, y)

    #init값 조정하기위한 란
    #init_b_state -= 43860
    # init_e_state += 49725

    print(init_a_state, init_b_state, init_c_state,init_d_state, init_e_state, init_f_state)

    while True:
        ret, vid = video.read()
        if not ret:
            print('비디오 읽기 오류')
            break;



        #영상 변환 및 추출
        frame = cvtAndExtract(vid)

        a_state = frame[0:int(x/3), int(y/4):int(y/2)].sum()
        b_state = frame[int(x/3):int(x*2/3), int(y/4):int(y/2)].sum()
        c_state = frame[int(x*2/3):x, int(y/4):int(y/2)].sum()
        d_state = frame[0:int(x/3), int(y/2):int(y*3/4)].sum()
        e_state = frame[int(x/3):int(x*2/3), int(y/2):int(y*3/4)].sum()
        f_state = frame[int(x*2/3):x, int(y/2):int(y*3/4)].sum()



        #각 구역의 합의 평균값을 구해서
        #midVal = int((int(a_state.sum()) + int(b_state.sum()) + int(c_state.sum()) + int(d_state.sum()) + int(e_state.sum()) + int(f_state.sum()))/6)

        states = []
        states.append(abs(int(init_a_state) - int(a_state)))
        states.append(abs(int(init_b_state) - int(b_state)))
        states.append(abs(int(init_c_state) - int(c_state)))
        states.append(abs(int(init_d_state) - int(d_state)))
        states.append(abs(int(init_e_state) - int(e_state)))
        states.append(abs(int(init_f_state) - int(f_state)))

        #사각형으로 구역 표시
        drawRectangle(frame, x,y)

        cv2.imshow('original', vid)
        cv2.imshow('video', frame)
        # cv2.waitKey(0)

        #list와 timestamp에 값이 있을때
        if list:
            temp = list[-1][0]

            if temp == states.index(max(states)) and abs(list[-1][1] - video.get(cv2.CAP_PROP_POS_MSEC)) > 2000  :
                print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), max(states),'-')
                # cv2.waitKey(0)
                list.append((states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), getSpeed(0.6, list[-1][1]/1000)))
                # timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))
                # velocity.append(getSpeed(0.6, timeStamp[-1]/1000))

            elif temp != states.index(max(states)) and abs(max(states))>10:
                print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), max(states),'--')
                # cv2.waitKey(0)
                list.append((states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), getSpeed(0.6, list[-1][1]/1000)))
                # timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))
                # velocity.append(getSpeed(0.6, timeStamp[-1]/1000))

        #list와 timestamp가 비어있을떄, 근데 이거 실행안됨 예외 처리하도록 해둔거임.
        if not list:
            print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC),'list 비어있었음 값넣을거야 ㅋ')
            # cv2.waitKey(0)
            list.append(states.index(max(states)))
            # timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))

        # cv2.imshow('original', vid)
        # cv2.imshow('video', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    #list에 있는 값들 출력
    # print(len(list),'개, ', len(timeStamp), '개')
    print(list)
    # print(timeStamp)
    # print(velocity)

    makeResultFile(list)

    video.release()
    cv2.destroyAllWindows()


def makeResultFile(list):
    f = open(r"C:\Users\clock\PycharmProjects\jjapaguri\result.txt", 'w')
    # for (loc, time, vel) in list:
    #     data = "%d %0.2f %0.2f\n" % (loc, time, vel)
    #     f.write(data)
    # f.close()
    i=1
    while i < len(list):
        if list[i][0] == 0:
            FROM = -1
            TO = -1
            if list[i][0]==0:
                if (i+1) < len(list):
                    FROM = list[i+1]
                if (i+2) < len(list):
                    TO = list[i+2][0]

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
            f.write('%d -> %d \n' % (FROM, TO) )


        else:
            continue

        i+=1


# showVideo(sys.argv[1])
showVideo('2_7.mkv')

