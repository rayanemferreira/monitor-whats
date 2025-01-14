import streamlit as st
import requests
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

API_HORA_URL = "http://localhost:8000/hora_com_mais_mensagens"
API_REMETENTE_URL = "http://localhost:8000/pessoas_mais_interagem"

def dashboard_whatsapp():
    st.title("Monitoramento do WhatsApp")

    st.header("Mensagens por Hora")
    # response_hora = requests.get(API_HORA_URL)
    response_hora = {'status_code':200,'hora_com_mais_mensagens': {'hora': 12, 'quantidade_mensagens': 27}, 'mensagens_por_hora': {10: 3, 12: 27, 13: 2, 14: 13, 15: 19, 16: 14, 17: 19, 18: 5, 19: 7, 20: 4, 21: 2, 22: 2}}
    # if response_hora.status_code == 200:
    if 1:
    
        dados_hora = response_hora #.json()

        if "mensagens_por_hora" in dados_hora:
            mensagens_por_hora = dados_hora["mensagens_por_hora"]
            bar_chart_hora = gerar_grafico_horas_com_mais_mensagens(mensagens_por_hora)
            st_pyecharts(bar_chart_hora)
        else:
            st.error("Dados de mensagens por hora não encontrados.")
    else:
        st.error(f"Erro ao carregar dados de mensagens por hora: {response_hora.status_code}")

    st.header("Interações por Usuario")
    # response_remetente = requests.get(API_REMETENTE_URL)
    response_remetente={'status_code':200,'usuario_mais_interacoes': {'usuario': ' Jackson', 'quantidade_interacoes': 13}, 'mensagens_por_usuario': {' Jackson': 13, ' +55 92 8467-6967': 12, ' +55 92 9472-8849': 9, ' +55 92 9465-6458': 8, ' +55 92 8471-0377': 7, ' +55 92 8216-5881': 7, ' Prof Marcela': 6, ' +55 92 8131-9982': 5, ' +55 92 8826-9491': 5, ' +55 92 8261-8754': 4, ' +55 92 9104-6440': 3, ' +55 92 8247-2041': 3, ' +55 92 8457-0207': 3, ' +55 92 8111-2310': 3, ' +55 92 8447-3035': 2, ' +55 92 8582-6530': 2, ' +55 92 9113-2808': 2, ' +55 92 9499-8837': 2, ' +55 92 8413-1864': 2, ' +55 92 9244-8687': 2, ' +55 92 9151-6646': 2, ' +55 92 8402-8408': 2, ' Gordinho': 2, ' +55 92 8404-0783': 1, ' Guilherme': 1, ' +55 92 9236-5943': 1, ' +55 97 8412-4499': 1, ' +55 92 8291-5304': 1, ' +55 92 9501-4742': 1, ' +55 92 8419-7189': 1, ' +55 92 9331-6807': 1, ' +55 92 8469-5287': 1, ' +55 92 9187-1406': 1, ' +55 92 9225-2762': 1}}
    if 1:
    # if response_remetente.status_code == 200:
        dados_remetente = response_remetente#.json()

        if "mensagens_por_usuario" in dados_remetente:
            mensagens_por_usuario = dados_remetente["mensagens_por_usuario"]
            bar_chart_remetente = gerar_grafico_interacoes_por_remetente(mensagens_por_usuario)
            st_pyecharts(bar_chart_remetente)
        else:
            st.error("Dados de interações por remetente não encontrados.")
    else:
        st.error(f"Erro ao carregar dados de interações por remetente: {response_remetente.status_code}")

def gerar_grafico_horas_com_mais_mensagens(mensagens_por_hora):
    # distribuicao_horas = {str(hora): mensagens_por_hora.get(str(hora), 0) for hora in range(24)}  
  
    distribuicao_horas={}
    for hora in mensagens_por_hora.keys():
        distribuicao_horas[str(hora)] = mensagens_por_hora[hora]
  
    bar = (
        Bar()
        .add_xaxis(list(distribuicao_horas.keys()))
        .add_yaxis(" Quantidade de Mensagens", list(distribuicao_horas.values()))
        .set_global_opts(
            #title_opts=opts.TitleOpts(title="Mensagens por Hora"),
            xaxis_opts=opts.AxisOpts(name="Hora", type_="category"),
            yaxis_opts=opts.AxisOpts(name="Quant. de Mensagens"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )
    return bar

def gerar_grafico_interacoes_por_remetente(mensagens_por_usuario):
    mensagens_por_usuario = dict(sorted(mensagens_por_usuario.items(), key=lambda item: item[1], reverse=True)[:4])
    remetentes = list(mensagens_por_usuario.keys())
    quantidades = list(mensagens_por_usuario.values())

    bar = (
        Bar()
        .add_xaxis(remetentes)
        .add_yaxis("Quantidade de Mensagens", quantidades)
        .set_global_opts(
            #title_opts=opts.TitleOpts(title="Interações por Usuario"),
            xaxis_opts=opts.AxisOpts(name="Mensagens", type_="value"),
            yaxis_opts=opts.AxisOpts(name="Usuario", type_="category", axislabel_opts={"rotate": 0}),
        )
        .reversal_axis()
    )
    return bar

if __name__ == "__main__":
    dashboard_whatsapp()