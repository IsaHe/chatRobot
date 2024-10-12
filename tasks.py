from robocorp.tasks import task
from robocorp import browser

from RPA.PDF import PDF
from RPA.Excel.Files import Files
from RPA.Tables import Tables

import os
import socket
import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

pdf = PDF()
exel = Files()
cvs = Tables()

chatbot = "chatgpt"
page = None

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_DRIVER_PATH = "cromeDriver/chromedriver"
PATH_TO_ATATCHMENT_FILE = "output/Respuesta.pdf"

@task
def openChat():
    
    browser.configure(
        slowmo=20000,
    )
    
    prompt = "Continua la siguiente historia sobre robots."
    prompt = preparePromt(prompt)
    
    if chatbot == "copilot":
        aiMessage = copilot(prompt)
        
    if chatbot == "chatgpt":
        aiMessage = chatgpt(prompt)
    
    pdf.html_to_pdf(aiMessage, "output/Respuesta.pdf")

def preparePromt(prompt):
    if not PATH_TO_ATATCHMENT_FILE:
        return prompt
    
    extensionArchivo = os.path.splitext(PATH_TO_ATATCHMENT_FILE)[1].lower()
    textoArchivo = ""
    
    if extensionArchivo == ".pdf":
        textoArchivo = pdf.get_text_from_pdf(PATH_TO_ATATCHMENT_FILE)[1].replace("\n", " ")
    
    if extensionArchivo == ".xlsx":
        exel.open_workbook(PATH_TO_ATATCHMENT_FILE)
        textoArchivo = exel.read_worksheet_as_table(header=True).to_string()
    
    if extensionArchivo == ".csv":
        textoArchivo = cvs.read_table_from_csv(PATH_TO_ATATCHMENT_FILE).to_string()
    
    return prompt + ":" + textoArchivo

def copilot(prompt):
    browser.goto("https://copilot.microsoft.com/?OCID=MA13R8")
    page = browser.page()
    page.fill("#userInput", prompt)
    page.click(".rounded-submitButton")
    aiMessage = page.locator('div[data-content="ai-message"]').inner_html()
    
    return aiMessage

def chatgpt(prompt):
    url = r"https://chat.openai.com"
    
    return abrirChrome(url, prompt)

def abrirChrome(url, prompt):
    puertoDisponible = encontrarPuertoDisponible()
    iniciarChrome(puertoDisponible, url)
    driver = inicializarWebDriver(puertoDisponible)
    esperarVerificacion(driver)
    obtenerCookie(driver)
    enviarPrompt(driver, prompt)
    esperarQueRespuestaTermine(driver)
    respuestaHtml = obtenerRespuesta(driver)
    driver.close()
    driver.quit()
    return respuestaHtml

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

def esperarVerificacion(driver):
    tiempoInicio = time.time()
    tiempoEsperaMax = 60

    while time.time() - tiempoInicio < tiempoEsperaMax:
        elements = driver.find_elements(By.CSS_SELECTOR, 'a.mt-5.cursor-pointer.text-sm.font-semibold.text-token-text-secondary.underline')
        if elements:
            elements[0].click()
            print("Verificado")
            break
        time.sleep(1)
    print("No verificado")

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

def enviarPrompt(driver, prompt):
    textArea = driver.find_element(By.ID, "prompt-textarea")
    textArea.send_keys(prompt)
    textArea.send_keys(Keys.RETURN)

def esperarQueRespuestaTermine(driver): # TODO: Mejorar esto para que funcione correctamente
    start_time = time.time()
    while len(driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')[-1].find_elements(
        by=By.CSS_SELECTOR, value='button.text-token-text-tertiary')) < 1:
        time.sleep(0.5)
        if time.time() - start_time > 60:
            print("Timeout")
            break
    time.sleep(1)

def obtenerRespuesta(driver):
    elements = driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')

    if elements:
        return elements[2].get_attribute('innerHTML')
    else:
        return ""