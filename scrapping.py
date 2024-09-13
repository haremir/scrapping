from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ChromeDriver yolunu ayarlayın
driver_path = "D:/Driver/chromedriver.exe"  # ChromeDriver yolunu burada güncelle

# ChromeDriver'ı başlat
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Hedef siteye gidiliyor
url = "https://ru.osiris-student.nl/onderwijscatalogus/extern/opleiding"
driver.get(url)
time.sleep(5)  # Sayfanın tamamen yüklenmesi için bekleme

# Sayfanın tamamen kaydırılmasını sağlamak için
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 1000);")  # Her seferinde 1000 piksel kaydır
        time.sleep(2)  # Kaydırma ve yeni içeriklerin yüklenmesi için bekleme
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_bottom(driver)

# 'font-li-head' class'ına sahip tüm elementleri bulma
elements = driver.find_elements(By.CLASS_NAME, "font-li-head")

# Verileri depolamak için liste oluştur
data = []

# Her bir elementi listeye ekleme (text'ini alarak)
for element in elements:
    text = element.text.strip()  # Boşlukları kaldır
    if text:  # Eğer text boş değilse ekle
        data.append(text)

# Verileri ekrana yazdır
for item in data:
    print(item)

# Tarayıcıyı kapatmadan önce bir süre beklemek
time.sleep(5)

# Tarayıcıyı kapat
driver.quit()
