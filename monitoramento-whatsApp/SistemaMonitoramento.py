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
    response_hora = requests.get(API_HORA_URL)

    if response_hora.status_code == 200:
        dados_hora = response_hora.json()

        if "mensagens_por_hora" in dados_hora:
            mensagens_por_hora = dados_hora["mensagens_por_hora"]
            bar_chart_hora = gerar_grafico_horas_com_mais_mensagens(mensagens_por_hora)
            st_pyecharts(bar_chart_hora)
        else:
            st.error("Dados de mensagens por hora não encontrados.")
    else:
        st.error(f"Erro ao carregar dados de mensagens por hora: {response_hora.status_code}")

    st.header("Interações por Usuario")
    response_remetente = requests.get(API_REMETENTE_URL)

    if response_remetente.status_code == 200:
        dados_remetente = response_remetente.json()

        if "mensagens_por_usuario" in dados_remetente:
            mensagens_por_usuario = dados_remetente["mensagens_por_usuario"]
            bar_chart_remetente = gerar_grafico_interacoes_por_remetente(mensagens_por_usuario)
            st_pyecharts(bar_chart_remetente)
        else:
            st.error("Dados de interações por remetente não encontrados.")
    else:
        st.error(f"Erro ao carregar dados de interações por remetente: {response_remetente.status_code}")

def gerar_grafico_horas_com_mais_mensagens(mensagens_por_hora):
    distribuicao_horas = {str(hora): mensagens_por_hora.get(str(hora), 0) for hora in range(24)}  

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