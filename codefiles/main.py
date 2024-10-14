# Importar bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Passo 1: Carregar os arquivos CSV
# Substitua pelos caminhos corretos dos arquivos CSV
df1 = pd.read_csv('Tabela 1 - Base de Incidência.csv', sep=';', encoding='latin1')
df2 = pd.read_csv('Tabela 2 - Tributo e Competência.csv', sep=';', encoding='latin1')

# Verificar as primeiras linhas de cada DataFrame
print("Primeiras linhas da Tabela 1 (Base de Incidência):")
print(df1.head())
print("\nPrimeiras linhas da Tabela 2 (Tributo e Competência):")
print(df2.head())

# Limpeza dos dados (remover valores nulos)
df1.dropna(inplace=True)
df2.dropna(inplace=True)

# Passo 2: Análise da Carga Tributária por Tipo de Imposto
# Agrupar os dados da Tabela 2 por tipo de tributo e somar os valores
tributos_por_tipo = df2.groupby('Tributo')['Valor'].sum()

# Visualização: Gráfico de barras dos tributos por tipo
plt.figure(figsize=(10, 6))
tributos_por_tipo.plot(kind='bar', color='blue')
plt.title('Carga Tributária por Tipo de Tributo')
plt.xlabel('Tipo de Tributo')
plt.ylabel('Valor (em milhões)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Passo 3: Evolução da Carga Tributária ao Longo do Tempo
# Converter a coluna de ano para formato de data
df1['ano'] = pd.to_datetime(df1['ano'], format='%Y')  # Ajuste conforme a sua coluna de ano
carga_por_ano = df1.groupby('ano')['Valor'].sum()

# Visualização: Gráfico de linha da evolução da carga tributária ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(carga_por_ano.index, carga_por_ano.values, marker='o', color='green')
plt.title('Evolução da Carga Tributária ao Longo do Tempo')
plt.xlabel('Ano')
plt.ylabel('Carga Tributária (em milhões)')
plt.grid(True)
plt.show()

# Passo 4: Comparação da Carga Tributária entre Setores ou Regiões
# Agrupar por setor ou região (dependendo da estrutura do arquivo)
# Ajustar o nome da coluna 'Setor' conforme o arquivo
carga_por_setor = df1.groupby('Setor')['Valor'].sum()

# Visualização: Gráfico de barras para comparação da carga entre setores
plt.figure(figsize=(10, 6))
carga_por_setor.plot(kind='bar', color='purple')
plt.title('Comparação da Carga Tributária por Setor')
plt.xlabel('Setor')
plt.ylabel('Carga Tributária (em milhões)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Passo 5: Análise da Proporção de Tipos de Tributos na Carga Total
# Calcular a proporção de cada tipo de tributo em relação ao total
proporcao_tributos = df2.groupby('Tributo')['Valor'].sum() / df2['Valor'].sum()

# Visualização: Gráfico de pizza para a proporção de cada tributo
plt.figure(figsize=(8, 8))
proporcao_tributos.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
plt.title('Proporção de Tipos de Tributos na Carga Total')
plt.ylabel('')  # Remover o rótulo do eixo y
plt.show()

# Fim do script
