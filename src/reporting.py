from typing import List
from rich.console import Console
from rich.table import Table
from src.scenarios import Scenario

class ReportGenerator:
    def __init__(self):
        self.console = Console()

    def print_comparison(self, scenarios: List[Scenario]):
        table = Table(title="IT Budget Scenario Comparison (Monthly)")

        table.add_column("Scenario", style="cyan", no_wrap=True)
        table.add_column("Total Cost (RUB)", justify="right", style="green")
        table.add_column("Difference", justify="right", style="magenta")

        base_cost = scenarios[0].total_monthly_cost if scenarios else 0

        for scenario in scenarios:
            diff = scenario.total_monthly_cost - base_cost
            diff_str = f"{diff:+.2f}" if scenario != scenarios[0] else "-"
            table.add_row(
                scenario.name,
                f"{scenario.total_monthly_cost:,.2f}",
                diff_str
            )

        self.console.print(table)
        self.console.print("\n[bold yellow]Disclaimer:[/bold yellow] These are estimates only. Not financial advice.")

    def generate_markdown(self, scenarios: List[Scenario]) -> str:
        md = "# IT Budget Comparison\n\n"
        md += "| Scenario | Total Cost (RUB) | Difference |\n"
        md += "|----------|------------------|------------|\n"
        
        base_cost = scenarios[0].total_monthly_cost if scenarios else 0
        
        for scenario in scenarios:
            diff = scenario.total_monthly_cost - base_cost
            diff_str = f"{diff:+.2f}" if scenario != scenarios[0] else "-"
            md += f"| {scenario.name} | {scenario.total_monthly_cost:,.2f} | {diff_str} |\n"
            
        md += "\n> **Disclaimer**: Estimates only.\n"
        return md
