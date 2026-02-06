import tkinter as tk
from tkinter import ttk
from database import conectar


def tela_relatorios(root):
    janela = tk.Toplevel(root)
    janela.title("Relatórios")
    janela.geometry("1050x560")
    janela.resizable(False, False)

    frame = tk.Frame(janela, bg="#ffffff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Relatórios - Pagamentos Mensais", font=("Segoe UI", 15, "bold"), bg="#ffffff").pack(pady=15)

    filtros = tk.Frame(frame, bg="#ffffff")
    filtros.pack()

    tk.Label(filtros, text="Pesquisar Idoso:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
    busca = ttk.Entry(filtros, width=35)
    busca.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(filtros, text="Filtrar Mês/Ano (ex: 02/2026):", bg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
    filtro_mes = ttk.Entry(filtros, width=18)
    filtro_mes.grid(row=0, column=3, padx=5, pady=5)

    cols = ("id", "idoso", "mes_ano", "data", "banco", "valor", "casa", "idoso_valor", "status", "obs", "usuario")
    tabela = ttk.Treeview(frame, columns=cols, show="headings", height=17)
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
    tabela.column("obs", width=160)
    tabela.column("usuario", width=80)

    def carregar(filtro_nome="", mes=""):
        for item in tabela.get_children():
            tabela.delete(item)

        conn = conectar()
        cur = conn.cursor()

        query = """
            SELECT p.id, i.nome, p.mes_ano, p.data, p.banco, p.valor,
                   p.valor_casa, p.valor_idoso, p.status, p.observacao, p.usuario
            FROM pagamentos p
            JOIN idosos i ON p.id_idoso = i.id
            WHERE 1=1
        """
        params = []

        if filtro_nome:
            query += " AND i.nome LIKE ?"
            params.append(f"%{filtro_nome}%")

        if mes:
            query += " AND p.mes_ano = ?"
            params.append(mes)

        query += " ORDER BY p.id DESC"

        cur.execute(query, tuple(params))
        dados = cur.fetchall()
        conn.close()

        for d in dados:
            tabela.insert("", "end", values=d)

    def pesquisar():
        carregar(busca.get().strip(), filtro_mes.get().strip())

    tk.Button(filtros, text="Pesquisar", bg="#2980b9", fg="white", relief="flat", width=15, command=pesquisar).grid(row=0, column=4, padx=5)

    carregar()
