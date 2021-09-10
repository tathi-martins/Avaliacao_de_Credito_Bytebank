from numpy.lib.twodim_base import _min_int
import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador
# Pressione Ctrl + C para liberar o terminal de volta ao ambiente venv (sair do streamlit hello)

#Cor de fundo do listbox
st.markdown('<style>div[role="listbox"] ul{background-color: #eee1f79e};</style>', unsafe_allow_html=True)

def avaliar_mau_pagador(dict_respostas):
    modelo = load('objetos/25Ago2021_pipeline_rf.joblib')
    features = load('objetos/25Ago2021_features.joblib')

    # Transforma os valores de Anos_desempregado em negativo e o designa para Anos_empregado
    if dict_respostas['Anos_desempregado'] > 0:
        dict_respostas['Anos_empregado'] = dict_respostas['Anos_desempregado'] * -1

    respostas = [] # Cria uma lista que conterá as respostas dos clientes

    # Adiciona as respostas dos clientes na lista criada acima e na coluna correspondente
    for coluna in features:
        respostas.append(dict_respostas[coluna])

    # Cria um dataframe com o mesmo formato que o usado para treinar o nosso modelo
    df_novo_cliente = pd.DataFrame(data=[respostas], columns=features)

    # Utilizando o método predict do nosso modelo com os novos dados (dados dos novos clientes)
    mau_pagador = modelo.predict(df_novo_cliente)[0] # [0] -> pega a primeira classificação do modelo, o primeiro cliente

    return mau_pagador


st.image('img/bytebank_logo.png')
st.write('# Simulador de Avaliação de Crédito')
st.write('## Passo 2 de 2')
st.write('### Com tecnologia de última geração e uma metodologia própria de avaliação com uso de inteligência artificial, a Bytebank oferece uma solução simples, rápida e econômica, que prioriza a experiência de nossos clientes e permite que cada vez mais pessoas possam fazer um empréstimo pessoal seguro, com mais conveniência e menos burocracia.')
st.write('Preencha o formulário abaixo e descubra na hora se o seu crédito foi aprovado.')

expander_trabalho = st.expander('Trabalho e Escolaridade')

expander_pessoal = st.expander('Pessoal')

expander_familia = st.expander('Família')


dict_respostas = {}
lista_campos = load('objetos/25Ago2021_lista_campos.joblib')
lista_features = load('objetos/25Ago2021_features.joblib')

with expander_trabalho:
    col1_form, col2_form = st.columns(2)

    dict_respostas['Categoria_de_renda'] = col1_form.selectbox('Qual a sua categoria de renda?', lista_campos['Categoria_de_renda'])
    
    dict_respostas['Ocupacao'] = col1_form.selectbox('Em que área você trabalha?', lista_campos['Ocupacao'])
    
    # O campo abaixo mostra na tela os salários mensais, o dataframe 
    # original está em anual, mas foi adaptado pro Brasil como salário 
    # mensal. Por isso o * 12 no final. Também foi estipulado os limites do salário, de forma excluir os outliers, entre 0 e 35 mil, 
    # e a graduação é de 500 em 500 reais
    dict_respostas['Rendimento_Anual'] = col1_form.slider('Qual o seu salário?', min_value = 0, max_value = 35000, step = 500) * 12
    
    dict_respostas['Tem_telefone_trabalho'] = 1 if col2_form.selectbox('Tem telefone do trabalho?', ['Sim', 'Não']) == 'Sim' else 0
    
    dict_respostas['Grau_Escolaridade'] = col2_form.selectbox('Qual é o seu grau de escolaridade?', lista_campos['Grau_Escolaridade'])
    
    dict_respostas['Anos_desempregado'] = 0
    if col2_form.radio('Você está desempregado?', ['Sim', 'Não']) == 'Sim':
        dict_respostas['Anos_desempregado'] = col2_form.number_input('Há quantos anos você está desempregado?', help='Preencha 0 se você estiver desempregado à menos de um ano', max_value=50, step=1)

    else:
        dict_respostas['Anos_empregado'] = col2_form.number_input('Há quantos anos você está empregado?', help='Você pode usar as teclas do teclado para para alterar os valores', max_value=50, step=1)
    


with expander_pessoal:
    col1_form, col2_form = st.columns(2)

    dict_respostas['Idade'] = col1_form.number_input('Qual a sua idade? (Apenas maiores de 18 anos)', min_value = 18, max_value=90, step=1)
    dict_respostas['Tem_telefone_fixo'] = 1 if col1_form.radio('Você possui telefone fixo?', ['Sim', 'Não']) == 'Sim' else 0
    dict_respostas['Tem_Carro'] = 1 if col1_form.radio('Você possui carro?', ['Sim', 'Não']) == 'Sim' else 0
    
    dict_respostas['Moradia'] = col2_form.selectbox('Qual é a sua condição de moradia?', lista_campos['Moradia'])
    dict_respostas['Tem_Casa_Propria'] = 1 if col2_form.radio('Você possui casa própria?', ['Sim', 'Não']) == 'Sim' else 0
    dict_respostas['Tem_email'] = 1 if col2_form.radio('Você possui e-mail?', ['Sim', 'Não']) == 'Sim' else 0

with expander_familia:
    col1_form, col2_form = st.columns(2)
    dict_respostas['Estado_Civil'] = col1_form.selectbox('Qual é o seu estado civil?', lista_campos['Estado_Civil'])
    dict_respostas['Qtd_Filhos'] = col1_form.number_input('Quantos filhos você tem?', min_value = 0, max_value=20, step=1)
    dict_respostas['Tamanho_Familia'] = col2_form.number_input('Qual o tamanho da sua família?', min_value = 1, max_value=20, step=1)


if st.button('Avaliar crédito'):
    if avaliar_mau_pagador(dict_respostas) == 1:
        st.error('Crédito Negado') # Isto não é exatamente um erro, mas estamos utilizando a estética aplicada na mensagem de erro do streamlit para entregar a mensagem de 'Crédito Negado'

    else:
        st.success('Crédito Aprovado')
