# src/main.py

import os
from data_acquisition import download_stock_data, save_data_to_csv, DEFAULT_TICKERS, DEFAULT_START_DATE, DEFAULT_END_DATE, RAW_DATA_DIR
from preprocessing import load_raw_data, inspect_data, clean_data, engineer_features, save_processed_data, PROCESSED_DATA_DIR, FILENAME_PREFIX_RAW

# Lista de tickers para o fluxo principal.
# Poderíamos usar os DEFAULT_TICKERS do data_acquisition ou definir uma nova lista aqui.
# Para consistência, vamos usar os tickers definidos em data_acquisition.py,
# mas ajustando para o formato esperado em preprocessing.py (sem o .SA para nomes de arquivo).
TICKERS_FOR_WORKFLOW = DEFAULT_TICKERS # Mantém o .SA para o download
TICKERS_FOR_PROCESSING = [ticker.replace('.SA', '') for ticker in DEFAULT_TICKERS] # Remove .SA para carregar/salvar arquivos

def run_data_pipeline(tickers_to_download, tickers_to_process, start_date, end_date, raw_data_dir, processed_data_dir):
    """
    Executa o pipeline completo de dados: aquisição e pré-processamento.
    """
    print("--- INICIANDO PIPELINE DE DADOS ---")

    # ETAPA 1: Aquisição de Dados
    print("\n--- Iniciando Etapa de Aquisição de Dados ---")
    downloaded_data_multi_ticker = download_stock_data(tickers_to_download, start_date, end_date)

    if downloaded_data_multi_ticker is not None and not downloaded_data_multi_ticker.empty:
        save_data_to_csv(downloaded_data_multi_ticker, raw_data_dir, filename_prefix='raw_stock_data')
        print("--- Etapa de Aquisição de Dados Concluída ---")
    else:
        print("Falha na aquisição de dados. Nenhum dado foi baixado. Encerrando pipeline.")
        return

    # ETAPA 2: Pré-processamento de Dados (para cada ticker)
    print("\n--- Iniciando Etapa de Pré-processamento de Dados ---")
    
    # Certifique-se de que o diretório de dados processados existe
    if not os.path.exists(processed_data_dir):
        os.makedirs(processed_data_dir)
        print(f"Diretório criado: {processed_data_dir}")

    for ticker_clean_name in tickers_to_process:
        print(f"\n===== Processando Ticker: {ticker_clean_name} =====")
        
        raw_df = load_raw_data(ticker_clean_name, base_dir=raw_data_dir, prefix=FILENAME_PREFIX_RAW)

        if raw_df is None:
            print(f"Não foi possível carregar dados brutos para {ticker_clean_name}. Pulando para o próximo.")
            continue

        # inspect_data(raw_df, ticker_clean_name) # Opcional no pipeline principal, mais para depuração

        cleaned_df = clean_data(raw_df.copy())
        if cleaned_df is None or cleaned_df.empty:
            print(f"Dados ficaram vazios após a limpeza para {ticker_clean_name}. Pulando.")
            continue
            
        featured_df = engineer_features(cleaned_df.copy())
        
        save_processed_data(featured_df, ticker_clean_name, base_dir=processed_data_dir)
        
    print("--- Etapa de Pré-processamento de Dados Concluída ---")
    print("\n--- PIPELINE DE DADOS FINALIZADO ---")

if __name__ == '__main__':
    # Definindo os parâmetros para o pipeline
    # Você pode ajustar os tickers e datas aqui ou, futuramente,
    # ler de um arquivo de configuração ou argumentos de linha de comando.
    
    start_date_pipeline = DEFAULT_START_DATE
    end_date_pipeline = DEFAULT_END_DATE
    
    # Caminhos relativos ao script main.py (que está em src/)
    # RAW_DATA_DIR e PROCESSED_DATA_DIR são importados, mas vamos garantir que estão corretos
    # em relação à execução de main.py dentro de src/
    # (Lembre-se que os scripts importados (data_acquisition, preprocessing) definem os caminhos como '../data/...')
    
    # Se você executar main.py de dentro da pasta src/, os caminhos '../data/raw' etc.,
    # definidos nos módulos importados, estarão corretos.

    run_data_pipeline(
        tickers_to_download=TICKERS_FOR_WORKFLOW,
        tickers_to_process=TICKERS_FOR_PROCESSING,
        start_date=start_date_pipeline,
        end_date=end_date_pipeline,
        raw_data_dir=RAW_DATA_DIR, # Usando o caminho definido em data_acquisition
        processed_data_dir=PROCESSED_DATA_DIR # Usando o caminho definido em preprocessing
    )