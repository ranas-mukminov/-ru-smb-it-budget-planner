from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from ru_smb_it_budget_planner.models.infra_model import InfraSpec, Workload, OnPremServer, ColocationUnit
from ru_smb_it_budget_planner.models.pricing_model import ElectricityTariff, ColocationTariff, CloudProfile
from ru_smb_it_budget_planner.calculator.on_prem_calc import calculate_server_total_cost, calculate_colo_cost
from ru_smb_it_budget_planner.calculator.cloud_calc import calculate_workload_cloud_cost

class ScenarioCost(BaseModel):
    scenario_name: str
    total_monthly_rub: float
    total_yearly_rub: float
    capex_yearly_amortized: float
    opex_monthly: float
    details: Dict[str, float] # Breakdown by category

class PricingContext(BaseModel):
    electricity: List[ElectricityTariff]
    colocation: List[ColocationTariff]
    cloud_profiles: List[CloudProfile]

    def get_electricity_tariff(self, region: str) -> Optional[ElectricityTariff]:
        for t in self.electricity:
            if t.region == region:
                return t
        return None

    def get_colocation_tariff(self, region: str) -> Optional[ColocationTariff]:
        for t in self.colocation:
            if t.region == region:
                return t
        return None

    def get_cloud_profile(self, code: str) -> Optional[CloudProfile]:
        for p in self.cloud_profiles:
            if p.code == code:
                return p
        return None

def calculate_as_is(infra: InfraSpec, pricing: PricingContext) -> ScenarioCost:
    total_monthly = 0.0
    capex_amortized = 0.0
    opex = 0.0
    details = {
        "hardware_amortization": 0.0,
        "electricity": 0.0,
        "colocation": 0.0,
        "cloud": 0.0,
        "licenses": 0.0
    }

    # On-prem servers
    for server in infra.current_deployment.on_prem_servers:
        tariff = pricing.get_electricity_tariff(server.region)
        if not tariff:
            # Fallback or error? For now fallback to 0 cost or default
            # In real app, should raise warning
            continue
            
        # We need to split amortization and energy for details
        # Re-implementing breakdown here for clarity
        # Amortization
        amort = server.capex_rub / ((server.age_years + 3) * 12.0) # Simplified lifetime
        details["hardware_amortization"] += amort
        capex_amortized += amort
        
        # Energy
        kwh = (server.power_watts / 1000.0) * 730
        energy = kwh * tariff.tariff_rub_per_kwh
        details["electricity"] += energy
        opex += energy

    # Colocation
    for unit in infra.current_deployment.colocation_units:
        tariff = pricing.get_colocation_tariff(unit.dc_region)
        if tariff:
            cost = unit.units * tariff.price_rub_per_u_per_month
            details["colocation"] += cost
            opex += cost

    # Cloud
    for usage in infra.current_deployment.cloud_usage:
        profile = pricing.get_cloud_profile(usage.provider_profile)
        if profile:
            # Re-calc based on usage
            cost = (usage.vcpus * profile.vCPU_price_rub_per_hour + 
                    usage.ram_gb * profile.ram_price_rub_per_gb_hour) * 730 + \
                   usage.storage_gb * profile.storage_price_rub_per_gb_month + \
                   usage.egress_gb * profile.egress_price_rub_per_gb
            details["cloud"] += cost
            opex += cost

    # Licenses
    for lic in infra.licenses:
        monthly = lic.cost_rub_per_year / 12.0
        details["licenses"] += monthly
        opex += monthly

    total_monthly = capex_amortized + opex
    
    return ScenarioCost(
        scenario_name="as_is",
        total_monthly_rub=total_monthly,
        total_yearly_rub=total_monthly * 12,
        capex_yearly_amortized=capex_amortized * 12,
        opex_monthly=opex,
        details=details
    )

def calculate_minimal_cloud(infra: InfraSpec, pricing: PricingContext) -> ScenarioCost:
    # Logic: Move stateless web to cloud.
    # We need to simulate the new state.
    # For simplicity, we'll iterate workloads and assign costs.
    # But wait, "as_is" was based on "current_deployment".
    # "minimal_cloud" should be based on "workloads".
    # If we only have "current_deployment", we don't know which server runs which workload unless we map them.
    # The prompt says: "workloads" list exists.
    # And "current_deployment" describes hardware.
    # This implies a gap: we need to map workloads to hardware to know what we can remove if we move to cloud.
    # OR, we assume "as_is" cost is fixed by hardware, and "cloud" cost is calculated from workloads.
    # If we move a workload to cloud, can we decommission a server?
    # That's hard to know without mapping.
    # 
    # Simplified approach for this tool:
    # 1. Calculate "As Is" based on hardware (as done above).
    # 2. Calculate "Cloud" cost for moved workloads.
    # 3. Estimate savings:
    #    If we move X% of vCPU/RAM to cloud, we assume we can reduce on-prem hardware by X% (linear scaling).
    #    This is an approximation.
    
    as_is = calculate_as_is(infra, pricing)
    
    total_vcpus = sum(w.vcpus for w in infra.workloads)
    moved_vcpus = 0
    cloud_cost_increase = 0.0
    
    # Identify candidates
    for w in infra.workloads:
        can_move = (w.type == "web") and (not w.contains_pd) and (not w.kii_related)
        if can_move:
            # Move to cloud
            # Pick a default profile, e.g. 'ru_cloud_gp'
            profile = pricing.get_cloud_profile('ru_cloud_gp')
            if profile:
                cost = calculate_workload_cloud_cost(w, profile)
                cloud_cost_increase += cost
                moved_vcpus += w.vcpus
    
    if total_vcpus == 0:
        reduction_factor = 0
    else:
        reduction_factor = moved_vcpus / total_vcpus

    # Apply reduction to on-prem costs (amortization, electricity, colo)
    # This assumes perfect consolidation.
    
    new_details = as_is.details.copy()
    
    # Reduce on-prem
    for cat in ["hardware_amortization", "electricity", "colocation"]:
        new_details[cat] = new_details[cat] * (1.0 - reduction_factor)
        
    # Add cloud cost
    new_details["cloud"] += cloud_cost_increase
    
    new_opex = new_details["electricity"] + new_details["colocation"] + new_details["cloud"] + new_details["licenses"]
    new_capex_monthly = new_details["hardware_amortization"]
    new_total = new_opex + new_capex_monthly
    
    return ScenarioCost(
        scenario_name="minimal_cloud",
        total_monthly_rub=new_total,
        total_yearly_rub=new_total * 12,
        capex_yearly_amortized=new_capex_monthly * 12,
        opex_monthly=new_opex,
        details=new_details
    )

def calculate_hybrid(infra: InfraSpec, pricing: PricingContext) -> ScenarioCost:
    # Similar to minimal, but maybe move more?
    # Or maybe "hybrid" means move everything EXCEPT PD/KII?
    # Let's define "minimal" as just WEB.
    # "Hybrid" as everything that is NOT PD/KII.
    
    as_is = calculate_as_is(infra, pricing)
    
    total_vcpus = sum(w.vcpus for w in infra.workloads)
    moved_vcpus = 0
    cloud_cost_increase = 0.0
    
    for w in infra.workloads:
        # Move everything that is legally allowed
        # Assuming PD/KII must stay on-prem for this scenario logic (conservative)
        must_stay = w.contains_pd or w.kii_related or w.contains_pd_special
        if not must_stay:
            profile = pricing.get_cloud_profile('ru_cloud_gp')
            if profile:
                cost = calculate_workload_cloud_cost(w, profile)
                cloud_cost_increase += cost
                moved_vcpus += w.vcpus

    if total_vcpus == 0:
        reduction_factor = 0
    else:
        reduction_factor = moved_vcpus / total_vcpus

    new_details = as_is.details.copy()
    
    for cat in ["hardware_amortization", "electricity", "colocation"]:
        new_details[cat] = new_details[cat] * (1.0 - reduction_factor)
        
    new_details["cloud"] += cloud_cost_increase
    
    new_opex = new_details["electricity"] + new_details["colocation"] + new_details["cloud"] + new_details["licenses"]
    new_capex_monthly = new_details["hardware_amortization"]
    new_total = new_opex + new_capex_monthly
    
    return ScenarioCost(
        scenario_name="hybrid",
        total_monthly_rub=new_total,
        total_yearly_rub=new_total * 12,
        capex_yearly_amortized=new_capex_monthly * 12,
        opex_monthly=new_opex,
        details=new_details
    )
