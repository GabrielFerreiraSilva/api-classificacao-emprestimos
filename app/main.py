import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.dto import ClassificacaoEmprestimoDTO
import uvicorn
from app.config import settings

modelo_ml = {}

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Carregando o modelo durante a inicialização
    print("Carregando o pipeline de ML...")
    try:
        modelo_ml["pipeline"] = joblib.load(settings.PIPELINE_PATH)
        print("Pipeline carregado com sucesso.")
    except FileNotFoundError:
        print(f"Erro: Arquivo do pipeline não encontrado em {settings.PIPELINE_PATH}")
        modelo_ml["pipeline"] = None
    yield
    # Limpando os modelos ao desligar
    modelo_ml.clear()
    print("Recursos de ML liberados.")

app = FastAPI(
    title="API de Classificação de Empréstimos",
    description="Uma API para prever a aprovação de empréstimos com base nos dados do cliente",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Risco de Crédito. Acesse /docs para a documentação."}

@app.get("/health", tags=["Status"])
def health_check():
    return {"status": "ok", "pipeline_loaded": modelo_ml.get("pipeline") is not None}

@app.post("/predict", tags=["Prediction"])
def predict(data: ClassificacaoEmprestimoDTO):
    if modelo_ml.get("pipeline") is None:
        raise HTTPException(status_code=503, detail="Modelo não está disponível. Verifique os logs do servidor.")

    try:
        # Convertendo o DTO Pydantic para um DataFrame do Pandas
        input_df = pd.DataFrame([data.model_dump()])

        prediction = modelo_ml["pipeline"].predict(input_df)
        probability = modelo_ml["pipeline"].predict_proba(input_df)
        
        # Mapeando o resultado numérico para a string correspondente
        status = 'aprovado' if prediction[0] == 1 else 'negado'
        
        # Probabilidade da classe 'aprovado' (classe 1)
        prob_aprovado = float(probability[0][1])

        return {
            "prediction_status": status,
            "probability_approved": f"{prob_aprovado:.2%}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a predição: {str(e)}")
    
if __name__ == "__main__":
    print(f"Iniciando servidor em http://{settings.APP_HOST}:{settings.APP_PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )