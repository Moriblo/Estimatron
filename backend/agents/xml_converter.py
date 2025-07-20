"""
###############################################################################
📦 Estimatron 3.0 — Módulo: xml_converter
Gera um XML técnico e validável com base nas métricas extraídas do modelo UML.
Esse XML será validado posteriormente contra um schema XSD no pipeline técnico.

Autor: MOACYR + Copilot
###############################################################################
"""

import xml.etree.ElementTree as ET
from fastapi import FastAPI
from typing import Dict

def gerar_xml(metricas: Dict[str, int]) -> str:
    """
    Gera uma string XML estruturada a partir das métricas do modelo UML.

    Parâmetros:
        metricas (dict): Dicionário contendo:
            - casosdeuso (int)
            - classes (int)
            - linhas_estimadas (int)

    Retorna:
        str: XML em formato string pronto para validação via XSD.
    """
    # 🔧 Criação do elemento raiz
    raiz = ET.Element("ModeloUML")

    # 📊 Inserção de elementos filhos com as métricas
    ET.SubElement(raiz, "CasosDeUso").text = str(metricas.get("casosdeuso", 0))
    ET.SubElement(raiz, "Classes").text = str(metricas.get("classes", 0))
    ET.SubElement(raiz, "LinhasEstimadas").text = str(metricas.get("linhas_estimadas", 0))

    # 🔄 Geração da string XML final
    xml_string = ET.tostring(raiz, encoding="utf-8", method="xml").decode("utf-8")
    return xml_string
