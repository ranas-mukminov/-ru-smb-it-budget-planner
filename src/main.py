import click
import yaml
from src.dsl import Infrastructure
from src.pricing import PricingCatalog
from src.scenarios import ScenarioGenerator
from src.reporting import ReportGenerator

@click.group()
def cli():
    """IT Budget Planner for Russian SMBs"""
    pass

@cli.command()
@click.option('--infra', type=click.Path(exists=True), required=True, help='Path to infrastructure YAML')
@click.option('--pricing', type=click.Path(exists=True), required=True, help='Path to pricing YAML')
@click.option('--markdown', is_flag=True, help='Output Markdown report')
def plan(infra, pricing, markdown):
    """Calculate and compare scenarios"""
    
    # Load DSL
    with open(infra, 'r', encoding='utf-8') as f:
        infra_data = yaml.safe_load(f)
    infrastructure = Infrastructure(**infra_data)
    
    # Load Pricing
    with open(pricing, 'r', encoding='utf-8') as f:
        pricing_data = yaml.safe_load(f)
    pricing_catalog = PricingCatalog(**pricing_data)
    
    # Generate Scenarios
    generator = ScenarioGenerator(infrastructure, pricing_catalog)
    scenarios = []
    scenarios.append(generator.get_as_is_scenario())
    scenarios.append(generator.get_cloud_scenario())
    
    # Report
    reporter = ReportGenerator()
    if markdown:
        print(reporter.generate_markdown(scenarios))
    else:
        reporter.print_comparison(scenarios)

if __name__ == '__main__':
    cli()
