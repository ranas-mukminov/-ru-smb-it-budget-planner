from typing import List
from ru_smb_it_budget_planner.calculator.scenario_builder import ScenarioCost

def generate_owner_report(scenarios: List[ScenarioCost]) -> str:
    # Find cheapest scenario
    cheapest = min(scenarios, key=lambda s: s.total_yearly_rub)
    as_is = next((s for s in scenarios if s.scenario_name == "as_is"), None)
    
    report = []
    report.append("# Отчет для собственника / директора")
    report.append("")
    report.append(f"**Рекомендуемый сценарий:** {cheapest.scenario_name}")
    
    if as_is and cheapest.scenario_name != "as_is":
        savings = as_is.total_yearly_rub - cheapest.total_yearly_rub
        pct = (savings / as_is.total_yearly_rub) * 100
        report.append(f"**Экономия:** {savings:,.0f} RUB в год ({pct:.1f}%)")
    elif cheapest.scenario_name == "as_is":
        report.append("Текущая конфигурация (As Is) является оптимальной по стоимости.")
    
    report.append("")
    report.append("## Сравнение сценариев (Итого в год)")
    for s in scenarios:
        diff_text = ""
        if as_is and s != as_is:
            diff = s.total_yearly_rub - as_is.total_yearly_rub
            sign = "+" if diff > 0 else ""
            diff_text = f" ({sign}{diff:,.0f})"
        report.append(f"- **{s.scenario_name}**: {s.total_yearly_rub:,.0f} RUB{diff_text}")
    
    report.append("")
    report.append("## Риски и возможности")
    report.append("- **As Is**: Риски старения оборудования, капитальные затраты (CAPEX).")
    report.append("- **Minimal Cloud**: Гибкость для веб-нагрузок, но зависимость от провайдера.")
    report.append("- **Hybrid**: Баланс безопасности (PD/KII on-prem) и масштабируемости.")
    
    report.append("")
    report.append("---")
    report.append("Сгенерировано ru-smb-it-budget-planner")
    
    return "\n".join(report)
