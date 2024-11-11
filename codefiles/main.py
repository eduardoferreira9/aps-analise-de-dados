# pip install -r requirements.txt <- Comando para instalação das dependencias
# Importar bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Passo 1: Carregar os arquivos CSV
df1 = pd.read_csv('./database/Tabela 1 - Base de Incidência.csv', sep=';', encoding='utf8')
df2 = pd.read_csv('./database/Tabela 2 - Tributo e Competência.csv', sep=';', encoding='utf8')

# Verificar as primeiras linhas de cada DataFrame
print("\nPrimeiras linhas da Tabela 1 (Base de Incidência):")
print(df1.head())
print("\nPrimeiras linhas da Tabela 2 (Tributo e Competência):")
print(df2.head())

# Limpeza dos dados (remover valores nulos)
#df1.dropna(inplace=True)                                                   #Estava Causando bug para na hora de chamar os valor da tabela 1 e 2
#df2.dropna(inplace=True)

# Passo 2: Conversão da coluna "Valor da Receita Tributária" para número
# Remover todos os caracteres que não são dígitos ou ponto e converter para float
df1['Valor da Receita Tributária'] = pd.to_numeric(df1['Valor da Receita Tributária'].str.replace(r'[^0-9,]', '', regex=True).str.replace(',', '.'), errors='coerce')
df2['Valor da Receita Tributária'] = pd.to_numeric(df2['Valor da Receita Tributária'].str.replace(r'[^0-9,]', '', regex=True).str.replace(',', '.'), errors='coerce')

# Verificar se a conversão foi bem-sucedida
print("Primeiras linhas após conversão da Tabela 1:")
print(df1[['Ano-calendário', 'Valor da Receita Tributária']].head())
print("Primeiras linhas após conversão da Tabela 2:")
print(df2[['Ano-calendário', 'Valor da Receita Tributária']].head())

# Passo 3: Análise da Carga Tributária por Tipo de Imposto
# Agrupar os dados da Tabela 2 por "Descrição" e somar os valores da coluna "Valor da Receita Tributária"
tributos_por_tipo = df2.groupby('Descrição')['Valor da Receita Tributária'].sum()

# Visualização: Gráfico de barras dos tributos por tipo
plt.figure(figsize=(10, 6))
tributos_por_tipo.plot(kind='bar', color='blue')
plt.title('Carga Tributária por Tipo de Tributo')
plt.xlabel('Tipo de Tributo')
plt.ylabel('Valor da Receita Tributária (em milhões)')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

# Passo 4: Evolução da Carga Tributária ao Longo do Tempo
# Converter a coluna "Ano-calendário" para inteiro (caso necessário)
df1['Ano-calendário'] = pd.to_datetime(df1['Ano-calendário'], format='%Y').dt.year

# Agrupar os dados por "Ano-calendário" e somar os valores
carga_por_ano = df1.groupby('Ano-calendário')['Valor da Receita Tributária'].sum().sort_index()

# Visualização: Gráfico de linha da evolução da carga tributária ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(carga_por_ano.index.astype(str), carga_por_ano.values, marker='o', linestyle='-', color='green')
plt.title('Evolução da Carga Tributária ao Longo do Tempo')
plt.xlabel('Ano')
plt.ylabel('Carga Tributária (em milhões)')
plt.grid(True)

# Adicionando rótulos de valores aos pontos
for x, y in zip(carga_por_ano.index, carga_por_ano.values):
    plt.text(str(x), y, f'{y:,.2f}', ha='center', va='bottom')
plt.show()

# Passo 5: Comparação da Carga Tributária entre Setores ou Orçamentos
# Agrupar por "Orçamento" (ajustar para o que for relevante)
carga_por_orcamento = df2.groupby('Orçamento')['Valor da Receita Tributária'].sum()

# Visualização: Gráfico de barras para comparação da carga entre orçamentos
plt.figure(figsize=(10, 6))
carga_por_orcamento.plot(kind='bar', color='purple')
plt.title('Comparação da Carga Tributária por Orçamento')
plt.xlabel('Orçamento')
plt.ylabel('Carga Tributária (em milhões)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Passo 6: Análise da Proporção de Tipos de Tributos na Carga Total
# Calcular a proporção de cada "Descrição" (tipo de tributo) em relação ao total
proporcao_tributos = df2.groupby('Descrição')['Valor da Receita Tributária'].sum() / df2['Valor da Receita Tributária'].sum()

# Calcular os percentuais para usar na legenda
percentuais = (proporcao_tributos * 100).round(1).astype(str) + '%'

# Visualização: Gráfico de pizza para a proporção de cada tributo
fig, ax = plt.subplots(figsize=(5, 5))  # Diminuir o tamanho da figura
proporcao_tributos.plot(kind='pie', autopct=None, startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f', '#ffad00', '#99ccff'], labels=[None]*len(proporcao_tributos), legend=False, fontsize=10)
plt.title('Proporção de Tipos de Tributos na Carga Total', fontsize=12)
plt.ylabel('')

# Legenda do lado direto
plt.legend(
    labels=[f"{desc}: {perc}" for desc, perc in zip(proporcao_tributos.index, percentuais)], loc="center left", bbox_to_anchor=(1.25, 0.5), title="Tipos de Tributos", fontsize=8, title_fontsize=10)
plt.subplots_adjust(left=0.1, right=0.85)
plt.show()
