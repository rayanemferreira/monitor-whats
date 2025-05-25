import pandas as pd
import os
import streamlit as st
import pandas as pd
import datetime
from collections import Counter
import re
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

model_path = 'svm_model1.pkl'
model = joblib.load(model_path)
CONVERSAS_CSV = '../conversas.csv'


def load_conversas_data() -> pd.DataFrame:
    if os.path.exists(CONVERSAS_CSV):
        
        data = pd.read_csv(CONVERSAS_CSV, delimiter=',')  
        print("Colunas do CSV:", data.columns)  
        data.columns = data.columns.str.strip().str.replace('"', '') 
        required_columns = ["Data", "Hora", "Usuario", "Mensagem"]
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"O arquivo CSV de conversas deve conter as colunas: {', '.join(required_columns)}.")
        return data
    else:
        return pd.DataFrame(columns=["Data", "Hora", "Usuario", "Mensagem"])


def datas_mais_movimentadas():
    try:
        data = load_conversas_data()

        if data.empty:
            raise Exception("Nenhuma conversa encontrada.")
        
        data['Data'] = pd.to_datetime(data['Data'], errors='coerce')

        if data['Data'].isnull().any():
            raise Exception("Existem datas inválidas na base de dados.")
        
        mensagens_por_data = data.groupby('Data').size().sort_values(ascending=False)
        
        if mensagens_por_data.empty:
            raise Exception("Não foi possível calcular as datas mais movimentadas.")

        top_7_datas = mensagens_por_data.head(7)
        
    
        top_7_datas_dict = top_7_datas.to_dict()
        print('top_7_datas_dict\n\n\n\n', top_7_datas_dict)

    except Exception as e:
        top_7_datas_dict={}

    return top_7_datas_dict  


 
def horas_mais_movimentadas(data_filtro):

    try:
        data = load_conversas_data()

        if data.empty:
            raise Exception("Nenhuma conversa encontrada.")
        
        # Converter a coluna 'Data' para datetime
        data['Data'] = pd.to_datetime(data['Data'], errors='coerce')

        if data['Data'].isnull().any():
            raise Exception("Existem datas inválidas na base de dados.")
        
        # Se o filtro de data foi passado, aplicar o filtro
        if data_filtro:
            data_filtro = pd.to_datetime(data_filtro, errors='coerce')
            if pd.isnull(data_filtro):
                raise Exception("Formato de data inválido para o filtro.")
            data = data[data['Data'].dt.date == data_filtro.date()]
        
        if data.empty:
            raise Exception("Nenhuma mensagem encontrada para a data filtrada.")

        # Criar nova coluna para hora
        data['Hora'] = pd.to_datetime(data['Hora'], errors='coerce').dt.hour

        # Agrupar por Hora
        mensagens_por_hora = data.groupby('Hora').size()

        if mensagens_por_hora.empty:
            raise Exception("Não foi possível calcular os horários mais movimentados.")

        # Reordenar por hora (crescente)
        mensagens_por_hora = mensagens_por_hora.sort_index()


        top_horas_dict = mensagens_por_hora.to_dict()

    except Exception as e:
        print("Erro:", e)
        top_horas_dict = {}

    return top_horas_dict

def data_top7(top_7_datas):
   
    return {
        "top_7_datas_mais_movimentadas": [
            {"data": str(data), "quantidade_mensagens": quantidade}
            for data, quantidade in top_7_datas.items()
        ]
    }


def movimentacao_semanal():
    try:
        data_semana = load_conversas_data()

        if data_semana.empty:
            raise Exception("Nenhuma conversa encontrada.")
        
        if 'Data' not in data_semana.columns:
            raise Exception("Coluna 'Data' não encontrada nos dados.")

    
        data_semana['Data'] = pd.to_datetime(data_semana['Data'], format='%d/%m/%Y', errors='coerce')


        if data_semana['Data'].isnull().any():
            raise Exception("Existem datas inválidas na base de dados.")
        
     
        data_semana['Semana'] = data_semana['Data'].dt.to_period('W').apply(lambda r: r.start_time)
        data_semana['DiaSemana'] = data_semana['Data'].dt.weekday
        print('>>>>',data_semana)

        mensagens_por_dia = data_semana.groupby(['Semana', 'DiaSemana']).size()
        print('>>>>',mensagens_por_dia)

        if mensagens_por_dia.empty:
            raise Exception("Não foi possível calcular os dados de mensagens por dia.")
     

 
        mensagens_por_semana = {}
        for (semana, dia_semana), count in mensagens_por_dia.items():
            if isinstance(semana, datetime.datetime): 
                semana_str = semana.strftime('%Y-%m-%d') 
            else:
                semana_str = datetime.datetime.fromtimestamp(semana).strftime('%Y-%m-%d')  
            
            if semana_str not in mensagens_por_semana:
                mensagens_por_semana[semana_str] = {i: 0 for i in range(7)}  
            
            mensagens_por_semana[semana_str][dia_semana] = count

       
        if not mensagens_por_semana:
            raise Exception("O dicionário de mensagens por semana está vazio ou mal formado.")
        
        
        print(mensagens_por_semana)  
 
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        
        mensagens_por_semana = {}
    
    return mensagens_por_semana




def extrair_emojis(texto):
    
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]")
    return emoji_pattern.findall(texto)

def top_emojis():
    try:
    
        data = load_conversas_data()

        if data.empty:
            raise Exception("Nenhuma conversa encontrada")
        
        
        emoji_counter = Counter()

        for mensagem in data['Mensagem']:
            emojis_na_mensagem = extrair_emojis(mensagem)
            emoji_counter.update(emojis_na_mensagem)

        if not emoji_counter:
            raise Exception("Nenhum emoji encontrado nas mensagens. ")

        
        top_5_emojis = emoji_counter.most_common(5)
        top_5_emojis_dict = {emoji: count for emoji, count in top_5_emojis}
        top_5_emojis_dict['Mensagem'] = '✨ Os 5 emojis mais usados:'

    except Exception as e:
        top_5_emojis_dict = {
            'Erro': str(e)  
        }

    return top_5_emojis_dict
    




# Função para pré-processamento de texto
def preprocess_text(text):
    stop_words = set(stopwords.words('portuguese'))
    lemmatizer = WordNetLemmatizer()

    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = re.sub(r'^b\s+', '', text)
    text = text.lower()

    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text

# Função para fazer previsão com base em um novo texto
def predict_gender(text):
    preprocessed_text = preprocess_text(text)
    prediction = model.predict([preprocessed_text])
    return prediction[0]

def chama_ia():
    genero_previsto = []
    
    data = load_conversas_data()

    
    for linha in data['Mensagem'].dropna():
        resultado = predict_gender(linha)  
        genero_previsto.append(resultado) 

        
    print("\n--- Gênero previsto para cada linha ---")
    print(genero_previsto)

    return genero_previsto




 

    

datas_mais_movimentadas()

movimentacao_semanal()

top_emojis()



