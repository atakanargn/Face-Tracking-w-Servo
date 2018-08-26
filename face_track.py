#!/usr/bin/python3
#-*-coding:utf-8-*-
# Yazar : Atakan Argın
# 

# OpenCV Kütüphanesi
import cv2
# Argümanlar için kütüphane
from sys import argv
# Raspberry Pi, GPIO pinleri için kütüphane, (General Purpose Input/Output)
import RPi.GPIO as GPIO
# sleep fonksiyonu için kütüphane
from time import sleep
from random import randint

# GPIO pinlerinin yerleşimini seçtik
GPIO.setmode(GPIO.BOARD)
# 11.pin servonun dijital pinine bağlamıştık,
# bu bacağı Output olarak ayarladık
GPIO.setup(11,GPIO.OUT)
# servoDeğer değişkeni, (0,180) arası değerler alır.
# Başlangıç değeri 105 derece.
servoDeger = 105
# servo nesnesi oluşturduk ve 50hz olarak ayarladık
servo=GPIO.PWM(11,50)
# DutyCycle yani Türkçesiyle Görev döngüsünü ayarladık,
# 50hz'de 0-15 arası değer alır,
# Biz girdiğimiz 0-180 arası değeri;
# 1/18 ile çarpıp, 2 ile toplayarak,
# 0-15 arası bir değere dönüştürdük
DutyCycle = 1/18 * (servoDeger) + 2
# servoyu başlattık, ve ilk hareketini verdik
servo.start(DutyCycle)
# hareket etmesi iiçn çok ufak bir süre tanıdık
sleep(0.05)
# 11.pini yani servo pinini temizleyerek,
# servonun takılmasını engelledik,
# sebebini blogta anlatmıştım.
GPIO.cleanup(11)

# servoyu kolayca hareket ettirmek için hazırladığım metod
# 0-180 arası değer alır, int veya float farketmez
def servoOynat(deger):
    # Burada yapılan işlemlerden bahsetmiştik,
    # servoyu her seferinde baştan kurmamın
    # ve baştan hareket ettirmemin sebebini
    # blogumda anlatmıştım.
    DutyCycle = 1/18* (deger) + 2
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.OUT)
    servo=GPIO.PWM(11,50)
    servo.start(DutyCycle)
    sleep(0.05)
    GPIO.cleanup(11)

# python betiğimizi çalıştırırken,
# 1.Argüman : haarscascade yüz modelimizin konumu, face_default.xml gibi
# 2.Argüman : Kamera dikey uzunluğu
# 3.Argüman : Kamera yatay uzunluğu
# 4.Argüman : Kamera index'i,
#       dahili kameraysa varsayılan olarak 0,
#       birden fazlaysa da 0'dan başlayarak deneyebilirsiniz.
cascPath     = argv[1]
cameraWidth  = float(argv[2])
cameraHeight = float(argv[3])
cameraIndex  = int(argv[4])

# Yukarda verdiğimiz, .xml yüz tanıma modelini
# sınıflandırıcı olarak belirledik.
faceCascade   = cv2.CascadeClassifier(cascPath)
# Kamerayı çalıştırdık
video_capture = cv2.VideoCapture(cameraIndex)

# Kameramızın aldığı boyutu,
# önceden verdiğimiz argümanlara göre ayarladık
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH ,cameraWidth)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,cameraHeight)

# Program sürekli çalışsın diye sonsuz döngüye girdik
while True:
    # Kamera açık mı? kontrolü yapalım
    if not video_capture.isOpened():
        # açık değilse, mesaj verip, 3 saniye bekleyelim
        # ve devam edelim
        print('Kamera yuklenemedi!')
        sleep(3)
        pass

    # Kameradan 2 değer okuyoruz biri return değeri, kamera çalışırsa True döndürür.
    # 2. yani frame isimli değer de kameradan aldığımız veri.
    ret, frame = video_capture.read()
    # Kameraya yatay olarak aynalama yaptık.
    frame = cv2.flip(frame,1)
    # Yüz tanıma işlemi için frame verisini,
    # gray verisine griye dönüştürüp atadık
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüz tanıma işlemi burada gerçekleşiyor
    # Önceden oluşturduğumuz faceCascade nesnesinin bir metodu
    # .detectMultiScale()
    # burada önemli olan minSize
    # bu değer algılanacak yüz boyutunun pixel cinsinden değerini belirtir.
    # opencv'nin çok küçük yani arkanızdaki uzak nesneleri denetlemesini
    # istemiyorsanız, bu değerlerle oynayıp deneyebilirsiniz.
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )
    # gelen yüz dizisinde 4 değişken var
    # x = yüzün yatayda 0. koordinatı
    # y = yüzün dikeyda 0. koordinatı
    # w = yüzün yatayda son koordinatı
    # h = yüzün dikeyde son koordinatı
    for (x, y, w, h) in faces:
        # for döngüsü içindeki değerler deneyseldir,
        # ben bu ayarlarla çalıştım,
        # sizde daha farklı olabilir.

        # x değeri 40'tan küçükse yani kameranın sol tarafına çok yakınsak
        if(x<40):
            # servoDeger maximum sınırı 160 derecede sabitledik
            if not(servoDeger>=160):
                # servonun derecesini 3 derece azalttık
                servoDeger-=3
            # servoyu son değere göre oynattık
            servoOynat(servoDeger)
        # servoDeger minimum sınırı 10 derecede sabitledik
        if(x>115):
            if not(servoDeger<=10):
                # servonun derecesini 3 derece arttırdık
                servoDeger+=3
            # servoyu son değere göre oynattık
            servoOynat(servoDeger)
        # koordinatları yüzün üstüne yazdırdık
        cv2.cv2.putText(frame,str(x)+","+str(y), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        # yüzü kırmızı dikdörtgen bir çerçeve içine aldık
        # çerçeve rengi şekilli olsun
        cerceve_renk = (randint(0,255), randint(0,255), randint(0,255))
        cv2.rectangle(frame, (x, y), (x+w, y+h), cerceve_renk, 3)

    # Elde ettiğimiz son görüntüyü ekranda gösterdik
    cv2.imshow('Kamera', frame)
    
    # 'q' tuşuna basılınca betik duracaktır.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Döngüden çıkınca, kamera kapasın
video_capture.release()
# tüm pencereler kapansın
cv2.destroyAllWindows()