from ru_smb_it_budget_planner.models.infra_model import Workload, CloudUsage
from ru_smb_it_budget_planner.models.pricing_model import CloudProfile

HOURS_PER_MONTH = 730

def calculate_cloud_profile_cost(profile: CloudProfile, vcpus: int, ram_gb: int, storage_gb: int, egress_gb: int) -> float:
    compute_cost = (vcpus * profile.vCPU_price_rub_per_hour + ram_gb * profile.ram_price_rub_per_gb_hour) * HOURS_PER_MONTH
    storage_cost = storage_gb * profile.storage_price_rub_per_gb_month
    egress_cost = egress_gb * profile.egress_price_rub_per_gb
    return compute_cost + storage_cost + egress_cost

def calculate_workload_cloud_cost(workload: Workload, profile: CloudProfile) -> float:
    # Estimate egress based on workload type if not known?
    # For now assume 0 or some default.
    egress_gb = 100 # Placeholder default
    return calculate_cloud_profile_cost(
        profile,
        workload.vcpus,
        workload.ram_gb,
        workload.storage_gb,
        egress_gb
    )
