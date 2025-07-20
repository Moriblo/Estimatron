"""
###############################################################################
📄 Estimatron 3.0 — Script: generate_docs.py

Orquestrador técnico do projeto:
- Gera documentação consolidada em Markdown dos módulos Python
- Extrai contrato da API FastAPI, docstrings, classes e assinaturas com tipos
- Gera automaticamente requirements.txt (produção) e requirements-dev.txt (desenvolvimento)
- Registra log técnico com data, bibliotecas alteradas e instruções corretivas
- Ignora rotas internas do FastAPI na documentação da API
- Adiciona observações para rotas com resposta binária
- Inclui pacotes essenciais se não forem detectados pelo pipreqs

Autor: MOACYR + Copilot
###############################################################################
"""

import os
import sys
import ast
import difflib
import importlib.util
import subprocess
from datetime import datetime
from typing import List, Tuple
from fastapi.responses import FileResponse  # usado para detectar rotas binárias

# ✅ Corrige o caminho dos módulos locais (usados em main.py)
# Assume que generate_docs.py está em backend/
base_dir = os.path.dirname(__file__)

# Garante acesso aos submódulos usados por main.py
sys.path.insert(0, os.path.abspath(base_dir))                             # backend/ → para importar main.py diretamente
sys.path.insert(0, os.path.abspath(os.path.join(base_dir, "models")))     # backend/models → onde está schemas.py
sys.path.insert(0, os.path.abspath(os.path.join(base_dir, "agents")))     # backend/agents → onde estão xmi_parser.py, etc


# 📁 Estrutura de projeto
PASTAS_ALVO = ["agents", "models", "backend", "."]
MODULOS_IGNORADOS = ["generate_docs.py", "__init__.py"]
EXTENSAO = ".py"

# 📄 Arquivos gerados
ARQUIVO_MD = "documentacao_estimatron.md"
REQ_PROD = "requirements.txt"
REQ_DEV = "requirements-dev.txt"
REQ_DEV_TEMP = "requirements-dev-temp.txt"

# 📦 Dependências mínimas obrigatórias
REQUIRED_PACKAGES = ["fastapi", "pydantic", "lxml"]
PACOTES_ESSENCIAIS = {
    "fastapi": "0.116.1",
    "pydantic": "2.11.7"
}

def checar_dependencias() -> None:
    faltantes = [pkg for pkg in REQUIRED_PACKAGES if importlib.util.find_spec(pkg) is None]
    if faltantes:
        print("⚠️ Dependências ausentes:", ", ".join(faltantes))
        print(f"💡 Instale com: pip install {' '.join(faltantes)}")
        sys.exit(1)

def formatar_assinatura(func: ast.FunctionDef) -> str:
    partes = []
    for arg in func.args.args:
        nome = arg.arg
        tipo = ast.unparse(arg.annotation) if arg.annotation else "Any"
        partes.append(f"{nome}: {tipo}")
    args_formatados = ", ".join(partes)
    retorno = ast.unparse(func.returns) if func.returns else "None"
    return f"{func.name}({args_formatados}) -> {retorno}"

def extrair_docstrings(caminho_arquivo: str, modulos_detectados: List[Tuple[str, str]]) -> str:
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        fonte = f.read()

    resultado = ""
    try:
        modulo = ast.parse(fonte)
        doc_modulo = ast.get_docstring(modulo)
        nome_arquivo = os.path.basename(caminho_arquivo)
        nome_id = nome_arquivo.replace(".py", "").lower()
        modulos_detectados.append((nome_arquivo, nome_id))

        resultado += f"\n## 🧩 {nome_arquivo}\n<a name=\"{nome_id}\"></a>\n"
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

def extrair_contrato_api() -> str:
    rotas_ignoradas = {
        "/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"
    }

    try:
        from main import app
        from fastapi.responses import FileResponse
    except ModuleNotFoundError as e:
        return f"\n⚠️ Não foi possível importar `main.py` ou inicializar FastAPI:\nO módulo requerido `{e.name}` não está instalado.\n💡 Para resolver, execute: `pip install {e.name}`\n"
    except Exception as e:
        return f"\n⚠️ Erro ao importar `main.py` ou construir `app`: {e}\n"

    resultado = "\n# 📡 Contrato da API (FastAPI)\n"
    for rota in app.routes:
        if rota.path in rotas_ignoradas:
            continue
        if hasattr(rota, "endpoint"):
            caminho = rota.path
            metodo = ",".join(rota.methods - {"HEAD", "OPTIONS"})
            nome_funcao = rota.endpoint.__name__
            doc = getattr(rota.endpoint, "__doc__", "") or "Sem descrição."
            modelo = getattr(rota, "response_model", None)
            tipo_saida = modelo.__name__ if modelo else "None"
            resultado += f"\n### `{metodo} {caminho}` → `{nome_funcao}()`\n"
            resultado += f"- Modelo de saída: `{tipo_saida}`\n"
            resultado += f"- Descrição: {doc.strip()}\n"

            retorno_funcao = rota.endpoint.__annotations__.get("return", "")
            if "FileResponse" in str(retorno_funcao) and modelo is None:
                resultado += "- Observação: Esta rota retorna um arquivo binário gerado pelo sistema, e por isso não define um modelo de resposta.\n"

    return resultado

def gerar_requirements_txt() -> bool:
    try:
        subprocess.run([
            "pipreqs",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            "--encoding=utf-8",
            "--force"
        ], check=True)

        garantir_pacotes_essenciais()
        return True
    except Exception as e:
        print(f"⚠️ Erro ao gerar requirements.txt: {e}")
        return False



def garantir_pacotes_essenciais() -> None:
    try:
        with open(REQ_PROD, "r", encoding="utf-8") as f:
            linhas = f.read().splitlines()
        presentes = set(linhas)
        modificou = False
        for nome, versao in PACOTES_ESSENCIAIS.items():
            if not any(nome in linha for linha in presentes):
                linhas.append(f"{nome}=={versao}")
                modificou = True
        if modificou:
            with open(REQ_PROD, "w", encoding="utf-8") as f:
                f.write("\n".join(linhas))
            print("🔧 Pacotes essenciais adicionados manualmente ao requirements.txt")
    except Exception as e:
        print(f"⚠️ Erro ao garantir pacotes essenciais: {e}")

def gerar_requirements_dev_txt() -> List[str]:
    try:
        subprocess.run(["pip", "freeze"], stdout=open(REQ_DEV_TEMP, "w"), check=True)
        if os.path.exists(REQ_DEV):
            with open(REQ_DEV, "r", encoding="utf-8") as old, open(REQ_DEV_TEMP, "r", encoding="utf-8") as new:
                antigo = old.readlines()
                atual = new.readlines()
            bruto_diff = difflib.unified_diff(antigo, atual, lineterm="")
            delta = [linha.strip() for linha in bruto_diff if linha.startswith("+") or linha.startswith("-")]
        else:
            delta = ["(arquivo criado pela primeira vez)"]
        os.replace(REQ_DEV_TEMP, REQ_DEV)
        os.remove(REQ_DEV_TEMP) if os.path.exists(REQ_DEV_TEMP) else None
        return delta
    except Exception as e:
        return [f"⚠️ Erro ao gerar requirements-dev.txt: {e}"]

def gerar_documentacao() -> None:
    checar_dependencias()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    modulos_detectados: List[Tuple[str, str]] = []

    log_md = f"## 📄 Log de Atualizações Técnicas\n\n"
    log_md += f"- 📆 Execução: **{timestamp}**\n"

    sucesso_reqs = gerar_requirements_txt()
    log_md += "- ✅ `requirements.txt` atualizado via pipreqs\n" if sucesso_reqs else "- ⚠️ Erro ao atualizar `requirements.txt`\n"
    log_md += "- 🛠️ Pacotes essenciais adicionados manualmente: fastapi, pydantic\n"

    diffs_dev = gerar_requirements_dev_txt()
    if diffs_dev:
        log_md += "- 🔎 Mudanças detectadas em `requirements-dev.txt`:\n"
        for linha in diffs_dev:
            log_md += f"  {linha}\n"
    else:
        log_md += "- ✅ Nenhuma alteração em `requirements-dev.txt`\n"

    doc_final = "# 📚 Documentação Técnica — Estimatron 3.0\n\n"
    doc_final += log_md
    doc_final += "\n---\n\n" + extrair_contrato_api()
    doc_final += "\n---\n\n## 📘 Índice de Módulos\n"

    conteudo_modular = ""
    for pasta in PASTAS_ALVO:
        for raiz, _, arquivos in os.walk(pasta):
            for arq in arquivos:
                if arq.endswith(EXTENSAO) and arq not in MODULOS_IGNORADOS:
                    caminho_completo = os.path.join(raiz, arq)
                    bloco = extrair_docstrings(caminho_completo, modulos_detectados)
                    conteudo_modular += bloco

    # 🗂️ Gera índice com âncoras dos módulos
    for nome, anchor in modulos_detectados:
        doc_final += f"- [{nome}](#{anchor})\n"

    doc_final += "\n---\n"
    doc_final += conteudo_modular

    # 📄 Salva arquivo Markdown
    with open(ARQUIVO_MD, "w", encoding="utf-8") as f:
        f.write(doc_final)

    print(f"\n✅ Documentação gerada com sucesso: {ARQUIVO_MD}")
    print(f"📦 requirements.txt e requirements-dev.txt atualizados.")
    print("📘 Log inserido no topo do Markdown.\n")

if __name__ == "__main__":
    gerar_documentacao()
