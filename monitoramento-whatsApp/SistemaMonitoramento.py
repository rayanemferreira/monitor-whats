import streamlit as st
from PIL import Image
from streamlit_echarts import st_pyecharts
from Grafico import grafico_horas_mais_movimentadas_por_data_especifica,grafico_linha, grafico_semanal, gerar_grafico_interacoes_por_remetente, grafico_emojis_top_5
from Transformador_csv import txt_para_csv
from Styles import apply_styles
from Processamento import datas_mais_movimentadas, movimentacao_semanal, top_emojis, horas_mais_movimentadas
import warnings

warnings.filterwarnings("ignore")

if 'file_flag' not in st.session_state:
    st.session_state.file_flag = False

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = None  

st.set_page_config(
    page_title="Monitoramento do WhatsApp",
    layout="wide",
)


def dashboard_whatsapp():
    apply_styles()

  
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False

    if not st.session_state.file_uploaded:
        st.markdown("<h1 style='text-align: center;'>Monitoramento do WhatsApp</h1>",
        unsafe_allow_html=True)
       
        uploaded_file = st.file_uploader("Escolha um arquivo", type=["txt"])

        if uploaded_file is not None:
            st.session_state.file_uploaded = True
            st.session_state.uploaded_file = uploaded_file
            st.rerun() 
    else:
        
        st.title("Analise dos dados")



  
        if st.session_state.file_uploaded  is not None:
            st.session_state.file_flag = True

        try:
            
            text = st.session_state.uploaded_file.read().decode("utf-8")
            csv_content = txt_para_csv(text) 


        
            image = Image.open("usuario_editado.png")
            image_resized = image.resize((290, 274))
            st.image(image_resized, caption="Nome do Usuário")


            
            st.header("Engajamento mensal do grupo ")
            try:
                response_hora = datas_mais_movimentadas()  
                if response_hora:
                    line_chart_hora = grafico_linha(response_hora)
                    st_pyecharts(line_chart_hora)
 
                else:
                    st.error("Dados de datas mais movimentadas não encontrados.")
            except Exception as e:
                st.error(f"Erro ao carregar dados de mensagens por data: {str(e)}")

            st.header("Mensagens semanais")
            try:
                response_semana = movimentacao_semanal()  
                if response_semana:
                    bar_chart_semana = grafico_semanal(response_semana)
                    st_pyecharts(bar_chart_semana)
                else:
                    st.error("Dados de semana não encontrados.")
            except Exception as e:
                st.error(f"Erro ao carregar dados de mensagens por semana: {e}")

        
            try:
                dados_emoji = top_emojis()  
                if 'Mensagem' in dados_emoji:
                    mensagens_por_usuario = dados_emoji
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.header("Emoji mais utilizados")
                        bar_chart_remetente = grafico_emojis_top_5(mensagens_por_usuario)
                        if bar_chart_remetente:
                            st_pyecharts(bar_chart_remetente)
                        else:
                            st.error("Erro ao gerar gráfico de emojis.")

                    with col2:
                        st.header("Horas mais movimentadas")
                        response_hora = horas_mais_movimentadas('27/06/2022')
                        if response_hora:
                            line_chart_hora = grafico_horas_mais_movimentadas_por_data_especifica(response_hora)
                            st_pyecharts(line_chart_hora)
                        else:
                            st.error("Dados de datas mais movimentadas não encontrados.")
                else:
                    st.error("Erro ao processar os dados de emojis.")
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")

        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")


 

dashboard_whatsapp()