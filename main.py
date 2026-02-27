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
    
    # Centralizar janela na tela
    root.update_idletasks()
    largura_janela = root.winfo_width()
    altura_janela = root.winfo_height()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    TelaLogin(root)

    root.mainloop()


if __name__ == "__main__":
    main()
