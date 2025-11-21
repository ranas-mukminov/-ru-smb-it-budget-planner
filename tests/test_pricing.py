import pytest
import yaml
from src.pricing import PricingCatalog, ElectricityTariff, CloudProfile

def test_pricing_catalog_loading():
    yaml_data = """
    electricity:
      - region: "Moscow"
        rub_per_kwh: 6.5
      - region: "Tatarstan"
        rub_per_kwh: 5.2

    colocation:
      - dc_tier: "Tier-3"
        region: "Moscow"
        rub_per_unit_month: 2000
        included_power_watts: 100

    cloud_profiles:
      - name: "ru_cloud_gp"
        rub_per_vcpu_hour: 1.5
        rub_per_gb_ram_hour: 0.5
        rub_per_gb_storage_month: 10.0
    """
    data = yaml.safe_load(yaml_data)
    catalog = PricingCatalog(**data)
    
    assert len(catalog.electricity) == 2
    assert catalog.get_electricity_price("Moscow") == 6.5
    assert catalog.get_electricity_price("Unknown") is None # Should handle missing gracefully or raise

    assert len(catalog.cloud_profiles) == 1
    assert catalog.cloud_profiles[0].name == "ru_cloud_gp"

def test_cloud_cost_calculation():
    # Test helper method if we put it on the model
    profile = CloudProfile(
        name="test",
        rub_per_vcpu_hour=2.0,
        rub_per_gb_ram_hour=1.0,
        rub_per_gb_storage_month=5.0
    )
    # 1 vCPU, 1 GB RAM for 720 hours + 10 GB storage
    # (2*1 + 1*1) * 720 + 10 * 5 = 3 * 720 + 50 = 2160 + 50 = 2210
    cost = profile.calculate_monthly_cost(vcpus=1, ram_gb=1, storage_gb=10)
    assert cost == 2210.0
