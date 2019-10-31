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




def showVideo(name):
    try:
        video = cv2.VideoCapture(name+'.mp4')
    except:
        print('영상 읽기 실패')
        return

    frameNum = video.get(cv2.CAP_PROP_FPS)

    ret, vid = video.read()
    if not ret:
        print('비디오 읽기 오류')
        return

    vid = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    ret, frame = cv2.threshold(vid, 180, 255, cv2.THRESH_BINARY)
    if not ret:
        print('Threshold 오류')
        return

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

    # init_b_state += 48960
    # init_e_state += 49725

    print(init_a_state.sum(), init_b_state.sum(), init_c_state.sum(), init_d_state.sum(), init_e_state.sum(),
          init_f_state.sum())

    while True:
        ret, vid = video.read()
        if not ret:
            print('비디오 읽기 오류')
            break;

        vid = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(vid, 170, 255, cv2.THRESH_BINARY)
        if not ret:
            print('Threshold 오류')
            break;

        kernel = np.ones((5,5), np.uint8)
        frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        # frame = cv2.erode(frame, kernel, iterations=2)
        # frame = cv2.dilate(frame, kernel, iterations=1)

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

        if list and timeStamp:
            temp = list.pop()
            # tempTime = timeStamp.pop()
            if temp == states.index(max(states)) and abs(timeStamp[-1] - video.get(cv2.CAP_PROP_POS_MSEC)) > 3000  :
                print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), max(states))
                cv2.imshow('temp', frame)
                cv2.waitKey(0)
                list.append(states.index(max(states)))
                timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))
            elif temp != states.index(max(states)) and abs(max(states))>100000:
                print(states.index(max(states)), video.get(cv2.CAP_PROP_POS_MSEC), max(states))
                # print(a_state.sum(), b_state.sum(), c_state.sum(), d_state.sum(), e_state.sum(), f_state.sum())
                # prevMax = states.index(max(states))
                cv2.imshow('temp', frame)
                cv2.waitKey(0)
                list.append(states.index(max(states)))
                timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))

            else:
                list.append(temp)
                # timeStamp.append(tempTime)

        if not list and not timeStamp:
            print(states.index(max(states)))
            # prevMax = states.index(max(states))
            cv2.imshow('temp', frame)
            cv2.waitKey(0)
            list.append(states.index(max(states)))
            timeStamp.append(video.get(cv2.CAP_PROP_POS_MSEC))

        # cv2.imshow('d', a_state)

        # if abs(int(a_state.sum()) - int(prev_a_state.sum())) > 30000:
        #     print('a',abs(int(a_state.sum()) - int(prev_a_state.sum())))
        #
        # if abs(int(b_state.sum()) - int(prev_b_state.sum())) > 30000:
        #     print('b',abs(int(b_state.sum()) - int(prev_b_state.sum())))
        #
        # if abs(int(c_state.sum()) - int(prev_c_state.sum())) > 30000:
        #     print('c',abs(int(c_state.sum()) - int(prev_c_state.sum())))
        #
        # if abs(int(d_state.sum()) - int(prev_d_state.sum())) > 30000:
        #     print('d',abs(int(d_state.sum()) - int(prev_d_state.sum())))
        #
        # if abs(int(e_state.sum()) - int(prev_e_state.sum())) > 30000:
        #     print('e',abs(int(e_state.sum()) - int(prev_e_state.sum())))
        #
        # if abs(int(f_state.sum()) - int(prev_f_state.sum())) > 30000:
        #     print('f',abs(int(f_state.sum()) - int(prev_f_state.sum())))

        # prev_a_state = a_state
        # prev_b_state = b_state
        # prev_c_state = c_state
        # prev_d_state = d_state
        # prev_e_state = e_state
        # prev_f_state = f_state


        cv2.imshow('video', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    for i in list:
        print(i, "-")

    video.release()
    cv2.destroyAllWindows()

showVideo("test2")


