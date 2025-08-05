# API de Classificação de Empréstimos

## 📖 Sobre o Projeto

Esta é uma API RESTful desenvolvida com **FastAPI** para classificar a aprovação de empréstimos financeiros. O projeto utiliza um modelo de Machine Learning (Random Forest) para prever a probabilidade de um cliente ter seu empréstimo aprovado ou não, com base em seus dados pessoais e financeiros.

A aplicação é containerizada com **Docker**, garantindo um ambiente de execução consistente e facilitando o deploy.

## ✨ Funcionalidades

-   **Predição de Risco de Crédito**: Classifica solicitações de empréstimo em `aprovado` ou `negado`.
-   **API RESTful**: Interface clara e documentada (via Swagger UI) para interação com o modelo.
-   **Containerização**: Fácil setup e deploy com Docker e Docker Compose.
-   **Modelo Robusto**: O modelo foi escolhido após uma análise comparativa rigorosa, priorizando a segurança contra falsos positivos.

## 🧠 O Processo de Machine Learning

Todo o fluxo de treinamento, avaliação e seleção do modelo está documentado no notebook `1 - Treinamento e Avaliação do Modelo.ipynb`.

### Fonte de Dados

A base de dados utilizada, `dados_tratados.csv`, foi pré-processada e analisada em um projeto anterior de análise exploratória de dados.
> **Link para o projeto de análise de dados:** [Projeto Análise de Dados de Empréstimos](https://github.com/GabrielFerreiraSilva/analise-de-dados-emprestimos)

### Engenharia de Features

Uma feature importante, `numero_parcelas`, não estava presente na base original. Ela foi criada sinteticamente através de um algoritmo que considera o valor do empréstimo, sua finalidade e o score de crédito do cliente. Foi adicionado ruído para garantir maior variabilidade e realismo aos dados.

### Modelagem e Avaliação

Para encontrar o melhor classificador, foram seguidos os seguintes passos:

1.  **Pré-processamento**: Foi criada uma pipeline para codificar variáveis categóricas e garantir que o processo fosse aplicado de forma consistente nos dados de treino e teste, evitando *data leakage*.
2.  **Modelos Testados**: Foram avaliados três algoritmos: **Árvore de Decisão**, **Random Forest** e **XGBoost**.
3.  **Tratamento de Desbalanceamento**: Como a base de dados era desbalanceada, foram testados dois cenários:
    -   **Cenário 1**: Uso do parâmetro `class_weight='balanced'` (e seu equivalente no XGBoost) para penalizar erros na classe minoritária.
    -   **Cenário 2**: Uso da técnica de oversampling **SMOTE** para balancear as classes antes do treinamento.
4.  **Métricas de Avaliação**: Os 6 modelos resultantes (3 algoritmos x 2 cenários) foram avaliados com base em Acurácia, Matriz de Confusão, Curva ROC, AUC, Precision, Recall e F1-Score.

### Seleção do Modelo

Considerando o **perfil conservador da empresa** em relação a riscos financeiros, o principal critério de escolha foi a minimização de **falsos positivos** (prever "aprovado" para um cliente que não deveria ser).

O modelo **Random Forest com `class_weight`** foi o escolhido, pois apresentou o melhor equilíbrio entre um baixo número de falsos positivos e um bom desempenho geral nas outras métricas.

A pipeline final, contendo o pré-processador e o modelo treinado, foi exportada para o arquivo `artifacts/random_forest_class_weight_pipeline.joblib`.

## 🛠️ Estrutura do Projeto

```
api-classificacao-emprestimos/
├── app/
│   ├── config.py           # Configurações da aplicação (variáveis de ambiente)
│   ├── dto.py              # Data Transfer Objects (Pydantic models) para a API
│   └── main.py             # Lógica principal da API com FastAPI
├── artifacts/
│   └── random_forest_class_weight_pipeline.joblib  # Pipeline do modelo treinado
├── bases/
│   └── dados_tratados.csv  # Base de dados utilizada
├── .dockerignore
├── .env                    # Arquivo de variáveis de ambiente (não versionado)
├── .gitignore
├── 1 - Treinamento e Avaliação do Modelo.ipynb # Notebook com o processo de ML
├── docker-compose.yml      # Orquestrador dos containers
├── Dockerfile              # Definição do container da aplicação
├── README.md
└── requirements.txt        # Dependências Python do projeto
```

## 🚀 Como Executar

### Pré-requisitos

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/GabrielFerreiraSilva/api-classificacao-emprestimos
    cd api-classificacao-emprestimos
    ```

2.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto, copiando o exemplo abaixo.

    ```env
    # .env
    PIPELINE_PATH=artifacts/random_forest_class_weight_pipeline.joblib
    APP_HOST="0.0.0.0"
    APP_PORT=8080
    ```
    *Obs: O `APP_HOST` deve ser `0.0.0.0` para ser acessível de fora do container Docker.*

3.  **Inicie a aplicação com Docker Compose:**
    ```bash
    docker-compose up --build -d
    ```

A API estará disponível em `http://localhost:8080`. A documentação interativa (Swagger UI) pode ser acessada em `http://localhost:8080/docs`.

## 🔌 Endpoints da API

### `GET /`

Endpoint raiz para verificar se a API está no ar.

-   **Resposta (200 OK):**
    ```json
    {
      "message": "Bem-vindo à API de Risco de Crédito. Acesse /docs para a documentação."
    }
    ```

### `GET /health`

Verifica o status da API e se a pipeline do modelo foi carregada com sucesso.

-   **Resposta (200 OK):**
    ```json
    {
      "status": "ok",
      "pipeline_loaded": true
    }
    ```

### `POST /predict`

Recebe os dados de um cliente e retorna a predição de aprovação do empréstimo.

-   **Corpo da Requisição (Request Body):**
    ```json
    {
      "idade": 24,
      "genero": "feminino",
      "escolaridade": "tecnologo",
      "renda_anual": 100684.0,
      "experiencia_profissional_anos": 3,
      "tipo_moradia": "aluguel",
      "valor_emprestimo": 35000.0,
      "finalidade_emprestimo": "pessoal",
      "taxa_juros_emprestimo": 8.90,
      "percentual_renda_comprometida": 0.35,
      "historico_credito_anos": 2,
      "score_credito": 544,
      "inadimplencia_anterior": "nao",
      "numero_parcelas": 66
    }
    ```

-   **Resposta (200 OK):**
    ```json
    {
      "prediction_status": "aprovado",
      "probability_approved": "94.00%"
    }
    ```

## 🔮 Próximos Passos

-   [ ] **Implementar SHAP**: Adicionar um endpoint para explicar as predições do modelo utilizando a biblioteca SHAP (SHapley Additive exPlanations).
-   [ ] **Retreinamento Periódico**: Criar um pipeline de MLOps para automatizar o retreinamento do modelo com a chegada de novos dados.
-   [ ] **Testes Unitários**: Aumentar a cobertura de testes para garantir a robustez da API.