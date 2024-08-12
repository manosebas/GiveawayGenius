import tkinter as tk
from tkinter import messagebox, scrolledtext
from bot import iniciar_bot, detener_bot, agregar_comentario, eliminar_comentario
import threading
from utils import log_message

# Variables globales
comentarios = []
usuario = ""
contraseña = ""
publicacion_url = ""
n_comentarios = 0
intervalo = 0
stop_bot = False
driver = None

def iniciar_gui():
    global comentarios, usuario, contraseña, publicacion_url, n_comentarios, intervalo, stop_bot, driver

    # Interfaz gráfica
    root = tk.Tk()
    root.title("Instagram Bot")

    # Frame para inicio de sesión
    frame_inicio_sesion = tk.Frame(root)
    frame_inicio_sesion.pack(padx=10, pady=10)

    tk.Label(frame_inicio_sesion, text="Usuario:").grid(row=0, column=0)
    entry_usuario = tk.Entry(frame_inicio_sesion)
    entry_usuario.grid(row=0, column=1)

    tk.Label(frame_inicio_sesion, text="Contraseña:").grid(row=1, column=0)
    entry_contrasena = tk.Entry(frame_inicio_sesion, show="*")
    entry_contrasena.grid(row=1, column=1)

    tk.Label(frame_inicio_sesion, text="URL de la publicación:").grid(row=2, column=0)
    entry_url = tk.Entry(frame_inicio_sesion)
    entry_url.grid(row=2, column=1)

    btn_siguiente = tk.Button(frame_inicio_sesion, text="Siguiente", command=lambda: frame_comentarios.pack())
    btn_siguiente.grid(row=3, columnspan=2)

    # Frame para comentarios
    frame_comentarios = tk.Frame(root)
    frame_comentarios.pack_forget()

    tk.Label(frame_comentarios, text="Agregar Comentario:").grid(row=0, column=0)
    entry_comentario = tk.Entry(frame_comentarios)
    entry_comentario.grid(row=0, column=1)
    btn_agregar_comentario = tk.Button(frame_comentarios, text="Agregar", command=lambda: agregar_comentario(entry_comentario, comentarios, listbox_comentarios))
    btn_agregar_comentario.grid(row=0, column=2)

    btn_eliminar_comentario = tk.Button(frame_comentarios, text="Eliminar", command=lambda: eliminar_comentario(comentarios, listbox_comentarios))
    btn_eliminar_comentario.grid(row=0, column=3)

    listbox_comentarios = tk.Listbox(frame_comentarios)
    listbox_comentarios.grid(row=1, columnspan=4)

    tk.Label(frame_comentarios, text="Número de comentarios:").grid(row=2, column=0)
    entry_num_comentarios = tk.Entry(frame_comentarios)
    entry_num_comentarios.grid(row=2, column=1)

    tk.Label(frame_comentarios, text="Repetición en minutos:").grid(row=3, column=0)
    entry_intervalo = tk.Entry(frame_comentarios)
    entry_intervalo.grid(row=3, column=1)

    btn_iniciar_bot = tk.Button(frame_comentarios, text="Iniciar Bot", command=lambda: threading.Thread(target=iniciar_bot, args=(entry_usuario, entry_contrasena, entry_url, entry_num_comentarios, entry_intervalo, comentarios, log_message, text_log)).start())
    btn_iniciar_bot.grid(row=4, columnspan=2)

    btn_detener_bot = tk.Button(frame_comentarios, text="Detener Bot", command=lambda: detener_bot(log_message, text_log))
    btn_detener_bot.grid(row=4, column=2, columnspan=2)

    # Frame de logs
    frame_logs = tk.Frame(root)
    frame_logs.pack(padx=10, pady=10)

    tk.Label(frame_logs, text="Logs:").pack()
    text_log = scrolledtext.ScrolledText(frame_logs, width=50, height=10)
    text_log.pack()

    root.mainloop()
