from player import Player
from db import iniciar_banco

db = iniciar_banco()
cursor = db.cursor()
cursor.execute("""SELECT link_episodio, temporada, n_episodio, STRFTIME('%Y-%m-%d', SUBSTR(data_lancamento, 7) || '-' || SUBSTR(data_lancamento, 4, 2) || '-' || SUBSTR(data_lancamento, 1, 2)) AS date_column
from episodios_southpark
where date_column > '2002-04-10'
order by date_column asc""")
rows = cursor.fetchall()

for row in rows:
    row = dict(row)
    #https://www.southparkstudios.com.br/episodios/7ux3j6/south-park-semana-do-saco-cheio-temporada-26-ep-6
    player = Player(row['link_episodio'],100,'chrome')
    # tela = player._iniciar_navegador()
    player.executar_video()