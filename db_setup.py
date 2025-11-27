import sqlite3
import os

def criar_banco_de_dados():
    db_path = 'condominio_moderno.db'
    
    # Remove o banco antigo para evitar conflitos de estrutura
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("Banco antigo removido para atualização da estrutura.")
        except:
            print("Aviso: Não foi possível remover o banco antigo automaticamente. Exclua manualmente se houver erros.")

    print(f"Conectando a {db_path}...")
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("Criando tabelas...")

    # 1. Unidades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bloco TEXT NOT NULL,
            numero TEXT NOT NULL,
            UNIQUE(bloco, numero)
        );
    """)

    # 2. Pessoas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT,
            tipo TEXT NOT NULL,
            unidade_id INTEGER,
            FOREIGN KEY (unidade_id) REFERENCES unidades(id) ON DELETE SET NULL
        );
    """)

    # 3. Veículos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            modelo TEXT NOT NULL,
            cor TEXT,
            pessoa_id INTEGER NOT NULL,
            FOREIGN KEY (pessoa_id) REFERENCES pessoas(id) ON DELETE CASCADE
        );
    """)
    
    # 4. Áreas Comuns (Salão de Festas, Churrasqueira, etc.)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS areas_comuns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );
    """)
    # Inserir algumas áreas padrão
    cursor.executemany("INSERT OR IGNORE INTO areas_comuns (nome) VALUES (?)", 
                       [('Salão de Festas',), ('Churrasqueira',), ('Quadra de Esportes',)])

    # 5. Reservas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id INTEGER NOT NULL,
            pessoa_id INTEGER NOT NULL,
            data_reserva TEXT NOT NULL, -- Formato YYYY-MM-DD
            status TEXT DEFAULT 'Confirmada',
            FOREIGN KEY (area_id) REFERENCES areas_comuns(id),
            FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
        );
    """)

    # 6. Financeiro
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL, -- 'Receita' ou 'Despesa'
            data_vencimento TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente' -- 'Pago', 'Pendente'
        );
    """)

    conexao.commit()
    conexao.close()
    print("Banco de dados completo criado com sucesso!")

if __name__ == "__main__":
    criar_banco_de_dados()