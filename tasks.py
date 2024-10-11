from robocorp.tasks import task
from robocorp import browser

from RPA.PDF import PDF

import os
import socket
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

prompt = "Dame una historia de amor sobre robots"
pdf = PDF()
chatbot = "chatgpt"
page = None

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_DRIVER_PATH = "cromeDriver/chromedriver"

@task
def openChat():
    browser.configure(
        slowmo=20000,
    )
    
    if chatbot == "copilot":
        aiMessage = copilot()
        
    if chatbot == "chatgpt":
        aiMessage = chatgpt()
    
    pdf.html_to_pdf(aiMessage, "output/Respuesta.pdf")

def copilot():
    browser.goto("https://copilot.microsoft.com/?OCID=MA13R8")
    page = browser.page()
    page.fill("#userInput", prompt)
    page.click(".rounded-submitButton")
    aiMessage = page.locator('div[data-content="ai-message"]').inner_html()
    
    return aiMessage

def chatgpt():
    url = r"https://chat.openai.com"
    
    return abrirChrome(url)

def abrirChrome(url):
    puertoDisponible = encontrarPuertoDisponible()
    iniciarChrome(puertoDisponible, url)
    esperarVerificacion()
    driver = inicializarWebDriver(puertoDisponible)
    obtenerCookie(driver)
    enviarPrompt(driver)
    esperarQueRespuestaTermine(driver)
    return obtenerRespuesta(driver)

def encontrarPuertoDisponible():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def iniciarChrome(puerto, url):
    def abrirChromeEnDebug():
        chromeCmd = f"'{CHROME_PATH}' --remote-debugging-port={puerto} --user-data-dir=remote-profile {url}"
        os.system(chromeCmd)

    threading.Thread(target=abrirChromeEnDebug).start()

def esperarVerificacion():
    time.sleep(60)  # TODO: Mejorar esto para que no sea un tiempo fijo

def inicializarWebDriver(puerto):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.binary_location = CHROME_DRIVER_PATH
    chromeOptions.add_experimental_option("debuggerAddress", f"localhost:{puerto}")
    driver = webdriver.Chrome(options=chromeOptions)
    return driver

def obtenerCookie(driver):    
    cookies = driver.get_cookies()
    session_cookies = [elem for elem in cookies if elem["name"] == '__Secure-next-auth.session-token']
    
    if session_cookies:
        cookie = session_cookies[0]['value']
        return cookie
    else:
        return

def enviarPrompt(driver):
    textArea = driver.find_element(By.ID, "prompt-textarea")
    textArea.send_keys(prompt)
    textArea.send_keys(Keys.RETURN)

def esperarQueRespuestaTermine(driver): # TODO: Mejorar esto para que funcione correctamente
    start_time = time.time()
    while len(driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')[-1].find_elements(
        by=By.CSS_SELECTOR, value='button.text-token-text-tertiary')) < 1:
        time.sleep(0.5)
        if time.time() - start_time > 60:
            break
    time.sleep(1)

def obtenerRespuesta(driver):
    elements = driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')

    if elements:
        return elements[2].get_attribute('innerHTML')
    else:
        return ""