import sqlite3
from conexao import Conexao

class GestaoCondominioModel:
    def __init__(self):
        self.conn_manager = Conexao()

    # Método auxiliar melhorado para capturar erros reais
    def _execute_query(self, query, params=(), commit=False):
        conexao = self.conn_manager.conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute(query, params)
            if commit:
                conexao.commit()
                return (True, "Operação realizada com sucesso!")
            else:
                result = cursor.fetchall()
                return result
        except sqlite3.IntegrityError as e:
            return (False, f"Erro de Integridade (Duplicidade?): {e}")
        except Exception as e:
            return (False, f"Erro Técnico: {e}")
        finally:
            cursor.close()
            conexao.close()

    # --- PESSOAS ---
    def cadastrar_pessoa_unidade(self, nome, cpf, telefone, tipo_pessoa, bloco, numero):
        # Lógica composta: Verifica unidade -> Cria unidade -> Cria pessoa
        conexao = self.conn_manager.conectar()
        cursor = conexao.cursor()
        try:
            # 1. Busca ou Cria Unidade
            cursor.execute("SELECT id FROM unidades WHERE bloco = ? AND numero = ?", (bloco, numero))
            unidade_data = cursor.fetchone()
            if not unidade_data:
                cursor.execute("INSERT INTO unidades (bloco, numero) VALUES (?, ?)", (bloco, numero))
                unidade_id = cursor.lastrowid
            else:
                unidade_id = unidade_data[0]

            # 2. Cria Pessoa
            cursor.execute("INSERT INTO pessoas (nome, cpf, telefone, tipo, unidade_id) VALUES (?, ?, ?, ?, ?)", 
                           (nome, cpf, telefone, tipo_pessoa, unidade_id))
            conexao.commit()
            return (True, "Cadastro realizado!")
        except sqlite3.IntegrityError:
            return (False, "Erro: CPF já cadastrado.")
        except Exception as e:
            return (False, f"Erro: {e}")
        finally:
            conexao.close()

    def atualizar_pessoa(self, id_pessoa, nome, telefone, tipo, bloco, numero):
        # Lógica composta para atualização
        conexao = self.conn_manager.conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT id FROM unidades WHERE bloco = ? AND numero = ?", (bloco, numero))
            unidade_data = cursor.fetchone()
            if not unidade_data:
                cursor.execute("INSERT INTO unidades (bloco, numero) VALUES (?, ?)", (bloco, numero))
                unidade_id = cursor.lastrowid
            else:
                unidade_id = unidade_data[0]

            cursor.execute("UPDATE pessoas SET nome=?, telefone=?, tipo=?, unidade_id=? WHERE id=?", 
                           (nome, telefone, tipo, unidade_id, id_pessoa))
            conexao.commit()
            return (True, "Pessoa atualizada!")
        except Exception as e:
            return (False, f"Erro ao atualizar: {e}")
        finally:
            conexao.close()

    def buscar_pessoas(self, termo=""):
        sql = """SELECT p.id, p.cpf, p.nome, p.telefone, p.tipo, u.bloco, u.numero
            FROM pessoas p LEFT JOIN unidades u ON p.unidade_id = u.id
            WHERE p.nome LIKE ? OR p.cpf LIKE ? OR u.numero LIKE ? ORDER BY p.nome"""
        busca = f"%{termo}%"
        res = self._execute_query(sql, (busca, busca, busca))
        return res if isinstance(res, list) else []
    
    def excluir_pessoa(self, id_pessoa): 
        return self._execute_query("DELETE FROM pessoas WHERE id=?", (id_pessoa,), commit=True)

    # --- VEÍCULOS ---
    def buscar_veiculos(self, termo=""):
        sql = """SELECT v.id, v.placa, v.modelo, v.cor, p.cpf, p.nome, u.bloco, u.numero 
            FROM veiculos v JOIN pessoas p ON v.pessoa_id = p.id LEFT JOIN unidades u ON p.unidade_id = u.id
            WHERE v.placa LIKE ? OR v.modelo LIKE ? OR p.nome LIKE ?"""
        busca = f"%{termo}%"
        res = self._execute_query(sql, (busca, busca, busca))
        return res if isinstance(res, list) else []

    def cadastrar_veiculo(self, placa, modelo, cor, cpf_dono):
        pessoa = self._execute_query("SELECT id FROM pessoas WHERE cpf=?", (cpf_dono,))
        if not isinstance(pessoa, list) or not pessoa: return (False, "CPF do dono não encontrado.")
        
        return self._execute_query("INSERT INTO veiculos (placa, modelo, cor, pessoa_id) VALUES (?,?,?,?)", 
                                   (placa, modelo, cor, pessoa[0][0]), commit=True)

    def atualizar_veiculo(self, id_veiculo, placa, modelo, cor, cpf_dono):
        pessoa = self._execute_query("SELECT id FROM pessoas WHERE cpf=?", (cpf_dono,))
        if not isinstance(pessoa, list) or not pessoa: return (False, "CPF do dono não encontrado.")
        
        return self._execute_query("UPDATE veiculos SET placa=?, modelo=?, cor=?, pessoa_id=? WHERE id=?", 
                                   (placa, modelo, cor, pessoa[0][0], id_veiculo), commit=True)

    def excluir_veiculo(self, id_veiculo): 
        return self._execute_query("DELETE FROM veiculos WHERE id=?", (id_veiculo,), commit=True)

    # --- RESERVAS ---
    def listar_areas(self): 
        res = self._execute_query("SELECT nome FROM areas_comuns")
        return res if isinstance(res, list) else []

    def buscar_reservas(self, termo=""):
        sql = """SELECT r.id, a.nome, p.cpf, p.nome, r.data_reserva, r.status
            FROM reservas r JOIN areas_comuns a ON r.area_id = a.id JOIN pessoas p ON r.pessoa_id = p.id
            WHERE p.nome LIKE ? OR a.nome LIKE ? OR r.data_reserva LIKE ? ORDER BY r.data_reserva DESC"""
        busca = f"%{termo}%"
        res = self._execute_query(sql, (busca, busca, busca))
        return res if isinstance(res, list) else []

    def criar_reserva(self, nome_area, cpf_pessoa, data, status):
        area = self._execute_query("SELECT id FROM areas_comuns WHERE nome=?", (nome_area,))
        pessoa = self._execute_query("SELECT id FROM pessoas WHERE cpf=?", (cpf_pessoa,))
        if not area or not pessoa: return (False, "Área ou CPF inválidos.")
        
        return self._execute_query("INSERT INTO reservas (area_id, pessoa_id, data_reserva, status) VALUES (?,?,?,?)", 
                                   (area[0][0], pessoa[0][0], data, status), commit=True)

    def atualizar_reserva(self, id_reserva, nome_area, cpf_pessoa, data, status):
        area = self._execute_query("SELECT id FROM areas_comuns WHERE nome=?", (nome_area,))
        pessoa = self._execute_query("SELECT id FROM pessoas WHERE cpf=?", (cpf_pessoa,))
        if not area or not pessoa: return (False, "Dados inválidos.")
        
        return self._execute_query("UPDATE reservas SET area_id=?, pessoa_id=?, data_reserva=?, status=? WHERE id=?", 
                                   (area[0][0], pessoa[0][0], data, status, id_reserva), commit=True)

    def excluir_reserva(self, id_reserva): 
        return self._execute_query("DELETE FROM reservas WHERE id=?", (id_reserva,), commit=True)

    # --- FINANCEIRO ---
    def buscar_financeiro(self, termo=""):
        sql = "SELECT id, descricao, tipo, valor, data_vencimento, status FROM financeiro WHERE descricao LIKE ? OR tipo LIKE ? ORDER BY data_vencimento"
        busca = f"%{termo}%"
        res = self._execute_query(sql, (busca, busca))
        return res if isinstance(res, list) else []

    def cadastrar_financeiro(self, descricao, valor, tipo, data, status):
        return self._execute_query("INSERT INTO financeiro (descricao, valor, tipo, data_vencimento, status) VALUES (?,?,?,?,?)", 
                                   (descricao, valor, tipo, data, status), commit=True)

    def atualizar_financeiro(self, id_fin, descricao, valor, tipo, data, status):
        return self._execute_query("UPDATE financeiro SET descricao=?, valor=?, tipo=?, data_vencimento=?, status=? WHERE id=?", 
                                   (descricao, valor, tipo, data, status, id_fin), commit=True)

    def excluir_financeiro(self, id_fin): 
        return self._execute_query("DELETE FROM financeiro WHERE id=?", (id_fin,), commit=True)