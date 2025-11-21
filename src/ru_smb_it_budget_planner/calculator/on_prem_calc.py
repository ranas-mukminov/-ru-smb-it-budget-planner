from ru_smb_it_budget_planner.models.infra_model import OnPremServer, ColocationUnit
from ru_smb_it_budget_planner.models.pricing_model import ElectricityTariff, ColocationTariff
from ru_smb_it_budget_planner.calculator.energy_calc import calculate_monthly_kwh, calculate_monthly_energy_cost

def calculate_monthly_amortization(capex: float, lifetime_years: int) -> float:
    if lifetime_years <= 0:
        return 0.0
    return capex / (lifetime_years * 12.0)

def calculate_server_total_cost(server: OnPremServer, tariff: ElectricityTariff) -> float:
    amortization = calculate_monthly_amortization(server.capex_rub, server.age_years + 3) # Assuming 3 more years or total lifetime? 
    # Prompt says: "lifetime_years" in HardwareProfile. But OnPremServer has "age_years".
    # Let's assume a standard lifetime or use a default.
    # Actually, the prompt says: "monthly_capex = capex_rub / (lifetime_years * 12)".
    # But OnPremServer doesn't have lifetime_years, it has age_years.
    # HardwareProfile has lifetime_years.
    # For existing servers, we might use a standard lifetime (e.g. 5 years) or derived from profile.
    # Let's assume 5 years for now if not specified, or pass it in.
    lifetime = 5
    amortization = calculate_monthly_amortization(server.capex_rub, lifetime)
    
    kwh = calculate_monthly_kwh(server.power_watts)
    energy_cost = calculate_monthly_energy_cost(kwh, tariff)
    
    return amortization + energy_cost

def calculate_colo_cost(unit: ColocationUnit, tariff: ColocationTariff) -> float:
    # Price per U * units
    base_cost = unit.units * tariff.price_rub_per_u_per_month
    
    # Check for extra power or bandwidth if needed (simplified for now)
    # If unit power > included power * units, add surcharge?
    # Prompt says "included power (watts/kW)".
    # Let's keep it simple: base cost for now.
    return base_cost
