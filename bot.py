from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import random
import datetime
from utils import log_message
import tkinter as tk

# service = Service("chromedriver/chromedriver.exe")
# driver = None

service = Service("C:/Users/inigu/Documents/ProyectosPersonales/IgBot/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)
stop_bot = False



def login_instagram(usuario, contraseña, log_message, text_log):
    global driver
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.instagram.com")
    time.sleep(3)
    
    # Aceptar cookies si es necesario
    try:
        accept_cookies = driver.find_element(By.XPATH, "//button[text()='Accept All']")
        accept_cookies.click()
        time.sleep(2)
    except Exception as e:
        log_message(text_log, "No se encontró el botón de cookies o ya está aceptado.")

    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    
    username.send_keys(usuario)
    password.send_keys(contraseña)
    password.send_keys(Keys.RETURN)
    
    time.sleep(5)

def comentar_publicacion(url, n_comentarios, comentarios, log_message, text_log):
    global stop_bot
    driver.get(url)
    time.sleep(5)
    
    for i in range(n_comentarios):
        if stop_bot:
            return
        comentario = random.choice(comentarios)
        
        try:
            # Asegurarse de que el campo de comentario está visible
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            comment_area = driver.find_element(By.CSS_SELECTOR, "textarea")
            comment_area.click()
            time.sleep(2)
            comment_area.send_keys(comentario)
            time.sleep(2)
            
            # Simular la tecla Enter para enviar el comentario
            comment_area.send_keys(Keys.RETURN)
            time.sleep(2)
            
            # Verificar si el comentario fue enviado
            retries = 0
            while comment_area.get_attribute('value') != '' and retries < 5:
                comment_area.send_keys(Keys.RETURN)
                time.sleep(2)
                retries += 1
            
            # Esperar unos segundos entre comentarios
            time.sleep(random.randint(2, 6))  

        except Exception as e:
            log_message(text_log, f"Error al comentar: {e}")
            continue
        
        log_message(text_log, f"Comentario {i+1} publicado!")

def iniciar_bot(entry_usuario, entry_contrasena, entry_url, entry_num_comentarios, entry_intervalo, comentarios, log_message, text_log):
    global stop_bot
    usuario = entry_usuario.get()
    contraseña = entry_contrasena.get()
    publicacion_url = entry_url.get()
    n_comentarios = int(entry_num_comentarios.get())
    intervalo = int(entry_intervalo.get()) * 60

    if usuario and contraseña and publicacion_url and comentarios and n_comentarios > 0 and intervalo > 0:
        stop_bot = False
        login_instagram(usuario, contraseña, log_message, text_log)
        while not stop_bot:
            comentar_publicacion(publicacion_url, n_comentarios, comentarios, log_message, text_log)
            if stop_bot:
                return
            log_message(text_log, f"--------------- Se han realizado {n_comentarios} comentarios ---------------")
            log_message(text_log, f"Esperando {intervalo // 60} minutos para continuar...")

            proximaHora = (datetime.datetime.now() + datetime.timedelta(seconds=intervalo)).strftime("%H:%M:%S")
            log_message(text_log, "Se volverá a comentar a las " + proximaHora)

            time.sleep(intervalo)  # Esperar el intervalo especificado
    else:
        log_message(text_log, "Campos incompletos, por favor revise los datos ingresados.")

def detener_bot(log_message, text_log):
    global stop_bot
    stop_bot = True
    if driver:
        driver.quit()
    log_message(text_log, "Bot detenido.")

def agregar_comentario(entry_comentario, comentarios, listbox_comentarios):
    comentario = entry_comentario.get()
    if comentario:
        comentarios.append(comentario)
        listbox_comentarios.insert(tk.END, comentario)
        entry_comentario.delete(0, tk.END)

def eliminar_comentario(comentarios, listbox_comentarios):
    selected_indices = listbox_comentarios.curselection()
    for index in selected_indices[::-1]:
        listbox_comentarios.delete(index)
        del comentarios[index]
