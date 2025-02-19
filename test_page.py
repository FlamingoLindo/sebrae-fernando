import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from dotenv import load_dotenv
import time

load_dotenv()

def save_data():
    df = pd.DataFrame(data, columns=["Demanda", "Nome", "Cargo", "CPF", "E-mail", "Telefone", "Celular"])
    df.to_excel("sebraetecprestadora.xlsx", index=False)
    print("Data saved to sebraetecprestadora.xlsx")

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

driver.get('https://sebraetecprestadora.sebrae-sc.com.br/index.php/site/login')

# Accept cookies
cookies = wait.until(EC.presence_of_element_located((By.ID, 'onetrust-close-btn-container')))
cookies.click()

# Login
cnpj_input = driver.find_element(By.ID, 'loginform-nr_cnpj')
cnpj_input.send_keys(os.getenv('LOGIN'))

password_input = driver.find_element(By.ID, 'loginform-password')
password_input.send_keys(os.getenv('PASSWORD'))
password_input.submit()

# Navigate to proposals
menu_btn = wait.until(EC.presence_of_element_located((By.ID, 'display-menu')))
menu_btn.click()

projects_opt = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#1123']")))
projects_opt.click()

proposals_opt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1123"]/div/a[4]/span')))
proposals_opt.click()

# Data storage
data = []

while True:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="formulario"]/div/div[2]/button')))
        folder_icons = driver.find_elements(By.CLASS_NAME, 'fa-folder-open')
        demands = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
        
        for i in range(len(folder_icons)):
            try:
                folder_icons = driver.find_elements(By.CLASS_NAME, 'fa-folder-open')
                demands = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
                
                demand_text = demands[i].text
                print(f'{demand_text} - {i + 1}/{len(folder_icons)}')
                
                folder_icons[i].click()
                
                attempts = 0
                while attempts < 3:
                    try:
                        clients_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modalidade"]/ul/li[3]/a')))
                        clients_btn.click()
                        break
                    except TimeoutException:
                        print("Clients button not found, refreshing page...")
                        driver.refresh()
                        time.sleep(3)
                        attempts += 1
                
                eye_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="w1"]/table/tbody/tr/td[5]/a')))
                eye_icon.click()
                
                legal_repre = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/legend')))
                
                re_name = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[1]/div/input').get_attribute("value")
                position = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[2]/div[1]/input').get_attribute("value")
                cpf = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[2]/div[2]/input').get_attribute("value")
                email = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[3]/div[1]/input').get_attribute("value")
                telephone = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[3]/div[2]/input').get_attribute("value")
                cellphone = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[4]/div/input').get_attribute("value")

                data.append([demand_text, re_name, position, cpf, email, telephone, cellphone])

                driver.back()
                
            except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
                print(f"Skipping an element due to error: {e}")
                continue

        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="w0"]/ul/li[@class="next"]/a')))
            next_btn.click()
            time.sleep(2)
        except:
            break
    
    except Exception as e:
        print(f"Script encountered an error: {e}")
        save_data()
        break

save_data()
driver.quit()