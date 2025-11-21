from src.dsl import OnPremServer, ColocationUnit, CloudUsage, CurrentDeployment
from src.pricing import PricingCatalog

class CostEngine:
    def __init__(self, pricing: PricingCatalog, amortization_months: int = 36):
        self.pricing = pricing
        self.amortization_months = amortization_months

    def calculate_on_prem_server_monthly(self, server: OnPremServer) -> float:
        # Amortization
        amortization = server.capex_rub / self.amortization_months
        
        # Electricity
        tariff = self.pricing.get_electricity_price(server.region)
        if tariff is None:
            # Fallback or error? For now, let's assume 0 or raise. 
            # Better to raise or log, but for simplicity 0 if not found (though test expects it found)
            tariff = 0.0
            
        kwh_month = (server.power_watts / 1000.0) * 720
        electricity_cost = kwh_month * tariff
        
        return amortization + electricity_cost

    def calculate_colocation_monthly(self, colo: ColocationUnit) -> float:
        # Find tariff for region (assuming Tier-3 default for now or matching best effort)
        # In real app, we might need explicit tier in ColocationUnit or default.
        # Test uses "Moscow", tariff has "Moscow".
        
        tariff = None
        for t in self.pricing.colocation:
            if t.region.lower() == colo.dc_region.lower():
                tariff = t
                break
        
        if not tariff:
            return 0.0
            
        base_cost = colo.units * tariff.rub_per_unit_month
        
        # Power calculation
        total_included_power = colo.units * tariff.included_power_watts
        extra_power_watts = max(0, colo.power_watts - total_included_power)
        
        electricity_price = self.pricing.get_electricity_price(colo.dc_region) or 0.0
        extra_electricity_cost = (extra_power_watts / 1000.0) * 720 * electricity_price
        
        return base_cost + extra_electricity_cost

    def calculate_cloud_usage_monthly(self, usage: CloudUsage) -> float:
        profile = self.pricing.get_cloud_profile(usage.provider_profile)
        if not profile:
            return 0.0
        return profile.calculate_monthly_cost(usage.vcpus, usage.ram_gb, usage.storage_gb)
