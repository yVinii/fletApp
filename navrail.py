from flet import *
from flet import DataTable
from flet import IconButton
import plotly.graph_objects as go
import io
import base64
import time  # Para pegar a hora e data atuais
import sys
import os

SALARIO_MINIMO = 1500
SALARIO_MAXIMO = 25000

# Definindo um valor padrão para is_dark_mode
is_dark_mode = False  # Padrão para claro
if len(sys.argv) > 1:  # Verifica se há argumentos suficientes
    is_dark_mode = sys.argv[1] == "True"  # Recebe o tema como argumento

ordenacao_combo = None
# Substitua a declaração da tabela
tabela = DataTable(
    columns=[
        DataColumn(Text("Nome", weight="bold")),
        DataColumn(Text("Salário", weight="bold")),
        DataColumn(Text("Data Inserção", weight="bold")),
        DataColumn(Text("Editar", weight="bold")),
        DataColumn(Text("Excluir", weight="bold")),
    ],
    rows=[],
    border=border.all(1, colors.BLACK)  # Borda para a tabela
)

def main(page: Page):
    global ordenacao_combo
    global tabela  # Declare como global na função main
    page.title = "Sistema Funcionários"
    page.window.maximized = True  # Maximiza a janela
    cadastros = []  # Lista para armazenar os funcionários

    page.theme_mode = "dark" if is_dark_mode else "light"

    def show_message(msg, color="green"):
        snack_bar = SnackBar(
            Text(msg, color=colors.WHITE),
            bgcolor=color,
        )
        page.overlay.append(snack_bar)  # Adiciona a mensagem na tela
        snack_bar.open = True
        page.update()

    def validar_salario(salario):
        try:
            salario_float = float(salario)  # Tenta converter o salário para float
            return SALARIO_MINIMO <= salario_float <= SALARIO_MAXIMO  # Verifica se está dentro do intervalo
        except ValueError:
            return False  # Se não der pra converter, retorna falso

    def validar_nome(nome):
        return len(nome) >= 3  # O nome deve ter pelo menos 3 letras

    # Atualizar a função de atualizar a tabela
    # Função para criar colunas da tabela
    def criar_colunas_tabela():
        return [
            DataColumn(Text("Nome")),
            DataColumn(Text("Salário")),
            DataColumn(Text("Data Inserção")),
            DataColumn(Text("Editar")),
            DataColumn(Text("Excluir")),
        ]

    # Atualizar a função de atualizar a tabela
    def atualizar_tabela(ordenacao="Nome"):
        global tabela
        if ordenacao == "Nome":
            cadastros.sort(key=lambda x: x["nome"])
        elif ordenacao == "Salário":
            cadastros.sort(key=lambda x: float(x["salario"]))
        elif ordenacao == "Data Inserção":
            cadastros.sort(key=lambda x: x["datainsercao"])

        # Limpa as linhas atuais da tabela
        tabela.rows.clear()
        
        # Adiciona cabeçalho da tabela
        tabela.columns = criar_colunas_tabela()  # Usa a função para criar colunas

        # Adiciona linhas à tabela
        for cadastro in cadastros:
            tabela.rows.append(
                DataRow(cells=[
                    DataCell(Text(cadastro["nome"])),
                    DataCell(Text(cadastro["salario"])),
                    DataCell(Text(cadastro["datainsercao"])),
                    DataCell(IconButton(icon=icons.EDIT, on_click=lambda e, c=cadastro: abrir_edicao(cadastro))),
                    DataCell(IconButton(icon=icons.DELETE, on_click=lambda e, c=cadastro: excluir_cadastro(cadastro))),
                ])
            )

        # Rodapé
        tabela.rows.append(
            DataRow(cells=[
                DataCell(Text(f"Total de Funcionários: {len(cadastros)}", weight="bold")),
                DataCell(Text(f"Soma dos Salários: R$ {sum(float(cadastro['salario']) for cadastro in cadastros):.2f}", weight="bold")),
                DataCell(Text("")),
                DataCell(Text("")),
                DataCell(Text(""))
            ])
        )

        # Estilização
        for column in tabela.columns:
            column.style = "padding: 8px; background-color: #f0f0f0; border-right: 1px solid black;"

        for row in tabela.rows:
            for cell in row.cells:
                cell.style = "border-right: 1px solid black; padding: 8px;"

        page.update()



    def excluir_cadastro(cadastro):
        cadastros.remove(cadastro)  # Remove o cadastro
        atualizar_tabela(ordenacao=ordenacao_combo.value)  # Atualiza a tabela

    dialog = None  # Inicialização da variável global

    def abrir_edicao(cadastro):
        salario_field = TextField(label="Novo Salário", value=cadastro["salario"], width=250)
        mensagem_erro = Text(value="", color="red")  # Campo para mensagens de erro

        dialog_content = Container(
            content=Column([
                salario_field,
                mensagem_erro  # Adiciona o campo de mensagem de erro no diálogo
            ]),
            padding=10,
            width=300,
            height=90,
        )

        dialog = AlertDialog(
            title=Text(f"Altere o salário do funcionário {cadastro['nome']}"),
            content=dialog_content,
            actions=[
                TextButton("Salvar", on_click=lambda e: salvar_edicao(cadastro, salario_field.value, mensagem_erro, dialog)),
                TextButton("Cancelar", on_click=lambda e: fechar_dialogo(dialog)),
            ],
        )

        page.overlay.append(dialog)  # Mostra a mini telinha
        dialog.open = True
        page.update()

    def atualizar_grafico_por_tipo(tipo_grafico, ordenacao):
        if not cadastros:
            grafico_img.src_base64 = ""  # Limpa a imagem se não houver dados
            page.update()
            return

        # Verifica se um tipo de gráfico foi selecionado
        if tipo_grafico is None:
            return  # Se nenhum tipo foi selecionado, não faça nada

        if ordenacao == "Nome":
            cadastros.sort(key=lambda x: x["nome"])
        elif ordenacao == "Salário":
            cadastros.sort(key=lambda x: float(x["salario"]))
        elif ordenacao == "Data Inserção":
            cadastros.sort(key=lambda x: x["datainsercao"])

        nomes = [cadastro["nome"] for cadastro in cadastros]
        salarios = [float(cadastro["salario"]) for cadastro in cadastros]

        fig = None

        if tipo_grafico == "Barras":
            fig = go.Figure(data=[go.Bar(x=nomes, y=salarios)])
        elif tipo_grafico == "Colunas":
            fig = go.Figure(data=[go.Bar(x=salarios, y=nomes, orientation="h")])
        elif tipo_grafico == "Linhas":
            fig = go.Figure(data=[go.Scatter(x=nomes, y=salarios, mode='lines+markers', line_shape='spline')])
        elif tipo_grafico == "Setor":
            fig = go.Figure(data=[go.Pie(labels=nomes, values=salarios)])
        elif tipo_grafico == "Área":
            fig = go.Figure(data=[go.Scatter(x=nomes, y=salarios, fill='tozeroy', mode='none')])

        if fig:
            img = fig.to_image(format="png")
            grafico_img.src_base64 = base64.b64encode(img).decode()
        else:
            grafico_img.src_base64 = ""  # Limpa a imagem se o gráfico não for gerado

        page.update()
        ordenacao_combo.visible = True
        atualizar_dados()

    def fechar_dialogo(dialog):
        dialog.open = False  # Fechar o diálogo
        page.update()  # Atualiza a página para refletir a mudança

    def salvar_edicao(cadastro, novo_salario, mensagem_erro, dialog):
        if not validar_salario(novo_salario):
            mensagem_erro.value = "O salário deve ser um número válido e maior que R$1500 e menor que R$25000!"
            page.update()  # Atualiza o diálogo para mostrar a mensagem
            return

        # Atualiza o salário do cadastro
        cadastro["salario"] = novo_salario

        # Atualiza a tabela com as informações mais recentes
        atualizar_tabela(ordenacao=ordenacao_combo.value)  
        show_message("Salário atualizado com sucesso!")
        
        fechar_dialogo(dialog)  # Fecha o diálogo corretamente

    def atualizar_dados():
        total_funcionarios = len(cadastros)
        total_salarios = sum(float(cadastro["salario"]) for cadastro in cadastros)

        dados_text.value = f"Total de Funcionários: {total_funcionarios}, Soma dos Salários: R$ {total_salarios:.2f}"
        page.update()

    def cadastrar(e):
        global ordenacao_combo  # Adicione isso para acessar a variável global aqui
        if not validar_nome(input_nome.value):
            show_message("O nome deve ter pelo menos 3 letras!", color="red")
            return
        if not validar_salario(input_salario.value):
            show_message("O salário deve ser um número válido e maior que R$1500 e menor que R$25000!", color="red")
            return

        datainsercao = time.strftime("%Y-%m-%d %H:%M:%S")  # Formata a data
        cadastros.append({"nome": input_nome.value, 
                        "salario": input_salario.value, 
                        "datainsercao": datainsercao})  # Adiciona as novas informações
        input_nome.value = ""
        input_salario.value = ""
        atualizar_tabela(ordenacao=ordenacao_combo.value)  # Atualiza a tabela
        show_message("Funcionário cadastrado com sucesso!")

    ordenacao_combo = Dropdown(
        label="Ordenar por:",
        options=[
            dropdown.Option("Nome"),
            dropdown.Option("Salário"),
            dropdown.Option("Data Inserção"),  # Opção para ordenar por Data Inserção
        ],
        value="Nome",
        on_change=lambda e: atualizar_tabela(ordenacao=e.control.value)
    )

    def logout(e):
        # Fecha a janela atual
        page.window.close()
        # Chama main.py passando o tema atual
        os.system(f'python main.py {str(is_dark_mode)}')

    # Função para alternar o tema
    def toggle_theme(e):
        global is_dark_mode
        is_dark_mode = not is_dark_mode  # Alterna entre True e False
        page.theme_mode = "dark" if is_dark_mode else "light"  # Alterna o tema

        # Atualiza o ícone no botão
        toggle_button.controls[0].icon = icons.DARK_MODE if is_dark_mode else icons.WB_SUNNY_OUTLINED

        page.update()  # Atualiza a página para refletir a mudança

    # Botão para alternar tema
    toggle_button = Row(
        controls=[
            IconButton(
                icon=icons.WB_SUNNY_OUTLINED if not is_dark_mode else icons.DARK_MODE,
                tooltip="Alternar Tema",
                on_click=toggle_theme  # Executa toggle_theme ao clicar no ícone
            ),
            GestureDetector(
                content=Text("Alternar Tema"),  # Usando GestureDetector para o texto
                on_tap=toggle_theme  # Executa toggle_theme ao clicar no texto
            )
        ],
        spacing=5  # Espaço entre o ícone e o texto
    )

    def update_container(selected_index):
        global grafico_img, ordenacao_combo, dados_text, tabela

        page.controls.clear()  # Limpa os controles da página

        if selected_index == 0:
            global input_nome, input_salario
            input_nome = TextField(label="Nome", width=300)
            input_salario = TextField(label="Salário", width=300)
            botao_cadastrar = ElevatedButton("Cadastrar Funcionário", on_click=cadastrar)

            container = Column([
                Text("Cadastro de Funcionários"),
                input_nome,
                input_salario,
                botao_cadastrar
            ], spacing=10)

        elif selected_index == 1:
            container = Column([
                Text("Listagem de Funcionários"),
                Row([ordenacao_combo]),
                tabela  # Agora estamos adicionando a tabela de dados
            ], spacing=10)

            atualizar_tabela(ordenacao=ordenacao_combo.value)


        elif selected_index == 2:
            grafico_selecionado = Dropdown(
                label="Selecione o Tipo de Gráfico",
                options=[
                    dropdown.Option("Barras"),
                    dropdown.Option("Colunas"),
                    dropdown.Option("Linhas"),
                    dropdown.Option("Setor"),
                    dropdown.Option("Área")
                ],
                on_change=lambda e: atualizar_grafico_por_tipo(e.control.value, ordenacao_combo.value)
            )

            grafico_img = Image()
            ordenacao_combo = Dropdown(
                label="Ordenar por:",
                options=[
                    dropdown.Option("Nome"),
                    dropdown.Option("Salário"),
                    dropdown.Option("Data Inserção"),  # Opção para ordenar por Data Inserção
                ],
                value="Nome",
                on_change=lambda e: atualizar_grafico_por_tipo(grafico_selecionado.value, e.control.value),
                visible=False
            )

            dados_text = Text("")  # Mostra dados adicionais

            container = Column([
                Text("Gráficos de Salários"),
                grafico_selecionado,
                grafico_img,
                ordenacao_combo,
                dados_text
            ], spacing=10)

        elif selected_index == 3:
            container = Column([
                toggle_button,
                ElevatedButton("Logout", on_click=logout)  # Botão de Logout
            ], spacing=10)

        page.add(
            Row(
                [
                    rail,
                    VerticalDivider(width=1),
                    Column(
                        [
                            container  # Adiciona o container selecionado
                        ],
                        expand=True,
                        alignment="center",
                        scroll=True  
                    )
                ],
                expand=True,
                alignment="center"
            )
        )

    rail = NavigationRail(
        selected_index=0,
        min_width=100,
        min_extended_width=200,
        label_type=NavigationRailLabelType.ALL,
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(icon=icons.PERSON_ADD, label="Cadastro Funcionários"),
            NavigationRailDestination(icon=icons.LIST, label="Listagem Funcionários"),
            NavigationRailDestination(icon=icons.BAR_CHART, label="Dados Funcionários"),
            NavigationRailDestination(icon=icons.SETTINGS_OUTLINED, label="Configurações"),
        ],
        on_change=lambda e: update_container(e.control.selected_index),
    )

    page.add(rail)
    update_container(0)

# Inicializando o aplicativo
app(target=main)
