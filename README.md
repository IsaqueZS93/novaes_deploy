# Novaes Deploy - Sistema Corporativo de Gestão de Contratos

## Visão geral
Plataforma web em Django para gestão operacional e financeira de contratos de saneamento (setor de perdas), com módulos de clientes, contratos, serviços, equipes, planejamento semanal, execução diária, custos, receitas, dashboards e relatórios.

## Stack
- Python 3.11+
- Django 5 (estrutura preparada)
- Bootstrap 5 + Bootstrap Icons
- Chart.js (KPI/financeiro)
- FullCalendar (cronograma)
- SQLite (dev local)

## Como executar
1. Crie e ative um ambiente virtual.
2. Instale dependências: `pip install -r requirements.txt`
3. Execute migrações: `python manage.py migrate`
4. Crie superusuário: `python manage.py createsuperuser`
5. Rode o servidor: `python manage.py runserver`

## Roadmap implementado
- Fase 1: arquitetura modular, apps, models centrais, layout corporativo.
- Fase 2-4: CRUD funcional de clientes/contratos/equipes/planejamento/execução/custos/receitas.
- Fase 5: dashboard executivo com KPIs e gráfico + relatório operacional base.
- Fase 6: documentação, base preparada para permissões finas e exportações PDF/Excel.

## Estrutura
- `apps/`: domínio por contexto de negócio
- `templates/`: templates globais e por módulo
- `static/`: css/js corporativo
- `docs/`: documentação adicional

## Observações
Este repositório entrega uma base real e expansível. Para produção, recomenda-se PostgreSQL, Celery e testes automatizados por módulo.
