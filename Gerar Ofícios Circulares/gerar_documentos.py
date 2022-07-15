import docx
import csv
from tkinter.filedialog import askopenfilename 
from docx.shared import Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from gtk_dialog import open_file_dialog

filtros_arquivos = {'.csv':'text/csv'}

diretorio_csv = open_file_dialog(filtros_arquivos,titulo="Selecione a planilha") 
if diretorio_csv:
    csv_file = open(diretorio_csv, encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter=',')
else:
    print("Operação cancelada")
    exit()
       
lista = []
numero = 541

for row in csv_reader:
	if row[1] == "Nome" or row[1] == "":
		continue
	lista.append({"[numero]":f"OFÍCIO  N° {numero}","[nome]": row[1],"[vocativo_endereço]":row[0],"[cargo]":row[2],
"[vocativo_cargo]":row[3],"[vocativo_corpo]":row[4],"[fecho]":row[5]
		})
	numero+=1

filtros_arquivos = {'.docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
local = open_file_dialog(filtros_arquivos,titulo="Selecione o documento Base")

if not local:
    print("Operação cancelada")
    exit()


for destinatario in lista:
	arquivo = local
	nome_arquivo= str(arquivo).split("/")[-1]
	local_savamento = str(arquivo).replace(nome_arquivo,"")

	doc = docx.Document(arquivo)
	style = doc.styles['Normal']
	font = style.font
	font.name = 'Carlito'
	font.size = Pt(12)

	for busca in destinatario.keys():
		for paragrafo in doc.paragraphs:
			if busca in paragrafo.text:
				paragrafo.text = paragrafo.text.replace(busca,destinatario[busca])
				
	doc.save(local_savamento+destinatario["[nome]"]+".docx")
	
