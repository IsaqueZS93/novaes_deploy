# Arquitetura
- Monólito modular Django (apps por domínio).
- Camadas: models, forms, views, services, templates.
- Regras de apuração no app `dashboards/services.py` (evoluir para `apps/finance/services.py`).
- Estrutura preparada para APIs futuras via DRF sem quebra arquitetural.
