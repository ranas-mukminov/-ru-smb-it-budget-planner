from typing import Dict, Any

def text_to_infra_yaml_stub(text: str) -> str:
    """
    Stub for AI-powered text-to-YAML conversion.
    In a real implementation, this would call an LLM.
    Here we use simple keyword matching for demonstration.
    """
    # Deterministic stub logic
    yaml_lines = ["company_profile:"]
    yaml_lines.append('  name: "Generated Company"')
    yaml_lines.append('  industry: "generic"')
    yaml_lines.append('  size_class: "10-50"')
    yaml_lines.append('  region: "Moscow"')
    
    if "персональные данные" in text.lower():
        yaml_lines.append('  has_pd: true')
    else:
        yaml_lines.append('  has_pd: false')
        
    yaml_lines.append('  has_pd_special: false')
    yaml_lines.append('  has_kii: false')
    
    yaml_lines.append("")
    yaml_lines.append("workloads:")
    
    if "сайт" in text.lower() or "web" in text.lower():
        yaml_lines.append('  - name: "website"')
        yaml_lines.append('    type: "web"')
        yaml_lines.append('    vcpus: 2')
        yaml_lines.append('    ram_gb: 4')
        yaml_lines.append('    storage_gb: 20')
        yaml_lines.append('    iops_profile: "low"')
        yaml_lines.append('    availability: "99.5"')
        yaml_lines.append('    contains_pd: false')
        yaml_lines.append('    contains_pd_special: false')
        yaml_lines.append('    kii_related: false')

    if "1с" in text.lower():
        yaml_lines.append('  - name: "1c-server"')
        yaml_lines.append('    type: "1c"')
        yaml_lines.append('    vcpus: 4')
        yaml_lines.append('    ram_gb: 16')
        yaml_lines.append('    storage_gb: 200')
        yaml_lines.append('    iops_profile: "medium"')
        yaml_lines.append('    availability: "99.9"')
        yaml_lines.append('    contains_pd: true')
        yaml_lines.append('    contains_pd_special: false')
        yaml_lines.append('    kii_related: false')
        
    yaml_lines.append("")
    yaml_lines.append("current_deployment:")
    yaml_lines.append("  on_prem_servers: []")
    yaml_lines.append("  colocation_units: []")
    yaml_lines.append("  cloud_usage: []")
    yaml_lines.append("")
    yaml_lines.append("licenses: []")
    
    return "\n".join(yaml_lines)
