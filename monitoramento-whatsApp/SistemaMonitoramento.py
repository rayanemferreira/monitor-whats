import streamlit as st
from PIL import Image
from streamlit_echarts import st_pyecharts
from Grafico import grafico_horas_mais_movimentadas_por_dia,grafico_linha, grafico_semanal, gerar_grafico_interacoes_por_remetente, grafico_emojis_top_5
from Transformador_csv import txt_para_csv
from Styles import apply_styles
from Processamento import datas_mais_movimentadas, movimentacao_semanal, top_emojis

import warnings


warnings.filterwarnings("ignore")

# Inicializa uma flag global no session_state
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


 
 
    # Inicializa uma flag global no session_state
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False

    # Se ainda não fez upload, mostra o uploader
    if not st.session_state.file_uploaded:
        st.title("Upload de Arquivo")
        uploaded_file = st.file_uploader("Escolha um arquivo", type=["txt"])

        # Quando o arquivo for enviado, ativa a flag
        if uploaded_file is not None:
            st.session_state.file_uploaded = True
            st.session_state.uploaded_file = uploaded_file
            st.rerun()  # Atualiza a tela para esconder o uploader
    else:
        # Quando já tiver feito upload, mostra o conteúdo
        st.title("Arquivo Carregado com Sucesso!")



  
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
                response_hora = datas_mais_movimentadas()  # Carrega os dados das datas mais movimentadas
                if response_hora:
                    line_chart_hora = grafico_linha(response_hora)
                    st_pyecharts(line_chart_hora)
 
                else:
                    st.error("Dados de datas mais movimentadas não encontrados.")
            except Exception as e:
                st.error(f"Erro ao carregar dados de mensagens por data: {str(e)}")

            st.header("Mensagens semanais")
            try:
                response_semana = movimentacao_semanal()  # Carrega os dados de movimentação semanal
                if response_semana:
                    bar_chart_semana = grafico_semanal(response_semana)
                    st_pyecharts(bar_chart_semana)
                else:
                    st.error("Dados de semana não encontrados.")
            except Exception as e:
                st.error(f"Erro ao carregar dados de mensagens por semana: {e}")

        
            try:
                dados_emoji = top_emojis()  # Carrega os dados de emojis
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
                        st.header("Engajamento do grupo")
                        response_hora = datas_mais_movimentadas()
                        if response_hora:
                            line_chart_hora = grafico_horas_mais_movimentadas_por_dia(response_hora)
                            st_pyecharts(line_chart_hora)
                        else:
                            st.error("Dados de datas mais movimentadas não encontrados.")
                else:
                    st.error("Erro ao processar os dados de emojis.")
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")

        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")







    # if not st.session_state.file_flag:
     

    #     st.markdown('<h1 class="title">Monitoramento do WhatsApp</h1>', unsafe_allow_html=True)
        
    #     # Exibe o carregamento enquanto o arquivo não for carregado
    #     uploaded_file = st.file_uploader("Escolha um arquivo txt", type=["txt"]),

    #     if uploaded_file is None:
    #         # Exibe apenas a tela inicial de carregamento de arquivo
    #         st.warning("Por favor, faça o upload de um arquivo TXT para começar.")
    #     else:
    #         st.session_state.file_uploaded=uploaded_file
 
    # else:
        # Quando já tiver feito upload, mostra o conteúdo
         
         
            
      





 

dashboard_whatsapp()