import re
import csv
import io
import streamlit as st

def txt_para_csv(text):
    lines = text.splitlines()

    with open('conversas.csv', mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
      
        csv_writer.writerow(['Data', 'Hora', 'Usuario', 'Mensagem'])

      
        csv_content = "Data, Hora, Usuario, Mensagem\n"

        for line in lines:
            match = re.match(r"(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.*?): (.*)", line)

            if match:
                data = match.group(1)
                hora = match.group(2)
                usuario = match.group(3)
                mensagem = match.group(4)

                
                csv_writer.writerow([data, hora, usuario, mensagem])

               
                csv_content += f"{data}, {hora}, {usuario}, {mensagem}\n"


    return csv_content
