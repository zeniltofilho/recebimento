import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar


def tela_idosos(root):
    janela = tk.Toplevel(root)
    janela.title("Cadastro de Idosos")
    janela.geometry("820x600")
    janela.resizable(False, False)

    frame = tk.Frame(janela, bg="#ffffff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Idosos", font=("Segoe UI", 15, "bold"), bg="#ffffff").pack(pady=15)

    form = tk.Frame(frame, bg="#ffffff")
    form.pack(pady=5)

    # Campos
    tk.Label(form, text="Nome:", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    nome = ttk.Entry(form, width=35)
    nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form, text="Banco:", bg="#ffffff").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    banco = ttk.Entry(form, width=20)
    banco.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(form, text="Agência:", bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    agencia = ttk.Entry(form, width=20)
    agencia.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form, text="Conta:", bg="#ffffff").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    conta = ttk.Entry(form, width=20)
    conta.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(form, text="Observações:", bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    obs = ttk.Entry(form, width=65)
    obs.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    # Lista
    cols = ("id", "nome", "banco", "agencia", "conta", "obs")
    tabela = ttk.Treeview(frame, columns=cols, show="headings", height=10)
    tabela.pack(pady=15, padx=10, fill="x")

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("banco", text="Banco")
    tabela.heading("agencia", text="Agência")
    tabela.heading("conta", text="Conta")
    tabela.heading("obs", text="Observações")

    tabela.column("id", width=50)
    tabela.column("nome", width=220)
    tabela.column("banco", width=140)
    tabela.column("agencia", width=100)
    tabela.column("conta", width=120)
    tabela.column("obs", width=250)

    def carregar():
        for item in tabela.get_children():
            tabela.delete(item)

        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, banco, agencia, conta, observacoes FROM idosos ORDER BY nome")
        dados = cur.fetchall()
        conn.close()

        for d in dados:
            tabela.insert("", "end", values=d)

    def salvar():
        n = nome.get().strip()
        b = banco.get().strip()
        ag = agencia.get().strip()
        ct = conta.get().strip()
        ob = obs.get().strip()

        if not n:
            messagebox.showwarning("Atenção", "Digite o nome do idoso.")
            return

        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO idosos (nome, banco, agencia, conta, observacoes) VALUES (?, ?, ?, ?, ?)",
            (n, b, ag, ct, ob)
        )
        conn.commit()
        conn.close()

        nome.delete(0, "end")
        banco.delete(0, "end")
        agencia.delete(0, "end")
        conta.delete(0, "end")
        obs.delete(0, "end")

        carregar()
        messagebox.showinfo("OK", "Idoso cadastrado com sucesso.")

    def remover():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um idoso na tabela.")
            return

        valores = tabela.item(item)["values"]
        id_idoso = valores[0]

        if not messagebox.askyesno("Confirmar", "Deseja remover esse idoso?"):
            return

        conn = conectar()
        cur = conn.cursor()
        cur.execute("DELETE FROM idosos WHERE id=?", (id_idoso,))
        conn.commit()
        conn.close()

        carregar()

    botoes = tk.Frame(frame, bg="#ffffff")
    botoes.pack(pady=5)

    tk.Button(botoes, text="Salvar", width=15, bg="#27ae60", fg="white", relief="flat", command=salvar).grid(row=0, column=0, padx=5)
    tk.Button(botoes, text="Remover", width=15, bg="#e74c3c", fg="white", relief="flat", command=remover).grid(row=0, column=1, padx=5)
    tk.Button(botoes, text="Atualizar Lista", width=15, bg="#2980b9", fg="white", relief="flat", command=carregar).grid(row=0, column=2, padx=5)

    carregar()
