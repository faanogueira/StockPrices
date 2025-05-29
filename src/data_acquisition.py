# src/data_acquisition.py

import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# --- Configurações Iniciais ---
# Lista de tickers de exemplo. Podemos expandir ou modificar esta lista.
# Para tickers brasileiros, geralmente usamos o sufixo ".SA"
# Exemplo: PETR4.SA (Petrobras), VALE3.SA (Vale), ITUB4.SA (Itaú Unibanco)
DEFAULT_TICKERS = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'MGLU3.SA', 'WEGE3.SA']

# Período padrão para download dos dados
DEFAULT_START_DATE = '2020-01-01'
DEFAULT_END_DATE = datetime.now().strftime('%Y-%m-%d') # Data de hoje

# Caminho para salvar os dados brutos
RAW_DATA_DIR = '../data/raw/' # Relativo à localização do script src/

def create_directory_if_not_exists(path):
    """
    Cria um diretório se ele não existir.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Diretório criado: {path}")

def download_stock_data(tickers, start_date, end_date):
    """
    Baixa os dados históricos de uma lista de tickers de ações usando o yfinance.

    Parâmetros:
    tickers (list): Uma lista de strings com os tickers das ações (ex: ['PETR4.SA', 'VALE3.SA']).
    start_date (str): Data de início no formato 'YYYY-MM-DD'.
    end_date (str): Data de fim no formato 'YYYY-MM-DD'.

    Retorna:
    pandas.DataFrame: Um DataFrame com os dados de todas as ações,
                      com um MultiIndex nas colunas (Atributo, Ticker).
                      Retorna None se houver erro no download.
    """
    print(f"Baixando dados para os tickers: {tickers}")
    print(f"Período: de {start_date} até {end_date}")
    try:
        # O download agrupa os dados por ticker se passarmos uma lista
        # O yfinance retorna um DataFrame com MultiIndex nas colunas
        data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker')
        
        if data.empty:
            print("Nenhum dado foi baixado. Verifique os tickers e o período.")
            return None
        
        # Reorganizando as colunas para ter o ticker como nível superior
        # Se houver apenas um ticker, o yfinance não agrupa por padrão da mesma forma.
        if len(tickers) == 1:
            # Adiciona o nome do ticker como nível superior nas colunas
            data.columns = pd.MultiIndex.from_product([[tickers[0]], data.columns])
            # Reorganiza para (Ticker, Atributo)
            data = data.stack(level=0).unstack(level=1).reorder_levels([1,0], axis=1).sort_index(axis=1)

        # Para múltiplos tickers, o yfinance já pode retornar (Ticker, Atributo)
        # Ou (Atributo, Ticker). Precisamos garantir o formato (Ticker, Atributo)
        # Se o primeiro nível das colunas for 'Open', 'High', etc., então precisamos trocar
        if data.columns.levels[0][0] in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
             data = data.stack(level=1).unstack(level=0) # Troca os níveis Ticker e Atributo

        print("Download concluído com sucesso!")
        return data
    except Exception as e:
        print(f"Ocorreu um erro durante o download: {e}")
        return None

def save_data_to_csv(data, directory, filename_prefix='stock_data'):
    """
    Salva cada ticker do DataFrame de MultiIndex em um arquivo CSV separado.

    Parâmetros:
    data (pandas.DataFrame): DataFrame com MultiIndex nas colunas (Ticker, Atributo).
    directory (str): Diretório onde os arquivos CSV serão salvos.
    filename_prefix (str): Prefixo para os nomes dos arquivos CSV.
    """
    if data is None or data.empty:
        print("Nenhum dado para salvar.")
        return

    create_directory_if_not_exists(directory)

    for ticker in data.columns.levels[0]: # Itera sobre o primeiro nível do MultiIndex (tickers)
        ticker_data = data[ticker]
        # Remove o ".SA" para um nome de arquivo mais limpo, se presente
        clean_ticker_name = ticker.replace('.SA', '')
        file_path = os.path.join(directory, f"{filename_prefix}_{clean_ticker_name}.csv")
        try:
            ticker_data.to_csv(file_path)
            print(f"Dados de {ticker} salvos em: {file_path}")
        except Exception as e:
            print(f"Não foi possível salvar os dados de {ticker}. Erro: {e}")

# --- Função Principal para Execução do Script ---
if __name__ == '__main__':
    print("Iniciando o script de aquisição de dados...")

    # Usar os tickers e datas padrão definidos no início do script
    # Para usar uma lista diferente, você pode modificar aqui:
    # tickers_to_download = ['ABEV3.SA', 'BBDC4.SA']
    tickers_to_download = DEFAULT_TICKERS
    start = DEFAULT_START_DATE
    end = DEFAULT_END_DATE

    # Baixar os dados
    downloaded_data = download_stock_data(tickers_to_download, start, end)

    # Salvar os dados baixados
    if downloaded_data is not None:
        save_data_to_csv(downloaded_data, RAW_DATA_DIR, filename_prefix='raw_stock_data')

    print("Script de aquisição de dados finalizado.")