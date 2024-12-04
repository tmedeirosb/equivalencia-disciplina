import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr
import streamlit as st
import numpy as np

# Função para calcular a similaridade com diferentes métricas
def calcular_similaridade(matriz_ocorrencia, metodo):
    if metodo == 'Cosine Similarity':
        return cosine_similarity(matriz_ocorrencia)
    elif metodo == 'Correlation Coefficient':
        return matriz_ocorrencia.T.corr(method='pearson').values

# Aplicação Streamlit
st.title('Análise de Similaridade entre Disciplinas de Ingresso')

# Carregar os dados
uploaded_file = st.file_uploader("Carregue o arquivo CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv('relacao_anonimo_professores_disciplinas.csv')

# Filtros de ano e modalidade
anos = df['ano_diario'].unique().tolist()
modalidades = df['modalidade'].unique().tolist()

ano_selecionado = st.multiselect('Selecione o(s) Ano(s)', anos, default=anos)
modalidade_selecionada = st.multiselect('Selecione a(s) Modalidade(s)', modalidades, default=modalidades)

# Filtrar o dataframe
df_filtrado = df[(df['ano_diario'].isin(ano_selecionado)) & (df['modalidade'].isin(modalidade_selecionada))]

# Criar a matriz de ocorrência
matriz_ocorrencia = pd.crosstab(df_filtrado['disciplina_ingresso'], df_filtrado['componente_curricular'])

# Selecionar a métrica de similaridade
metodo_similaridade = st.selectbox('Selecione a Métrica de Similaridade', ['Cosine Similarity', 'Correlation Coefficient'])

# Calcular a similaridade
similaridade = calcular_similaridade(matriz_ocorrencia, metodo_similaridade)
matriz_similaridade = pd.DataFrame(similaridade, index=matriz_ocorrencia.index, columns=matriz_ocorrencia.index)

# Filtros e inputs do usuário
disciplinas = matriz_similaridade.index.tolist()
disciplina_selecionada = st.selectbox('Selecione uma Disciplina de Ingresso', disciplinas)
k = st.slider('Selecione o valor de k (número de disciplinas similares)', min_value=1, max_value=30, value=5)
th = st.slider('Defina o Threshold de Similaridade', min_value=0.0, max_value=1.0, value=0.5)

gerar_graficos = st.button('Gerar Resultados')

# Função para obter disciplinas similares
def obter_disciplinas_similares(matriz_similaridade, disciplina, top_n=5, threshold=0.5):
    similares = matriz_similaridade[disciplina].sort_values(ascending=False)
    similares = similares.drop(disciplina)
    similares = similares[similares >= threshold]
    return similares.head(top_n)

if gerar_graficos:
    # Gerar o mapa de calor das k disciplinas mais similares
    disciplinas_similares = obter_disciplinas_similares(matriz_similaridade, disciplina_selecionada, top_n=k, threshold=th)
    disciplinas_similares_indices = disciplinas_similares.index.tolist()
    disciplinas_para_mapa = [disciplina_selecionada] + disciplinas_similares_indices

    # Exibir o texto antes do mapa de calor
    st.subheader('Equivalência Pedagógica')
    texto_equivalencia = f"Há equivalência pedagógica para a Matéria/Disciplina de **{disciplina_selecionada}** com as seguintes disciplinas:"
    st.write(texto_equivalencia)

    # Formatar as disciplinas similares como uma lista
    if disciplinas_similares_indices:
        for disciplina in disciplinas_similares_indices:
            st.markdown(f"- {disciplina}")
    else:
        st.write("Nenhuma disciplina similar foi encontrada com os critérios estabelecidos.")

    # Filtrar a matriz de similaridade para as disciplinas selecionadas
    matriz_filtrada = matriz_similaridade.loc[disciplinas_para_mapa, disciplinas_para_mapa]

    # Plotar o mapa de calor
    st.subheader('Mapa de Calor das Disciplinas Selecionadas')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(matriz_filtrada, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    # Gerar o dendograma
    st.subheader('Dendrograma das Disciplinas Selecionadas')
    linked = linkage(1 - matriz_filtrada, 'single')  # 1 - similaridade para converter em distância
    fig_dendro, ax_dendro = plt.subplots(figsize=(10, 7))
    dendrogram(linked, labels=matriz_filtrada.index, distance_sort='descending', show_leaf_counts=True, ax=ax_dendro)
    plt.xticks(rotation=90)
    st.pyplot(fig_dendro)

    # Gerar o crosstab das disciplinas similares
    st.subheader('Crosstab das Disciplinas Selecionadas')
    df_crosstab = df_filtrado[df_filtrado['disciplina_ingresso'].isin(disciplinas_para_mapa)]
    crosstab = pd.crosstab(df_crosstab['disciplina_ingresso'], df_crosstab['componente_curricular'])
    st.write(crosstab)