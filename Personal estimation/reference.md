<h1>＜学習方法＞</h1>
python retrain.py --imagedir="FilePath"<br>
学習スタート<br>
<h1>＜認識部分＞</h1>
カメラ二台の場合<br>
python start.py<br>
認識部分のみの場合<br>
python camera1.py<br>
<h2>推論部分のコード変更</h2>
各pcの環境に応じてプログラムの書き換えを行ってください.<br>
cmd=(['start','python','label_image.py','--image=FilePath\\face.jpg'])<br>
ディレクトリは//で設定をお願いします.<br>
<h1>推論部分</h1>
python label_image.py<br>

通常カメラ2台でも1台でも認識部分は自動的に起動するように設定してあります.
認識クライアント部分はprocessingで作成しています.
<pre>
環境情報
学習に必要なもの.
・TF
・TF-HUB
・anaconda
・python
認識に必要なもの.
・python
・processing
</pre>
