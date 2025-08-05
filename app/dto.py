from pydantic import BaseModel, Field
from typing import Literal

class ClassificacaoEmprestimoDTO(BaseModel):
    idade: int = Field(..., gt=0, description="Idade do cliente")
    genero: Literal['masculino', 'feminino']
    escolaridade: Literal['ensino_medio', 'tecnologo', 'graduacao', 'mestrado', 'doutorado']
    renda_anual: float = Field(..., gt=0)
    experiencia_profissional_anos: int = Field(..., ge=0)
    tipo_moradia: Literal['aluguel', 'financiada', 'propria', 'outro']
    valor_emprestimo: float = Field(..., gt=0)
    finalidade_emprestimo: Literal['educacao', 'saude', 'empreendimento', 'pessoal', 'consolidacao_dividas', 'reforma_residencial']
    taxa_juros_emprestimo: float = Field(..., gt=0)
    percentual_renda_comprometida: float = Field(..., ge=0, le=1)
    historico_credito_anos: int = Field(..., gt=0)
    score_credito: int = Field(..., gt=0)
    inadimplencia_anterior: Literal['sim', 'nao']
    numero_parcelas: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                'idade': 21,
                'genero': 'feminino',
                'escolaridade': 'ensino_medio',
                'renda_anual': 12282.0,
                'experiencia_profissional_anos': 0,
                'tipo_moradia': 'propria',
                'valor_emprestimo': 1000.0,
                'finalidade_emprestimo': 'educacao',
                'taxa_juros_emprestimo': 11.14,
                'percentual_renda_comprometida': 0.08,
                'historico_credito_anos': 2,
                'score_credito': 504,
                'inadimplencia_anterior': 'sim',
                'numero_parcelas': 36
            }
        }