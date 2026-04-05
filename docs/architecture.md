# Arquitetura Técnica

## Princípios
- Modularidade por domínio de negócio
- Separação de responsabilidades (views finas + services para cálculo)
- Evolução incremental por fases
- Reuso de componentes visuais e template base

## Núcleo de negócio
- **Planejamento semanal** (`apps/planning`) com calendário e filtros
- **Execução diária** (`apps/execution`) com diário operacional filtrável
- **Comparativo planejado x executado** (`apps/planning/services.py`)
- **Apuração financeira e operacional** (`apps/contracts/services.py`, `apps/dashboards/services.py`)

## Escalabilidade
- Fácil inclusão de novos apps sem quebrar módulos atuais
- Modelo pronto para mover cálculos para tarefas assíncronas no futuro
- Compatível com migração para PostgreSQL e criação de APIs DRF
