import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import conectar

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

import os

# Só funciona no Windows (impressão direta)
try:
    import win32api
except:
    win32api = None


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

    # ============================
    # FUNÇÕES
    # ============================

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

    def pegar_dados_da_tabela():
        dados = []
        for item in tabela.get_children():
            dados.append(tabela.item(item)["values"])
        return dados

    # ============================
    # GERAR PDF
    # ============================

    def gerar_pdf():
        dados = pegar_dados_da_tabela()

        if not dados:
            messagebox.showwarning("Atenção", "Não há dados para gerar o PDF.")
            return

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf")],
            title="Salvar Relatório em PDF",
            initialfile="relatorio_pagamentos.pdf"
        )

        if not arquivo:
            return

        # Página A4 paisagem (cabe melhor)
        largura, altura = landscape(A4)
        c = canvas.Canvas(arquivo, pagesize=landscape(A4))

        # Cabeçalho
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, altura - 1.5 * cm, "RELATÓRIO - PAGAMENTOS MENSAIS")

        c.setFont("Helvetica", 10)
        c.drawString(2 * cm, altura - 2.3 * cm, f"Filtro Nome: {busca.get().strip() or 'TODOS'}")
        c.drawString(10 * cm, altura - 2.3 * cm, f"Filtro Mês/Ano: {filtro_mes.get().strip() or 'TODOS'}")

        # Linha
        c.line(2 * cm, altura - 2.6 * cm, largura - 2 * cm, altura - 2.6 * cm)

        # Colunas no PDF
        colunas = ["ID", "IDOSO", "MÊS/ANO", "DATA", "BANCO", "VALOR", "CASA", "IDOSO", "STATUS", "OBS", "USUÁRIO"]
        larguras = [1.2, 4.5, 2.0, 2.2, 3.0, 2.0, 2.0, 2.0, 2.0, 4.5, 2.2]

        x_inicio = 2 * cm
        y = altura - 3.3 * cm

        c.setFont("Helvetica-Bold", 9)

        x = x_inicio
        for i, col in enumerate(colunas):
            c.drawString(x, y, col)
            x += larguras[i] * cm

        y -= 0.5 * cm
        c.setFont("Helvetica", 8)

        total_valor = 0
        total_casa = 0
        total_idoso = 0

        for linha in dados:
            # quebra página
            if y < 1.5 * cm:
                c.showPage()
                y = altura - 2 * cm

            # valores
            try:
                total_valor += float(linha[5])
            except:
                pass
            try:
                total_casa += float(linha[6])
            except:
                pass
            try:
                total_idoso += float(linha[7])
            except:
                pass

            x = x_inicio
            for i, valor in enumerate(linha):
                texto = str(valor)

                # encurtar obs se ficar gigante
                if i == 9 and len(texto) > 35:
                    texto = texto[:35] + "..."

                c.drawString(x, y, texto)
                x += larguras[i] * cm

            y -= 0.45 * cm

        # Totais
        y -= 0.5 * cm
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2 * cm, y, f"TOTAL GERAL: R$ {total_valor:.2f}")
        c.drawString(8 * cm, y, f"TOTAL CASA: R$ {total_casa:.2f}")
        c.drawString(14 * cm, y, f"TOTAL IDOSO: R$ {total_idoso:.2f}")

        c.save()

        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\n\n{arquivo}")

    # ============================
    # IMPRIMIR
    # ============================

    def imprimir_pdf():
        if win32api is None:
            messagebox.showerror(
                "Erro",
                "Impressão automática só funciona no Windows.\n\nInstale: pip install pywin32"
            )
            return

        dados = pegar_dados_da_tabela()
        if not dados:
            messagebox.showwarning("Atenção", "Não há dados para imprimir.")
            return

        # gera um PDF temporário na pasta do sistema
        temp_pdf = os.path.join(os.getcwd(), "relatorio_temp.pdf")

        # gerar pdf automaticamente
        largura, altura = landscape(A4)
        c = canvas.Canvas(temp_pdf, pagesize=landscape(A4))

        c.setFont("Helvetica-Bold", 14)
        c.drawString(2 * cm, altura - 1.5 * cm, "RELATÓRIO - PAGAMENTOS MENSAIS")

        c.setFont("Helvetica", 10)
        c.drawString(2 * cm, altura - 2.3 * cm, f"Filtro Nome: {busca.get().strip() or 'TODOS'}")
        c.drawString(10 * cm, altura - 2.3 * cm, f"Filtro Mês/Ano: {filtro_mes.get().strip() or 'TODOS'}")

        c.line(2 * cm, altura - 2.6 * cm, largura - 2 * cm, altura - 2.6 * cm)

        colunas = ["ID", "IDOSO", "MÊS/ANO", "DATA", "BANCO", "VALOR", "CASA", "IDOSO", "STATUS", "OBS", "USUÁRIO"]
        larguras = [1.2, 4.5, 2.0, 2.2, 3.0, 2.0, 2.0, 2.0, 2.0, 4.5, 2.2]

        x_inicio = 2 * cm
        y = altura - 3.3 * cm

        c.setFont("Helvetica-Bold", 9)
        x = x_inicio
        for i, col in enumerate(colunas):
            c.drawString(x, y, col)
            x += larguras[i] * cm

        y -= 0.5 * cm
        c.setFont("Helvetica", 8)

        for linha in dados:
            if y < 1.5 * cm:
                c.showPage()
                y = altura - 2 * cm

            x = x_inicio
            for i, valor in enumerate(linha):
                texto = str(valor)
                if i == 9 and len(texto) > 35:
                    texto = texto[:35] + "..."
                c.drawString(x, y, texto)
                x += larguras[i] * cm

            y -= 0.45 * cm

        c.save()

        # manda imprimir
        try:
            win32api.ShellExecute(0, "print", temp_pdf, None, ".", 0)
            messagebox.showinfo("Imprimir", "Relatório enviado para impressão.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível imprimir.\n\n{e}")

    # ============================
    # BOTÕES
    # ============================

    tk.Button(
        filtros,
        text="Pesquisar",
        bg="#2980b9",
        fg="white",
        relief="flat",
        width=14,
        command=pesquisar
    ).grid(row=0, column=4, padx=5)

    tk.Button(
        filtros,
        text="Gerar PDF",
        bg="#27ae60",
        fg="white",
        relief="flat",
        width=14,
        command=gerar_pdf
    ).grid(row=0, column=5, padx=5)

    tk.Button(
        filtros,
        text="Imprimir",
        bg="#8e44ad",
        fg="white",
        relief="flat",
        width=14,
        command=imprimir_pdf
    ).grid(row=0, column=6, padx=5)

    carregar()
