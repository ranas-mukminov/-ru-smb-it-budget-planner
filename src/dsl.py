from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class CompanyProfile(BaseModel):
    name: str
    region: str
    industry: Optional[str] = None
    size_class: Optional[str] = None
    has_pd: bool = False
    has_pd_special: bool = False
    has_kii: bool = False

class BackupRequirements(BaseModel):
    daily_full: bool = False
    retention_days: int = 30

class Workload(BaseModel):
    name: str
    type: str  # e.g., "1c", "web", "db"
    vcpus: int
    ram_gb: int
    storage_gb: int
    iops_profile: str = "low"  # low, medium, high
    availability: str = "99.5"
    contains_pd: bool = False
    contains_pd_special: bool = False
    kii_related: bool = False
    backup: Optional[BackupRequirements] = None

class OnPremServer(BaseModel):
    name: str
    vcpus: int
    ram_gb: int
    storage_gb: int
    power_watts: int
    region: str
    age_years: int
    capex_rub: float

class ColocationUnit(BaseModel):
    dc_region: str
    units: int
    power_watts: int
    bandwidth_mbps: int

class CloudUsage(BaseModel):
    provider_profile: str
    vcpus: int
    ram_gb: int
    storage_gb: int
    region: str

class CurrentDeployment(BaseModel):
    on_prem_servers: List[OnPremServer] = Field(default_factory=list)
    colocation_units: List[ColocationUnit] = Field(default_factory=list)
    cloud_usage: List[CloudUsage] = Field(default_factory=list)

class License(BaseModel):
    product: str
    seats: int
    cost_rub_per_year: float
    metric: str

class Infrastructure(BaseModel):
    company_profile: CompanyProfile
    workloads: List[Workload]
    current_deployment: Optional[CurrentDeployment] = None
    licenses: List[License] = Field(default_factory=list)
