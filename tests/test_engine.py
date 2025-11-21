import pytest
from src.dsl import OnPremServer, ColocationUnit, CloudUsage, CurrentDeployment
from src.pricing import PricingCatalog, ElectricityTariff, ColocationTariff, CloudProfile
from src.engine import CostEngine

@pytest.fixture
def pricing():
    return PricingCatalog(
        electricity=[ElectricityTariff(region="Moscow", rub_per_kwh=5.0)],
        colocation=[ColocationTariff(dc_tier="Tier-3", region="Moscow", rub_per_unit_month=2000, included_power_watts=100)],
        cloud_profiles=[CloudProfile(name="ru_cloud", rub_per_vcpu_hour=1.0, rub_per_gb_ram_hour=0.5, rub_per_gb_storage_month=10.0)]
    )

def test_on_prem_cost(pricing):
    server = OnPremServer(
        name="srv1", vcpus=4, ram_gb=16, storage_gb=1000,
        power_watts=200, region="Moscow", age_years=1, capex_rub=120000
    )
    # Amortization (3 years default): 120000 / 36 = 3333.33
    # Electricity: 0.2 kW * 720h * 5.0 rub = 720 rub
    # Total: ~4053.33
    
    engine = CostEngine(pricing)
    cost = engine.calculate_on_prem_server_monthly(server)
    assert 4053 < cost < 4054

def test_colocation_cost(pricing):
    # 2 units, 500W total. Included 100W per unit? Or per contract?
    # Let's assume the tariff is per unit, and included power is per unit.
    # 2 units * 2000 = 4000 rub.
    # Included power = 2 * 100 = 200W.
    # Extra power = 500 - 200 = 300W = 0.3 kW.
    # Electricity: 0.3 * 720 * 5.0 = 1080 rub.
    # Total: 5080 rub.
    
    colo = ColocationUnit(dc_region="Moscow", units=2, power_watts=500, bandwidth_mbps=100)
    engine = CostEngine(pricing)
    cost = engine.calculate_colocation_monthly(colo)
    assert cost == 5080.0

def test_cloud_cost(pricing):
    usage = CloudUsage(provider_profile="ru_cloud", vcpus=2, ram_gb=4, storage_gb=50, region="ru-central")
    # (2*1 + 4*0.5) * 720 + 50*10 = (2+2)*720 + 500 = 2880 + 500 = 3380
    engine = CostEngine(pricing)
    cost = engine.calculate_cloud_usage_monthly(usage)
    assert cost == 3380.0
