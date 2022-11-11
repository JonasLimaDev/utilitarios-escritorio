import gi
from gerador_documento import inserir_imagens
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


CONFIG = {"4.5 x 4.5":{"grade":4,"largura_imagem":4.5,"altura_imagem":4.5,"centralizar":False,"margin":True,"legenda":False},
"4.5 x 6":{"grade":4,"largura_imagem":4.5,"altura_imagem":6,"centralizar":True,"margin":True,"legenda":False},
"5 X 6.5":{"grade":3,"largura_imagem":5,"altura_imagem":6.5,"centralizar":True,"margin":False,"legenda":False},
"5 x 7":{"grade":3,"largura_imagem":5,"altura_imagem":7,"centralizar":True,"margin":False,"legenda":False},
"6 x 6":{"grade":3,"largura_imagem":6,"altura_imagem":6,"centralizar":True,"margin":True,"legenda":False},
"7 x 5":{"grade":2,"largura_imagem":7,"altura_imagem":5,"centralizar":True,"margin":False,"legenda":False}
}

class ButtonWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Inserir Fotos em DOCX")

        self.set_border_width(40) # margem dos objetos
        try:
            self.set_icon_from_file("./logo-img-in-docx.ico")
        except:
            pass

        self.set_default_size(250, 80) # tamnaho da janela
        self.set_resizable(False) # desabilita o redimensionamento da janela

        self.files_list = None
        self.state_legenda= False
        lista_botoes = []

        self.opcao_ativa = "4.5 x 4.5"

        button_click = Gtk.Button.new_with_label("Gerar Arquivo")
        button_click.connect("clicked", self.on_click_me_clicked)
        # opções de dimensionamento para criar os botões
        lista_opcoes = ["4.5 x 4.5","4.5 x 6","5 X 6.5","5 x 7","6 x 6","7 x 5"]
        for opcao in lista_opcoes:
            """
            Cria uma objetos de botões radio e adiciona em uma lista
            """
            if not lista_botoes:
                button = Gtk.RadioButton.new_with_label_from_widget(None, f"{opcao}")
                button.connect("toggled", self.on_button_toggled, f"{opcao}")
            else:
                button = Gtk.RadioButton.new_with_label_from_widget(lista_botoes[0], f"{opcao}")
                button.connect("toggled", self.on_button_toggled, f"{opcao}")

            lista_botoes.append(button)

        dimesao = Gtk.Label(label="Dimensão das Fotos (cm)")
        label = Gtk.Label(label="")
        span = Gtk.Label(label="")
        span2 = Gtk.Label(label="")
        buttonFile = Gtk.Button(label="Escolha os Arquivos")
        buttonFile.set_label("Selecionar Fotos")
        buttonFile.connect("clicked", self.on_file_clicked)
        # # box.add(button1)

        legenda = Gtk.Label(label="Legenda")
        switch = Gtk.Switch()
        switch.connect("notify::active", self.on_switch_activated)
        switch.set_active(False)

        grid = Gtk.Grid()

        position = 1
        # grid.add(dimesao)
        grid.attach(dimesao, 1, 0, 1, 1)
        #adicionaos botões da lista no grid
        for botao in lista_botoes:
            grid.attach(botao, 1, position, 2, 1)
            position+=1

        grid.attach(span2, 1, position+1, 1, 1)
        grid.attach_next_to(legenda, span2,Gtk.PositionType.BOTTOM,1, 1)
        grid.attach_next_to(switch,legenda, Gtk.PositionType.RIGHT,1, 1)

        grid.attach_next_to(label,  legenda,Gtk.PositionType.BOTTOM,1, 1)
        grid.attach_next_to(buttonFile, label,Gtk.PositionType.BOTTOM,2, 1)
        grid.attach_next_to(span, buttonFile,Gtk.PositionType.BOTTOM,1, 1)
        grid.attach_next_to(button_click, span ,Gtk.PositionType.BOTTOM,2, 1)

        self.add(grid)


        # hbox.pack_start(switch, True, True, 0)

    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
            self.state_legenda = True

        else:
            state = "off"
            self.state_legenda = False
        print(self.state_legenda)


    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Selecione as Fotos que irá usar", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )
        dialog.set_select_multiple(True)
        dialog.set_default_size(800, 400)
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            # print("File selected: " + dialog.get_filenames())
            self.files_list = dialog.get_filenames()
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()

    def add_filters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Imagens")
        filter_image.add_mime_type("image/jpeg")#
        filter_image.add_mime_type("image/png")
        dialog.add_filter(filter_image)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)



    def alert_finished_process(self):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="O Processo Foi Finalizado",
        )

        dialog.format_secondary_text(
            "O processo terminou e o arquivo foi criado com sucesso."
        )
        dialog.run()

        dialog.destroy()


    def alert_fall_process(self,falha):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="O Processo Não Foi Execultado",
        )

        dialog.format_secondary_text(
            f"O processo NÃO Foi Executado!!\n\nMotivo:\n{falha}"
        )
        dialog.run()
        print("INFO dialog closed")

        dialog.destroy()



    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
            self.opcao_ativa = name
        else:
            state = "off"
        print("Button", name, "was turned", state)


    def on_click_me_clicked(self, button):
        print('"Click me" button was clicked')
        # print(self.files_list)
        print(f"botão ativo: {self.opcao_ativa}")
        # print(self.files_list)
        if self.files_list:
            self.alert_finished_process()
            CONFIG[self.opcao_ativa]["legenda"]=self.state_legenda
            print(CONFIG[self.opcao_ativa]["legenda"])
            inserir_imagens(self.files_list,CONFIG[self.opcao_ativa])
            #limpa os arquivos selecionados ao fim do processo
            self.files_list = None
        else:
            self.alert_fall_process("Nenhuma Imagem Foi Selecionada")


win = ButtonWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
