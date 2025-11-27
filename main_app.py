import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from models import GestaoCondominioModel

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SistemaCondominioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Condominial - Alegria v3.1")
        self.geometry("1280x720")
        
        self.model = GestaoCondominioModel()
        
        # Variáveis de Estado para Edição (ID ou None)
        self.id_pessoa_edit = None
        self.id_veiculo_edit = None
        self.id_reserva_edit = None
        self.id_fin_edit = None

        # Configuração de Abas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_cadastro = self.tabview.add("Moradores")
        self.tab_veiculos = self.tabview.add("Veículos")
        self.tab_reservas = self.tabview.add("Reservas")
        self.tab_financeiro = self.tabview.add("Financeiro")

        self.setup_tab_cadastro()
        self.setup_tab_veiculos()
        self.setup_tab_reservas()
        self.setup_tab_financeiro()

    # --- UTILITÁRIOS ---
    def formatar_telefone(self, event):
        texto = self.entry_telefone.get()
        limpo = "".join(filter(str.isdigit, texto))[:11]
        novo = ""
        if len(limpo) > 10: novo = f"({limpo[:2]}) {limpo[2:7]}-{limpo[7:]}"
        elif len(limpo) > 6: novo = f"({limpo[:2]}) {limpo[2:6]}-{limpo[6:]}"
        elif len(limpo) > 2: novo = f"({limpo[:2]}) {limpo[2:]}"
        else: novo = limpo
        if self.entry_telefone.get() != novo: self.entry_telefone.delete(0, tk.END); self.entry_telefone.insert(0, novo)

    def formatar_cpf(self, event, entry_widget):
        texto = entry_widget.get()
        limpo = "".join(filter(str.isdigit, texto))[:11]
        novo = ""
        if len(limpo) > 9: novo = f"{limpo[:3]}.{limpo[3:6]}.{limpo[6:9]}-{limpo[9:]}"
        elif len(limpo) > 6: novo = f"{limpo[:3]}.{limpo[3:6]}.{limpo[6:]}"
        elif len(limpo) > 3: novo = f"{limpo[:3]}.{limpo[3:]}"
        else: novo = limpo
        if entry_widget.get() != novo: entry_widget.delete(0, tk.END); entry_widget.insert(0, novo)

    def criar_layout_padrao(self, tab, titulo):
        frame_form = ctk.CTkFrame(tab)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(frame_form, text=titulo, font=("Arial", 18, "bold")).pack(pady=10)
        frame_lista = ctk.CTkFrame(tab)
        frame_lista.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        return frame_form, frame_lista

    def criar_barra_busca(self, parent, comando):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        entry = ctk.CTkEntry(frame, placeholder_text="Pesquisar...")
        entry.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(frame, text="Buscar", width=80, command=comando).pack(side="right", padx=5)
        return entry

    def criar_treeview(self, parent, colunas):
        style = ttk.Style(); style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#3d3d3d", foreground="white", font=('Arial', 10, 'bold'))
        tree = ttk.Treeview(parent, columns=colunas, show='headings')
        for col in colunas: tree.heading(col, text=col); tree.column(col, width=100)
        sb = ctk.CTkScrollbar(parent, command=tree.yview)
        tree.configure(yscrollcommand=sb.set); sb.pack(side="right", fill="y"); tree.pack(side="left", fill="both", expand=True)
        return tree

    def atualizar_tree(self, tree, dados):
        for i in tree.get_children(): tree.delete(i)
        for item in dados: tree.insert('', tk.END, values=[str(val) if val is not None else "-" for val in item])

    # ==========================
    # ABA 1: MORADORES
    # ==========================
    def setup_tab_cadastro(self):
        f_form, f_lista = self.criar_layout_padrao(self.tab_cadastro, "Moradores")
        ctk.CTkLabel(f_form, text="CPF:").pack(anchor="w", padx=10)
        self.p_cpf = ctk.CTkEntry(f_form); self.p_cpf.pack(fill="x", padx=10, pady=5)
        self.p_cpf.bind("<KeyRelease>", lambda e: self.formatar_cpf(e, self.p_cpf))
        ctk.CTkLabel(f_form, text="Nome:").pack(anchor="w", padx=10)
        self.p_nome = ctk.CTkEntry(f_form); self.p_nome.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Telefone:").pack(anchor="w", padx=10)
        self.entry_telefone = ctk.CTkEntry(f_form); self.entry_telefone.pack(fill="x", padx=10, pady=5)
        self.entry_telefone.bind("<KeyRelease>", self.formatar_telefone)
        ctk.CTkLabel(f_form, text="Tipo:").pack(anchor="w", padx=10)
        self.p_tipo = ctk.CTkComboBox(f_form, values=["Proprietário", "Inquilino", "Dependente"]); self.p_tipo.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Bloco / Unidade:").pack(anchor="w", padx=10)
        f_unid = ctk.CTkFrame(f_form, fg_color="transparent"); f_unid.pack(fill="x", padx=10)
        self.p_bloco = ctk.CTkEntry(f_unid, placeholder_text="BL", width=60); self.p_bloco.pack(side="left", padx=(0,5))
        self.p_num = ctk.CTkEntry(f_unid, placeholder_text="APTO", width=80); self.p_num.pack(side="left")

        self.btn_p_save = ctk.CTkButton(f_form, text="Cadastrar", command=self.save_pessoa, fg_color="#2ecc71")
        self.btn_p_save.pack(fill="x", padx=10, pady=(20,5))
        ctk.CTkButton(f_form, text="Editar Selecionado", command=self.edit_pessoa, fg_color="#f39c12").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Limpar", command=self.clear_pessoa, fg_color="#95a5a6").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Excluir", command=self.del_pessoa, fg_color="#e74c3c").pack(fill="x", padx=10, pady=5)

        self.p_busca = self.criar_barra_busca(f_lista, self.buscar_pessoas)
        self.tree_pessoas = self.criar_treeview(f_lista, ('ID', 'CPF', 'Nome', 'Telefone', 'Tipo', 'Bloco', 'Unidade'))
        self.buscar_pessoas()

    def buscar_pessoas(self): self.atualizar_tree(self.tree_pessoas, self.model.buscar_pessoas(self.p_busca.get()))
    
    def edit_pessoa(self):
        sel = self.tree_pessoas.selection()
        if not sel: return messagebox.showwarning("Aviso", "Selecione um registro na lista.")
        val = self.tree_pessoas.item(sel[0])['values']
        
        self.id_pessoa_edit = int(val[0]) # Força conversão para inteiro
        self.p_cpf.delete(0,tk.END); self.p_cpf.insert(0, val[1])
        self.p_nome.delete(0,tk.END); self.p_nome.insert(0, val[2])
        self.entry_telefone.delete(0,tk.END); self.entry_telefone.insert(0, val[3])
        self.p_tipo.set(val[4])
        self.p_bloco.delete(0,tk.END); self.p_bloco.insert(0, val[5] if val[5]!='-' else '')
        self.p_num.delete(0,tk.END); self.p_num.insert(0, val[6] if val[6]!='-' else '')
        self.btn_p_save.configure(text="Salvar Alterações", fg_color="#3498db")

    def save_pessoa(self):
        if not self.p_nome.get() or not self.p_cpf.get(): return messagebox.showerror("Erro", "Nome e CPF obrigatórios")
        
        if self.id_pessoa_edit:
            res = self.model.atualizar_pessoa(self.id_pessoa_edit, self.p_nome.get(), self.entry_telefone.get(), self.p_tipo.get(), self.p_bloco.get().upper(), self.p_num.get())
        else:
            res = self.model.cadastrar_pessoa_unidade(self.p_nome.get(), self.p_cpf.get(), self.entry_telefone.get(), self.p_tipo.get(), self.p_bloco.get().upper(), self.p_num.get())
        
        if res[0]: messagebox.showinfo("Sucesso", res[1]); self.clear_pessoa(); self.buscar_pessoas()
        else: messagebox.showerror("Erro", res[1])

    def clear_pessoa(self):
        self.id_pessoa_edit = None; self.btn_p_save.configure(text="Cadastrar", fg_color="#2ecc71")
        for e in [self.p_cpf, self.p_nome, self.entry_telefone, self.p_bloco, self.p_num]: e.delete(0, tk.END)

    def del_pessoa(self):
        sel = self.tree_pessoas.selection()
        if sel and messagebox.askyesno("Confirmar", "Excluir?"):
            self.model.excluir_pessoa(int(self.tree_pessoas.item(sel[0])['values'][0])); self.buscar_pessoas()

    # ==========================
    # ABA 2: VEÍCULOS
    # ==========================
    def setup_tab_veiculos(self):
        f_form, f_lista = self.criar_layout_padrao(self.tab_veiculos, "Gestão de Veículos")
        ctk.CTkLabel(f_form, text="Placa:").pack(anchor="w", padx=10)
        self.v_placa = ctk.CTkEntry(f_form); self.v_placa.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Modelo:").pack(anchor="w", padx=10)
        self.v_modelo = ctk.CTkEntry(f_form); self.v_modelo.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Cor:").pack(anchor="w", padx=10)
        self.v_cor = ctk.CTkEntry(f_form); self.v_cor.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="CPF do Dono:").pack(anchor="w", padx=10)
        self.v_cpf = ctk.CTkEntry(f_form); self.v_cpf.pack(fill="x", padx=10, pady=5)
        self.v_cpf.bind("<KeyRelease>", lambda e: self.formatar_cpf(e, self.v_cpf))

        self.btn_v_save = ctk.CTkButton(f_form, text="Adicionar Veículo", command=self.save_veiculo, fg_color="#2ecc71")
        self.btn_v_save.pack(fill="x", padx=10, pady=(20,5))
        ctk.CTkButton(f_form, text="Editar Selecionado", command=self.edit_veiculo, fg_color="#f39c12").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Limpar", command=self.clear_veiculo, fg_color="#95a5a6").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Excluir", command=self.del_veiculo, fg_color="#e74c3c").pack(fill="x", padx=10, pady=5)

        self.v_busca = self.criar_barra_busca(f_lista, self.buscar_veiculos)
        self.tree_veiculos = self.criar_treeview(f_lista, ('ID', 'Placa', 'Modelo', 'Cor', 'CPF Dono', 'Nome Dono', 'Bloco', 'Unid'))
        self.buscar_veiculos()

    def buscar_veiculos(self): self.atualizar_tree(self.tree_veiculos, self.model.buscar_veiculos(self.v_busca.get()))

    def edit_veiculo(self):
        sel = self.tree_veiculos.selection()
        if not sel: return messagebox.showwarning("Aviso", "Selecione um veículo.")
        val = self.tree_veiculos.item(sel[0])['values']
        
        self.id_veiculo_edit = int(val[0]) # ID
        self.v_placa.delete(0,tk.END); self.v_placa.insert(0, val[1])
        self.v_modelo.delete(0,tk.END); self.v_modelo.insert(0, val[2])
        self.v_cor.delete(0,tk.END); self.v_cor.insert(0, val[3])
        self.v_cpf.delete(0,tk.END); self.v_cpf.insert(0, val[4])
        self.btn_v_save.configure(text="Salvar Alteração", fg_color="#3498db")

    def save_veiculo(self):
        if self.id_veiculo_edit:
            res = self.model.atualizar_veiculo(self.id_veiculo_edit, self.v_placa.get(), self.v_modelo.get(), self.v_cor.get(), self.v_cpf.get())
        else:
            res = self.model.cadastrar_veiculo(self.v_placa.get(), self.v_modelo.get(), self.v_cor.get(), self.v_cpf.get())
        
        if res[0]: messagebox.showinfo("Sucesso", res[1]); self.clear_veiculo(); self.buscar_veiculos()
        else: messagebox.showerror("Erro", res[1])

    def clear_veiculo(self):
        self.id_veiculo_edit = None; self.btn_v_save.configure(text="Adicionar Veículo", fg_color="#2ecc71")
        for e in [self.v_placa, self.v_modelo, self.v_cor, self.v_cpf]: e.delete(0, tk.END)

    def del_veiculo(self):
        sel = self.tree_veiculos.selection()
        if sel: self.model.excluir_veiculo(int(self.tree_veiculos.item(sel[0])['values'][0])); self.buscar_veiculos()

    # ==========================
    # ABA 3: RESERVAS
    # ==========================
    def setup_tab_reservas(self):
        f_form, f_lista = self.criar_layout_padrao(self.tab_reservas, "Reservas de Áreas")
        ctk.CTkLabel(f_form, text="Área Comum:").pack(anchor="w", padx=10)
        areas = [x[0] for x in self.model.listar_areas()]
        self.r_area = ctk.CTkComboBox(f_form, values=areas if areas else ["Nenhuma"]); self.r_area.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="CPF Solicitante:").pack(anchor="w", padx=10)
        self.r_cpf = ctk.CTkEntry(f_form); self.r_cpf.pack(fill="x", padx=10, pady=5)
        self.r_cpf.bind("<KeyRelease>", lambda e: self.formatar_cpf(e, self.r_cpf))
        ctk.CTkLabel(f_form, text="Data (AAAA-MM-DD):").pack(anchor="w", padx=10)
        self.r_data = ctk.CTkEntry(f_form); self.r_data.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Status:").pack(anchor="w", padx=10)
        self.r_status = ctk.CTkComboBox(f_form, values=["Confirmada", "Pendente", "Cancelada", "Concluída"]); self.r_status.pack(fill="x", padx=10, pady=5)

        self.btn_r_save = ctk.CTkButton(f_form, text="Criar Reserva", command=self.save_reserva, fg_color="#2ecc71")
        self.btn_r_save.pack(fill="x", padx=10, pady=(20,5))
        ctk.CTkButton(f_form, text="Editar Selecionado", command=self.edit_reserva, fg_color="#f39c12").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Limpar", command=self.clear_reserva, fg_color="#95a5a6").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Excluir", command=self.del_reserva, fg_color="#e74c3c").pack(fill="x", padx=10, pady=5)

        self.r_busca = self.criar_barra_busca(f_lista, self.buscar_reservas)
        self.tree_reservas = self.criar_treeview(f_lista, ('ID', 'Área', 'CPF', 'Nome', 'Data', 'Status'))
        self.buscar_reservas()

    def buscar_reservas(self): self.atualizar_tree(self.tree_reservas, self.model.buscar_reservas(self.r_busca.get()))

    def edit_reserva(self):
        sel = self.tree_reservas.selection()
        if not sel: return messagebox.showwarning("Aviso", "Selecione uma reserva.")
        val = self.tree_reservas.item(sel[0])['values']
        
        self.id_reserva_edit = int(val[0])
        self.r_area.set(val[1])
        self.r_cpf.delete(0,tk.END); self.r_cpf.insert(0, val[2])
        self.r_data.delete(0,tk.END); self.r_data.insert(0, val[4])
        self.r_status.set(val[5])
        self.btn_r_save.configure(text="Salvar Alteração", fg_color="#3498db")

    def save_reserva(self):
        if self.id_reserva_edit:
            res = self.model.atualizar_reserva(self.id_reserva_edit, self.r_area.get(), self.r_cpf.get(), self.r_data.get(), self.r_status.get())
        else:
            res = self.model.criar_reserva(self.r_area.get(), self.r_cpf.get(), self.r_data.get(), self.r_status.get())
        
        if res[0]: messagebox.showinfo("Sucesso", res[1]); self.clear_reserva(); self.buscar_reservas()
        else: messagebox.showerror("Erro", res[1])

    def clear_reserva(self):
        self.id_reserva_edit = None; self.btn_r_save.configure(text="Criar Reserva", fg_color="#2ecc71")
        self.r_cpf.delete(0,tk.END); self.r_data.delete(0,tk.END); self.r_status.set("Confirmada")

    def del_reserva(self):
        sel = self.tree_reservas.selection()
        if sel: self.model.excluir_reserva(int(self.tree_reservas.item(sel[0])['values'][0])); self.buscar_reservas()

    # ==========================
    # ABA 4: FINANCEIRO
    # ==========================
    def setup_tab_financeiro(self):
        f_form, f_lista = self.criar_layout_padrao(self.tab_financeiro, "Controle Financeiro")
        ctk.CTkLabel(f_form, text="Descrição:").pack(anchor="w", padx=10)
        self.f_desc = ctk.CTkEntry(f_form); self.f_desc.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Valor (R$):").pack(anchor="w", padx=10)
        self.f_valor = ctk.CTkEntry(f_form); self.f_valor.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Tipo:").pack(anchor="w", padx=10)
        self.f_tipo = ctk.CTkComboBox(f_form, values=["Receita", "Despesa"]); self.f_tipo.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Vencimento:").pack(anchor="w", padx=10)
        self.f_data = ctk.CTkEntry(f_form); self.f_data.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_form, text="Status:").pack(anchor="w", padx=10)
        self.f_status = ctk.CTkComboBox(f_form, values=["Pendente", "Pago", "Atrasado"]); self.f_status.pack(fill="x", padx=10, pady=5)

        self.btn_f_save = ctk.CTkButton(f_form, text="Lançar", command=self.save_fin, fg_color="#2ecc71")
        self.btn_f_save.pack(fill="x", padx=10, pady=(20,5))
        ctk.CTkButton(f_form, text="Editar Selecionado", command=self.edit_fin, fg_color="#f39c12").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Limpar", command=self.clear_fin, fg_color="#95a5a6").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(f_form, text="Excluir", command=self.del_fin, fg_color="#e74c3c").pack(fill="x", padx=10, pady=5)

        self.f_busca = self.criar_barra_busca(f_lista, self.buscar_fin)
        self.tree_fin = self.criar_treeview(f_lista, ('ID', 'Descrição', 'Tipo', 'Valor', 'Vencimento', 'Status'))
        self.buscar_fin()

    def buscar_fin(self): self.atualizar_tree(self.tree_fin, self.model.buscar_financeiro(self.f_busca.get()))

    def edit_fin(self):
        sel = self.tree_fin.selection()
        if not sel: return messagebox.showwarning("Aviso", "Selecione um lançamento.")
        val = self.tree_fin.item(sel[0])['values']
        
        self.id_fin_edit = int(val[0])
        self.f_desc.delete(0,tk.END); self.f_desc.insert(0, val[1])
        self.f_tipo.set(val[2])
        self.f_valor.delete(0,tk.END); self.f_valor.insert(0, val[3])
        self.f_data.delete(0,tk.END); self.f_data.insert(0, val[4])
        self.f_status.set(val[5])
        self.btn_f_save.configure(text="Salvar Alteração", fg_color="#3498db")

    def save_fin(self):
        try:
            val = float(self.f_valor.get().replace(',', '.'))
            if self.id_fin_edit:
                res = self.model.atualizar_financeiro(self.id_fin_edit, self.f_desc.get(), val, self.f_tipo.get(), self.f_data.get(), self.f_status.get())
            else:
                res = self.model.cadastrar_financeiro(self.f_desc.get(), val, self.f_tipo.get(), self.f_data.get(), self.f_status.get())
            
            if res[0]: messagebox.showinfo("Sucesso", res[1]); self.clear_fin(); self.buscar_fin()
            else: messagebox.showerror("Erro", res[1])
        except ValueError: messagebox.showerror("Erro", "Valor inválido (use ponto para decimais)")

    def clear_fin(self):
        self.id_fin_edit = None; self.btn_f_save.configure(text="Lançar", fg_color="#2ecc71")
        for e in [self.f_desc, self.f_valor, self.f_data]: e.delete(0, tk.END)

    def del_fin(self):
        sel = self.tree_fin.selection()
        if sel: self.model.excluir_financeiro(int(self.tree_fin.item(sel[0])['values'][0])); self.buscar_fin()

if __name__ == "__main__":
    app = SistemaCondominioApp()
    app.mainloop()