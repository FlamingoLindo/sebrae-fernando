import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv

load_dotenv()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

driver.get('https://sebraetecprestadora.sebrae-sc.com.br/index.php/site/login')

cookies = wait.until(EC.presence_of_element_located((By.ID, 'onetrust-close-btn-container')))
cookies.click()

cnpj_input = driver.find_element(By.ID, 'loginform-nr_cnpj')
cnpj_input.send_keys(os.getenv('LOGIN'))

password_input = driver.find_element(By.ID, 'loginform-password')
password_input.send_keys(os.getenv('PASSWORD'))

password_input.submit()

menu_btn = wait.until(EC.presence_of_element_located((By.ID, 'display-menu')))
menu_btn.click()

projects_opt = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#1123']")))
projects_opt.click()

proposals_opt = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="1123"]/div/a[4]/span')))
proposals_opt.click()

while True:
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="formulario"]/div/div[2]/button')))
    
    folder_icons = driver.find_elements(By.CLASS_NAME, 'fa-folder-open')
    folder_count = len(folder_icons)
    
    for i in range(folder_count):
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="formulario"]/div/div[2]/button')))

        demands = driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
        print(demands[i].text)
        
        folder_icons = driver.find_elements(By.CLASS_NAME, 'fa-folder-open')
        
        folder_icons[i].click()
        
        clients_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalidade"]/ul/li[3]/a')))
        clients_btn.click()
        
        eye_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="w1"]/table/tbody/tr/td[5]/a')))
        eye_icon.click()
        
        legal_repre = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/legend')))
        ActionChains(driver).scroll_to_element(legal_repre).perform()
        
        re_name = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[1]/div/input'))).get_attribute("value")
        print(re_name)

        position = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[2]/div[1]/input').get_attribute("value")
        print(position)
        
        cpf = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[2]/div[2]/input').get_attribute("value")
        print(cpf)
        
        email = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[3]/div[1]/input').get_attribute("value")
        print(email)
        
        telephone = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[3]/div[2]/input').get_attribute("value")
        print(telephone)
        
        cellphone = driver.find_element(By.XPATH, '//*[@id="modal-2"]/div/div/div/div/fieldset[3]/div[4]/div/input').get_attribute("value")
        print(cellphone)
        
        print('\n')
        print(i)
        
        driver.back()

    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="w0"]/ul/li[12]/a')))
    next_btn.click()