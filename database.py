import sqlite3

DB_NAME = "lar_idosos.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = conectar()
    cur = conn.cursor()

    # LOGIN
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)

    # IDOSOS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS idosos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        banco TEXT,
        agencia TEXT,
        conta TEXT,
        observacoes TEXT
    )
    """)

    # PAGAMENTOS MENSAIS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_idoso INTEGER NOT NULL,
        mes_ano TEXT NOT NULL,
        data TEXT NOT NULL,
        banco TEXT NOT NULL,
        valor REAL NOT NULL,
        valor_casa REAL NOT NULL,
        valor_idoso REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDENTE',
        observacao TEXT,
        usuario TEXT NOT NULL,
        criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_idoso) REFERENCES idosos(id)
    )
    """)

    # Impede duplicar pagamento do mesmo idoso no mesmo mês
    cur.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_pagamento_unico
    ON pagamentos (id_idoso, mes_ano)
    """)

    conn.commit()
    conn.close()


def criar_usuario_padrao():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM usuarios")
    total = cur.fetchone()[0]

    if total == 0:
        cur.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ("admin", "123"))
        conn.commit()

    conn.close()
