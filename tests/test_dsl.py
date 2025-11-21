import pytest
import yaml
from pydantic import ValidationError
from src.dsl import Infrastructure, CompanyProfile, Workload, CurrentDeployment

def test_valid_infrastructure_parsing():
    yaml_data = """
    company_profile:
      name: "Test Corp"
      region: "Moscow"
      industry: "IT"
      size_class: "10-50"
      has_pd: true
      has_pd_special: false
      has_kii: false

    workloads:
      - name: "web-app"
        type: "web"
        vcpus: 2
        ram_gb: 4
        storage_gb: 50
        iops_profile: "low"
        availability: "99.5"
        contains_pd: false
        contains_pd_special: false
        kii_related: false

    current_deployment:
      on_prem_servers: []
      colocation_units: []
      cloud_usage: []
    
    licenses: []
    """
    data = yaml.safe_load(yaml_data)
    infra = Infrastructure(**data)
    
    assert infra.company_profile.name == "Test Corp"
    assert len(infra.workloads) == 1
    assert infra.workloads[0].name == "web-app"
    assert infra.workloads[0].vcpus == 2

def test_invalid_workload_validation():
    # Missing required fields
    yaml_data = """
    company_profile:
      name: "Test Corp"
      region: "Moscow"
    workloads:
      - name: "broken-app"
    """
    data = yaml.safe_load(yaml_data)
    
    with pytest.raises(ValidationError):
        Infrastructure(**data)

def test_pd_constraints():
    # If has_pd_special is true, has_pd must be true (logical constraint, though Pydantic might just check types first)
    # We can enforce this in a validator if we want, but for now let's check basic types.
    pass
