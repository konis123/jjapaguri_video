import cv2
import numpy as np
import matplotlib


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



#오렌지 색만 추출
def cvtAndExtract(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    ##8, 20 이 hue의 오렌지 영역
    h = cv2.inRange(h, 115, 125)
    color = cv2.bitwise_and(hsv, hsv, mask=h)
    color = cv2.cvtColor(color, cv2.COLOR_HSV2BGR)

    # cv2.imshow('thresholding 전 영상', color)

    #180이상인값은 흰색으로 낮은값은 검은색 threshold
    ret, frame = cv2.threshold(color, 180, 255, cv2.THRESH_BINARY)
    if not ret:
        print('Threshold 오류')
        return

    kernel = np.ones((5, 5), np.uint8)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)

    return frame

def showVideo(name):
    try:
        video = cv2.VideoCapture(name+'.mp4')
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

    list = []
    timeStamp = []

    init_a_state = frame[0:int(x / 3), int(y / 4):int(y / 2)].sum()
    init_b_state = frame[int(x / 3):int(x * 2 / 3), int(y / 4):int(y / 2)].sum()
    init_c_state = frame[int(x * 2 / 3):x, int(y / 4):int(y / 2)].sum()
    init_d_state = frame[0:int(x / 3), int(y / 2):int(y * 3 / 4)].sum()
    init_e_state = frame[int(x / 3):int(x * 2 / 3), int(y / 2):int(y * 3 / 4)].sum()
    init_f_state = frame[int(x * 2 / 3):int(x), int(y / 2):int(y * 3 / 4)].sum()

    drawRectangle(frame, x, y)

    #init값 조정하기위한 란
    init_b_state -= 43860
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

        #list와 timestamp에 값이 있을때
        if list and timeStamp:
            temp = list[-1]

            if temp == states.index(max(states)) and abs(timeStamp[-1] - video.get(cv2.CAP_PROP_POS_MSEC)) > 3000  :
                print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), max(states))
                cv2.waitKey(0)
                list.append(states.index(max(states)))
                timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))
            elif temp != states.index(max(states)) and abs(max(states))>10000:
                print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), max(states))
                cv2.waitKey(0)
                list.append(states.index(max(states)))
                timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))

        #list와 timestamp가 비어있을떄
        if not list and not timeStamp:
            print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC),'list 비어있었음 값넣을거야 ㅋ')
            cv2.waitKey(0)
            list.append(states.index(max(states)))
            timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))


        cv2.imshow('video', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    #list에 있는 값들 출력
    print(len(list),'개, ', len(timeStamp), '개')
    print(list)
    print(timeStamp)

    video.release()
    cv2.destroyAllWindows()

showVideo("videoplayback")


