



def gerar_grafico_horas_com_mais_mensagens(mensagens_por_hora):
    distribuicao_horas={}
    for hora in mensagens_por_hora.keys():
        distribuicao_horas[str(hora)] = mensagens_por_hora[hora]
    
    print(distribuicao_horas)
    

response_hora = {'status_code':200,'hora_com_mais_mensagens': {'hora': 12, 'quantidade_mensagens': 27}, 'mensagens_por_hora': {10: 3, 12: 27, 13: 2, 14: 13, 15: 19, 16: 14, 17: 19, 18: 5, 19: 7, 20: 4, 21: 2, 22: 2}}

gerar_grafico_horas_com_mais_mensagens(response_hora['mensagens_por_hora'])