import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from datetime import datetime


def tela_saques(root, usuario):
    janela = tk.Toplevel(root)
    janela.title("Registrar Saques")
    janela.geometry("950x520")
    janela.resizable(False, False)

    frame = tk.Frame(janela, bg="#ffffff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Registrar Saques", font=("Segoe UI", 15, "bold"), bg="#ffffff").pack(pady=15)

    form = tk.Frame(frame, bg="#ffffff")
    form.pack()

    # Carregar idosos
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM idosos ORDER BY nome")
    idosos = cur.fetchall()
    conn.close()

    if not idosos:
        messagebox.showwarning("Atenção", "Nenhum idoso cadastrado. Cadastre antes.")
        janela.destroy()
        return

    lista_nomes = [f"{i[0]} - {i[1]}" for i in idosos]

    tk.Label(form, text="Idoso:", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    cb_idoso = ttk.Combobox(form, values=lista_nomes, width=40, state="readonly")
    cb_idoso.grid(row=0, column=1, padx=5, pady=5)
    cb_idoso.current(0)

    tk.Label(form, text="Banco do saque:", bg="#ffffff").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    banco = ttk.Entry(form, width=25)
    banco.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(form, text="Data:", bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    data = ttk.Entry(form, width=20)
    data.grid(row=1, column=1, padx=5, pady=5)
    data.insert(0, datetime.now().strftime("%d/%m/%Y"))

    tk.Label(form, text="Valor sacado:", bg="#ffffff").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    valor = ttk.Entry(form, width=25)
    valor.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(form, text="Observação:", bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    obs = ttk.Entry(form, width=80)
    obs.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    # Labels de cálculo
    calc_frame = tk.Frame(frame, bg="#ffffff")
    calc_frame.pack(pady=10)

    lbl_casa = tk.Label(calc_frame, text="70% Casa: R$ 0,00", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2c3e50")
    lbl_casa.grid(row=0, column=0, padx=15)

    lbl_idoso = tk.Label(calc_frame, text="30% Idoso: R$ 0,00", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2c3e50")
    lbl_idoso.grid(row=0, column=1, padx=15)

    def atualizar_calculo(*args):
        try:
            v = valor.get().replace(",", ".").strip()
            if not v:
                lbl_casa.config(text="70% Casa: R$ 0,00")
                lbl_idoso.config(text="30% Idoso: R$ 0,00")
                return

            v = float(v)
            casa = v * 0.70
            idoso = v * 0.30

            lbl_casa.config(text=f"70% Casa: R$ {casa:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            lbl_idoso.config(text=f"30% Idoso: R$ {idoso:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        except:
            lbl_casa.config(text="70% Casa: R$ 0,00")
            lbl_idoso.config(text="30% Idoso: R$ 0,00")

    valor.bind("<KeyRelease>", atualizar_calculo)

    # Tabela
    cols = ("id", "idoso", "data", "banco", "valor", "casa", "idoso_valor", "usuario")
    tabela = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    tabela.pack(pady=10, padx=10, fill="x")

    tabela.heading("id", text="ID")
    tabela.heading("idoso", text="Idoso")
    tabela.heading("data", text="Data")
    tabela.heading("banco", text="Banco")
    tabela.heading("valor", text="Valor")
    tabela.heading("casa", text="70% Casa")
    tabela.heading("idoso_valor", text="30% Idoso")
    tabela.heading("usuario", text="Usuário")

    tabela.column("id", width=50)
    tabela.column("idoso", width=220)
    tabela.column("data", width=90)
    tabela.column("banco", width=140)
    tabela.column("valor", width=90)
    tabela.column("casa", width=90)
    tabela.column("idoso_valor", width=90)
    tabela.column("usuario", width=90)

    def carregar():
        for item in tabela.get_children():
            tabela.delete(item)

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, i.nome, s.data, s.banco, s.valor, s.valor_casa, s.valor_idoso, s.usuario
            FROM saques s
            JOIN idosos i ON s.id_idoso = i.id
            ORDER BY s.id DESC
            LIMIT 100
        """)
        dados = cur.fetchall()
        conn.close()

        for d in dados:
            tabela.insert("", "end", values=d)

    def salvar():
        try:
            id_idoso = int(cb_idoso.get().split(" - ")[0])
            b = banco.get().strip()
            dt = data.get().strip()
            v = float(valor.get().replace(",", ".").strip())
            ob = obs.get().strip()

            if not b:
                messagebox.showwarning("Atenção", "Digite o banco do saque.")
                return

            casa = round(v * 0.70, 2)
            idoso_val = round(v * 0.30, 2)

            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO saques (id_idoso, data, banco, valor, valor_casa, valor_idoso, observacao, usuario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_idoso, dt, b, v, casa, idoso_val, ob, usuario))
            conn.commit()
            conn.close()

            banco.delete(0, "end")
            valor.delete(0, "end")
            obs.delete(0, "end")
            atualizar_calculo()

            carregar()
            messagebox.showinfo("OK", "Saque registrado com sucesso.")
        except:
            messagebox.showerror("Erro", "Preencha corretamente os campos (principalmente o valor).")

    botoes = tk.Frame(frame, bg="#ffffff")
    botoes.pack(pady=5)

    tk.Button(botoes, text="Salvar Saque", width=18, bg="#27ae60", fg="white", relief="flat", command=salvar).grid(row=0, column=0, padx=5)
    tk.Button(botoes, text="Atualizar Lista", width=18, bg="#2980b9", fg="white", relief="flat", command=carregar).grid(row=0, column=1, padx=5)

    carregar()
