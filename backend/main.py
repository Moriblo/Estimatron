"""
###############################################################################
🚀 Estimatron 3.0 — Módulo principal da API

Orquestra os agentes para processar arquivos XMI e JSON,
gerar XML, validar via XSD, aplicar COCOMO II e compor proposta comercial.

Autor: MOACYR + Copilot
###############################################################################
"""

from fastapi import FastAPI, UploadFile, File, Response
from fastapi.responses import JSONResponse
from typing import Dict
import json

# 📦 Agentes técnicos
from agents import (
    xmi_parser,
    xml_converter,
    xsd_validator,
    skill_mapper,
    cocomo_estimator,
    proposal_writer
)

# 📘 Modelos tipados
from models.schemas import Metricas, Proposta

# 📂 Caminho para o esquema XSD
XSD_PATH = "utils/xsd/schema.xsd"

app = FastAPI(title="Estimatron 3.0")

# 🗂️ Cache técnico para endpoints auxiliares
cache_metricas: Dict = {}
cache_proposta: str = ""

@app.post("/upload/", response_model=Metricas)
async def upload_model(xmifile: UploadFile = File(...), custos_json: UploadFile = File(...)) -> JSONResponse:
    """
    Extrai métricas técnicas do modelo UML e valida XML com esquema XSD.
    """
    try:
        xmi_bytes = await xmifile.read()
        custos_bytes = await custos_json.read()
        custos_data = json.loads(custos_bytes)

        metricas = xmi_parser.extrair_metrica(xmi_bytes)
        xml_string = xml_converter.gerar_xml(metricas)
        xsd_validator.validar(xml_string, XSD_PATH)

        cache_metricas.clear()
        cache_metricas.update(metricas)

        return JSONResponse(content=metricas)
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

@app.get("/metrics/", response_model=Metricas)
async def get_metrics() -> JSONResponse:
    """
    Retorna as métricas extraídas do último arquivo processado.
    """
    if cache_metricas:
        return JSONResponse(content=cache_metricas)
    return JSONResponse(status_code=404, content={"erro": "Nenhuma métrica disponível"})

@app.post("/generate/", response_model=Proposta)
async def generate_proposal(xmifile: UploadFile = File(...), custos_json: UploadFile = File(...)) -> JSONResponse:
    """
    Gera proposta comercial com escopo, esforço, prazo e custo técnico.
    """
    try:
        xmi_bytes = await xmifile.read()
        custos_bytes = await custos_json.read()
        custos_data = json.loads(custos_bytes)

        metricas = xmi_parser.extrair_metrica(xmi_bytes)
        xml_string = xml_converter.gerar_xml(metricas)
        xsd_validator.validar(xml_string, XSD_PATH)

        resumo_cocomo = cocomo_estimator.estimar_cocomo(
            tamanho_kloc=metricas["linhas_estimadas"] / 1000,
            multiplicador=1.15,
            custo_mensal=18000
        )

        distribuicao = skill_mapper.mapear_skills(metricas, custos_data)

        proposta_texto = proposal_writer.gerar(metricas, distribuicao, resumo_cocomo)

        cache_metricas.clear()
        cache_metricas.update(metricas)
        global cache_proposta
        cache_proposta = proposta_texto

        return JSONResponse(content={"texto": proposta_texto})
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

@app.get("/export/")
async def export_proposal(format: str = "md") -> Response:
    """
    Exporta a proposta gerada em formato .md, .txt ou .pdf.
    """
    if format not in ["md", "txt", "pdf"]:
        return JSONResponse(status_code=400, content={"erro": "Formato inválido"})
    if not cache_proposta:
        return JSONResponse(status_code=404, content={"erro": "Nenhuma proposta disponível"})

    filename = f"proposta.{format}"
    mime = {
        "md": "text/markdown",
        "txt": "text/plain",
        "pdf": "application/pdf"
    }.get(format, "application/octet-stream")

    return Response(content=cache_proposta, media_type=mime, headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })


