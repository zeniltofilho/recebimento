import tkinter as tk
from database import init_db, criar_usuario_padrao
from login import TelaLogin


def main():
    init_db()
    criar_usuario_padrao()

    root = tk.Tk()
    root.title("Sistema - Lar de Idosos")
    root.geometry("420x300")
    root.resizable(False, False)

    TelaLogin(root)

    root.mainloop()


if __name__ == "__main__":
    main()
