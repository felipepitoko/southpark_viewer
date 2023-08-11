from player import Player
from db import iniciar_banco
from datetime import datetime

def get_todos_episodios():
    try:
        db = iniciar_banco()
        cursor = db.cursor()
        cursor.execute("""SELECT *,  STRFTIME('%Y-%m-%d', SUBSTR(data_lancamento, 7) || '-' || SUBSTR(data_lancamento, 4, 2) || '-' || SUBSTR(data_lancamento, 1, 2)) AS date_column
        from episodios_southpark
        where date_column >= '1997-08-13'
        order by date_column asc""")

        rows = cursor.fetchall()        
        resultado = [dict(item) for item in rows]

        return resultado
                    
    except Exception as e:
        """"""

def get_one_episode_info(temporada:str,n_episodio:str)->str:
    try:
        db = iniciar_banco()
        cursor = db.cursor()
        cursor.execute(f"""SELECT *,  STRFTIME('%Y-%m-%d', SUBSTR(data_lancamento, 7) || '-' || SUBSTR(data_lancamento, 4, 2) || '-' || SUBSTR(data_lancamento, 1, 2)) AS date_column
        from episodios_southpark
        where temporada = '{temporada}' and n_episodio = '{n_episodio}'
        """)

        row = cursor.fetchone()     
        return dict(row)
    except Exception as e:
        print(e)

def atualizar_historico(ultimo_ep:str):
    try:
        current_datetime = datetime.now()
        formatted_date_time = current_datetime.strftime("%d/%m/%Y %H:%M")

        db = iniciar_banco()
        cursor = db.cursor()
        cursor.execute(f"""DELETE FROM historico_episodios""")
        db.commit()
        
        cursor.execute(f"""INSERT INTO historico_episodios (ultimo_ep,data_hora)
        VALUES ('{ultimo_ep}', '{formatted_date_time}')""")

        db.commit() 
        db.close()                   
    except Exception as e:
        print('Banco:',e)
        """"""

def get_ultimo_ep_assistido()->str:
    try:
        db = iniciar_banco()
        cursor = db.cursor()
        cursor.execute("""SELECT *
        FROM historico_episodios
        order by historico_id desc""")

        rows = cursor.fetchall()        
        resultado = [dict(item) for item in rows][0]
        historico = f"{resultado['data_hora']}: {resultado['ultimo_ep']}"
        return historico
                    
    except Exception as e:
        """"""
        return None

#2002-04-10

# db = iniciar_banco()
# cursor = db.cursor()
# cursor.execute("""SELECT link_episodio, temporada, n_episodio, STRFTIME('%Y-%m-%d', SUBSTR(data_lancamento, 7) || '-' || SUBSTR(data_lancamento, 4, 2) || '-' || SUBSTR(data_lancamento, 1, 2)) AS date_column
# from episodios_southpark
# where date_column >= '2002-07-10'
# order by date_column asc""")
# rows = cursor.fetchall()
# print('Achei tantos',len(rows))
# count = 1
# for row in rows:
# #     row = dict(row)
#     temporada = row['temporada']
# #     n_episodio = row['n_episodio']
# #     cursor.execute(f"""UPDATE episodios_southpark set ordem_episodio={count}
# # where temporada ='{temporada}' and n_episodio='{n_episodio}'""")
# #     count +=1
# #     db.commit()
#     row = dict(row)
#     #https://www.southparkstudios.com.br/episodios/7ux3j6/south-park-semana-do-saco-cheio-temporada-26-ep-6
#     player = Player(row['link_episodio'],100,'chrome')
#     # tela = player._iniciar_navegador()
#     player.executar_video()


# result = get_todos_episodios()
# print(result)