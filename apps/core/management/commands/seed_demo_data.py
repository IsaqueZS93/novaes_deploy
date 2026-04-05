from datetime import date, timedelta
from random import randint

from django.core.management.base import BaseCommand

from apps.accounts.models import Role, User
from apps.clients.models import Client
from apps.contracts.models import Contract, ContractService, ServiceCategory
from apps.finance.models import CostCategory, CostExpense, Revenue
from apps.planning.models import WeeklyPlanning
from apps.execution.models import DailyExecution
from apps.teams.models import Team
from apps.core.models import CenterCost


class Command(BaseCommand):
    help = "Cria dados fictícios para demonstração do sistema"

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(name=Role.ADMIN, defaults={"description": "Administrador"})
        user, _ = User.objects.get_or_create(
            username="admin_demo",
            defaults={"email": "admin@demo.com", "role": admin_role, "is_staff": True, "is_superuser": True},
        )
        user.set_password("admin123")
        user.save()

        center, _ = CenterCost.objects.get_or_create(name="CC-OPERACIONAL")
        cat_service, _ = ServiceCategory.objects.get_or_create(name="Perdas")
        cost_cat, _ = CostCategory.objects.get_or_create(name="Mão de obra")
        team, _ = Team.objects.get_or_create(name="Equipe Alfa", defaults={"leader": "Carlos", "operation_type": "Campo"})

        client, _ = Client.objects.get_or_create(
            cnpj="00.000.000/0001-00",
            defaults={"corporate_name": "Companhia de Saneamento Demo", "city": "São Paulo", "state": "SP"},
        )

        contract, _ = Contract.objects.get_or_create(
            number="CTR-2026-001",
            defaults={
                "client": client,
                "name": "Contrato Setor de Perdas",
                "object": "Serviços operacionais de perdas",
                "start_date": date.today() - timedelta(days=30),
                "end_date": date.today() + timedelta(days=365),
                "global_value": 5000000,
                "cost_center": center,
                "internal_manager": user,
                "region": "Capital",
            },
        )

        service, _ = ContractService.objects.get_or_create(
            contract=contract,
            name="Pesquisa de vazamentos",
            defaults={
                "category": cat_service,
                "unit_measure": "unidade",
                "billing_type": "unidade",
                "contracted_quantity": 10000,
                "unit_value": 45,
            },
        )

        for i in range(14):
            day = date.today() - timedelta(days=i)
            plan, _ = WeeklyPlanning.objects.get_or_create(
                contract=contract,
                service=service,
                team=team,
                planned_date=day,
                location="Zona Leste",
                defaults={"planned_quantity": 30 + randint(0, 10), "status": "planejado"},
            )
            DailyExecution.objects.get_or_create(
                planning=plan,
                contract=contract,
                service=service,
                team=team,
                execution_date=day,
                location="Zona Leste",
                defaults={
                    "executed_quantity": 20 + randint(0, 15),
                    "expected_value": 1200,
                    "actual_value": 1100 + randint(-100, 200),
                    "launched_by": user,
                },
            )
            CostExpense.objects.get_or_create(
                contract=contract,
                service=service,
                team=team,
                category=cost_cat,
                launch_date=day,
                competence=day.replace(day=1),
                description=f"Custo operação {day}",
                defaults={"value": 500 + randint(0, 250), "cost_center": center},
            )
            Revenue.objects.get_or_create(
                contract=contract,
                service=service,
                launch_date=day,
                competence=day.replace(day=1),
                origin="Medição mensal",
                defaults={"expected_value": 1400, "billed_value": 1300, "received_value": 1200},
            )

        self.stdout.write(self.style.SUCCESS("Dados fictícios criados com sucesso."))
