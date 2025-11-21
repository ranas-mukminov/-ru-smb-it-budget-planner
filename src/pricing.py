from typing import List, Optional
from pydantic import BaseModel

class ElectricityTariff(BaseModel):
    region: str
    rub_per_kwh: float

class ColocationTariff(BaseModel):
    dc_tier: str
    region: str
    rub_per_unit_month: float
    included_power_watts: int = 0

class CloudProfile(BaseModel):
    name: str
    rub_per_vcpu_hour: float
    rub_per_gb_ram_hour: float
    rub_per_gb_storage_month: float

    def calculate_monthly_cost(self, vcpus: int, ram_gb: int, storage_gb: int, hours: int = 720) -> float:
        compute_cost = (vcpus * self.rub_per_vcpu_hour + ram_gb * self.rub_per_gb_ram_hour) * hours
        storage_cost = storage_gb * self.rub_per_gb_storage_month
        return compute_cost + storage_cost

class PricingCatalog(BaseModel):
    electricity: List[ElectricityTariff]
    colocation: List[ColocationTariff]
    cloud_profiles: List[CloudProfile]

    def get_electricity_price(self, region: str) -> Optional[float]:
        for tariff in self.electricity:
            if tariff.region.lower() == region.lower():
                return tariff.rub_per_kwh
        return None

    def get_cloud_profile(self, name: str) -> Optional[CloudProfile]:
        for profile in self.cloud_profiles:
            if profile.name == name:
                return profile
        return None
