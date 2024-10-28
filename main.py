import subprocess
import sys
import os
from flet import Page, TextField, ElevatedButton, Column, Text, Container, IconButton, icons, alignment, colors, SnackBar

# Definindo um valor padrão para is_dark_mode
is_dark_mode = False  # Padrão para claro
if len(sys.argv) > 1:  # Verifica se há argumentos suficientes
    is_dark_mode = sys.argv[1] == "True"  # Recebe o tema como argumento

def main(page: Page):
    global is_dark_mode  # Usando a variável global

    page.title = "Tela de Login"
    page.window.maximized = True
    page.theme_mode = "dark" if is_dark_mode else "light"  # Define o tema inicial

    # Alterna o tema
    def toggle_theme(e):
        global is_dark_mode  # Define que vamos usar a variável global
        is_dark_mode = not is_dark_mode
        page.theme_mode = "dark" if is_dark_mode else "light"
        toggle_button.icon = icons.DARK_MODE if is_dark_mode else icons.WB_SUNNY_OUTLINED
        page.update()

    # Função para mostrar mensagem com SnackBar
    def show_message(msg, color=colors.GREEN):
        snack_bar = SnackBar(
            content=Text(msg, color=colors.WHITE),
            bgcolor=color,
        )
        page.overlay.append(snack_bar)  # Adiciona a mensagem na tela
        snack_bar.open = True
        page.update()

    # Função de entrada
    def entrar(e):
        if not user_field.value or not password_field.value:
            show_message("Preencha todos os campos!", color=colors.RED)  # Mostra mensagem de erro
            return
        # Fecha a janela atual
        page.window.close()
        # Chama main.py passando o tema atual
        os.system(f'python navrail.py {str(is_dark_mode)}')

    # Botão de alternância de tema
    toggle_button = IconButton(
        icon=icons.WB_SUNNY_OUTLINED if not is_dark_mode else icons.DARK_MODE,
        on_click=toggle_theme,
        tooltip="Alternar Tema"
    )

    # Campos de entrada
    user_field = TextField(label="Usuário", width=300)
    password_field = TextField(label="Senha", password=True, width=300)
    
    # Layout da tela centralizado
    container = Container(
        content=Column(
            [
                Text("Tela de Login", size=24, weight="bold", color=colors.BLUE),
                user_field,
                password_field,
                ElevatedButton("Entrar", on_click=entrar, width=150),
                ElevatedButton("Esqueceu sua senha?", on_click=lambda e: print("Esqueceu a senha?"), width=150),
                ElevatedButton("Registrar", on_click=lambda e: print("Registrar novo usuário"), width=150),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10
        ),
        alignment=alignment.center,
    )

    page.appbar = Column([toggle_button], alignment="end")  # Botão de tema no topo
    page.add(container)

# Executar o aplicativo
if __name__ == "__main__":
    import flet
    flet.app(target=main)
