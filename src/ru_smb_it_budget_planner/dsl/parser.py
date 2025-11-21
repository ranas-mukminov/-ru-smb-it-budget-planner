import yaml
from typing import Dict, Any
from pydantic import ValidationError
from ru_smb_it_budget_planner.models.infra_model import InfraSpec
from ru_smb_it_budget_planner.models.pricing_model import (
    ElectricityTariff, ColocationTariff, CloudProfile, HardwareProfile
)

def load_yaml(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибка чтения YAML: {e}")

def parse_infra_spec(file_path: str) -> InfraSpec:
    data = load_yaml(file_path)
    try:
        return InfraSpec(**data)
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error['loc'])
            msg = error['msg']
            # Simple translation map for common errors
            if "Field required" in msg:
                msg = "Обязательное поле отсутствует"
            elif "Input should be a valid" in msg:
                msg = "Неверный формат данных"
            
            error_messages.append(f"Поле '{loc}': {msg}")
        
        raise ValueError("Ошибка валидации конфигурации инфраструктуры:\n" + "\n".join(error_messages))

def parse_pricing_config(file_path: str) -> Dict[str, Any]:
    # This function expects a specific structure for pricing.yaml
    # For now, we'll return a raw dict, but ideally we should map it to models.
    # The prompt implies pricing.yaml contains lists of tariffs.
    data = load_yaml(file_path)
    # TODO: Validate pricing config against models if a strict schema is defined for the whole file
    return data
