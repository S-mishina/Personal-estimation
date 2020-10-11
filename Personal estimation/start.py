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
import socket

abc1=1
#if abc1==1:
  #cmd=(['start','python','client.py'])
  #proc = Popen( cmd,shell=True )
  #abc1=0

###########################################################################

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ソケットオブジェクト作成
#s.bind(("192.168.11.4", 30))    # サーバー側PCのipと使用するポート
#print("接続待機中")  
#s.listen(1)                     # 接続要求を待機
#soc, addr = s.accept()          # 要求が来るまでブロック
#print(str(addr)+"と接続完了")  
#cam = cv2.VideoCapture(0)#カメラオブジェクト作成

#############################################################################

abc=1
if abc ==1:
  cmd=(['start','python','camera1.py'])
  proc = Popen( cmd,shell=True )
  abc=0
cap = cv2.VideoCapture(1)#カメラ設定
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')#保存拡張子指定
face_cascade_path = 'haarcascade_frontalface_default.xml'#顔カスケードファイル
eye_cascade_path = 'haarcascade_eye.xml'#目カスケードファイル
face_cascade = cv2.CascadeClassifier(face_cascade_path)
#eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
cnt =0#通知開始時のカウント変数
cntt=0#認識時のカウント変数
today=0#ファイル作成時のカウント変数
n=1#ファイル作成時のループ変数

def message():#開始時の通知関数
    line_notify_token = ''
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = '監視カメラを起動しました。'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token} 
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    print('監視カメラを起動しました')

def message1():#終了時の通知関数
    line_notify_token = ''
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = '監視カメラを終了します'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    print('監視カメラを終了します')

cap1 = cv2.VideoCapture(0)#カメラ設定
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')#保存拡張子指定
face_cascade_path = 'haarcascade_frontalface_default.xml'#顔カスケードファイル
eye_cascade_path = 'haarcascade_eye.xml'#目カスケードファイル
face_cascade = cv2.CascadeClassifier(face_cascade_path)
#eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
cnt =0#通知開始時のカウント変数
cntt=0#認識時のカウント変数
today=0#ファイル作成時のカウント変数
n=1#ファイル作成時のループ変数

while(cap1.isOpened()):#撮影開始　ループ回り続ける
    ret1, frame1 = cap.read()

    while n==1:
        if cnt ==0:#開始メッセージを一度しかさせないためのif文
         #message()#開始メッセージ
         cnt =1
        if os.path.isdir(str(datetime.date.today())+str(today)):
         print('存在します')
         today=today+1#日付＋回数の回数をカウントする
         print(str(today))#回数カウント
        else:
         print('OK')
         os.makedirs(str(datetime.date.today())+str(today))#ファイル生成
         test=str(datetime.date.today())+str(today)#日付＋回数
         print(test)
         out = cv2.VideoWriter(str(test)+'/'+str(datetime.date.today())+'.mp4',fourcc, 10.0, (640,480))
         print('====================================================================================')
         print('ここから撮影が開始されます')
         n=0
         aaa=0
    if ret1==True:
        img = frame1.tostring()        #numpy行列からバイトデータに変換
        faces = face_cascade.detectMultiScale(frame1, scaleFactor=1.3, minNeighbors=5)
        for x, y, w, h in faces:
         print(x,y,w,h)#座標表示
         color=255, 0, 0#囲む色
         pattern=5#囲み方のpattern
         cv2.rectangle(frame1, (x, y), (x + w, y + h), color, pattern)
         gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
         face = frame1[y: y + h, x: x + w]
         aaa=1
         print (aaa)
         cntt=cntt+1
         print(cntt)#画像のカウント表示
         cv2.imwrite('face.jpg',face)#lineに送るための画像ファイル生成
         cv2.imwrite(str(datetime.date.today())+str(today)+'/'+str(cntt)+'face.jpg',face)#保存用の画像ファイル生成
         print('人が検知されました')
         #message3()
        print('検知できませんでした')
        out.write(frame1)
        #soc.send(img)              # ソケットにデータを送信
        cv2.imshow('frame',frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'):#Qで終了　押されない場合は回り続ける
         #message1()
         print('====================================================================================')
         print('videonファイルに動画が保存されます')
         print('終了しました。')
         print(datetime.date.today())
         break

cap1.release()
out.release()
cv2.destroyAllWindows()
