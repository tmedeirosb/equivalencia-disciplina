import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import streamlit as st

# Aplicação Streamlit
st.title('Análise de Similaridade entre Disciplinas de Ingresso')

# Carregar as matrizes salvas
matriz_ocorrencia = pd.read_csv('matriz_ocorrencia.csv', index_col=0)
matriz_similaridade = pd.read_csv('matriz_similaridade.csv', index_col=0)

# Filtros e inputs do usuário
disciplinas = matriz_similaridade.index.tolist()
disciplina_selecionada = st.selectbox('Selecione uma Disciplina de Ingresso', disciplinas)
k = st.slider('Selecione o valor de k (número de disciplinas similares)', min_value=1, max_value=10, value=5)

gerar_graficos = st.button('Gerar Gráficos')

# Função para obter disciplinas similares
def obter_disciplinas_similares(matriz_similaridade, disciplina, top_n=5):
    similares = matriz_similaridade[disciplina].sort_values(ascending=False)
    similares = similares.drop(disciplina)
    return similares.head(top_n)

if gerar_graficos:
    # Gerar o mapa de calor das k disciplinas mais similares
    disciplinas_similares = obter_disciplinas_similares(matriz_similaridade, disciplina_selecionada, top_n=k)
    disciplinas_similares_indices = disciplinas_similares.index.tolist()
    disciplinas_para_mapa = [disciplina_selecionada] + disciplinas_similares_indices

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
