"""
###############################################################################
📄 Estimatron 3.0 — Script: generate_docs.py

Percorre módulos Python do projeto e gera documentação técnica (Markdown)
com cabeçalhos, funções, assinaturas e docstrings dos arquivos encontrados.

Autor: MOACYR + Copilot
###############################################################################
"""

import os
import ast

# 🔍 Pastas a serem analisadas
PASTAS_ALVO = ["agents", "models", "backend", "."]
EXTENSAO = ".py"
ARQUIVO_SAIDA = "documentacao_estimatron.md"

def formatar_assinatura(func: ast.FunctionDef) -> str:
    """
    Gera a assinatura completa de uma função com tipos e retorno (se disponíveis).
    """
    partes = []
    for arg in func.args.args:
        nome = arg.arg
        tipo = ast.unparse(arg.annotation) if arg.annotation else "Any"
        partes.append(f"{nome}: {tipo}")
    args_formatados = ", ".join(partes)

    retorno = ast.unparse(func.returns) if func.returns else "None"
    return f"{func.name}({args_formatados}) -> {retorno}"

def extrair_docstrings(caminho_arquivo: str) -> str:
    """
    Extrai cabeçalho, assinaturas e docstrings de funções/classes de um arquivo .py.
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        fonte = f.read()

    resultado = ""
    try:
        modulo = ast.parse(fonte)
        doc_modulo = ast.get_docstring(modulo)
        nome = os.path.basename(caminho_arquivo)

        resultado += f"\n## 🧩 {nome}\n"
        if doc_modulo:
            resultado += f"\n> {doc_modulo.strip()}\n"

        for item in modulo.body:
            if isinstance(item, (ast.FunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(item)
                if isinstance(item, ast.FunctionDef):
                    assinatura = formatar_assinatura(item)
                    resultado += f"\n### 📘 Função: `{assinatura}`\n"
                else:
                    resultado += f"\n### 🏷️ Classe: `{item.name}`\n"
                if doc:
                    resultado += f"{doc.strip()}\n"

    except Exception as e:
        resultado += f"\n⚠️ Erro ao processar `{caminho_arquivo}`: {e}\n"

    return resultado

def gerar_documentacao():
    """
    Percorre os arquivos Python e gera a documentação consolidada.
    """
    doc_final = "# 📚 Documentação Técnica — Estimatron 3.0\n"

    for pasta in PASTAS_ALVO:
        for raiz, _, arquivos in os.walk(pasta):
            for arq in arquivos:
                if arq.endswith(EXTENSAO) and not arq.startswith("__"):
                    caminho_completo = os.path.join(raiz, arq)
                    bloco_md = extrair_docstrings(caminho_completo)
                    doc_final += bloco_md

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write(doc_final)

    print(f"✅ Documentação gerada com sucesso: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    gerar_documentacao()
