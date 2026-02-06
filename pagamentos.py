import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar
from datetime import datetime


def tela_pagamentos(root, usuario):
    janela = tk.Toplevel(root)
    janela.title("Pagamentos Mensais")
    janela.geometry("1000x600")
    janela.resizable(False, False)

    frame = tk.Frame(janela, bg="#ffffff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Pagamentos Mensais", font=("Segoe UI", 15, "bold"), bg="#ffffff").pack(pady=15)

    # Carregar idosos
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, banco FROM idosos ORDER BY nome")
    idosos = cur.fetchall()
    conn.close()

    if not idosos:
        messagebox.showwarning("Atenção", "Nenhum idoso cadastrado. Cadastre antes.")
        janela.destroy()
        return

    lista_nomes = [f"{i[0]} - {i[1]}" for i in idosos]

    form = tk.Frame(frame, bg="#ffffff")
    form.pack(pady=5)

    tk.Label(form, text="Idoso:", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    cb_idoso = ttk.Combobox(form, values=lista_nomes, width=40, state="readonly")
    cb_idoso.grid(row=0, column=1, padx=5, pady=5)
    cb_idoso.current(0)

    tk.Label(form, text="Mês/Ano (ex: 02/2026):", bg="#ffffff").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    mes_ano = ttk.Entry(form, width=20)
    mes_ano.grid(row=0, column=3, padx=5, pady=5)
    mes_ano.insert(0, datetime.now().strftime("%m/%Y"))

    tk.Label(form, text="Data do saque:", bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    data = ttk.Entry(form, width=20)
    data.grid(row=1, column=1, padx=5, pady=5)
    data.insert(0, datetime.now().strftime("%d/%m/%Y"))

    tk.Label(form, text="Banco:", bg="#ffffff").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    banco = ttk.Entry(form, width=25)
    banco.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(form, text="Valor:", bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    valor = ttk.Entry(form, width=20)
    valor.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form, text="Status:", bg="#ffffff").grid(row=2, column=2, sticky="w", padx=5, pady=5)
    cb_status = ttk.Combobox(form, values=["Pago", "Pendente", "Bloqueado", "Prova Vida", "Óbito", "Família"], width=22, state="readonly")
    cb_status.grid(row=2, column=3, padx=5, pady=5)
    cb_status.current(0)

    tk.Label(form, text="Observação:", bg="#ffffff").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    obs = ttk.Entry(form, width=80)
    obs.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

    # Labels cálculo
    calc_frame = tk.Frame(frame, bg="#ffffff")
    calc_frame.pack(pady=10)

    lbl_casa = tk.Label(calc_frame, text="70% Casa: R$ 0,00", font=("Segoe UI", 12, "bold"), bg="#ffffff")
    lbl_casa.grid(row=0, column=0, padx=15)

    lbl_idoso = tk.Label(calc_frame, text="30% Idoso: R$ 0,00", font=("Segoe UI", 12, "bold"), bg="#ffffff")
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
            idoso_v = v * 0.30

            def br(x):
                return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            lbl_casa.config(text=f"70% Casa: R$ {br(casa)}")
            lbl_idoso.config(text=f"30% Idoso: R$ {br(idoso_v)}")
        except:
            lbl_casa.config(text="70% Casa: R$ 0,00")
            lbl_idoso.config(text="30% Idoso: R$ 0,00")

    valor.bind("<KeyRelease>", atualizar_calculo)

    # Tabela
    cols = ("id", "idoso", "mes_ano", "data", "banco", "valor", "casa", "idoso_valor", "status", "usuario")
    tabela = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    tabela.pack(pady=10, padx=10, fill="x")

    for c in cols:
        tabela.heading(c, text=c.upper())

    tabela.column("id", width=50)
    tabela.column("idoso", width=180)
    tabela.column("mes_ano", width=80)
    tabela.column("data", width=90)
    tabela.column("banco", width=120)
    tabela.column("valor", width=80)
    tabela.column("casa", width=80)
    tabela.column("idoso_valor", width=80)
    tabela.column("status", width=90)
    tabela.column("usuario", width=90)

    def carregar():
        for item in tabela.get_children():
            tabela.delete(item)

        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, i.nome, p.mes_ano, p.data, p.banco, p.valor,
                   p.valor_casa, p.valor_idoso, p.status, p.usuario
            FROM pagamentos p
            JOIN idosos i ON p.id_idoso = i.id
            ORDER BY p.id DESC
            LIMIT 150
        """)
        dados = cur.fetchall()
        conn.close()

        for d in dados:
            tabela.insert("", "end", values=d)

    def salvar():
        try:
            id_idoso = int(cb_idoso.get().split(" - ")[0])
            ma = mes_ano.get().strip()
            dt = data.get().strip()
            b = banco.get().strip()
            v = float(valor.get().replace(",", ".").strip())
            st = cb_status.get().strip()
            ob = obs.get().strip()

            if not ma or "/" not in ma:
                messagebox.showwarning("Atenção", "Digite o mês/ano corretamente (ex: 02/2026).")
                return

            if not b:
                messagebox.showwarning("Atenção", "Digite o banco.")
                return

            casa = round(v * 0.70, 2)
            idoso_v = round(v * 0.30, 2)

            conn = conectar()
            cur = conn.cursor()

            # Se já existir pagamento daquele idoso no mesmo mês, atualiza
            cur.execute("""
                SELECT id FROM pagamentos WHERE id_idoso=? AND mes_ano=?
            """, (id_idoso, ma))
            existe = cur.fetchone()

            if existe:
                id_pag = existe[0]
                cur.execute("""
                    UPDATE pagamentos
                    SET data=?, banco=?, valor=?, valor_casa=?, valor_idoso=?, status=?, observacao=?, usuario=?
                    WHERE id=?
                """, (dt, b, v, casa, idoso_v, st, ob, usuario, id_pag))
            else:
                cur.execute("""
                    INSERT INTO pagamentos
                    (id_idoso, mes_ano, data, banco, valor, valor_casa, valor_idoso, status, observacao, usuario)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (id_idoso, ma, dt, b, v, casa, idoso_v, st, ob, usuario))

            conn.commit()
            conn.close()

            messagebox.showinfo("OK", "Pagamento salvo com sucesso.")
            carregar()

        except:
            messagebox.showerror("Erro", "Preencha corretamente os campos (principalmente o valor).")

    def carregar_banco_do_idoso():
        try:
            id_idoso = int(cb_idoso.get().split(" - ")[0])
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT banco FROM idosos WHERE id=?", (id_idoso,))
            dado = cur.fetchone()
            conn.close()

            banco.delete(0, "end")
            if dado and dado[0]:
                banco.insert(0, dado[0])
        except:
            pass

    cb_idoso.bind("<<ComboboxSelected>>", lambda e: carregar_banco_do_idoso())

    botoes = tk.Frame(frame, bg="#ffffff")
    botoes.pack(pady=5)

    tk.Button(botoes, text="Salvar / Atualizar Mês", width=22, bg="#27ae60", fg="white", relief="flat", command=salvar).grid(row=0, column=0, padx=5)
    tk.Button(botoes, text="Atualizar Lista", width=18, bg="#2980b9", fg="white", relief="flat", command=carregar).grid(row=0, column=1, padx=5)

    carregar_banco_do_idoso()
    carregar()
