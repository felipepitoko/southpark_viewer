import tkinter as tk
from tkinter import ttk
import threading
from exec import get_todos_episodios, atualizar_historico, get_ultimo_ep_assistido
from player import Player
import re, time

window = tk.Tk()
window.geometry("600x400")
window.title("Maratonador de South Park")
window.resizable(False, False)

lista_episodios = get_todos_episodios()
lista_nomes_episodios = [f"T{item['temporada']} - E{item['n_episodio']}: {item['titulo']}" for item in lista_episodios]
ultimo_ep_assistido:str = get_ultimo_ep_assistido()

def escolher_episodio(selected_value):
    try:        
        temporada = re.findall(pattern=r"\d+ -", string=selected_value)[0].replace(' -','').strip()
        n_episodio = re.findall(pattern=r"\d:",string=selected_value)[0].replace(':','').strip()
        print('voce quer',temporada,n_episodio)

        episodio_execucao = lista_episodios.copy()

        for episodio in lista_episodios:     

            if episodio['temporada'] == temporada and episodio['n_episodio'] == n_episodio:
                executar_em_serie(episodio_execucao)
                break                

            episodio_execucao.pop(0)
    except Exception as e:
        print(e)

def executar_em_serie(lista_episodios:list):
    print('Vamos assistir',len(lista_episodios))
    for episodio in lista_episodios:
        result_text.set('Assistindo: '+f"T{episodio['temporada']} - E{episodio['n_episodio']}")
        # print('iniciando',episodio)
        player = Player(episodio['link_episodio'],100,'firefox')
        player.executar_video()
        print('Atualizando...')   
        atualizar_historico(f"T{episodio['temporada']} - E{episodio['n_episodio']}: {episodio['titulo']}")
    
def on_option_selected():    
    selected_value = selected_var.get()
    button.config(state=tk.DISABLED)
    # escolher_episodio(selected_value)
    thread = threading.Thread(target=escolher_episodio,args=(selected_value,))
    thread.start()

def on_selected_value(*args):
    selected_value = selected_var.get()
    temporada = re.findall(pattern=r"\d+ -", string=selected_value)[0].replace(' -','').strip()
    n_episodio = re.findall(pattern=r"\d:",string=selected_value)[0].replace(':','').strip()

    for episodio in lista_episodios:     
        if episodio['temporada'] == temporada and episodio['n_episodio'] == n_episodio:
            label_text.set(f"{episodio['descricao']}")

selected_var = tk.StringVar(window)
selected_var.set(None)
selected_var.trace("w", on_selected_value)

prompt_label = tk.Label(window, text="Selecione um episodio por onde comecar")
prompt_label.pack()

dropdown_menu = ttk.Combobox(window, textvariable=selected_var, values=lista_nomes_episodios,width=70)
dropdown_menu.pack()

button = tk.Button(window, text="Iniciar maratona", command=on_option_selected)
button.pack()

label_text = tk.StringVar()
label_1 = tk.Label(window,textvariable=label_text,wraplength=200)
label_1.pack()

label_2_text = tk.StringVar()
label_2 = tk.Label(window,textvariable=label_2_text,wraplength=200)
label_2.pack()                  

result_text = tk.StringVar()
result_label = tk.Label(window,textvariable=result_text,wraplength=200)
result_label.pack()
result_text.set(ultimo_ep_assistido)

window.mainloop()