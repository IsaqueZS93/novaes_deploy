# Novaes Ops — Sistema Corporativo de Gestão de Contratos (Saneamento/Perdas)

## 1) Arquitetura recomendada (implementada)
- **Monólito modular Django** com separação por contexto de negócio em apps (`clients`, `contracts`, `planning`, `execution`, `finance`, etc.).
- Camadas organizadas por módulo: `models`, `forms`, `views`, `services`, `urls`, `templates`.
- Cálculos gerenciais centralizados em serviços (`apps/dashboards/services.py`, `apps/contracts/services.py`) para evolução futura e testes.
- Estrutura preparada para crescimento com novos módulos sem acoplamento excessivo.

## 2) Stack final escolhida
- Python 3.11+
- Django 5
- Bootstrap 5 + Bootstrap Icons
- HTMX para evolução de interações dinâmicas
- Chart.js (dashboards)
- FullCalendar (cronograma semanal)
- SQLite local (inicial), com caminho claro para PostgreSQL

## 3) Estrutura de diretórios
```text
.
├── manage.py
├── config/
├── apps/
│   ├── accounts/
│   ├── clients/
│   ├── contracts/
│   ├── teams/
│   ├── planning/
│   ├── execution/
│   ├── finance/
│   ├── dashboards/
│   ├── reports/
│   └── core/
├── templates/
├── static/
├── media/
└── docs/
```

## 4) Modelagem de entidades
- Usuários e perfis (`User`, `Role`)
- Clientes (`Client`)
- Contratos e serviços por contrato (`Contract`, `ContractService`, `ServiceCategory`)
- Operação de campo (`Team`, `WeeklyPlanning`, `DailyExecution`)
- Financeiro (`CostCategory`, `CostExpense`, `Revenue`, `CenterCost`)
- Suporte (`Attachment`, `MovementHistory`)

## 5) Fluxo de navegação das telas
1. Login
2. Dashboard gerencial com filtros
3. Clientes
4. Contratos (lista)
5. Contrato detalhe (abas: resumo, serviços, cronograma, execução, custos, receitas)
6. Equipes
7. Cronograma semanal (calendário + comparativo planejado x executado)
8. Execução diária (diário operacional com filtros)
9. Custos e despesas
10. Receitas/faturamento
11. Relatórios e exportação CSV

## 6) Funcionalidades entregues por fase
### Fase 1
- Projeto Django e arquitetura modular
- Base de dados e domínio inicial

### Fase 2
- Login Django + estrutura de usuários
- CRUD de Clientes
- CRUD de Contratos e Serviços por contrato

### Fase 3
- CRUD Equipes
- Módulo de Planejamento semanal com FullCalendar
- Módulo de Execução diária com filtros

### Fase 4
- Custos e Despesas
- Receitas/Faturamento
- Apuração de indicadores por contrato e dashboard

### Fase 5
- Dashboard com filtros e gráficos reais
- Relatório operacional com exportação CSV

### Fase 6
- Refino visual premium com layout corporativo
- Documentação técnica

## 7) Como executar localmente
1. Criar e ativar virtualenv
2. Instalar dependências: `pip install -r requirements.txt`
3. Rodar migrações: `python manage.py migrate`
4. Criar superusuário: `python manage.py createsuperuser`
5. Subir servidor: `python manage.py runserver`

## 8) Próximos incrementos recomendados
- Permissões granulares por ação/módulo (RBAC completo)
- Exportação PDF/Excel avançada
- Módulo de anexos por entidade com storage desacoplado
- Histórico automatizado via sinais de domínio
- API REST para integração mobile/BI
