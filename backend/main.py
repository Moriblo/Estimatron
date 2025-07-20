"""
###############################################################################
🚀 Estimatron 3.0 — Módulo principal da API

Orquestra os agentes para processar arquivos XMI UML,
gerar XML, validar via XSD, aplicar COCOMO II e compor proposta comercial.

Autor: MOACYR + Copilot
###############################################################################
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from typing import Optional
from xmi_parser import extrair_metrica
from xml_converter import gerar_xml
from xsd_validator import validar
from skill_mapper import mapear_skills
from cocomo_estimator import estimar_cocomo
from proposal_writer import gerar
from schemas import Metricas, Proposta
import os

app = FastAPI()

# 🔗 Estado compartilhado para simular armazenamento mínimo
estado_metricas: Optional[Metricas] = None
estado_proposta: Optional[str] = None

@app.post("/upload/", response_model=Metricas)
async def upload_model(file: UploadFile = File(...)) -> Metricas:
    """
    Recebe um arquivo XMI UML via upload, extrai as métricas técnicas do modelo (casos de uso, classes, linhas estimadas)
    e valida a estrutura XML gerada com base em um schema XSD.

    O arquivo deve representar um modelo UML exportado por ferramentas compatíveis (formato XMI 2.x ou 1.x).

    Returns:
        Metricas: Objeto contendo as métricas extraídas do modelo UML.
    """
    # O arquivo XMI representa um modelo UML exportado por ferramentas como StarUML ou Enterprise Architect
    file_bytes = await file.read()
    metricas_dict = extrair_metrica(file_bytes)
    xml_gerado = gerar_xml(metricas_dict)

    caminho_xsd = "schemas/estimatron.xsd"
    valido = validar(xml_gerado, caminho_xsd)

    if not valido:
        raise ValueError("XML gerado não válido segundo schema XSD.")

    global estado_metricas
    estado_metricas = Metricas(**metricas_dict)
    return estado_metricas

@app.get("/metrics/", response_model=Metricas)
async def get_metrics() -> Metricas:
    """
    Retorna as métricas extraídas do último arquivo processado via /upload/.

    Returns:
        Metricas: Objeto com número de casos de uso, classes e linhas estimadas.
    """
    if not estado_metricas:
        raise ValueError("Nenhuma métrica foi carregada ainda.")
    return estado_metricas

@app.post("/generate/", response_model=Proposta)
async def generate_proposal() -> Proposta:
    """
    Gera proposta comercial com escopo, esforço, prazo e custo técnico
    com base nas métricas extraídas e perfis profissionais definidos.

    Returns:
        Proposta: Estrutura contendo resumo técnico e distribuição por perfil.
    """
    if not estado_metricas:
        raise ValueError("Nenhuma métrica foi carregada ainda.")

    # Parâmetros fictícios para cálculo
    custos = {"Arquiteto": 180.0, "Dev Senior": 120.0, "Dev Pleno": 95.0}
    distribuicao = mapear_skills(estado_metricas.dict(), custos)
    resumo = estimar_cocomo(estado_metricas.linhas_estimadas, multiplicador=1.15, custo_mensal=18000.0)

    texto_final = gerar(estado_metricas.dict(), distribuicao, resumo)

    global estado_proposta
    estado_proposta = texto_final

    return Proposta(
        metricas=estado_metricas,
        distribuicao=distribuicao,
        resumo=resumo,
        conteudo=texto_final
    )

@app.get("/export/")
async def export_proposal() -> FileResponse:
    """
    Exporta a proposta comercial gerada para arquivo em formato .md.

    Observação:
        Esta rota retorna um arquivo binário gerado pelo sistema, e por isso não define um modelo de resposta.
    """
    if not estado_proposta:
        raise ValueError("Nenhuma proposta foi gerada ainda.")

    nome_arquivo = "proposta_estimatron.md"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(estado_proposta)

    return FileResponse(nome_arquivo, media_type="text/markdown", filename=nome_arquivo)
