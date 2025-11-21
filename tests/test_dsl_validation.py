import pytest
import yaml
from ru_smb_it_budget_planner.dsl.parser import parse_infra_spec
from pydantic import ValidationError

def test_valid_infra_yaml(tmp_path):
    valid_yaml = """
company_profile:
  name: "Test Corp"
  industry: "IT"
  size_class: "10-50"
  region: "Moscow"
  has_pd: true
  has_pd_special: false
  has_kii: false

workloads:
  - name: "web-server"
    type: "web"
    vcpus: 2
    ram_gb: 4
    storage_gb: 20
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
    f = tmp_path / "infra.yaml"
    f.write_text(valid_yaml, encoding="utf-8")
    
    spec = parse_infra_spec(str(f))
    assert spec.company_profile.name == "Test Corp"
    assert len(spec.workloads) == 1

def test_invalid_infra_yaml_missing_field(tmp_path):
    invalid_yaml = """
company_profile:
  name: "Test Corp"
  # Missing industry
  size_class: "10-50"
  region: "Moscow"
  has_pd: true
  has_pd_special: false
  has_kii: false

workloads: []
current_deployment: {}
"""
    f = tmp_path / "infra.yaml"
    f.write_text(invalid_yaml, encoding="utf-8")
    
    with pytest.raises(ValueError) as excinfo:
        parse_infra_spec(str(f))
    
    assert "Обязательное поле отсутствует" in str(excinfo.value)
    assert "company_profile -> industry" in str(excinfo.value)

def test_invalid_infra_yaml_wrong_type(tmp_path):
    invalid_yaml = """
company_profile:
  name: "Test Corp"
  industry: "IT"
  size_class: "10-50"
  region: "Moscow"
  has_pd: "not_a_bool" # Should be bool
  has_pd_special: false
  has_kii: false

workloads: []
current_deployment: {}
"""
    f = tmp_path / "infra.yaml"
    f.write_text(invalid_yaml, encoding="utf-8")
    
    with pytest.raises(ValueError) as excinfo:
        parse_infra_spec(str(f))
    
    # Pydantic might coerce "yes" to True if strict=False, but let's check.
    # Actually Pydantic v2 is stricter. "yes" is not a valid bool by default.
    assert "Поле 'company_profile -> has_pd'" in str(excinfo.value)
