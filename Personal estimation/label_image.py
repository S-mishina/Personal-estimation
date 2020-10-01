# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
#LINEの通知プログラムの実装

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import time
import argparse
import requests
import socket
import datetime

host = "192.168.159.1" #Processingで立ち上げたサーバのIPアドレス
port = 10001       #Processingで設定したポート番号

datetime.date.today().year#年
datetime.date.today().day#日
cnvtime=datetime.datetime.today().strftime("%Y%m%d")#フォーマットの指定
cnvtime1=datetime.datetime.today().strftime("%Y/%m/%d/%H/%M/%S")#フォーマットの指定
f = open(str(cnvtime) +'.txt','a')
print (cnvtime)

def message():#開始時の通知関数
    line_notify_token = 'lineAPI'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = ''
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token} 
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    print('監視カメラを起動しました')

def message1():#終了時の通知関数
    line_notify_token = 'lineAPI'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = ''
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    print('監視カメラを終了します')

def message2():#開始時の通知関数
    line_notify_token = 'lineAPI'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = 'lineAPI'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token} 
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    print('監視カメラを起動しました')

def message3():#終了時の通知関数
    line_notify_token = 'lineAPI'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = 'それ以外が検出されました'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    print('監視カメラを終了します')

import numpy as np
import tensorflow as tf

t1 = time.time() 
def load_graph(model_file):
  
  graph = tf.Graph()
  graph_def = tf.GraphDef()
  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


if __name__ == "__main__":
  file_name = "tensorflow/examples/label_image/data/grace_hopper.jpg"
  model_file = \
    "tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb"
  label_file = "tensorflow/examples/label_image/data/imagenet_slim_labels.txt"
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255
  input_layer = "input"
  output_layer = "InceptionV3/Predictions/Reshape_1"

  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed",default='C:\\1face.jpg')
  parser.add_argument("--graph", help="graph/model to be executed",default='C:\\tmp\output_graph.pb')
  parser.add_argument("--labels", help="name of file containing labels",default='C:\\tmp\output_labels.txt')
  parser.add_argument("--input_height", type=int, help="input height")
  parser.add_argument("--input_width", type=int, help="input width")
  parser.add_argument("--input_mean", type=int, help="input mean")
  parser.add_argument("--input_std", type=int, help="input std")
  parser.add_argument("--input_layer", help="name of input layer",default='Placeholder')
  parser.add_argument("--output_layer", help="name of output layer",default='final_result')
  args = parser.parse_args()

  if args.graph:
    model_file = args.graph
  if args.image:
    file_name = args.image
  if args.labels:
    label_file = args.labels
  if args.input_height:
    input_height = args.input_height
  if args.input_width:
    input_width = args.input_width
  if args.input_mean:
    input_mean = args.input_mean
  if args.input_std:
    input_std = args.input_std
  if args.input_layer:
    input_layer = args.input_layer
  if args.output_layer:
    output_layer = args.output_layer

  graph = load_graph(model_file)
  t = read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)
  print (labels[0],results[0])
  print (labels[1],results[1])
  print (labels[2],results[2])
  a=results[0]
  b=results[1]
  c=results[2]
  d=results[3]
  a=a*100
  b=b*100
  c=c*100
  d=d*100
  print(a)
  print(b)
  print(c)
  print(d)
#ここからsocketプログラムを書く
if a>=80 :
   print('A')
   f.write(str(cnvtime1)+'A'+'\n')
   #message()
   ni=1
elif b>=80:
   print('B')
   f.write(str(cnvtime1)+'B'+'\n')
   #message1()
   ni=2
elif c>=80:
   print('不審者を検知しました')
   f.write(str(cnvtime1)+'不審者を検知'+'\n')
   #message2()
   ni=3
elif d>=80:
   print('D)
   f.write(str(cnvtime1)+'D'+'\n')
   #message3()
   ni=4
else :
   print('不審者を検知しました.')
t2 = time.time() 
#後日実行速度の計測を行う.
#スピードの調整を行う.
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")
#ここにsocket処理を盛り込む
f.close()
if __name__ == '__main__':
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成
    socket_client.connect((host, port))                               #サーバに接続

    #socket_client.send(1)                
    #データを送信 Python2
    socket_client.send(str(ni).encode('utf-8')) #データを送信 Python3

