from ru_smb_it_budget_planner.models.pricing_model import ElectricityTariff

HOURS_PER_MONTH = 730

def calculate_monthly_kwh(power_watts: int, hours: int = HOURS_PER_MONTH) -> float:
    return (power_watts / 1000.0) * hours

def calculate_monthly_energy_cost(kwh: float, tariff: ElectricityTariff) -> float:
    return kwh * tariff.tariff_rub_per_kwh
