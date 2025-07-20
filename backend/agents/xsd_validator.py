"""
###############################################################################
📦 Estimatron 3.0 — Módulo: xsd_validator
Valida documentos XML gerados contra um esquema XSD. Essa etapa garante
conformidade estrutural antes de aplicar os modelos de estimativa.

Autor: MOACYR + Copilot
###############################################################################
"""

from lxml import etree
from fastapi import FastAPI

def validar(xml_string: str, xsd_path: str) -> bool:
    """
    Valida um documento XML contra um esquema XSD.

    Parâmetros:
        xml_string (str): Conteúdo XML como string.
        xsd_path (str): Caminho absoluto ou relativo para o arquivo .xsd

    Retorna:
        bool: True se o XML for válido segundo o XSD.

    Levanta:
        etree.XMLSyntaxError: Se o XML ou o XSD estiver malformado.
        etree.DocumentInvalid: Se o XML não atender à estrutura definida no XSD.
    """
    # 📥 Carrega o schema XSD
    with open(xsd_path, "rb") as xsd_file:
        schema_root = etree.XML(xsd_file.read())
        schema = etree.XMLSchema(schema_root)

    # 📄 Interpreta a string XML
    xml_doc = etree.fromstring(xml_string.encode("utf-8"))

    # 🛡️ Valida o XML contra o XSD
    schema.assertValid(xml_doc)
    return True
