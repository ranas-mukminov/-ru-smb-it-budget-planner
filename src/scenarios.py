from typing import List, Union
from pydantic import BaseModel
from src.dsl import Infrastructure, OnPremServer, ColocationUnit, CloudUsage, Workload
from src.pricing import PricingCatalog
from src.engine import CostEngine

class Scenario(BaseModel):
    name: str
    items: List[Union[OnPremServer, ColocationUnit, CloudUsage]]
    total_monthly_cost: float = 0.0

class ScenarioGenerator:
    def __init__(self, infra: Infrastructure, pricing: PricingCatalog):
        self.infra = infra
        self.pricing = pricing
        self.engine = CostEngine(pricing)

    def get_as_is_scenario(self) -> Scenario:
        items = []
        if self.infra.current_deployment:
            items.extend(self.infra.current_deployment.on_prem_servers)
            items.extend(self.infra.current_deployment.colocation_units)
            items.extend(self.infra.current_deployment.cloud_usage)
        
        cost = self._calculate_total(items)
        return Scenario(name="As-Is", items=items, total_monthly_cost=cost)

    def get_cloud_scenario(self, cloud_provider: str = "ru_cloud_gp") -> Scenario:
        items = []
        keep_on_prem = False
        
        # Check if we need to keep on-prem for KII
        # Also check company-wide flags
        force_on_prem = self.infra.company_profile.has_kii
        
        for w in self.infra.workloads:
            if w.kii_related or force_on_prem:
                keep_on_prem = True
                # We do NOT create a cloud usage for this workload
            else:
                # Migrate to cloud
                usage = CloudUsage(
                    provider_profile=cloud_provider,
                    vcpus=w.vcpus,
                    ram_gb=w.ram_gb,
                    storage_gb=w.storage_gb,
                    region=self.infra.company_profile.region 
                )
                items.append(usage)
        
        if keep_on_prem and self.infra.current_deployment:
            # Pessimistic: keep all on-prem servers if any KII workload exists
            items.extend(self.infra.current_deployment.on_prem_servers)
            # We might also need to keep colocation if it's used for KII?
            # Let's assume colocation is also "on-prem" in this context (hardware ownership)
            items.extend(self.infra.current_deployment.colocation_units)

        cost = self._calculate_total(items)
        return Scenario(name="Cloud Migration", items=items, total_monthly_cost=cost)

    def _calculate_total(self, items: List) -> float:
        total = 0.0
        for item in items:
            if isinstance(item, OnPremServer):
                total += self.engine.calculate_on_prem_server_monthly(item)
            elif isinstance(item, ColocationUnit):
                total += self.engine.calculate_colocation_monthly(item)
            elif isinstance(item, CloudUsage):
                total += self.engine.calculate_cloud_usage_monthly(item)
        return total
