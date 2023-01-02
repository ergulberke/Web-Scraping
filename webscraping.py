from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv
import random
import pandas as pd

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QToolTip
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt 

class Window2(QMainWindow):      
         def __init__(self):
            super().__init__()
            self.setWindowTitle("Product Comments")

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        content2=QtWidgets.QLabel(self)
        content2.setPixmap(QtGui.QPixmap("hepsiburadalogo2.png"))
        
        content2.move(300,100)
        content2.resize(587,100)

        
        
        
        self.setMinimumSize(QSize(1200, 800))    
        self.setWindowTitle("Comment Analyzer") 

        self.nameLabel = QLabel(self)
        
        self.nameLabel.setText('Link:')
        self.line = QLineEdit(self)

        self.line.move(250, 230)
        self.line.resize(700, 40)
        self.nameLabel.move(190, 232)
        

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(250,40)
        pybutton.move(455, 290)        
        
    def clickMethod(self):
        print("Your Link is: " +self.line.text())
        
        
        self.main_window()

    def main_window(self):
        
        self.label = QLabel("Manager", self)
        self.label.move(285, 175)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()
        

    def window2(self):                                           
        
        
        self.w = Window2()
        
        self.w.show()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 18pt;}")
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )


ser = Service("D:\driver\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

# link = input("Hepsiburada Ürün Linkini Giriniz Örnek:https://www.hepsiburada.com/lenovo-lp1-livepods-tws-kablosuz-bluetooth-kulaklik-ithalatci-garantilidir-p-hbv00000xbds6")
link = "https://www.hepsiburada.com/taotronics-soundliberty-94-sarj-kilifli-dort-mikrofonlu-aktif-gurultu-engelleyicili-usb-c-bluetooth-kulaklik-32-saat-muzik-p-HBV00000YDZZ3"
time.sleep(1)
driver.get(link+"-yorumlari")
time.sleep(1)


# browser.close()


kabul = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
driver.execute_script("arguments[0].click();", kabul)

content = driver.find_elements(By.CSS_SELECTOR, '.paginationContentHolder')
sayilar = driver.find_elements(By.CSS_SELECTOR, '.paginationBarHolder')


hepsiburada = driver.page_source
hepsiburada_soup = BeautifulSoup(hepsiburada, "lxml")

hepsiburada_bilgiler = hepsiburada_soup.find(
    "div", attrs={"class": "hermes-Comments-module-kV6VmHxTOAz2NZN1JIxw"})


hepsiburada_bilgiler

sayilar = hepsiburada_bilgiler.find(
    "div", attrs={"class": "paginationBarHolder"})

sayidetaylari = sayilar.find(
    "div", attrs={"class": "hermes-MobilePageHolder-module-NcTGvZxwUbL_zG_85m_B"}).text

sayi = sayidetaylari.split('/')

sayfasayisi = int(sayi[1])

print(sayfasayisi)

count = 0
random = str(random.randint(0, 1000))
rowContent = []
adlar = []
tarihler = []
aciklamalar = []
saticilar = []
begenmeler = []

for i in range(sayfasayisi):
    i = i+1
    a = str(i)
    count = count + 1

    driver.get(link+"-yorumlari?sayfa=" + a)
    print(link)
    print(driver.current_url)
    if (link+"-yorumlari" == driver.current_url):
        driver.close()
        message = "Tarayıcı Kapatıldı ve Yorumlar CSV Dosyasına Yazıldı"
        break

    else:

        hepsiburada = driver.page_source
        hepsiburada_soup = BeautifulSoup(hepsiburada, "lxml")

        hepsiburada_bilgiler = hepsiburada_soup.find(
            "div", attrs={"class": "hermes-Comments-module-kV6VmHxTOAz2NZN1JIxw"})

        yorumlar = hepsiburada_bilgiler.find(
            "div", attrs={"class": "paginationContentHolder"})

        yorumdetaylari = yorumlar.find_all("div", attrs={"itemprop": "review"})

        product_name = hepsiburada_bilgiler.find("h1").text
        average_star = hepsiburada_bilgiler.find(
            "span", attrs={"itemprop": "ratingValue"}).text

        for yorum in yorumdetaylari:

            yorum_adlari = yorum.find_all(
                "div", attrs={"class": "hermes-ReviewCard-module-smSufrjDnuVpMaizDCFn"})
            yorum_tarihleri = yorum.find_all(
                "div", attrs={"class": "hermes-ReviewCard-module-ba888_vGEW2e_XKxTgdA"})
            yorum_aciklamalari = yorum.find_all(
                "div", attrs={"class": "hermes-ReviewCard-module-KaU17BbDowCWcTZ9zzxw"})
            yorum_saticilari = yorum.find_all(
                "div", attrs={"class": "hermes-ReviewCard-module-KmAp6RGZFgoRuElVHoHy"})
            yorum_begenmeleri = yorum.find_all(
                "div", attrs={"class": "hermes-ReviewCard-module-PIYjivsoZ80VfkdrlGgg"})

            for i in yorum_adlari:
                ad = i.find("strong", attrs={"data-testid": "title"}).text
                rowContent.append(str(ad))
                adlar.append(ad)

            for i in yorum_tarihleri:
                tarih = i.find(
                    "span", attrs={"class": "hermes-ReviewCard-module-WROMVGVqxBDYV9UkBWTS"}).text
                rowContent.append(str(tarih))
                tarihler.append(tarih)

            for i in yorum_aciklamalari:
                try:
                    aciklama = i.find(
                        "span", attrs={"itemprop": "description"}).text
                    rowContent.append(str(aciklama))
                    aciklamalar.append(aciklama)
                except:
                    continue

            for i in yorum_saticilari:
                satici = i.find(
                    "span", attrs={"class": "hermes-ReviewCard-module-_yfz1l8ZrCQDTEOSHbzQ"}).text
                rowContent.append(str(satici))
                saticilar.append(satici)

            for i in yorum_begenmeleri:
                begenme_sayisi = i.find(
                    "div", attrs={"class": "hermes-ReviewCard-module-X2QyqJuzO3qbXSWF8zHK"}).text
                rowContent.append(str(begenme_sayisi))
                begenmeler.append(begenme_sayisi)
                print("Ad:" + ad + "|Tarih:" + tarih + "|Yorum:" + aciklama +
                      "|Satıcı:" + satici + "|Yorum Beğenilme Sayısı:" + begenme_sayisi)
                print("---------------------")

    dictionary = {'Adlar': adlar, 'Tarihler': tarihler,
                  'Yorumlar': aciklamalar, 'Satıcı': saticilar, 'Begenme': begenmeler}
    df = pd.DataFrame.from_dict(dictionary, orient='index')
    df = df.transpose()
    to_csv = df.to_csv(f"./yorumlar{random}.csv")

print(len(adlar))
print(len(tarihler))
print(len(aciklamalar))
print(len(saticilar))
print(len(begenmeler))
print(count)
