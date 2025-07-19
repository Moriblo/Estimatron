# 📚 Documentação Técnica — Estimatron 3.0

## 🧩 generate_docs.py

> ###############################################################################
📄 Estimatron 3.0 — Script: generate_docs.py

Percorre módulos Python do projeto e gera uma documentação estática (Markdown)
com os cabeçalhos, nomes de funções e docstrings dos arquivos encontrados.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `extrair_docstrings()`
Extrai cabeçalho e docstrings de funções/classes de um arquivo .py

Parâmetros:
    caminho_arquivo (str): Caminho completo para o módulo Python

Retorna:
    str: Bloco Markdown com documentação encontrada

### 📘 Função: `gerar_documentacao()`
Percorre as pastas-alvo e gera o arquivo Markdown consolidado.

## 🧩 main.py

> ###############################################################################
🚀 Estimatron 3.0 — Módulo principal da API

Orquestra os agentes para processar arquivos XMI e JSON,
gerar XML, validar via XSD, aplicar COCOMO II e compor proposta comercial.

Autor: MOACYR + Copilot
###############################################################################

## 🧩 cocomo_estimator.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: cocomo_estimator

Aplica o modelo COCOMO II (Pós-Arquitetura) para estimar esforço técnico,
prazo de projeto e custo estimado com base em KLOC e fatores de ajuste.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `estimar_cocomo()`
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

## 🧩 proposal_writer.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: proposal_writer

Gera o conteúdo final da proposta comercial com base nas métricas extraídas,
distribuição de esforço por perfil técnico e resumo da estimativa COCOMO II.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar()`
Gera o conteúdo textual da proposta comercial formatada.

Parâmetros:
    metricas (dict): Métricas técnicas do modelo UML.
    distribuicao (dict): Esforço por perfil com PMs e custo.
    resumo_cocomo (dict): Contém esforço, prazo e custo estimado.

Retorna:
    str: Texto formatado da proposta comercial.

## 🧩 skill_mapper.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: skill_mapper

Mapeia métricas extraídas do modelo UML para perfis profissionais técnicos.
Aplica os custos por perfil informados via JSON e calcula distribuição de esforço.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `mapear_skills()`
Distribui esforço estimado entre perfis profissionais com base nas métricas e custos.

Parâmetros:
    metrica (dict): Métricas técnicas do modelo UML.
    custos_json (dict): Tabela com custos por perfil (R$/hora).

Retorna:
    dict: Distribuição por skill contendo:
        - PM (float): Pessoa-mês estimado por perfil
        - custo_total (float): Custo calculado com base na taxa/hora

## 🧩 xmi_parser.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xmi_parser
Responsável por interpretar arquivos XMI UML e extrair métricas técnicas
como casos de uso, classes e linhas estimadas de código. Etapa inicial
do pipeline de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `extrair_metrica()`
Extrai métricas técnicas de um arquivo XMI UML.

Parâmetros:
    xmi_bytes (bytes): Conteúdo bruto do arquivo XMI.

Retorna:
    dict: Métricas estimadas contendo:
        - casosdeuso (int): total de casos de uso detectados
        - classes (int): total de classes identificadas
        - linhas_estimadas (int): estimativa de LOC com base na complexidade

## 🧩 xml_converter.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xml_converter
Gera um XML técnico e validável com base nas métricas extraídas do modelo UML.
Esse XML será validado posteriormente contra um schema XSD no pipeline técnico.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar_xml()`
Gera uma string XML estruturada a partir das métricas do modelo UML.

Parâmetros:
    metricas (dict): Dicionário contendo:
        - casosdeuso (int)
        - classes (int)
        - linhas_estimadas (int)

Retorna:
    str: XML em formato string pronto para validação via XSD.

## 🧩 xsd_validator.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xsd_validator
Valida documentos XML gerados contra um esquema XSD. Essa etapa garante
conformidade estrutural antes de aplicar os modelos de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `validar()`
Valida um documento XML contra um esquema XSD.

Parâmetros:
    xml_string (str): Conteúdo XML como string.
    xsd_path (str): Caminho absoluto ou relativo para o arquivo .xsd

Retorna:
    bool: True se o XML for válido segundo o XSD.

Levanta:
    etree.XMLSyntaxError: Se o XML ou o XSD estiver malformado.
    etree.DocumentInvalid: Se o XML não atender à estrutura definida no XSD.

## 🧩 schemas.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: schemas

Define modelos Pydantic para validação de entrada e saída na API.
Utilizado opcionalmente nos endpoints para tipagem forte e compatibilidade OpenAPI.

Autor: MOACYR + Copilot
###############################################################################

### 🏷️ Classe: `Metricas()`
Representa as métricas técnicas extraídas de um modelo UML.

### 🏷️ Classe: `PerfilDistribuido()`
Representa o esforço técnico e custo por perfil profissional.

### 🏷️ Classe: `Proposta()`
Estrutura para o retorno da proposta comercial.

## 🧩 generate_docs.py

> ###############################################################################
📄 Estimatron 3.0 — Script: generate_docs.py

Percorre módulos Python do projeto e gera uma documentação estática (Markdown)
com os cabeçalhos, nomes de funções e docstrings dos arquivos encontrados.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `extrair_docstrings()`
Extrai cabeçalho e docstrings de funções/classes de um arquivo .py

Parâmetros:
    caminho_arquivo (str): Caminho completo para o módulo Python

Retorna:
    str: Bloco Markdown com documentação encontrada

### 📘 Função: `gerar_documentacao()`
Percorre as pastas-alvo e gera o arquivo Markdown consolidado.

## 🧩 main.py

> ###############################################################################
🚀 Estimatron 3.0 — Módulo principal da API

Orquestra os agentes para processar arquivos XMI e JSON,
gerar XML, validar via XSD, aplicar COCOMO II e compor proposta comercial.

Autor: MOACYR + Copilot
###############################################################################

## 🧩 cocomo_estimator.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: cocomo_estimator

Aplica o modelo COCOMO II (Pós-Arquitetura) para estimar esforço técnico,
prazo de projeto e custo estimado com base em KLOC e fatores de ajuste.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `estimar_cocomo()`
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

## 🧩 proposal_writer.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: proposal_writer

Gera o conteúdo final da proposta comercial com base nas métricas extraídas,
distribuição de esforço por perfil técnico e resumo da estimativa COCOMO II.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar()`
Gera o conteúdo textual da proposta comercial formatada.

Parâmetros:
    metricas (dict): Métricas técnicas do modelo UML.
    distribuicao (dict): Esforço por perfil com PMs e custo.
    resumo_cocomo (dict): Contém esforço, prazo e custo estimado.

Retorna:
    str: Texto formatado da proposta comercial.

## 🧩 skill_mapper.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: skill_mapper

Mapeia métricas extraídas do modelo UML para perfis profissionais técnicos.
Aplica os custos por perfil informados via JSON e calcula distribuição de esforço.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `mapear_skills()`
Distribui esforço estimado entre perfis profissionais com base nas métricas e custos.

Parâmetros:
    metrica (dict): Métricas técnicas do modelo UML.
    custos_json (dict): Tabela com custos por perfil (R$/hora).

Retorna:
    dict: Distribuição por skill contendo:
        - PM (float): Pessoa-mês estimado por perfil
        - custo_total (float): Custo calculado com base na taxa/hora

## 🧩 xmi_parser.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xmi_parser
Responsável por interpretar arquivos XMI UML e extrair métricas técnicas
como casos de uso, classes e linhas estimadas de código. Etapa inicial
do pipeline de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `extrair_metrica()`
Extrai métricas técnicas de um arquivo XMI UML.

Parâmetros:
    xmi_bytes (bytes): Conteúdo bruto do arquivo XMI.

Retorna:
    dict: Métricas estimadas contendo:
        - casosdeuso (int): total de casos de uso detectados
        - classes (int): total de classes identificadas
        - linhas_estimadas (int): estimativa de LOC com base na complexidade

## 🧩 xml_converter.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xml_converter
Gera um XML técnico e validável com base nas métricas extraídas do modelo UML.
Esse XML será validado posteriormente contra um schema XSD no pipeline técnico.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar_xml()`
Gera uma string XML estruturada a partir das métricas do modelo UML.

Parâmetros:
    metricas (dict): Dicionário contendo:
        - casosdeuso (int)
        - classes (int)
        - linhas_estimadas (int)

Retorna:
    str: XML em formato string pronto para validação via XSD.

## 🧩 xsd_validator.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xsd_validator
Valida documentos XML gerados contra um esquema XSD. Essa etapa garante
conformidade estrutural antes de aplicar os modelos de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `validar()`
Valida um documento XML contra um esquema XSD.

Parâmetros:
    xml_string (str): Conteúdo XML como string.
    xsd_path (str): Caminho absoluto ou relativo para o arquivo .xsd

Retorna:
    bool: True se o XML for válido segundo o XSD.

Levanta:
    etree.XMLSyntaxError: Se o XML ou o XSD estiver malformado.
    etree.DocumentInvalid: Se o XML não atender à estrutura definida no XSD.

## 🧩 schemas.py

> ###############################################################################
📦 Estimatron 3.0 — Módulo: schemas

Define modelos Pydantic para validação de entrada e saída na API.
Utilizado opcionalmente nos endpoints para tipagem forte e compatibilidade OpenAPI.

Autor: MOACYR + Copilot
###############################################################################

### 🏷️ Classe: `Metricas()`
Representa as métricas técnicas extraídas de um modelo UML.

### 🏷️ Classe: `PerfilDistribuido()`
Representa o esforço técnico e custo por perfil profissional.

### 🏷️ Classe: `Proposta()`
Estrutura para o retorno da proposta comercial.
