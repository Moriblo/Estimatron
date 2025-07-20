"""
###############################################################################
📦 Estimatron 3.0 — Módulo: proposal_writer

Gera o conteúdo final da proposta comercial com base nas métricas extraídas,
distribuição de esforço por perfil técnico e resumo da estimativa COCOMO II.

Autor: MOACYR + Copilot
###############################################################################
"""

from typing import Dict
from fastapi import FastAPI

def gerar(
    metricas: Dict[str, int],
    distribuicao: Dict[str, Dict[str, float]],
    resumo_cocomo: Dict[str, float]
) -> str:
    """
    Gera o conteúdo textual da proposta comercial formatada.

    Parâmetros:
        metricas (dict): Métricas técnicas do modelo UML.
        distribuicao (dict): Esforço por perfil com PMs e custo.
        resumo_cocomo (dict): Contém esforço, prazo e custo estimado.

    Retorna:
        str: Texto formatado da proposta comercial.
    """
    esforco_total = resumo_cocomo.get("esforco", 0)
    prazo = resumo_cocomo.get("prazo_meses", 0)
    custo_estimado = resumo_cocomo.get("custo_total")

    proposta = f"""
Projeto: Estimatron 3.0

📄 Escopo Técnico:
- Casos de Uso: {metricas['casosdeuso']}
- Classes: {metricas['classes']}
- Linhas Estimadas de Código: {metricas['linhas_estimadas']}

🧠 Estimativa COCOMO II:
- Esforço Total: {esforco_total:.2f} pessoas/mês
- Prazo Estimado: {prazo:.2f} meses
"""

    if custo_estimado is not None:
        proposta += f"- Custo Total Estimado: R$ {custo_estimado:,.2f}\n"

    proposta += "\n📊 Distribuição por Perfil:\n"
    for perfil, dados in distribuicao.items():
        proposta += f"- {perfil}: {dados['PM']:.2f} PMs, Custo: R$ {dados['custo_total']:.2f}\n"

    total_perfil = sum(v["custo_total"] for v in distribuicao.values())
    proposta += f"\n🎯 Subtotal por Perfis Técnicos: R$ {total_perfil:,.2f}\n"

    return proposta.strip()
