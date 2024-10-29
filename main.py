import sys
import os
from flet import Page, TextField, ElevatedButton, Column, Text, Container, IconButton, icons, alignment, colors, SnackBar, AlertDialog, Row

# Definindo um valor padrão para is_dark_mode
is_dark_mode = False  # Padrão para claro
if len(sys.argv) > 1:  # Verifica se há argumentos suficientes
    is_dark_mode = sys.argv[1] == "True"  # Recebe o tema como argumento

dialog = None  # Inicialização da variável global

def main(page: Page):
    global is_dark_mode  # Usando a variável global

    page.title = "Tela de Login"
    page.window.maximized = True
    page.theme_mode = "dark" if is_dark_mode else "light"  # Define o tema inicial

    # Função para alternar o tema
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

    # Função para abrir o AlertDialog de recuperação de senha
    def open_password_recovery_dialog(e):
        # Campos do dialog
        email_field = TextField(label="Email", width=320)
        new_password_field = TextField(label="Nova Senha", password=True, width=320)
        confirm_password_field = TextField(label="Confirme a Nova Senha", password=True, width=320)
        mensagem_erro = Text(value="", color=colors.RED)  # Campo para mensagens de erro

        # Conteúdo do AlertDialog
        dialog_content = Container(
            content=Column([
                email_field,
                new_password_field,
                confirm_password_field,
                mensagem_erro,  # Adiciona o campo de mensagem de erro no diálogo
                Row([
                    ElevatedButton(
                        "Cancelar", 
                        on_click=lambda e: close_dialog(),
                        color=colors.BLUE  # Cor azul padrão
                    ),
                    ElevatedButton(
                        "Concluir",  # Alterado para 'Concluir'
                        on_click=lambda e: validate_fields(email_field, new_password_field, confirm_password_field, mensagem_erro),
                        color=colors.BLUE  # Cor azul padrão
                    ),
                ], alignment="center", spacing=10)  # Centraliza os botões
            ], spacing=10),
            padding=10,
            width=350,  # Largura do dialog
            height=250,  # Altura do dialog
        )

        global dialog  # Usando a variável global para o dialog
        dialog = AlertDialog(
            title=Text("Recuperar Senha", size=20, weight="bold", color=colors.BLUE),
            content=dialog_content,
            actions=[],  # Não precisa adicionar botões aqui, já estão no content
        )

        page.overlay.append(dialog)  # Adiciona o AlertDialog à sobreposição da página
        dialog.open = True  # Abre o AlertDialog
        page.update()  # Atualiza a página

    # Função para fechar o dialog
    def close_dialog():
        dialog.open = False  # Fecha o dialog definindo open como False
        page.update()  # Atualiza a página

    # Função para validar os campos e mostrar mensagens
    def validate_fields(email_field, new_password_field, confirm_password_field, mensagem_erro):
        email = email_field.value
        new_password = new_password_field.value
        confirm_password = confirm_password_field.value
        
        # Verifica se o email é válido
        if "@" not in email or "." not in email.split("@")[-1]:
            mensagem_erro.value = "Email inválido!"
            page.update()
            return
        
        # Verifica se as senhas estão preenchidas e se são iguais
        if not new_password or not confirm_password:
            mensagem_erro.value = "Preencha todos os campos!"
            page.update()
            return
        if new_password != confirm_password:
            mensagem_erro.value = "As senhas não coincidem!"
            page.update()
            return

        # Se tudo estiver válido, mostra mensagem de sucesso e fecha o dialog
        show_message("Senha alterada com sucesso!", color=colors.GREEN)
        close_dialog()  # Fecha o dialog

    # Função para abrir o AlertDialog de registro
    def open_registration_dialog(e):
        # Campos do dialog
        user_field = TextField(label="Usuário", width=320)
        email_field = TextField(label="Email", width=320)
        password_field = TextField(label="Senha", password=True, width=320)
        confirm_password_field = TextField(label="Confirme a Senha", password=True, width=320)
        mensagem_erro = Text(value="", color=colors.RED)  # Campo para mensagens de erro

        # Conteúdo do AlertDialog
        dialog_content = Container(
            content=Column([
                user_field,
                email_field,
                password_field,
                confirm_password_field,
                mensagem_erro,
                Row([
                    ElevatedButton(
                        "Cancelar", 
                        on_click=lambda e: close_dialog(),
                        color=colors.BLUE  # Cor azul padrão
                    ),
                    ElevatedButton(
                        "Registrar", 
                        on_click=lambda e: validate_registration_fields(user_field, email_field, password_field, confirm_password_field, mensagem_erro),
                        color=colors.BLUE  # Cor azul padrão
                    ),
                ], alignment="center", spacing=10)  # Centraliza os botões
            ], spacing=10),
            padding=10,
            width=350,  # Largura do dialog
            height=300,  # Altura do dialog
        )

        global dialog  # Usando a variável global para o dialog
        dialog = AlertDialog(
            title=Text("Registrar", size=20, weight="bold", color=colors.BLUE),
            content=dialog_content,
            actions=[],  # Não precisa adicionar botões aqui, já estão no content
        )

        page.overlay.append(dialog)  # Adiciona o AlertDialog à sobreposição da página
        dialog.open = True  # Abre o AlertDialog
        page.update()  # Atualiza a página

    # Função para validar os campos de registro e mostrar mensagens
    def validate_registration_fields(user_field, email_field, password_field, confirm_password_field, mensagem_erro):
        user = user_field.value
        email = email_field.value
        password = password_field.value
        confirm_password = confirm_password_field.value

        # Verifica se todos os campos estão preenchidos
        if not user or not email or not password or not confirm_password:
            mensagem_erro.value = "Preencha todos os campos!"
            page.update()
            return
        
        # Verifica se o email é válido
        if "@" not in email or "." not in email.split("@")[-1]:
            mensagem_erro.value = "Email inválido!"
            page.update()
            return
        
        # Verifica se as senhas estão iguais
        if password != confirm_password:
            mensagem_erro.value = "As senhas não coincidem!"
            page.update()
            return

        # Se tudo estiver válido, mostra mensagem de sucesso
        show_message("Registro realizado com sucesso!", color=colors.GREEN)
        close_dialog()  # Fecha o dialog

    # Função de entrada
    def entrar(e):
        if not user_field.value or not password_field.value:
            show_message("Preencha todos os campos!", color=colors.RED)  # Mostra mensagem de erro
            return
        
        # Fecha a janela atual
        page.window.close()
        # Chama navrail.py passando o tema atual
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
                Text("Login", size=24, weight="bold", color=colors.BLUE),  # Alterado para 'Login'
                user_field,
                password_field,
                Column(  # Mudança para a disposição vertical dos botões
                    [
                        ElevatedButton("Entrar", on_click=entrar, width=250, color=colors.BLUE),
                        ElevatedButton("Esqueceu sua senha?", on_click=open_password_recovery_dialog, width=250, color=colors.BLUE),
                        ElevatedButton("Registrar", on_click=open_registration_dialog, width=250, color=colors.BLUE),  # Abre o dialog de registro
                    ],
                    alignment="center",  # Centraliza os botões
                    spacing=20  # Espaçamento de 20 px entre os botões
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20
        ),
        alignment=alignment.center,
    )

    page.appbar = Column([toggle_button], alignment="end")  # Botão de tema no topo
    page.add(container)  # Adiciona o container à página

# Executar o aplicativo
if __name__ == "__main__":
    import flet
    flet.app(target=main)
