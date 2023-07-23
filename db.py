import sqlite3

def iniciar_banco():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()			

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episodios_southpark (
            episodio_id INTEGER PRIMARY KEY,
            link_episodio TEXT,
            titulo TEXT,
            descricao TEXT,
            temporada TEXT,
            n_episodio TEXT,
            data_lancamento TEXT
        )
    ''')

    conn.commit()
    return conn

if __name__ == '__main__':
    iniciar_banco()