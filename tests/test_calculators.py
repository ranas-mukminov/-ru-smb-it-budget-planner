import pytest
from ru_smb_it_budget_planner.models.infra_model import InfraSpec, CompanyProfile, Workload, CurrentDeployment, OnPremServer
from ru_smb_it_budget_planner.models.pricing_model import ElectricityTariff, ColocationTariff, CloudProfile
from ru_smb_it_budget_planner.calculator.scenario_builder import calculate_as_is, calculate_minimal_cloud, PricingContext

@pytest.fixture
def sample_infra():
    return InfraSpec(
        company_profile=CompanyProfile(
            name="Test", industry="IT", size_class="S", region="Moscow",
            has_pd=False, has_pd_special=False, has_kii=False
        ),
        workloads=[
            Workload(name="web", type="web", vcpus=2, ram_gb=4, storage_gb=20, iops_profile="low", availability="99.5", contains_pd=False, contains_pd_special=False, kii_related=False),
            Workload(name="db", type="db", vcpus=4, ram_gb=8, storage_gb=100, iops_profile="medium", availability="99.9", contains_pd=True, contains_pd_special=False, kii_related=False)
        ],
        current_deployment=CurrentDeployment(
            on_prem_servers=[
                OnPremServer(name="srv1", vcpus=8, ram_gb=16, storage_gb=500, power_watts=200, region="Moscow", age_years=1, capex_rub=100000)
            ]
        )
    )

@pytest.fixture
def sample_pricing():
    return PricingContext(
        electricity=[ElectricityTariff(region="Moscow", tariff_rub_per_kwh=5.0, updated_at="2025")],
        colocation=[],
        cloud_profiles=[
            CloudProfile(code="ru_cloud_gp", vCPU_price_rub_per_hour=1.0, ram_price_rub_per_gb_hour=0.5, storage_price_rub_per_gb_month=10.0, egress_price_rub_per_gb=1.0)
        ]
    )

def test_as_is_calculation(sample_infra, sample_pricing):
    cost = calculate_as_is(sample_infra, sample_pricing)
    assert cost.scenario_name == "as_is"
    assert cost.details["hardware_amortization"] > 0
    assert cost.details["electricity"] > 0

def test_minimal_cloud_calculation(sample_infra, sample_pricing):
    # Web workload should move
    cost = calculate_minimal_cloud(sample_infra, sample_pricing)
    assert cost.scenario_name == "minimal_cloud"
    assert cost.details["cloud"] > 0
    # Amortization should be reduced (linear scaling assumption)
    as_is = calculate_as_is(sample_infra, sample_pricing)
    assert cost.details["hardware_amortization"] < as_is.details["hardware_amortization"]
