"""
###############################################################################
📦 Estimatron 3.0 — Módulo: schemas

Define modelos Pydantic para validação de entrada e saída na API.
Utilizado opcionalmente nos endpoints para tipagem forte e compatibilidade OpenAPI.

Autor: MOACYR + Copilot
###############################################################################
"""

from pydantic import BaseModel
from typing import Dict
from fastapi import FastAPI
class Metricas(BaseModel):
    """
    Representa as métricas técnicas extraídas de um modelo UML.
    """
    casosdeuso: int
    classes: int
    linhas_estimadas: int

class PerfilDistribuido(BaseModel):
    """
    Representa o esforço técnico e custo por perfil profissional.
    """
    PM: float
    custo_total: float

class Proposta(BaseModel):
    """
    Estrutura para o retorno da proposta comercial.
    """
    texto: str
