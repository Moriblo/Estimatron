# Estimatron

```
Estimatron_3.0/
├── backend/
│   ├── main.py                      # Orquestra a API REST com FastAPI
│   ├── generate_docs.py             # Gera documentação automática via docstrings
│   ├── agents/                      # Agentes inteligentes do pipeline técnico
│   │   ├── xmi_parser.py            # Extrai métricas técnicas do XMI
│   │   ├── xml_converter.py         # (Futuramente) Converte XMI para XML simplificado
│   │   ├── xsd_validator.py         # Valida XML com base no schema XSD
│   │   ├── skill_mapper.py          # Mapeia perfis profissionais e aplica custos
│   │   ├── cocomo_estimator.py      # Calcula esforço técnico com COCOMO II
│   │   └── proposal_writer.py       # Compõe proposta comercial final
│   ├── models/
│   │   └── schemas.py               # (Opcional) Modelos pydantic para validação de dados
│   ├── utils/
│   │   └── xsd/
│   │       └── schema.xsd           # Esquema XML para validação estrutural do projeto
│   └── requirements.txt             # Lista de dependências do backend
├── frontend/
│   ├── app.py                       # Interface Streamlit (a desenvolver)
│   └── requirements.txt             # Dependências do frontend
├── data/
│   ├── exemplo.xmi                  # Exemplo de arquivo UML XMI
│   ├── custos.json                  # JSON de entrada com custos por skill
│   ├── modelo.xml                   # XML intermediário gerado (futuramente)
│   └── proposta.md                  # Saída gerada da proposta comercial
├── README.md                        # Instruções e visão geral do projeto
└── docker-compose.yml               # (Opcional) Orquestração para deploy containerizado
```
