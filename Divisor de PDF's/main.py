import PySimpleGUI as sg
from modulos import gerar_arquivos
sg.theme('BluePurple')   #  DarkBlue4,LightPurple Add a touch of color
# All the stuff inside your window.
fonte=("Arail","12")
# [sg.Column(col_interior, element_justification='c', size=(500, 300), background_color='red')]
layout_column = [  [sg.T("")],
          [sg.Text("Selecione o Arquivo: ",font=fonte)], [sg.Input(readonly=True, size=(70,3)), sg.FileBrowse("Procurar",key="-IN-",font=fonte)],
          [sg.T("")],
            [sg.Text('Informe os intervalos para dividir o arquivo',font=fonte)], [sg.InputText(font=fonte)],
            [sg.Text('Intervalos para unir',font=fonte)],[sg.InputText(font=fonte)],
            [sg.T("")],
            [sg.Button('Ok',font=fonte), sg.Button('Limpar',font=fonte), sg.Button('Fechar',font=fonte)] ]
layout = [[sg.Column(layout_column, element_justification='c')]]
# Create the Window
window = sg.Window('Divisor de Arquivos', layout,size=(620,320) )
# Event Loop to process "events" and get the "values" of the inputs
#print(sg.theme_list())
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Fechar': # if user closes window or clicks cancel
        break
    elif event == 'Limpar': # Limpa os dados do formulário
        for i in range(3):
            window[i]('')
    elif event == 'Ok':
        #print(len(values))
        local_arquivo = values[0]
        if local_arquivo:
            intervalos = values[1].split(";")
            unir = values[2].split(",")
            #print(intervalos)
            if intervalos != ['']:
                gerar_arquivos(local_arquivo,intervalos,unir)
                sg.popup_ok(f"Os Arquivos Foram Criados com Sucesso", title="Operção Finalizada", keep_on_top=True)
                for i in range(3):
                    window[i]('')
            else:
                sg.popup_error(f"Nenhum intervalo de divisão foi informado", title="Erro no Formulário",
                               keep_on_top=True)
        else:
            sg.popup_error(f"Nenhum arquivo foi selecionado", title="Erro no Formulário", keep_on_top=True)

window.close()
