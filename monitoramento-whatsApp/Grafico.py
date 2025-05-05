from pyecharts.charts import Bar, Line
from pyecharts import options as opts
import streamlit as st



def grafico_linha(mensagens_por_data):
    datas_ordenadas = sorted(mensagens_por_data.keys())

    datas_formatadas = [date.strftime('%Y-%m-%d') for date in datas_ordenadas]

    
    mensagens_ordenadas = [mensagens_por_data[date] for date in datas_ordenadas]
    
    linha = (
        Line()
        .add_xaxis(datas_formatadas) 
        .add_yaxis("Quantidade de Mensagens", mensagens_ordenadas) 
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="Data", type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(name="Quant. de Mensagens"),
        )
    )
    return linha





def grafico_horas_mais_movimentadas_por_data_especifica(mensagens_por_hora):

    mensagens_ordenadas = dict(sorted(mensagens_por_hora.items(), key=lambda item: item[0], reverse=True))
    print('mensagens_por_hora\n\n\n\n', mensagens_ordenadas)

    x_data = list(mensagens_ordenadas.keys())
    y_data = list(mensagens_ordenadas.values())


    
    bar = (
        Bar()
        .add_xaxis([str(x) for x in x_data])  # Convertendo chaves para string
        .add_yaxis("Valores", y_data, itemstyle_opts=opts.ItemStyleOpts(color="lightcoral") )
        .reversal_axis()  # Inverte para barras horizontais
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="Quant."),
            yaxis_opts=opts.AxisOpts(name="Hora")
        )
    )
    return bar




def grafico_semanal(mensagens_por_semana):
    if not mensagens_por_semana:
        st.error("Nenhum dado de mensagens por semana encontrado.")
        return None
    
    
    semanas = list(mensagens_por_semana.keys())  
    semana_selecionada = st.selectbox("Escolha uma semana", semanas)

    mensagens_dia = mensagens_por_semana.get(semana_selecionada, {})

    if not mensagens_dia:
        st.error(f"Nenhuma mensagem registrada para a semana {semana_selecionada}.")
        return None
    
    distribuicao_dias = {str(dia): mensagens_dia.get(dia, 0) for dia in range(7)}
 
    dias_da_semana = ["Segunda", "Terça", "Quarta", "Qui", "Sex", "Sáb", "Dom"]  

    
    bar = (
        Bar()
        .add_xaxis(dias_da_semana)  
        .add_yaxis(
            "Quantidade de Mensagens", 
            list(distribuicao_dias.values()),  
            itemstyle_opts=opts.ItemStyleOpts(color="pink"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"Mensagens por Dia da Semana - {semana_selecionada}"),
            xaxis_opts=opts.AxisOpts(
                name="Dia da Semana", 
                type_="category", 
            ),
            yaxis_opts=opts.AxisOpts(name="Quant. de Mensagens"),
        )
    )
    return bar




def grafico_emojis_top_5(top_5_emojis_dict):
    try:
        
        if 'Erro' in top_5_emojis_dict:
            raise Exception(top_5_emojis_dict['Erro'])

        
        emojis = list(top_5_emojis_dict.keys())[:-1]  
        contagens = list(top_5_emojis_dict.values())[:-1]  

    
        bar = (
            Bar()
            .add_xaxis(emojis)
            .add_yaxis(
                "Quantidade de Emojis", 
                contagens,
                itemstyle_opts=opts.ItemStyleOpts(color="lightcoral")
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(name="Emojis", type_="category"),
                yaxis_opts=opts.AxisOpts(name="Quantidade"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
            )
        )
        return bar

    except Exception as e:
        print(f"Erro: {str(e)}")
        return None

def gerar_grafico_interacoes_por_remetente(mensagens_por_usuario):
    mensagens_por_usuario = dict(sorted(mensagens_por_usuario.items(), key=lambda item: item[1], reverse=True)[:4])
    remetentes = list(mensagens_por_usuario.keys())
    quantidades = list(mensagens_por_usuario.values())
    
    bar = (
        Bar()
        .add_xaxis(remetentes)
        .add_yaxis("Quantidade de Mensagens", quantidades)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="Mensagens", type_="value"),
            yaxis_opts=opts.AxisOpts(name="Usuário", type_="category", axislabel_opts={"rotate": 0}),
        )
        .reversal_axis()
    )
    return bar
