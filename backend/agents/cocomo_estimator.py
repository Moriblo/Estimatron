"""
###############################################################################
📦 Estimatron 3.0 — Módulo: cocomo_estimator

Aplica o modelo COCOMO II (Pós-Arquitetura) para estimar esforço técnico,
prazo de projeto e custo estimado com base em KLOC e fatores de ajuste.

Autor: MOACYR + Copilot
###############################################################################
"""

from typing import Dict, Union

def estimar_cocomo(
    tamanho_kloc: Union[int, float],
    multiplicador: float = 1.15,
    custo_mensal: float = None
) -> Dict[str, float]:
    """
    Calcula esforço, prazo e custo estimado via modelo COCOMO II.

    Parâmetros:
        tamanho_kloc (float): Tamanho do projeto em mil linhas de código (KLOC).
        multiplicador (float): Fator de ajuste (EAF), default = 1.15.
        custo_mensal (float, opcional): Valor mensal por PM (R$).

    Retorna:
        dict: Contém os campos:
            - esforco (PMs)
            - prazo_meses
            - custo_total (se custo_mensal fornecido)
    """
    A = 2.94
    B = 1.12
    esforco = A * (tamanho_kloc ** B) * multiplicador
    prazo = 3.67 * (esforco ** 0.35)

    resultado = {
        "esforco": round(esforco, 2),
        "prazo_meses": round(prazo, 2)
    }

    if custo_mensal:
        resultado["custo_total"] = round(esforco * custo_mensal, 2)

    return resultado
