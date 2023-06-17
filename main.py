from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json


url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2/"
keywords = ["Django", "django", "Flask", "flask"]

# Run the driver

options = Options()
# options.page_load_strategy = 'eager' for fast check, dowloads only 20 div
options.page_load_strategy = "normal"

try:
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    vacancys = driver.find_elements(By.CLASS_NAME, "vacancy-serp-item__layout")
    vac_list = {}
    vac_list["vacancy"] = []
    for vacancy in vacancys:
        vacancy_string = {}
        vacancy_name = vacancy.find_element(By.CLASS_NAME, "serp-item__title").text
        for keyword in keywords:
            if keyword in vacancy_name:
                vacancy_string["name"] = vacancy_name

                try:
                    salary_array = vacancy.find_element(
                        By.CSS_SELECTOR, "span.bloko-header-section-3"
                    ).text
                    salary_array = salary_array.replace("\u202f", " ")
                    vacancy_string["salary_array"] = salary_array
                except Exception as ex:
                    salary_array = "Не указана"
                    vacancy_string["salary_array"] = salary_array
                company_name = vacancy.find_element(
                    By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-employer"]'
                ).text
                town = vacancy.find_element(
                    By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-address"]'
                ).text
                vacancy_string["company"] = company_name
                vacancy_string["town"] = town
                vac_list["vacancy"].append(vacancy_string)
    print(vac_list)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
with open("data.txt", "w", encoding='Utf-8') as outfile:
    json.dump(vac_list, outfile, indent=4, ensure_ascii=False,)
