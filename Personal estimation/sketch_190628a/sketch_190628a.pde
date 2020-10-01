import processing.net.*;

int port = 10001; // 適当なポート番号を設定

Server server;
PImage img;
PImage img2;
PImage img3;

void setup() {
 size(300,300); 
  server = new Server(this, port);
  println("server address: " + server.ip()); // IPアドレスを出力
    img = loadImage("C:/fase/15face.jpg");
    img2 = loadImage("C:/fase/68face.jpg");
    img3 = loadImage("C:/fase/14face.jpg");
}


void draw() {
  Client client = server.available();
  if (client !=null) {
    String whatClientSaid = client.readString();
    if (whatClientSaid != null) {
      int j0 = Integer.valueOf(whatClientSaid);
      println(j0); // Pythonからのメッセージを出力
    
  if(j0==1){
  background(204);
    image(img, 0, 0);
    text("A"+"検出しました", 65, 290);
    
}else if(j0==2){
  background(204);
  image(img2, 0, 0);
  text("B"+"検出しました", 65, 290);
}else if(j0==3){
    background(204);
    text("C"+"検出しました", 65, 290);
}else if(j0==4){
    background(204);
    image(img3, 0, 0);
    text("D"+"検出しました", 65, 290);
}else if(j0==5){
  background(204);  
  
}
  }
  } 
}
