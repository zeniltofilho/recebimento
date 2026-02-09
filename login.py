import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from dashboard import TelaDashboard


class TelaLogin:
    def __init__(self, root):
        self.root = root

        self.frame = tk.Frame(root, bg="#f5f6fa")
        self.frame.pack(fill="both", expand=True)

        titulo = tk.Label(
            self.frame,
            text="Login - Lar de Idosos",
            font=("Segoe UI", 16, "bold"),
            bg="#f5f6fa"
        )
        titulo.pack(pady=25)

        form = tk.Frame(self.frame, bg="#f5f6fa")
        form.pack()

        tk.Label(form, text="Usuário:", font=("Segoe UI", 11), bg="#f5f6fa").grid(row=0, column=0, sticky="w", pady=8)
        self.usuario = ttk.Entry(form, width=28)
        self.usuario.grid(row=0, column=1, pady=8)

        tk.Label(form, text="Senha:", font=("Segoe UI", 11), bg="#f5f6fa").grid(row=1, column=0, sticky="w", pady=8)
        self.senha = ttk.Entry(form, width=28, show="*")
        self.senha.grid(row=1, column=1, pady=8)

        btn = tk.Button(
            self.frame,
            text="Entrar",
            font=("Segoe UI", 11, "bold"),
            bg="#2d98da",
            fg="white",
            relief="flat",
            width=20,
            command=self.entrar
        )
        btn.pack(pady=20)

        info = tk.Label(
            self.frame,
            text="Usuário padrão: admin | Senha: 123",
            font=("Segoe UI", 9),
            bg="#f5f6fa",
            fg="#555"
        )
        info.pack(pady=5)

        # ========= ENTER FUNCIONANDO =========
        self.root.bind("<Return>", self.entrar)

        # opcional: já começa com foco no usuário
        self.usuario.focus()

    def entrar(self, event=None):
        user = self.usuario.get().strip()
        senha = self.senha.get().strip()

        if not user or not senha:
            messagebox.showwarning("Atenção", "Digite usuário e senha.")
            return

        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (user, senha))
        achou = cur.fetchone()
        conn.close()

        if achou:
            self.frame.destroy()
            TelaDashboard(self.root, user)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")
