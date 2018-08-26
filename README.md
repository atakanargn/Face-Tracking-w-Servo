# Face-Tracking-w-Servo
Servo motor ve web kamera ile Raspberry Pi üstünde yüz takibi.
Kod açıklamaları face_track.py dosyası içinde mevcut.

Kodları çektikten sonra, '''pip install opencv_python''' komutunu verip opencv kütüphanesini kurun.

Eğer opencv kütüphanesi ile ilgili hata alırsanız, istediği bağımlılıkları kurarak tekrar deneyin çalışacaktır.

Servo motoru Raspberry Pi 11.pinine bağlayın ve 5v üstünden besleyebilirsiniz.
![Alt text](https://2.bp.blogspot.com/-Gnq_oDQaw5U/W4L98MSkOuI/AAAAAAAAANE/22L4V2jdKiMD-6m_MRiN2ULptbjdiqUawCLcBGAs/s320/raspi_servo.png)

## Kullanım
'''
python3 face_track.py face_default.xml 400 400 0
'''

## Sonuç
Servo motorun üstüne de kamerayı sabitleyin. Ve şöyle bir sonuç elde edeceksiniz;
(gif 10mb olduğundan github yükleyemedi)

https://3.bp.blogspot.com/-qnYdSG_ITls/W4MCBZGIDuI/AAAAAAAAANQ/gO8g2tULpEoTosb0XHR_UJdFK5bV_KOTACLcBGAs/s1600/20180820_225939.gif
