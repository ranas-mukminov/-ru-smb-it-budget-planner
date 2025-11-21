import pytest
from ru_smb_it_budget_planner.calculator.scenario_builder import ScenarioCost
from ru_smb_it_budget_planner.reporting.owner_report_ru import generate_owner_report

def test_owner_report_generation():
    scenarios = [
        ScenarioCost(
            scenario_name="as_is",
            total_monthly_rub=100000,
            total_yearly_rub=1200000,
            capex_yearly_amortized=600000,
            opex_monthly=50000,
            details={}
        ),
        ScenarioCost(
            scenario_name="minimal_cloud",
            total_monthly_rub=80000,
            total_yearly_rub=960000,
            capex_yearly_amortized=400000,
            opex_monthly=46666,
            details={}
        )
    ]
    
    report = generate_owner_report(scenarios)
    assert "Отчет для собственника" in report
    assert "minimal_cloud" in report
    assert "Экономия" in report
    assert "240,000 RUB" in report # 1.2M - 0.96M
