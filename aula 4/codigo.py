import flet as ft

# função principal que será executada ao iniciar o programa
def main(pagina):
    pagina.title = "AngáChat"  # define o título da página no navegador
    texto = ft.Text("AngáChat", size=30, weight=ft.FontWeight.BOLD, font_family="Cursive")

    # cria a coluna onde as mensagens vão aparecer e define que ela terá o scroll
    chat = ft.Column(scroll=ft.ScrollMode.ALWAYS)

    # cria o container que vai envolver a coluna de chat
    chat_container = ft.Container(
        content=chat,  # conteúdo da caixa de chat será a coluna 'chat'
        padding=ft.Padding(top=10, right=10, bottom=10, left=10),  # espaço interno do container
        border=ft.border.all(2, ft.colors.BLUE_GREY_500),  # borda do container
        border_radius=10,  # bordas arredondadas
        width=300,  # largura do container de chat
        height=400,  # altura do container de chat
        bgcolor=ft.colors.LIGHT_GREEN_50,  # cor de fundo do container
        margin=ft.Margin(10, 10, 10, 10)  # margem ao redor do container
    )

    nome_usuario = ft.TextField(label="Escreva seu nome")

    cor_usuario = ft.Dropdown(
        label="Escolha uma cor para suas mensagens",
        options=[
            ft.dropdown.Option("black", text="Preto"),
            ft.dropdown.Option("blue", text="Azul"),
            ft.dropdown.Option("green", text="Verde"),
            ft.dropdown.Option("pink", text="Rosa")
        ]
    )

    # mensagens de erro para nome de usuário e mensagem
    nome_usuario_error = ft.Text("", color=ft.colors.RED, size=12)
    campo_mensagem_error = ft.Text("", color=ft.colors.RED, size=12)

    # função que é chamada quando uma mensagem é enviada
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]  # tipo da mensagem (mensagem ou entrada)
        cor_mensagem = mensagem.get("cor", "black")  # cor da mensagem, se não for definida será preta
        if tipo == "mensagem":  # se for uma mensagem
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]

            # adiciona a mensagem ao chat
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}", color=cor_mensagem))

            # remove a primeira mensagem se o número de mensagens exceder o limite
            if len(chat.controls) > 99:
                chat.controls.pop(0)

        else:
            usuario_mensagem = mensagem["usuario"]
            # mensagem indicando que o usuário entrou no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", 
                                         size=12, italic=True, color=cor_mensagem))

        pagina.update()  # atualiza a página

    # inscreve a função para receber as mensagens
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    # função para enviar mensagem
    def enviar_mensagem(evento):
        nome_usuario_error.value = ""
        campo_mensagem_error.value = ""
        
        # verifica se o nome do usuário foi preenchido
        if not nome_usuario.value.strip():
            nome_usuario_error.value = "Por favor, digite seu nome para entrar no chat."
        
        # verifica se o campo de mensagem foi preenchido
        if not campo_mensagem.value.strip():
            campo_mensagem_error.value = "Por favor, digite uma mensagem antes de enviar."
        
        # se houver erro, não envia a mensagem
        if nome_usuario_error.value or campo_mensagem_error.value:
            pagina.update()
            return

        # envia a mensagem para todos os inscritos no pubsub
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value,
                                "cor": cor_usuario.value, "tipo": "mensagem"})
        campo_mensagem.value = ""  # limpa o campo de mensagem
        pagina.update()

    # campo para digitar a mensagem
    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)

    # botão para enviar a mensagem
    botao_enviar_mensagem = ft.ElevatedButton(
        "Enviar", on_click=enviar_mensagem,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_900,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(left=20, top=10, right=20, bottom=10)
        )
    )

    # função para abrir o popup de entrada
    def entrar_popup(evento):
        # verifica se o nome de usuário foi preenchido
        if not nome_usuario.value.strip():
            nome_usuario_error.value = "Por favor, digite seu nome para entrar no chat."
            pagina.update()
            return

        # envia a entrada do usuário para o pubsub (canal)
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "cor": cor_usuario.value, "tipo": "entrada"})
        pagina.add(chat_container)  # adiciona o container do chat na página
        popup.open = False  # fecha o popup
        pagina.remove(botao_iniciar)  # remove o botão de iniciar
        pagina.remove(texto)  # remove o título do chat
        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem]))  # adiciona os campos de mensagem
        pagina.update()

    # cria o popup de boas-vindas
    popup = ft.AlertDialog(
        open=False,  # popup inicialmente fechado
        modal=True,  # modal = resto da página fica bloqueado até o popup ser fechado
        title=ft.Text("Bem-vindo ao AngáChat"),
        content=ft.Column([nome_usuario, cor_usuario]),  # conteúdo do popup (nome e cor do usuário)
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],  # botão para entrar no chat
    )

    # função para abrir o popup de boas-vindas
    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True  # abre o popup
        pagina.update()

    # botão para iniciar o chat
    botao_iniciar = ft.ElevatedButton(
        "Iniciar chat", on_click=entrar_chat,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN_900,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(left=20, top=10, right=20, bottom=10)
        )
    )

    # adiciona o título e o botão para iniciar o chat na página
    pagina.add(texto)
    pagina.add(botao_iniciar)

    # adiciona as mensagens de erro abaixo dos campos de entrada
    pagina.add(nome_usuario_error)
    pagina.add(campo_mensagem_error)

# inicializa o aplicativo Flet no navegador
print("Página aberta no navegador: http://localhost:8000")
ft.app(target=main, view=ft.WEB_BROWSER, port=8000)