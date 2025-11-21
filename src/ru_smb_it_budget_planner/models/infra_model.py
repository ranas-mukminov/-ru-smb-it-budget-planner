from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class CompanyProfile(BaseModel):
    name: str
    industry: str
    size_class: str
    region: str
    has_pd: bool = Field(description="Handles Personal Data (152-FZ)")
    has_pd_special: bool = Field(description="Handles Special Category Personal Data")
    has_kii: bool = Field(description="Critical Information Infrastructure (187-FZ)")

class BackupSpec(BaseModel):
    daily_full: bool
    retention_days: int

class Workload(BaseModel):
    name: str
    type: Literal["web", "db", "1c", "bitrix", "email", "vpn", "other"]
    vcpus: int
    ram_gb: int
    storage_gb: int
    iops_profile: Literal["low", "medium", "high"]
    availability: Literal["99.5", "99.9", "99.95", "99.99"]
    contains_pd: bool
    contains_pd_special: bool
    kii_related: bool
    backup: Optional[BackupSpec] = None

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
    egress_gb: int

class CurrentDeployment(BaseModel):
    on_prem_servers: List[OnPremServer] = []
    colocation_units: List[ColocationUnit] = []
    cloud_usage: List[CloudUsage] = []

class License(BaseModel):
    product: str
    metric: Literal["user", "socket", "vm"]
    seats: int
    cost_rub_per_year: float

class InfraSpec(BaseModel):
    company_profile: CompanyProfile
    workloads: List[Workload]
    current_deployment: CurrentDeployment
    licenses: List[License] = []
