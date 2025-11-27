# 🏢 SGC Alegria v3.1 - Sistema de Gestão Condominial

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![CustomTkinter](https://img.shields.io/badge/Interface-CustomTkinter-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Concluído-success)

## 📖 Sobre o Projeto
O **Alegria v3.1** é uma aplicação desktop desenvolvida para simplificar a administração de condomínios. Construído inteiramente em Python, o sistema foca em ser leve, rápido e fácil de utilizar, sem necessidade de servidores complexos ou conexão constante com a internet.

Esta versão 3.1 traz uma interface moderna (Dark Mode) construída com **CustomTkinter** e otimização no banco de dados SQLite.

---

## 📸 Capturas de Tela
<div align="center">
  <img width="1279" height="751" alt="Tela de Moradores" src="https://github.com/user-attachments/assets/2384d8ea-f6d2-43d0-8849-2489da4c6d89" />
  <br><br>
  <img width="1280" height="746" alt="Tela de Veículos" src="https://github.com/user-attachments/assets/b3c2712c-9e0f-4391-ac39-3c4cf5336b6d" />
  <br><br>
  <img width="1273" height="748" alt="Tela de Reservas" src="https://github.com/user-attachments/assets/3565fa72-b8c7-4823-9e14-8d05e435cd46" />
  <br><br>
  <img width="1283" height="745" alt="Tela Financeiro" src="https://github.com/user-attachments/assets/960436fa-7158-41df-9e49-aaf7f5a6cd7d" />
</div>

---

## 🚀 Funcionalidades
* **👥 Gestão de Moradores:** Cadastro completo (CPF, Telefone, Unidade) e distinção entre proprietários e inquilinos.
* **🚗 Controle de Veículos:** Associação de veículos aos moradores com placa, modelo e cor.
* **📅 Reservas de Áreas:** Agendamento de espaços comuns (Salão de festas, Churrasqueira, Quadra) com status de aprovação.
* **💰 Controle Financeiro:** Registro de receitas e despesas com datas de vencimento e status de pagamento.
* **🎨 Interface Moderna:** Layout escuro (Dark Mode) nativo e responsivo.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** [Python 3](https://www.python.org/)
* **GUI:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (UI Moderna)
* **Banco de Dados:** SQLite3 (Nativo)

## 📂 Estrutura do Projeto
* `main_app.py`: Interface gráfica principal e lógica de eventos.
* `models.py`: Regras de negócio e operações CRUD no banco de dados.
* `conexao.py`: Gerenciamento da conexão com o SQLite.
* `db_setup.py`: Script de inicialização para criar as tabelas automaticamente.

---

## 📦 Como Baixar e Executar

Siga os passos abaixo para rodar o projeto na sua máquina:

### 1. Clonar o Repositório
Abra o terminal e clone o projeto:
```bash
git clone [https://github.com/brunnodev50/alegria-sgc-python.git](https://github.com/brunnodev50/alegria-sgc-python.git)
