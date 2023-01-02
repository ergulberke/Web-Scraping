from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'HepsiBurada Comment Analyzer'
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 800
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        content2=QLabel(self)
        content2.setPixmap(QPixmap("./hepsiburadalogo2.png"))

        content2.move(300,100)
        content2.resize(587,100)
        
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(275, 250)
        self.textbox.resize(560,40)
        
        # Create a button in the window
        self.button = QPushButton('Yorumları Getir', self)
        self.button.move(850,250)
        self.button.resize(180,40)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
        
    
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Hepsiburada Comment Analyzer', "Yorumlar Getiriliyor Lütfen Açılan Pencereyi Kapatmayın ve Hiçbir Şeye Tıklamayın Yorumlar Csv Olarak Kaydedilecektir", QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")
        link = textboxValue
        
        ser = Service("./chromedriver.exe")
        op = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ser, options=op)

        # link = input("Hepsiburada Ürün Linkini Giriniz Örnek:https://www.hepsiburada.com/lenovo-lp1-livepods-tws-kablosuz-bluetooth-kulaklik-ithalatci-garantilidir-p-hbv00000xbds6")

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



        sayilar = hepsiburada_bilgiler.find(
            "div", attrs={"class": "paginationBarHolder"})

        sayidetaylari = sayilar.find(
            "div", attrs={"class": "hermes-MobilePageHolder-module-NcTGvZxwUbL_zG_85m_B"}).text

        sayi = sayidetaylari.split('/')

        sayfasayisi = int(sayi[1])

        print(sayfasayisi)

        count = 0
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


            dictionary = {'Adlar': adlar, 'Tarihler': tarihler,
                        'Yorumlar': aciklamalar, 'Satıcı': saticilar, 'Begenme': begenmeler}
            df = pd.DataFrame.from_dict(dictionary, orient='index')
            df = df.transpose()
            to_csv = df.to_csv(f"./yorumlar.csv")



        print(len(adlar))
        print(len(tarihler))
        print(len(aciklamalar))
        print(len(saticilar))
        print(len(begenmeler))
        print(count)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


