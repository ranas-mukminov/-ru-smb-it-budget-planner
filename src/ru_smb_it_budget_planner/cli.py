import click
import yaml
from pathlib import Path
from ru_smb_it_budget_planner.dsl.parser import parse_infra_spec
from ru_smb_it_budget_planner.models.pricing_model import ElectricityTariff, ColocationTariff, CloudProfile
from ru_smb_it_budget_planner.calculator.scenario_builder import (
    PricingContext, calculate_as_is, calculate_minimal_cloud, calculate_hybrid
)
from ru_smb_it_budget_planner.reporting.tables import print_scenario_comparison, print_cost_breakdown
from ru_smb_it_budget_planner.reporting.owner_report_ru import generate_owner_report

def load_pricing_context(file_path: str) -> PricingContext:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return PricingContext(
        electricity=[ElectricityTariff(**t) for t in data.get('electricity', [])],
        colocation=[ColocationTariff(**t) for t in data.get('colocation', [])],
        cloud_profiles=[CloudProfile(**t) for t in data.get('cloud_profiles', [])]
    )

@click.group()
def cli():
    """IT Budget Planner for Russian SMBs"""
    pass

@cli.command()
@click.argument('infra_file', type=click.Path(exists=True))
def validate(infra_file):
    """Validate infrastructure YAML"""
    try:
        parse_infra_spec(infra_file)
        click.secho("Конфигурация корректна!", fg="green")
    except Exception as e:
        click.secho(str(e), fg="red")
        exit(1)

@cli.command()
@click.argument('infra_file', type=click.Path(exists=True))
@click.argument('pricing_file', type=click.Path(exists=True))
def plan(infra_file, pricing_file):
    """Calculate and compare budget scenarios"""
    try:
        infra = parse_infra_spec(infra_file)
        pricing = load_pricing_context(pricing_file)
        
        scenarios = [
            calculate_as_is(infra, pricing),
            calculate_minimal_cloud(infra, pricing),
            calculate_hybrid(infra, pricing)
        ]
        
        print_scenario_comparison(scenarios)
        print_cost_breakdown(scenarios)
        
    except Exception as e:
        click.secho(f"Ошибка: {e}", fg="red")
        exit(1)

@cli.command()
@click.argument('infra_file', type=click.Path(exists=True))
@click.argument('pricing_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help="Output file for report")
def report(infra_file, pricing_file, output):
    """Generate detailed report for owner"""
    try:
        infra = parse_infra_spec(infra_file)
        pricing = load_pricing_context(pricing_file)
        
        scenarios = [
            calculate_as_is(infra, pricing),
            calculate_minimal_cloud(infra, pricing),
            calculate_hybrid(infra, pricing)
        ]
        
        text = generate_owner_report(scenarios)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(text)
            click.secho(f"Отчет сохранен в {output}", fg="green")
        else:
            click.echo(text)
            
    except Exception as e:
        click.secho(f"Ошибка: {e}", fg="red")
        exit(1)

@cli.command()
def init_sample():
    """Generate sample configuration files"""
    infra_sample = """company_profile:
  name: "ООО Малый Бизнес"
  region: "Татарстан"
  industry: "retail"
  size_class: "50-100"
  has_pd: true
  has_pd_special: false
  has_kii: false

workloads:
  - name: "1C-accounting"
    type: "1c"
    vcpus: 4
    ram_gb: 16
    storage_gb: 500
    iops_profile: "medium"
    availability: "99.9"
    contains_pd: true
    contains_pd_special: false
    kii_related: false
    backup:
      daily_full: true
      retention_days: 30

  - name: "public-website"
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
  on_prem_servers:
    - name: "srv-1"
      vcpus: 8
      ram_gb: 32
      storage_gb: 2000
      power_watts: 400
      region: "Татарстан"
      age_years: 3
      capex_rub: 250000

  colocation_units:
    - dc_region: "Москва"
      units: 2
      power_watts: 600
      bandwidth_mbps: 100

  cloud_usage: []

licenses:
  - product: "1C"
    metric: "user"
    seats: 10
    cost_rub_per_year: 120000
"""
    pricing_sample = """electricity:
  - region: "Татарстан"
    tariff_rub_per_kwh: 6.5
    updated_at: "2025-01-01"
  - region: "Москва"
    tariff_rub_per_kwh: 7.0
    updated_at: "2025-01-01"

colocation:
  - region: "Москва"
    price_rub_per_u_per_month: 3000
    included_power_watts: 300
    included_bandwidth_mbps: 100

cloud_profiles:
  - code: "ru_cloud_gp"
    vCPU_price_rub_per_hour: 1.5
    ram_price_rub_per_gb_hour: 0.5
    storage_price_rub_per_gb_month: 5.0
    egress_price_rub_per_gb: 1.0
"""
    with open("infra.yaml", "w", encoding="utf-8") as f:
        f.write(infra_sample)
    with open("pricing.yaml", "w", encoding="utf-8") as f:
        f.write(pricing_sample)
    
    click.secho("Созданы файлы infra.yaml и pricing.yaml", fg="green")

if __name__ == '__main__':
    cli()
