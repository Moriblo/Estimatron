"""
###############################################################################
📦 Estimatron 3.0 — Módulo: skill_mapper

Mapeia métricas extraídas do modelo UML para perfis profissionais técnicos.
Aplica os custos por perfil informados via JSON e calcula distribuição de esforço.

Autor: MOACYR + Copilot
###############################################################################
"""

from typing import Dict

def mapear_skills(metrica: Dict[str, int], custos_json: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    """
    Distribui esforço estimado entre perfis profissionais com base nas métricas e custos.

    Parâmetros:
        metrica (dict): Métricas técnicas do modelo UML.
        custos_json (dict): Tabela com custos por perfil (R$/hora).

    Retorna:
        dict: Distribuição por skill contendo:
            - PM (float): Pessoa-mês estimado por perfil
            - custo_total (float): Custo calculado com base na taxa/hora
    """
    # 📊 Distribuição estática — pode ser parametrizada futuramente
    distribuicao = {
        "Analista de Requisitos": 0.2,
        "Arquiteto de Software": 0.2,
        "Desenvolvedor": 0.4,
        "Testador": 0.2
    }

    # 🧮 Esforço total simplificado (ajuste via COCOMO real)
    total_esforco = 52  # Pessoa-mês

    resultado = {}
    for perfil, proporcao in distribuicao.items():
        pm = total_esforco * proporcao
        horas = pm * 160  # Assumindo 160h/mês
        taxa = custos_json.get(perfil, 100)  # Valor padrão se ausente
        custo = horas * taxa

        resultado[perfil] = {
            "PM": round(pm, 2),
            "custo_total": round(custo, 2)
        }

    return resultado
