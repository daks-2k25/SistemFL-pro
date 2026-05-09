import customtkinter as ctk
from tkinter import messagebox
import hashlib
import random
import json
import os

# Configurações Visuais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SistemFL(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SistemFL Pro - v4.0")
        self.geometry("450x600")
        self.resizable(False, False)

        # Caminho do banco de dados e credenciais admin
        self.db_file = "database_gui.json"
        self.usuarios = self.carregar_banco()
        self.admin_info = ("admin", "8767")

        self.mostrar_login_admin()

    # --- LÓGICA DE DADOS (PERSISTÊNCIA) ---
    def carregar_banco(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def salvar_banco(self):
        try:
            with open(self.db_file, "w") as f:
                json.dump(self.usuarios, f, indent=4)
        except Exception as e:
            messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar os dados: {e}")

    def gerar_hash(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- TELA: LOGIN ADMIN ---
    def mostrar_login_admin(self):
        self.limpar_tela()
        
        header = ctk.CTkFrame(self, height=80, fg_color="#1f538d", corner_radius=0)
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text="SistemFL PRO", font=("Roboto", 28, "bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        frame_login = ctk.CTkFrame(self, fg_color="transparent")
        frame_login.pack(pady=20, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame_login, text="AUTENTICAÇÃO RESTRITA", font=("Roboto", 12, "bold"), text_color="gray").pack(pady=10)

        self.u_ent = ctk.CTkEntry(frame_login, placeholder_text="Usuário Admin", height=45)
        self.u_ent.pack(pady=10, fill="x")

        self.s_ent = ctk.CTkEntry(frame_login, placeholder_text="Senha Admin", show="*", height=45)
        self.s_ent.pack(pady=10, fill="x")

        ctk.CTkButton(frame_login, text="ACESSAR SISTEMA", height=50, font=("Roboto", 14, "bold"), command=self.validar_admin).pack(pady=20, fill="x")
        
        ctk.CTkLabel(frame_login, text="OU", text_color="gray").pack()

        ctk.CTkButton(frame_login, text="LOGIN USUÁRIO COMUM", fg_color="transparent", border_width=2, command=self.mostrar_login_usuario).pack(pady=10, fill="x")

    # --- TELA: PAINEL PRINCIPAL (ADMIN) ---
    def mostrar_painel_admin(self):
        self.limpar_tela()
        
        ctk.CTkLabel(self, text="CENTRAL DE COMANDO", font=("Roboto", 22, "bold")).pack(pady=30)

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(pady=10, padx=50, fill="x")

        ctk.CTkButton(grid, text="✚ CADASTRAR USUÁRIO", height=45, command=self.tela_cadastro).pack(pady=10, fill="x")
        ctk.CTkButton(grid, text="📋 LISTAR REGISTROS", height=45, command=self.tela_listagem).pack(pady=10, fill="x")
        ctk.CTkButton(grid, text="🗑 REMOVER ACESSO", height=45, fg_color="#a83232", hover_color="#7a2424", command=self.tela_remocao).pack(pady=10, fill="x")
        
        ctk.CTkButton(self, text="EFETUAR LOGOFF", fg_color="transparent", text_color="gray", command=self.mostrar_login_admin).pack(side="bottom", pady=20)

    # --- TELA: CADASTRO ---
    def tela_cadastro(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="REGISTRO DE CREDENCIAIS", font=("Roboto", 18, "bold")).pack(pady=30)
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(padx=60, fill="x")

        nome_ent = ctk.CTkEntry(frame, placeholder_text="Novo Login", height=40)
        nome_ent.pack(pady=10, fill="x")
        
        senha_ent = ctk.CTkEntry(frame, placeholder_text="Senha (min. 4 dígitos)", show="*", height=40)
        senha_ent.pack(pady=10, fill="x")

        def salvar():
            nome = nome_ent.get().strip()
            senha = senha_ent.get()
            
            if not nome or len(senha) < 4:
                messagebox.showwarning("Aviso", "Preencha o nome e use uma senha de no mínimo 4 dígitos!")
                return

            if nome in self.usuarios:
                messagebox.showerror("Erro", "Este usuário já existe!")
            else:
                self.usuarios[nome] = {"senha": self.gerar_hash(senha), "codigo": random.randint(1000, 9999)}
                self.salvar_banco()
                messagebox.showinfo("Sucesso", f"Usuário {nome} ativado!")
                self.mostrar_painel_admin()

        ctk.CTkButton(self, text="CONFIRMAR CADASTRO", fg_color="#2b8a3e", hover_color="#206a2f", command=salvar).pack(pady=30)
        ctk.CTkButton(self, text="CANCELAR", fg_color="gray", command=self.mostrar_painel_admin).pack()

    # --- TELA: LISTAGEM ---
    def tela_listagem(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="BANCO DE DADOS ATIVO", font=("Roboto", 18, "bold")).pack(pady=20)
        
        caixa = ctk.CTkTextbox(self, width=380, height=350, font=("Courier New", 13), border_width=2)
        caixa.pack(pady=10, padx=20)
        
        if not self.usuarios:
            caixa.insert("0.0", ">>> NENHUM REGISTRO ENCONTRADO <<<")
        else:
            header = f"{'USUÁRIO':<20} | {'ID':<10}\n" + "-"*35 + "\n"
            caixa.insert("end", header)
            for nome, dados in self.usuarios.items():
                caixa.insert("end", f"{str(nome):<20} | {str(dados['codigo'])}\n")
        
        caixa.configure(state="disabled")
        ctk.CTkButton(self, text="VOLTAR AO PAINEL", command=self.mostrar_painel_admin).pack(pady=20)

    # --- TELA: REMOÇÃO ---
    def tela_remocao(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="EXCLUSÃO DE REGISTRO", font=("Roboto", 18, "bold"), text_color="#a83232").pack(pady=30)
        
        rem_ent = ctk.CTkEntry(self, placeholder_text="Digite o nome do usuário", width=300, height=40)
        rem_ent.pack(pady=10)

        def confirmar():
            alvo = rem_ent.get().strip()
            if alvo in self.usuarios:
                if messagebox.askyesno("Confirmar", f"Deseja realmente deletar {alvo}?"):
                    del self.usuarios[alvo]
                    self.salvar_banco()
                    messagebox.showinfo("Deletado", "Usuário removido com sucesso.")
                    self.mostrar_painel_admin()
            else:
                messagebox.showerror("Erro", "Usuário não localizado.")

        ctk.CTkButton(self, text="EXCLUIR PERMANENTEMENTE", fg_color="#a83232", command=confirmar).pack(pady=20)
        ctk.CTkButton(self, text="VOLTAR", command=self.mostrar_painel_admin).pack()

    # --- TELA: LOGIN USUÁRIO COMUM ---
    def mostrar_login_usuario(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="ACESSO DE COLABORADOR", font=("Roboto", 20, "bold")).pack(pady=40)
        
        u_log = ctk.CTkEntry(self, placeholder_text="Nome de Usuário", width=280, height=40)
        u_log.pack(pady=10)
        
        s_log = ctk.CTkEntry(self, placeholder_text="Sua Senha", show="*", width=280, height=40)
        s_log.pack(pady=10)

        def entrar():
            u, s = u_log.get().strip(), s_log.get()
            if u in self.usuarios and self.usuarios[u]["senha"] == self.gerar_hash(s):
                messagebox.showinfo("Acesso Liberado", f"Bem-vindo, {u}!\nID de Sessão: {self.usuarios[u]['codigo']}")
            else:
                messagebox.showerror("Bloqueado", "Credenciais inválidas.")

        ctk.CTkButton(self, text="LOGAR", width=280, height=45, command=entrar).pack(pady=20)
        ctk.CTkButton(self, text="RETORNAR", fg_color="transparent", command=self.mostrar_login_admin).pack()

    # --- LÓGICA DE VALIDAÇÃO ADMIN ---
    def validar_admin(self):
        # Correção final: admin_info[0] e admin_info[1]
        if self.u_ent.get() == self.admin_info[0] and self.s_ent.get() == self.admin_info[1]:
            self.mostrar_painel_admin()
        else:
            messagebox.showerror("Acesso Negado", "Usuário ou Senha de Admin inválidos.")

if __name__ == "__main__":
    app = SistemFL()
    app.mainloop()
