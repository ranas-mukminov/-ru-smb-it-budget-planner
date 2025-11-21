from typing import List
from ru_smb_it_budget_planner.calculator.scenario_builder import ScenarioCost

def generate_report_text_stub(scenarios: List[ScenarioCost]) -> str:
    """
    Stub for AI-powered report generation.
    """
    cheapest = min(scenarios, key=lambda s: s.total_yearly_rub)
    
    return f"""
    Анализ бюджета завершен.
    
    Наиболее выгодный сценарий: {cheapest.scenario_name}.
    Годовые затраты составят: {cheapest.total_yearly_rub:,.0f} RUB.
    
    Рекомендуется рассмотреть миграцию части нагрузок в облако для оптимизации OPEX.
    """
