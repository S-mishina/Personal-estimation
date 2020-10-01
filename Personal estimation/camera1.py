from subprocess import Popen
import subprocess
import os
import os.path
import numpy as np
import cv2
import datetime
import requests
import time
import subprocess

cap = cv2.VideoCapture(0)#カメラ設定
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')#保存拡張子指定
face_cascade_path = 'haarcascade_frontalface_default.xml'#顔カスケードファイル
eye_cascade_path = 'haarcascade_eye.xml'#目カスケードファイル
face_cascade = cv2.CascadeClassifier(face_cascade_path)
#eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
cnt =0#通知開始時のカウント変数
cntt=0#認識時のカウント変数
today=0#ファイル作成時のカウント変数
n=1#ファイル作成時のループ変数
while(cap.isOpened()):#撮影開始　ループ回り続ける
    ret, frame = cap.read()
    aaa=0
    if ret==True:
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)
        for x, y, w, h in faces:
         print(x,y,w,h)#座標表示
         color=255, 0, 0#囲む色
         pattern=5#囲み方のpattern
         cv2.rectangle(frame, (x, y), (x + w, y + h), color, pattern)
         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         face = frame[y: y + h, x: x + w]
         aaa=1
         print (aaa)
         cntt=cntt+1
         print(cntt)#画像のカウント表示
         cv2.imwrite('face.jpg',face)#lineに送るための画像ファイル生成
         cv2.imwrite(str(datetime.date.today())+str(today)+'/'+str(cntt)+'face.jpg',face)#保存用の画像ファイル生成
         print('人が検知されました')
        if aaa==1:
             cmd=(['start','python','label_image.py','--image=C:\\Users\\管理アカウント\\Desktop\\fase\\face.jpg'])
             proc = Popen( cmd,shell=True )
             time.sleep(30)
             aaa=0
         #message3()
        print('検知できませんでした')
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):#Qで終了　押されない場合は回り続ける
         print('終了しました。')
         break

cap.release()
out.release()
cv2.destroyAllWindows()