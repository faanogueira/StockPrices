# 📊 StockPrices BR 🇧🇷 - Análise e Pré-processamento de Ações Brasileiras

![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Status do Projeto](https://img.shields.io/badge/status-em%20desenvolvimento-green)](.)

Bem-vindo ao **StockPrices BR**! Este projeto é sua plataforma completa para mergulhar no universo dos dados de ações da bolsa brasileira (B3). Nosso principal objetivo é aplicar técnicas robustas de coleta, limpeza e pré-processamento de dados, transformando informações brutas de preços de ações em um conjunto de dados valioso e pronto para análises avançadas, visualizações e modelagem preditiva. 📈📉

## 🚀 Funcionalidades Principais

* **Coleta de Dados Simplificada:** Busca dados históricos de ações diretamente do Yahoo Finance utilizando a biblioteca `yfinance`.
* **Limpeza Abrangente:** Tratamento de dados ausentes, verificação de tipos, remoção de duplicatas.
* **Pré-processamento Inteligente:** Normalização de dados e preparação para análises.
* **Engenharia de Atributos:** Criação de features relevantes como retornos diários e médias móveis (SMA).
* **Estrutura Organizada:** Código modularizado para facilitar a manutenção e expansão.
* **Pipeline Automatizado:** Script principal (`main.py`) para orquestrar todo o fluxo de trabalho.
* **Visualização Interativa:** Notebooks Jupyter para explorar os dados processados e extrair insights visuais.

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma para manter tudo claro e acessível:

```
stockprices/
├── data/                           # Armazenamento de dados
│   ├── raw/                        # Dados brutos baixados (CSVs individuais por ticker)
│   └── processed/                  # Dados limpos e processados (CSVs individuais por ticker)
├── notebooks/                      # Notebooks Jupyter para análise exploratória e visualização
│   └── visualizacao_PETR4.ipynb    # Exemplo de notebook para visualização
├── src/                            # Código fonte principal do projeto
│   ├── data_acquisition.py         # Script para baixar os dados das ações
│   ├── preprocessing.py            # Script para limpar e pré-processar os dados
│   └── main.py                     # Script principal para orquestrar o pipeline
├── requirements.txt                # Lista de dependências do projeto Python
└── README.md                       # Este arquivo incrível que você está lendo!
```

## 🛠️ Tecnologias Utilizadas

* **Python 3.7+**
* **Pandas:** Para manipulação e análise de dados de alta performance.
* **NumPy:** Para computação numérica fundamental.
* **yfinance:** Para baixar dados históricos do mercado de ações do Yahoo Finance.
* **Matplotlib & Seaborn:** Para criar visualizações estáticas, animadas e interativas.
* **JupyterLab (ou Jupyter Notebook):** Para desenvolvimento interativo e análise exploratória.

## ⚙️ Configuração e Instalação

Siga estes passos para configurar o ambiente e rodar o projeto:

1.  **Pré-requisitos:**
    * Python 3.7 ou superior instalado.
    * Git instalado (para clonar o repositório).

2.  **Clone o Repositório:**
    (Se o seu projeto estiver no GitHub, substitua pela URL correta)
    ```bash
    git clone [https://github.com/faanogueira/stockprices.git](https://github.com/faanogueira/stockprices.git)
    cd stockprices
    ```

3.  **Crie e Ative um Ambiente Virtual:**
    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    # Criar o ambiente virtual (ex: usando venv)
    python -m venv venv_stockprices

    # Ativar o ambiente virtual
    # No Windows:
    # venv_stockprices\Scripts\activate
    # No macOS/Linux:
    # source venv_stockprices/bin/activate
    ```

4.  **Instale as Dependências:**
    Com o ambiente virtual ativo, instale todas as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Como Executar o Projeto

1.  **Executar o Pipeline Completo (Coleta e Pré-processamento):**
    Navegue até a pasta `src/` e execute o script `main.py`:
    ```bash
    cd src
    python main.py
    ```
    Isso irá:
    * Baixar os dados brutos para os tickers configurados (padrão em `data_acquisition.py`).
    * Salvar os dados brutos em `data/raw/`.
    * Processar cada arquivo de dados brutos.
    * Salvar os dados limpos e com features em `data/processed/`.

2.  **Visualizar os Dados Processados:**
    * Inicie o JupyterLab (ou Jupyter Notebook) na pasta raiz do projeto:
        ```bash
        # Na pasta raiz 'stockprices/'
        jupyter lab
        # ou 'jupyter notebook'
        ```
    * No seu navegador, navegue até a pasta `notebooks/`.
    * Abra um notebook existente (ex: `visualizacao_acao_exemplo.ipynb`) ou crie um novo para carregar e visualizar os arquivos `.csv` da pasta `data/processed/`.

## 🧩 Descrição dos Módulos Principais

* **`src/data_acquisition.py`:** Responsável por se conectar à API do Yahoo Finance (`yfinance`) e baixar os dados históricos de preços para uma lista configurável de tickers. Os dados são salvos individualmente em formato CSV na pasta `data/raw/`.
* **`src/preprocessing.py`:** Carrega os dados brutos, realiza uma série de etapas de limpeza (tratamento de valores ausentes, remoção de duplicatas, verificação de tipos), engenharia de features (cálculo de retornos, médias móveis) e salva os dados transformados na pasta `data/processed/`.
* **`src/main.py`:** O maestro do projeto! Orquestra a execução dos scripts de aquisição e pré-processamento de forma sequencial, automatizando o fluxo de trabalho.
* **`notebooks/`:** Seu playground para análise exploratória! Contém exemplos de como carregar os dados processados e gerar visualizações para entender melhor as características e tendências das ações.

## 🔧 Configuração Personalizada

* **Lista de Tickers:** Para alterar as ações a serem analisadas, modifique a lista `DEFAULT_TICKERS` no arquivo `src/data_acquisition.py` (e, consequentemente, as listas derivadas em `src/main.py`). Lembre-se de usar o sufixo `.SA` para ações brasileiras (ex: `PETR4.SA`, `VALE3.SA`).
* **Período de Análise:** As datas `DEFAULT_START_DATE` e `DEFAULT_END_DATE` também podem ser ajustadas em `src/data_acquisition.py` para definir o intervalo histórico dos dados.

## 🔮 Próximos Passos e Melhorias Futuras

O StockPrices BR é um projeto com grande potencial de expansão! Algumas ideias para o futuro incluem:

* [ ] Implementar mais técnicas de engenharia de atributos (ex: volatilidade, indicadores técnicos como RSI, MACD).
* [ ] Adicionar uma camada de logging mais robusta.
* [ ] Parameterizar os scripts para aceitar tickers e datas via argumentos de linha de comando.
* [ ] Integrar com um banco de dados (SQL ou NoSQL) para armazenamento mais eficiente.
* [ ] Desenvolver modelos preditivos básicos (ex: séries temporais ARIMA, Prophet).
* [ ] Criar uma interface de usuário simples (Streamlit ou Flask) para interagir com os dados.
* [ ] Expandir a cobertura para "todas" as ações da B3 (requer uma fonte confiável e dinâmica para a lista de tickers).

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` (você precisaria criar um) para mais detalhes.

---

## 📩 Contato
Atividade realizada por **Fábio Nogueira**

<p>
<a href="https://www.linkedin.com/in/faanogueira/" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=13930&format=png&color=000000" target="_blank" width="80" title="LinkedIn"></a>
<a href="https://github.com/faanogueira" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=AZOZNnY73haj&format=png&color=000000" target="_blank" width="80" title="GitHub"></a>
<a href="https://api.whatsapp.com/send?phone=5571983937557" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=16713&format=png&color=000000" target="_blank" width="80" title="WhatsApp"></a>
<a href="https://fabio-nogueira.vercel.app" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=9x65MLqCekT5&format=png&color=000000" target="_blank" width="80" title="Portfólio"></a> 
<a href="mailto:faanogueira@gmail.com"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=P7UIlhbpWzZm&format=png&color=000000" target="_blank" width="80" title="Email"></a> 
</p>
