from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# WebDriver başlatma
driver = webdriver.Chrome()

# URL'yi açma
driver.get("https://ru.osiris-student.nl/onderwijscatalogus/extern/opleiding")

# Biraz bekle (isteğe bağlı)
time.sleep(5)

# Sayfada aşağı kaydırma ve program başlıklarını alma
program_elements = driver.find_elements(By.CSS_SELECTOR, ".program-class")  # Doğru CSS seçiciye göre değiştirilmelidir

# Verileri kaydedeceğimiz liste
collected_data = []

# Her bir program başlığına tıklayarak ders bilgilerini çekme
for program in program_elements:
    try:
        # Programa tıklama
        program.click()
        time.sleep(2)
        
        # Açılır menüde "Study Programme" kısmını bulma ve tıklama
        study_programme_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//xpath-of-study-programme"))
        )
        study_programme_button.click()
        
        # Zorunlu dersleri bulma
        mandatory_courses = driver.find_element(By.XPATH, "//xpath-of-mandatory-courses")
        courses_text = mandatory_courses.text
        
        # Veriyi listeye ekleme
        collected_data.append({
            "programme": program.text,
            "courses": courses_text
        })
        
        # Geri dönme
        driver.back()
        time.sleep(2)
    
    except Exception as e:
        print(f"Veri alınamadı: {e}")
        continue

# CSV'ye veri kaydetme
with open('C:/Users/emirh/Desktop/DOSYALAR/veri_bilimi/scrapping/program_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Programme", "Courses"])  # Başlıklar
    for data in collected_data:
        writer.writerow([data['programme'], data['courses']])

# WebDriver'i kapatma
driver.quit()
