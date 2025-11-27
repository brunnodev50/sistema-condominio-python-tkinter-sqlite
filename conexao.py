# conexao.py
import sqlite3

class Conexao:
    def __init__(self, db_name='condominio_moderno.db'):
        self.db_name = db_name

    def conectar(self):
        conexao = None
        try:
            # detect_types ajuda a lidar com datas se necessário no futuro
            conexao = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            # Importante para integridade referencial
            conexao.execute("PRAGMA foreign_keys = ON;")
        except sqlite3.DatabaseError as err:
            print(f"Erro ao conectar o banco de dados {self.db_name}: {err}")
        return conexao