import json
import yaml
from ru_smb_it_budget_planner.models.infra_model import InfraSpec

def generate_schema():
    schema = InfraSpec.model_json_schema()
    with open('src/ru_smb_it_budget_planner/dsl/schema.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(schema, f, allow_unicode=True)
    print("Schema generated at src/ru_smb_it_budget_planner/dsl/schema.yaml")

if __name__ == "__main__":
    generate_schema()
