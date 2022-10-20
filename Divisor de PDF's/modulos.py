import PyPDF2
from pathlib import Path


def criar_arquivo_pdf(objeto_leitura,intervalo_inicial,intervalo_final,nome_arquivo,pasta):
    pagina = intervalo_inicial
    #cria o objeto de escrita que vai gerar o novo arquivo
    objeto_escrita = PyPDF2.PdfFileWriter()
    while pagina <= intervalo_final:
        #adiciona as páginas do intervalo ao objeto de escrita
        objeto_escrita.addPage(objeto_leitura.getPage(pagina))
        pagina +=1
    #cria um novo arquivo
    novo_arquivo = open(f'{pasta}{nome_arquivo}', 'wb')
    #escreve o conteúdo das página no novo arquivo
    objeto_escrita.write(novo_arquivo)
    #fecha o arquivo
    novo_arquivo.close()



def unificar_arquivos(lista_arquivos,nome_arquivo,pasta):
    mergeFile = PyPDF2.PdfFileMerger()
    print("aqui")
    novo_arquivo = open(f"{pasta}/arquivos/unificado_{nome_arquivo}.pdf", 'wb')
    for arquivo in lista_arquivos:
        print(arquivo)
        # objeto_pdf = open(arquivo, 'rb')
        # pdfReader = PyPDF2.PdfFileReader(PyPDF2.PdfFileReader(_pdf, 'rb'))
        mergeFile.append(PyPDF2.PdfFileReader(arquivo, 'rb'))
        # print(file)
    mergeFile.write(f"{pasta}/arquivos/unificado_{nome_arquivo}.pdf")



def pegar_pasta(diretorio):
    arquivo = diretorio.split('/')[-1]
    pasta = diretorio.replace(arquivo,"")
    return pasta,arquivo.split('.')[0]


def gerar_arquivos(caminho,intervalos,unir):
    pasta, nome_arquivo_origem = pegar_pasta(caminho)
    objeto_pdf = open(caminho,'rb')
    pdfReader = PyPDF2.PdfFileReader(objeto_pdf)
    Path(f"{pasta}/arquivos").mkdir(exist_ok=True)
    lista_unir = []

    for intervalo in intervalos:
        if '-' in intervalo:
            inicio, fim = intervalo.split('-')
            #print(intervalo.split('-'))
            criar_arquivo_pdf(pdfReader,int(inicio)-1,int(fim)-1,f'parte{intervalos.index(intervalo)+1}_{nome_arquivo_origem}.pdf',f"{pasta}/arquivos/")

            if unir != [''] and str(intervalos.index(intervalo)+1) in unir:
                print("add")
                lista_unir.append(f"{pasta}/arquivos/parte{intervalos.index(intervalo)+1}_{nome_arquivo_origem}.pdf")
    if unir != ['']:
        print('foi')
        unificar_arquivos(lista_unir,nome_arquivo_origem,pasta)

    objeto_pdf.close()

#print("chama")
if __name__ == "__main__":
    print("chama")
