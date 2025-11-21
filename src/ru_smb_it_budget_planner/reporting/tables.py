from typing import List
from rich.table import Table
from rich.console import Console
from ru_smb_it_budget_planner.calculator.scenario_builder import ScenarioCost

def print_scenario_comparison(scenarios: List[ScenarioCost]):
    console = Console()
    table = Table(title="Сравнение сценариев бюджета (RUB)")

    table.add_column("Сценарий", style="cyan", no_wrap=True)
    table.add_column("OPEX / мес", justify="right")
    table.add_column("CAPEX (аморт) / мес", justify="right")
    table.add_column("Итого / мес", justify="right", style="green")
    table.add_column("Итого / год", justify="right", style="bold green")

    for s in scenarios:
        table.add_row(
            s.scenario_name,
            f"{s.opex_monthly:,.2f}",
            f"{s.capex_yearly_amortized / 12:,.2f}",
            f"{s.total_monthly_rub:,.2f}",
            f"{s.total_yearly_rub:,.2f}"
        )

    console.print(table)

def print_cost_breakdown(scenarios: List[ScenarioCost]):
    console = Console()
    table = Table(title="Детализация расходов (RUB/мес)")

    table.add_column("Категория", style="magenta")
    for s in scenarios:
        table.add_column(s.scenario_name, justify="right")

    categories = ["hardware_amortization", "electricity", "colocation", "cloud", "licenses"]
    
    for cat in categories:
        row_data = [cat]
        for s in scenarios:
            val = s.details.get(cat, 0.0)
            row_data.append(f"{val:,.2f}")
        table.add_row(*row_data)

    console.print(table)
