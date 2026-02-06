import tkinter as tk
from idosos import tela_idosos
from pagamentos import tela_pagamentos
from relatorios import tela_relatorios


class TelaDashboard:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario

        self.frame = tk.Frame(root, bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        titulo = tk.Label(
            self.frame,
            text="Dashboard - Lar de Idosos",
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff"
        )
        titulo.pack(pady=20)

        sub = tk.Label(
            self.frame,
            text=f"Usuário logado: {usuario}",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#555"
        )
        sub.pack(pady=5)

        botoes = tk.Frame(self.frame, bg="#ffffff")
        botoes.pack(pady=25)

        def criar_botao(texto, comando):
            return tk.Button(
                botoes,
                text=texto,
                font=("Segoe UI", 11, "bold"),
                bg="#2d98da",
                fg="white",
                relief="flat",
                width=25,
                height=2,
                command=comando
            )

        criar_botao("Cadastro de Idosos", lambda: tela_idosos(self.root)).pack(pady=8)
        criar_botao("Pagamentos Mensais", lambda: tela_pagamentos(self.root, self.usuario)).pack(pady=8)
        criar_botao("Relatórios", lambda: tela_relatorios(self.root)).pack(pady=8)

        tk.Button(
            self.frame,
            text="Sair",
            font=("Segoe UI", 10),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            width=12,
            command=self.sair
        ).pack(pady=15)

    def sair(self):
        self.frame.destroy()
        from login import TelaLogin
        TelaLogin(self.root)
