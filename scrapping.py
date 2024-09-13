from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# ChromeDriver yolunu ayarlayın
driver_path = r"C:\Users\emirh\Desktop\DOSYALAR\veri_bilimi\chromedriver-win64\chromedriver.exe"    # ChromeDriver yolunu burada güncelle

# Brave tarayıcı ayarları
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Brave tarayıcının kurulu olduğu yol

# Brave için tarayıcı ayarları oluşturuluyor
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# ChromeDriver ile Brave başlatılıyor
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Hedef siteye gidiliyor
url = "https://ru.osiris-student.nl/onderwijscatalogus/extern/opleiding"
driver.get(url)
time.sleep(5)  # Sayfanın tamamen yüklenmesi için bekleme

# Verileri depolamak için liste oluştur
data = []

# Ana sayfadaki tüm bölümleri bul (Örnek bir class adı; gerçek class adını bulman gerekebilir)
departments = driver.find_elements(By.CLASS_NAME, "panel-link")  # Bölümlerin listelendiği sınıf adı

# Her bir bölümün detayına girip ders bilgilerini çek
for department in departments:
    try:
        # Bölüm linkine tıklamak için
        department.click()
        time.sleep(3)  # Sayfanın yüklenmesini bekle

        # Açılan detay panelinden gerekli bilgileri çek
        title = driver.find_element(By.TAG_NAME, "h1").text
        faculty = driver.find_element(By.XPATH, "//p[contains(text(), 'Faculty:')]").text
        study_points = driver.find_element(By.XPATH, "//p[contains(text(), 'Study points:')]").text

        # Ders programına gitmek için ilgili butonu bulup tıklama
        try:
            study_programme_button = driver.find_element(By.LINK_TEXT, "Study Programme")
            study_programme_button.click()
            time.sleep(3)  # Ders programının açılmasını bekle

            # Dersleri çekme (örneğin, derslerin olduğu bir tabloyu bul)
            courses = driver.find_elements(By.CLASS_NAME, "course-class")  # Derslerin olduğu class adını güncelle
            course_list = [course.text for course in courses]

            # Her dönem için dersleri çekmek gerekebilir
            # Daha detaylı veriler için ilgili elemanları kontrol etmeliyiz
            periods = driver.find_elements(By.CLASS_NAME, "period-class")  # Örnek sınıf adı; güncellenmesi gerekebilir

            # Dönem ve ders bilgilerini kaydet
            period_courses = {}
            for i, period in enumerate(periods):
                period_name = f"Dönem {i+1}"
                period_courses[period_name] = [course.text for course in period.find_elements(By.CLASS_NAME, "course-item")]

            # Bölüm bilgilerini kaydet
            data.append({
                "Bölüm Adı": title,
                "Fakülte": faculty,
                "Kredi": study_points,
                "Dersler": course_list,
                **period_courses
            })
        except Exception as e:
            print(f"Ders programına erişilemedi: {e}")

        # Detay sayfasını kapatıp ana sayfaya dönmek
        driver.back()
        time.sleep(2)  # Ana sayfanın yüklenmesi için bekleme
    except Exception as e:
        print(f"Bölüm detaylarına erişilemedi: {e}")

# Verileri bir DataFrame'e dönüştürme ve Excel'e kaydetme
df = pd.DataFrame(data)
df.to_excel("bolumler.xlsx", index=False)
print("Veriler Excel dosyasına kaydedildi.")

# Tarayıcıyı kapatma
driver.quit()
