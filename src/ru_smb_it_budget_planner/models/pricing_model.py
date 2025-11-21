from typing import Optional
from pydantic import BaseModel

class ElectricityTariff(BaseModel):
    region: str
    tariff_rub_per_kwh: float
    updated_at: str
    comment: Optional[str] = None

class ColocationTariff(BaseModel):
    region: str
    price_rub_per_u_per_month: float
    included_power_watts: int
    included_bandwidth_mbps: int

class CloudProfile(BaseModel):
    code: str
    vCPU_price_rub_per_hour: float
    ram_price_rub_per_gb_hour: float
    storage_price_rub_per_gb_month: float
    egress_price_rub_per_gb: float

class HardwareProfile(BaseModel):
    capex_rub: float
    lifetime_years: int
    power_watts: int
