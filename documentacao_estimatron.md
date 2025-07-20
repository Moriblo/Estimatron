# 📚 Documentação Técnica — Estimatron 3.0

## 📄 Log de Atualizações Técnicas

- 📆 Execução: **2025-07-19 23:16**
- ✅ `requirements.txt` atualizado via pipreqs
- 🛠️ Pacotes essenciais adicionados manualmente: fastapi, pydantic
- ✅ Nenhuma alteração em `requirements-dev.txt`

---


# 📡 Contrato da API (FastAPI)

### `POST /upload/` → `upload_model()`
- Modelo de saída: `Metricas`
- Descrição: Recebe um arquivo XMI UML via upload, extrai as métricas técnicas do modelo (casos de uso, classes, linhas estimadas)
    e valida a estrutura XML gerada com base em um schema XSD.

    O arquivo deve representar um modelo UML exportado por ferramentas compatíveis (formato XMI 2.x ou 1.x).

    Returns:
        Metricas: Objeto contendo as métricas extraídas do modelo UML.

### `GET /metrics/` → `get_metrics()`
- Modelo de saída: `Metricas`
- Descrição: Retorna as métricas extraídas do último arquivo processado via /upload/.

    Returns:
        Metricas: Objeto com número de casos de uso, classes e linhas estimadas.

### `POST /generate/` → `generate_proposal()`
- Modelo de saída: `Proposta`
- Descrição: Gera proposta comercial com escopo, esforço, prazo e custo técnico
    com base nas métricas extraídas e perfis profissionais definidos.

    Returns:
        Proposta: Estrutura contendo resumo técnico e distribuição por perfil.

### `GET /export/` → `export_proposal()`
- Modelo de saída: `None`
- Descrição: Exporta a proposta comercial gerada para arquivo em formato .md.

    Observação:
        Esta rota retorna um arquivo binário gerado pelo sistema, e por isso não define um modelo de resposta.
- Observação: Esta rota retorna um arquivo binário gerado pelo sistema, e por isso não define um modelo de resposta.

---

## 📘 Índice de Módulos
- [main.py](#main)
- [cocomo_estimator.py](#cocomo_estimator)
- [proposal_writer.py](#proposal_writer)
- [skill_mapper.py](#skill_mapper)
- [xmi_parser.py](#xmi_parser)
- [xml_converter.py](#xml_converter)
- [xsd_validator.py](#xsd_validator)
- [schemas.py](#schemas)
- [main.py](#main)
- [cocomo_estimator.py](#cocomo_estimator)
- [proposal_writer.py](#proposal_writer)
- [skill_mapper.py](#skill_mapper)
- [xmi_parser.py](#xmi_parser)
- [xml_converter.py](#xml_converter)
- [xsd_validator.py](#xsd_validator)
- [schemas.py](#schemas)

---

## 🧩 main.py
<a name="main"></a>

> ###############################################################################
🚀 Estimatron 3.0 — Módulo principal da API

Orquestra os agentes para processar arquivos XMI UML,
gerar XML, validar via XSD, aplicar COCOMO II e compor proposta comercial.

Autor: MOACYR + Copilot
###############################################################################

## 🧩 cocomo_estimator.py
<a name="cocomo_estimator"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: cocomo_estimator

Aplica o modelo COCOMO II (Pós-Arquitetura) para estimar esforço técnico,
prazo de projeto e custo estimado com base em KLOC e fatores de ajuste.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `estimar_cocomo(tamanho_kloc: Union[int, float], multiplicador: float, custo_mensal: float) -> Dict[str, float]`
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
<a name="proposal_writer"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: proposal_writer

Gera o conteúdo final da proposta comercial com base nas métricas extraídas,
distribuição de esforço por perfil técnico e resumo da estimativa COCOMO II.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar(metricas: Dict[str, int], distribuicao: Dict[str, Dict[str, float]], resumo_cocomo: Dict[str, float]) -> str`
Gera o conteúdo textual da proposta comercial formatada.

Parâmetros:
    metricas (dict): Métricas técnicas do modelo UML.
    distribuicao (dict): Esforço por perfil com PMs e custo.
    resumo_cocomo (dict): Contém esforço, prazo e custo estimado.

Retorna:
    str: Texto formatado da proposta comercial.

## 🧩 skill_mapper.py
<a name="skill_mapper"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: skill_mapper

Mapeia métricas extraídas do modelo UML para perfis profissionais técnicos.
Aplica os custos por perfil informados via JSON e calcula distribuição de esforço.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `mapear_skills(metrica: Dict[str, int], custos_json: Dict[str, float]) -> Dict[str, Dict[str, float]]`
Distribui esforço estimado entre perfis profissionais com base nas métricas e custos.

Parâmetros:
    metrica (dict): Métricas técnicas do modelo UML.
    custos_json (dict): Tabela com custos por perfil (R$/hora).

Retorna:
    dict: Distribuição por skill contendo:
        - PM (float): Pessoa-mês estimado por perfil
        - custo_total (float): Custo calculado com base na taxa/hora

## 🧩 xmi_parser.py
<a name="xmi_parser"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xmi_parser
Responsável por interpretar arquivos XMI UML e extrair métricas técnicas
como casos de uso, classes e linhas estimadas de código. Etapa inicial
do pipeline de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `extrair_metrica(xmi_bytes: bytes) -> Dict[str, int]`
Extrai métricas técnicas de um arquivo XMI UML.

Parâmetros:
    xmi_bytes (bytes): Conteúdo bruto do arquivo XMI.

Retorna:
    dict: Métricas estimadas contendo:
        - casosdeuso (int): total de casos de uso detectados
        - classes (int): total de classes identificadas
        - linhas_estimadas (int): estimativa de LOC com base na complexidade

## 🧩 xml_converter.py
<a name="xml_converter"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xml_converter
Gera um XML técnico e validável com base nas métricas extraídas do modelo UML.
Esse XML será validado posteriormente contra um schema XSD no pipeline técnico.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar_xml(metricas: Dict[str, int]) -> str`
Gera uma string XML estruturada a partir das métricas do modelo UML.

Parâmetros:
    metricas (dict): Dicionário contendo:
        - casosdeuso (int)
        - classes (int)
        - linhas_estimadas (int)

Retorna:
    str: XML em formato string pronto para validação via XSD.

## 🧩 xsd_validator.py
<a name="xsd_validator"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xsd_validator
Valida documentos XML gerados contra um esquema XSD. Essa etapa garante
conformidade estrutural antes de aplicar os modelos de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `validar(xml_string: str, xsd_path: str) -> bool`
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
<a name="schemas"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: schemas

Define modelos Pydantic para validação de entrada e saída na API.
Utilizado opcionalmente nos endpoints para tipagem forte e compatibilidade OpenAPI.

Autor: MOACYR + Copilot
###############################################################################

### 🏷️ Classe: `Metricas`
Representa as métricas técnicas extraídas de um modelo UML.

### 🏷️ Classe: `PerfilDistribuido`
Representa o esforço técnico e custo por perfil profissional.

### 🏷️ Classe: `Proposta`
Estrutura para o retorno da proposta comercial.

## 🧩 main.py
<a name="main"></a>

> ###############################################################################
🚀 Estimatron 3.0 — Módulo principal da API

Orquestra os agentes para processar arquivos XMI UML,
gerar XML, validar via XSD, aplicar COCOMO II e compor proposta comercial.

Autor: MOACYR + Copilot
###############################################################################

## 🧩 cocomo_estimator.py
<a name="cocomo_estimator"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: cocomo_estimator

Aplica o modelo COCOMO II (Pós-Arquitetura) para estimar esforço técnico,
prazo de projeto e custo estimado com base em KLOC e fatores de ajuste.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `estimar_cocomo(tamanho_kloc: Union[int, float], multiplicador: float, custo_mensal: float) -> Dict[str, float]`
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
<a name="proposal_writer"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: proposal_writer

Gera o conteúdo final da proposta comercial com base nas métricas extraídas,
distribuição de esforço por perfil técnico e resumo da estimativa COCOMO II.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar(metricas: Dict[str, int], distribuicao: Dict[str, Dict[str, float]], resumo_cocomo: Dict[str, float]) -> str`
Gera o conteúdo textual da proposta comercial formatada.

Parâmetros:
    metricas (dict): Métricas técnicas do modelo UML.
    distribuicao (dict): Esforço por perfil com PMs e custo.
    resumo_cocomo (dict): Contém esforço, prazo e custo estimado.

Retorna:
    str: Texto formatado da proposta comercial.

## 🧩 skill_mapper.py
<a name="skill_mapper"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: skill_mapper

Mapeia métricas extraídas do modelo UML para perfis profissionais técnicos.
Aplica os custos por perfil informados via JSON e calcula distribuição de esforço.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `mapear_skills(metrica: Dict[str, int], custos_json: Dict[str, float]) -> Dict[str, Dict[str, float]]`
Distribui esforço estimado entre perfis profissionais com base nas métricas e custos.

Parâmetros:
    metrica (dict): Métricas técnicas do modelo UML.
    custos_json (dict): Tabela com custos por perfil (R$/hora).

Retorna:
    dict: Distribuição por skill contendo:
        - PM (float): Pessoa-mês estimado por perfil
        - custo_total (float): Custo calculado com base na taxa/hora

## 🧩 xmi_parser.py
<a name="xmi_parser"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xmi_parser
Responsável por interpretar arquivos XMI UML e extrair métricas técnicas
como casos de uso, classes e linhas estimadas de código. Etapa inicial
do pipeline de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `extrair_metrica(xmi_bytes: bytes) -> Dict[str, int]`
Extrai métricas técnicas de um arquivo XMI UML.

Parâmetros:
    xmi_bytes (bytes): Conteúdo bruto do arquivo XMI.

Retorna:
    dict: Métricas estimadas contendo:
        - casosdeuso (int): total de casos de uso detectados
        - classes (int): total de classes identificadas
        - linhas_estimadas (int): estimativa de LOC com base na complexidade

## 🧩 xml_converter.py
<a name="xml_converter"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xml_converter
Gera um XML técnico e validável com base nas métricas extraídas do modelo UML.
Esse XML será validado posteriormente contra um schema XSD no pipeline técnico.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `gerar_xml(metricas: Dict[str, int]) -> str`
Gera uma string XML estruturada a partir das métricas do modelo UML.

Parâmetros:
    metricas (dict): Dicionário contendo:
        - casosdeuso (int)
        - classes (int)
        - linhas_estimadas (int)

Retorna:
    str: XML em formato string pronto para validação via XSD.

## 🧩 xsd_validator.py
<a name="xsd_validator"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: xsd_validator
Valida documentos XML gerados contra um esquema XSD. Essa etapa garante
conformidade estrutural antes de aplicar os modelos de estimativa.

Autor: MOACYR + Copilot
###############################################################################

### 📘 Função: `validar(xml_string: str, xsd_path: str) -> bool`
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
<a name="schemas"></a>

> ###############################################################################
📦 Estimatron 3.0 — Módulo: schemas

Define modelos Pydantic para validação de entrada e saída na API.
Utilizado opcionalmente nos endpoints para tipagem forte e compatibilidade OpenAPI.

Autor: MOACYR + Copilot
###############################################################################

### 🏷️ Classe: `Metricas`
Representa as métricas técnicas extraídas de um modelo UML.

### 🏷️ Classe: `PerfilDistribuido`
Representa o esforço técnico e custo por perfil profissional.

### 🏷️ Classe: `Proposta`
Estrutura para o retorno da proposta comercial.
