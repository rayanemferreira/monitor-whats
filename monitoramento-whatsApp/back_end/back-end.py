import pandas as pd
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

CONVERSAS_CSV = 'conversas.csv'
PRODUTOS_CSV = 'produtos.csv'

def load_conversas_data() -> pd.DataFrame:
    """Carrega as conversas do arquivo conversas.csv."""
    if os.path.exists(CONVERSAS_CSV):
        data = pd.read_csv(CONVERSAS_CSV, delimiter=';') 
        data.columns = data.columns.str.strip().str.replace('"', '')  
        required_columns = ['Data','Hora','Remetente','Mensagem']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"O arquivo CSV de conversas deve conter as colunas: {', '.join(required_columns)}.")
        return data
    else:
        return pd.DataFrame(columns=['Data', 'Hora', 'Remetente', 'Mensagem'])


@app.get("/conversas")
def get_conversas():
    data = load_conversas_data()
    if data.empty:
        raise HTTPException(status_code=404, detail="Nenhuma conversa encontrada.")
    return data.to_dict(orient="records")


@app.get("/hora_com_mais_mensagens")
def hora_com_mais_mensagens():
   
    data = load_conversas_data() 

    if data.empty:
        raise HTTPException(status_code=404, detail="Nenhuma conversa encontrada.")
    
    
    data['Hora'] = pd.to_datetime(data['Hora'], errors='coerce').dt.hour
    
  
    if data['Hora'].isnull().any():
        raise HTTPException(status_code=400, detail="Existem horários inválidos na base de dados.")
    
   
    mensagens_por_hora = data['Hora'].value_counts().sort_index(ascending=True)
    
    if mensagens_por_hora.empty:
        raise HTTPException(status_code=404, detail="Não foi possível calcular a hora com mais mensagens.")
    
    hora_mais_mensagens = int(mensagens_por_hora.idxmax())  
    quantidade_mensagens = int(mensagens_por_hora.max())  
    
    
    mensagens_por_hora_dict = mensagens_por_hora.to_dict()  
    
    print(mensagens_por_hora_dict)
  
    return {
        "hora_com_mais_mensagens": {
            "hora": hora_mais_mensagens,
            "quantidade_mensagens": quantidade_mensagens
            
        },
        "mensagens_por_hora": mensagens_por_hora_dict  
    }


@app.get("/pessoas_mais_interagem")
def pessoas_mais_interagem():
    data = load_conversas_data()

    if data.empty:
        raise HTTPException(status_code=404, detail="Nenhuma conversa encontrada.")

    if "Remetente" not in data.columns:
        raise HTTPException(status_code=400, detail="A coluna 'Remetente' está ausente na base de dados.")

    # Contar mensagens por remetente
    mensagens_por_usuario = data["Remetente"].value_counts()

    if mensagens_por_usuario.empty:
        raise HTTPException(status_code=404, detail="Não foi possível calcular as interações por remetente.")

    usuario_mais_interacoes = mensagens_por_usuario.idxmax()
    quantidade_interacoes = mensagens_por_usuario.max()

    mensagens_por_usuario_dict = mensagens_por_usuario.to_dict()

    return {
        "usuario_mais_interacoes": {
            "usuario": usuario_mais_interacoes,
            "quantidade_interacoes": int(quantidade_interacoes)
        },
        "mensagens_por_usuario": mensagens_por_usuario_dict
    }
