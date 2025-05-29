# src/preprocessing.py

import pandas as pd
import numpy as np
import os

# --- Configurações de Caminhos ---
# Caminho relativo à localização do script src/
RAW_DATA_DIR = '../data/raw/'
PROCESSED_DATA_DIR = '../data/processed/'
FILENAME_PREFIX_RAW = 'raw_stock_data_'
FILENAME_PREFIX_PROCESSED = 'processed_stock_data_'

# Lista de tickers de exemplo para processar.
# Deve corresponder aos tickers para os quais você baixou os dados.
DEFAULT_TICKERS_TO_PROCESS = ['PETR4', 'VALE3', 'ITUB4', 'MGLU3', 'WEGE3'] # Sem o .SA aqui, pois usamos no nome do arquivo

def create_directory_if_not_exists(path):
    """
    Cria um diretório se ele não existir.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Diretório criado: {path}")

def load_raw_data(ticker_symbol, base_dir=RAW_DATA_DIR, prefix=FILENAME_PREFIX_RAW):
    """
    Carrega os dados brutos de um arquivo CSV para um determinado ticker.

    Parâmetros:
    ticker_symbol (str): O símbolo do ticker (ex: 'PETR4'). O '.SA' não é necessário aqui.
    base_dir (str): O diretório base onde os dados brutos estão localizados.
    prefix (str): O prefixo do nome do arquivo.

    Retorna:
    pandas.DataFrame: DataFrame com os dados carregados, ou None se o arquivo não for encontrado.
    """
    file_path = os.path.join(base_dir, f"{prefix}{ticker_symbol}.csv")
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return None
    try:
        # A primeira coluna (Date) é o índice e deve ser parseada como data
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        print(f"Dados carregados para {ticker_symbol} de {file_path}")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo {file_path}: {e}")
        return None

def inspect_data(df, ticker_symbol):
    """
    Realiza uma inspeção básica nos dados.

    Parâmetros:
    df (pandas.DataFrame): O DataFrame para inspecionar.
    ticker_symbol (str): O nome do ticker para referência nos prints.
    """
    if df is None:
        return

    print(f"\n--- Inspeção Inicial para {ticker_symbol} ---")
    print("Forma do DataFrame (linhas, colunas):", df.shape)
    print("\nPrimeiras 5 linhas:")
    print(df.head())
    print("\nÚltimas 5 linhas:")
    print(df.tail())
    print("\nInformações do DataFrame:")
    df.info()
    print("\nEstatísticas Descritivas:")
    print(df.describe())
    print("\nVerificação de valores ausentes (por coluna):")
    print(df.isnull().sum())
    print("--- Fim da Inspeção ---")

def clean_data(df):
    """
    Limpa os dados do DataFrame.

    Parâmetros:
    df (pandas.DataFrame): O DataFrame para limpar.

    Retorna:
    pandas.DataFrame: O DataFrame limpo.
    """
    if df is None:
        return None

    print("\n--- Limpeza de Dados Iniciada ---")

    # 1. Tratar valores ausentes
    # Para dados de séries temporais de ações, 'forward fill' é uma estratégia comum.
    # Isso preenche NaNs com o último valor válido conhecido.
    # Outra opção seria `df.interpolate(method='time')` se o índice for DatetimeIndex.
    # Também é comum remover dias com Volume = 0, pois podem indicar não pregão (se não filtrado antes)
    
    # Vamos verificar se há colunas com TODOS os valores ausentes (improvável com yfinance, mas bom checar)
    df.dropna(axis=1, how='all', inplace=True)

    # Preencher valores ausentes restantes (ex: para preços e volume)
    cols_to_ffill = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in cols_to_ffill:
        if col in df.columns:
            # Se Volume for NaN, pode ser mais apropriado preencher com 0 ou a média,
            # mas ffill é um começo. Ou até mesmo remover a linha se o Volume for crucial e NaN.
            if df[col].isnull().any():
                 df[col] = df[col].fillna(method='ffill')
                 # Preencher NaNs restantes no início (se houver) com 'backward fill'
                 df[col] = df[col].fillna(method='bfill') 
            
            # Garantir que Volume seja numérico, caso haja algum erro no load
            if col == 'Volume':
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(np.int64)
            else: # Preços
                df[col] = pd.to_numeric(df[col], errors='coerce')


    # Verificar se ainda há NaNs e decidir o que fazer (ex: remover linhas)
    if df.isnull().any().any():
        print("Valores ausentes restantes após ffill/bfill. Removendo linhas com NaNs...")
        df.dropna(inplace=True)

    # 2. Garantir que o índice é DatetimeIndex (já deve ser por conta do parse_dates=True no load)
    if not isinstance(df.index, pd.DatetimeIndex):
        print("Índice não é DatetimeIndex. Tentando converter...")
        # Se o índice não foi parseado corretamente, esta seria uma tentativa,
        # mas o ideal é garantir no load_raw_data.
        # df.index = pd.to_datetime(df.index)
        pass # Já deve estar correto

    # 3. Ordenar pelo índice (data) para garantir a ordem cronológica
    df.sort_index(inplace=True)

    # 4. Verificar e remover duplicatas no índice (dias duplicados)
    if df.index.duplicated().any():
        print("Datas duplicadas encontradas. Mantendo a primeira ocorrência.")
        df = df[~df.index.duplicated(keep='first')]

    # 5. Assegurar tipos de dados numéricos para colunas de preço/volume
    # (Já feito parcialmente acima durante o tratamento de NaN)
    for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'Volume' in df.columns:
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0).astype(np.int64)

    # Remover linhas onde o 'Close' pode ter se tornado NaN após coerção e não foi tratado
    df.dropna(subset=['Close'], inplace=True)


    print("Tipos de dados após limpeza:")
    df.info(verbose=False) # verbose=False para um output mais conciso
    print("--- Limpeza de Dados Concluída ---")
    return df

def engineer_features(df):
    """
    Cria novas features (colunas) no DataFrame.

    Parâmetros:
    df (pandas.DataFrame): O DataFrame com os dados limpos.

    Retorna:
    pandas.DataFrame: O DataFrame com as novas features.
    """
    if df is None:
        return None

    print("\n--- Engenharia de Features Iniciada ---")

    # 1. Calcular Retorno Diário (sobre o 'Adj Close' para considerar dividendos/splits)
    # Retorno = (Preço_hoje / Preço_ontem) - 1
    if 'Adj Close' in df.columns:
        df['Daily_Return'] = df['Adj Close'].pct_change()
    elif 'Close' in df.columns: # Fallback para 'Close' se 'Adj Close' não estiver presente
        df['Daily_Return'] = df['Close'].pct_change()
    
    # 2. Médias Móveis Simples (SMA - Simple Moving Average)
    # Por exemplo, SMA de 20 dias e 50 dias para o 'Adj Close'
    if 'Adj Close' in df.columns:
        df['SMA_20'] = df['Adj Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Adj Close'].rolling(window=50).mean()
    elif 'Close' in df.columns: # Fallback
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # A primeira janela de 'Daily_Return' e das SMAs será NaN, podemos removê-los ou deixar.
    # Se for remover: df.dropna(inplace=True)
    # Por enquanto, vamos mantê-los, pois podem ser tratados em etapas posteriores de modelagem.

    print("Novas features adicionadas: 'Daily_Return', 'SMA_20', 'SMA_50'")
    print("--- Engenharia de Features Concluída ---")
    return df

def save_processed_data(df, ticker_symbol, base_dir=PROCESSED_DATA_DIR, prefix=FILENAME_PREFIX_PROCESSED):
    """
    Salva o DataFrame processado em um arquivo CSV.

    Parâmetros:
    df (pandas.DataFrame): O DataFrame processado para salvar.
    ticker_symbol (str): O símbolo do ticker para nomear o arquivo.
    base_dir (str): O diretório base onde os dados processados serão salvos.
    prefix (str): O prefixo do nome do arquivo.
    """
    if df is None:
        print(f"Nenhum dado para salvar para {ticker_symbol}.")
        return

    create_directory_if_not_exists(base_dir)
    file_path = os.path.join(base_dir, f"{prefix}{ticker_symbol}.csv")
    try:
        df.to_csv(file_path)
        print(f"Dados processados para {ticker_symbol} salvos em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo {file_path}: {e}")

# --- Função Principal para Execução do Script ---
if __name__ == '__main__':
    print("Iniciando o script de pré-processamento de dados...")

    # Criar o diretório de dados processados, se não existir
    create_directory_if_not_exists(PROCESSED_DATA_DIR)

    # Itera sobre a lista de tickers para processar cada um
    for ticker in DEFAULT_TICKERS_TO_PROCESS:
        print(f"\n===== Processando Ticker: {ticker} =====")
        
        # 1. Carregar dados brutos
        raw_df = load_raw_data(ticker)

        if raw_df is None:
            print(f"Não foi possível carregar dados para {ticker}. Pulando para o próximo.")
            continue # Pula para o próximo ticker na lista

        # 2. Inspecionar dados
        inspect_data(raw_df, ticker)

        # 3. Limpar dados
        cleaned_df = clean_data(raw_df.copy()) # Usar .copy() para evitar SettingWithCopyWarning

        if cleaned_df is None or cleaned_df.empty:
            print(f"Dados ficaram vazios após a limpeza para {ticker}. Pulando.")
            continue
            
        # 4. Engenharia de Features
        featured_df = engineer_features(cleaned_df.copy()) # Usar .copy()

        # 5. Salvar dados processados
        save_processed_data(featured_df, ticker)

    print("\nScript de pré-processamento de dados finalizado.")