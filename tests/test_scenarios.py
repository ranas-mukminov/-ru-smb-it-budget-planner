import pytest
from src.dsl import Infrastructure, Workload, CurrentDeployment, OnPremServer, CloudUsage
from src.pricing import PricingCatalog, CloudProfile, ElectricityTariff
from src.scenarios import ScenarioGenerator, Scenario

@pytest.fixture
def simple_infra():
    return Infrastructure(
        company_profile={"name": "Test", "region": "Moscow"},
        workloads=[
            Workload(name="web", type="web", vcpus=2, ram_gb=4, storage_gb=50),
            Workload(name="secure-db", type="db", vcpus=4, ram_gb=16, storage_gb=500, kii_related=True)
        ],
        current_deployment=CurrentDeployment(
            on_prem_servers=[
                OnPremServer(name="srv1", vcpus=8, ram_gb=32, storage_gb=1000, power_watts=300, region="Moscow", age_years=2, capex_rub=200000)
            ]
        )
    )

@pytest.fixture
def pricing():
    return PricingCatalog(
        electricity=[ElectricityTariff(region="Moscow", rub_per_kwh=5.0)],
        colocation=[],
        cloud_profiles=[CloudProfile(name="ru_cloud", rub_per_vcpu_hour=1.0, rub_per_gb_ram_hour=0.5, rub_per_gb_storage_month=10.0)]
    )

def test_as_is_scenario(simple_infra, pricing):
    generator = ScenarioGenerator(simple_infra, pricing)
    scenario = generator.get_as_is_scenario()
    
    # Should contain the 1 on-prem server
    assert len(scenario.items) == 1
    assert isinstance(scenario.items[0], OnPremServer)
    # Cost should be calculated
    assert scenario.total_monthly_cost > 0

def test_cloud_migration_scenario(simple_infra, pricing):
    generator = ScenarioGenerator(simple_infra, pricing)
    scenario = generator.get_cloud_scenario(cloud_provider="ru_cloud")
    
    # "web" should go to cloud
    # "secure-db" is KII, should stay on prem (mapped to existing server if possible, or just flagged)
    # For this test, let's assume the generator is smart enough to keep KII on existing hardware 
    # OR we define a rule: "If KII, keep in As-Is state for that workload".
    # Since we don't have explicit mapping of Workload <-> Server in DSL, 
    # we might just say: "KII workloads are not migrated, so we add a placeholder or keep the whole on-prem server?"
    
    # Simplest approach for MVP:
    # 1. Calculate Cloud cost for ALL non-KII workloads.
    # 2. For KII workloads, if we can't migrate, we assume we keep the ENTIRE current on-prem infra 
    #    (pessimistic) or we assume we can downsize on-prem?
    #    Downsizing is hard.
    #    Let's assume: KII workloads require us to keep specific servers. 
    #    But we don't know which server runs what.
    
    # Revised Strategy for MVP:
    # "Cloud Scenario" = Cost of Cloud for (All Workloads - KII) + Cost of On-Prem (As-Is) * (KII_Ratio?)
    # No, that's too magic.
    
    # Let's just map Workloads to CloudUsage.
    # If KII, we map it to "OnPremServer" (virtual) with same specs? 
    # Or we just fail to migrate it and report it.
    
    # Let's expect:
    # 1 CloudUsage item for "web"
    # 1 OnPremServer item (virtual/placeholder) for "secure-db" OR we keep the existing server.
    
    # Let's assume the generator returns a list of resources.
    # For "secure-db", since it's KII, it might default to "Colocation" or "OnPrem".
    # Let's say we map it to a "Virtual OnPrem" with 0 CAPEX (sunk cost) but paying electricity?
    # Or just keep the existing server in the list.
    
    items = scenario.items
    cloud_items = [i for i in items if isinstance(i, CloudUsage)]
    on_prem_items = [i for i in items if isinstance(i, OnPremServer)]
    
    assert len(cloud_items) == 1
    assert cloud_items[0].vcpus == 2 # web
    
    # The KII workload must be accounted for. 
    # If we keep the existing server to run it:
    assert len(on_prem_items) == 1
    assert on_prem_items[0].name == "srv1"
