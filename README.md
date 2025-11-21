# IT Budget Planner for Russian SMBs 💰

![CI Status](https://github.com/ranas-mukminov/ru-smb-it-budget-planner/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

---

A comprehensive command-line tool for calculating and comparing IT infrastructure costs (TCO - Total Cost of Ownership) across different deployment scenarios: On-Premise, Colocation, and Russian Cloud providers. Designed specifically for small and medium businesses in Russia, with built-in compliance awareness for data privacy (152-FZ) and critical infrastructure (187-FZ) regulations.

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)  
**Website**: [run-as-daemon.ru](https://run-as-daemon.ru)

---

## Overview

Managing IT budgets in Russia requires balancing technical capabilities, costs, and regulatory compliance. This tool helps business owners, CTOs, and system administrators make informed decisions by:

- Modeling current infrastructure in a simple YAML format
- Calculating realistic TCO for multiple deployment scenarios
- Comparing On-Premise, Colocation, and Cloud costs side-by-side
- Accounting for Russian data sovereignty requirements (152-FZ, 187-FZ)
- Generating executive-friendly reports in Russian

Whether you're evaluating cloud migration, optimizing current infrastructure, or planning capacity expansion, this tool provides data-driven insights to support your decision-making process.

---

## Key Features

- **YAML-based DSL**: Describe your infrastructure using a simple, human-readable configuration format
- **Multi-scenario analysis**: Automatically calculate "As Is", "Minimal Cloud", and "Hybrid" deployment scenarios
- **Compliance-aware**: Flag workloads containing personal data or critical infrastructure to ensure proper placement
- **TCO breakdown**: Detailed cost analysis including CAPEX, OPEX, energy, colocation, cloud services, and licenses
- **Russian-first**: All reports, error messages, and documentation in Russian language
- **CLI interface**: Fast, scriptable command-line tool for automation and CI/CD integration
- **Realistic pricing**: Use your own vendor pricing data via configurable `pricing.yaml`
- **Validation engine**: Built-in schema validation to catch configuration errors early
- **Extensible AI layer**: Placeholder interfaces for future AI-powered cost optimization and report generation

---

## Architecture / Components

The tool is organized into several modules:

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Interface                        │
│           (validate, plan, report, init-sample)          │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  DSL Parser  │  │ Calculators  │  │  Reporting   │
│              │  │              │  │              │
│ - YAML load  │  │ - On-Prem    │  │ - Tables     │
│ - Validation │  │ - Cloud      │  │ - Owner      │
│ - Schema gen │  │ - Energy     │  │   reports    │
└──────────────┘  │ - Scenarios  │  └──────────────┘
                  └──────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │    Models    │
                  │              │
                  │ - Infra      │
                  │ - Pricing    │
                  │ - Workloads  │
                  └──────────────┘
```

**Data Flow**:
1. User provides `infra.yaml` (infrastructure description) and `pricing.yaml` (cost data)
2. DSL parser validates and loads configurations into Pydantic models
3. Calculators compute TCO for each scenario based on workload requirements
4. Reporting module formats results as tables or executive summaries
5. Results output to console or saved to file

---

## Requirements

### System Requirements

- **Operating System**: Linux, macOS, or Windows with Python support
- **Python Version**: 3.9 or higher
- **Disk Space**: ~50 MB for installation (including dependencies)
- **Memory**: Minimal (~10 MB runtime footprint)

### Dependencies

All dependencies are automatically installed via `pip`:

- `pydantic >= 2.0.0` — Data validation and schema modeling
- `pyyaml >= 6.0` — YAML configuration parsing
- `click >= 8.0.0` — Command-line interface framework
- `rich >= 10.0.0` — Terminal formatting and colorized output

### Development Dependencies (Optional)

For contributors and developers:

- `pytest` — Unit testing framework
- `pytest-cov` — Code coverage reporting
- `ruff` — Fast Python linter
- `mypy` — Static type checking
- `bandit` — Security vulnerability scanner

---

## Quick Start (TL;DR)

Get started in 3 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/ranas-mukminov/ru-smb-it-budget-planner.git
cd ru-smb-it-budget-planner

# 2. Install the tool
pip install .

# 3. Generate sample configuration files
ru-smb-it-budget-planner init-sample

# 4. Validate your configuration
ru-smb-it-budget-planner validate infra.yaml

# 5. Calculate budget scenarios
ru-smb-it-budget-planner plan infra.yaml pricing.yaml

# 6. Generate an executive report
ru-smb-it-budget-planner report infra.yaml pricing.yaml -o report.txt
```

You'll see a comparison table showing projected costs for different deployment scenarios.

---

## Detailed Installation

### Install from Git Repository

```bash
# Clone the repository
git clone https://github.com/ranas-mukminov/ru-smb-it-budget-planner.git
cd ru-smb-it-budget-planner

# Install in development mode (editable)
pip install -e .

# Or install normally
pip install .
```

### Install Development Dependencies

For development, testing, and linting:

```bash
pip install -e .[dev]
pip install pytest pytest-cov ruff mypy bandit
```

### Verify Installation

```bash
ru-smb-it-budget-planner --help
```

You should see the CLI help message with available commands.

---

## Configuration

The tool requires two YAML configuration files:

### 1. Infrastructure Configuration (`infra.yaml`)

Describes your IT infrastructure, workloads, and compliance requirements.

```yaml
company_profile:
  name: "ООО Малый Бизнес"
  region: "Татарстан"
  industry: "retail"
  size_class: "50-100"
  has_pd: true              # Contains personal data (152-FZ)
  has_pd_special: false     # Special categories of personal data
  has_kii: false            # Critical Information Infrastructure (187-FZ)

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
```

### 2. Pricing Configuration (`pricing.yaml`)

Define regional pricing for electricity, colocation, and cloud services.

```yaml
electricity:
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
```

> [!TIP]
> Update `pricing.yaml` with actual pricing from your vendors for accurate TCO calculations.

---

## Usage & Common Tasks

### Generate Sample Configuration

Create template files to get started:

```bash
ru-smb-it-budget-planner init-sample
```

This creates `infra.yaml` and `pricing.yaml` in your current directory.

### Validate Configuration

Check your infrastructure configuration for syntax and schema errors:

```bash
ru-smb-it-budget-planner validate infra.yaml
```

If valid, you'll see: `Конфигурация корректна!`

### Calculate Budget Scenarios

Compare TCO across multiple deployment scenarios:

```bash
ru-smb-it-budget-planner plan infra.yaml pricing.yaml
```

Output shows:
- **As Is**: Current deployment costs
- **Minimal Cloud**: Migrate web workloads to Russian cloud
- **Hybrid**: Compliance-aware hybrid deployment

### Generate Executive Report

Create a detailed Russian-language report for management:

```bash
ru-smb-it-budget-planner report infra.yaml pricing.yaml -o report.txt
```

The report includes:
- Cost breakdown by category (CAPEX, OPEX, cloud, licenses)
- Scenario comparison and recommendations
- Compliance notes for 152-FZ and 187-FZ

### View CLI Help

```bash
ru-smb-it-budget-planner --help
ru-smb-it-budget-planner plan --help
```

---

## Update / Upgrade

To update the tool to the latest version:

```bash
cd ru-smb-it-budget-planner
git pull origin main
pip install --upgrade .
```

If you're using editable mode (`pip install -e .`), simply pull the latest code:

```bash
git pull origin main
```

---

## Logs, Monitoring, Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'ru_smb_it_budget_planner'`

**Solution**: Ensure you've installed the package correctly:
```bash
pip install .
```

---

**Issue**: `Ошибка: Конфигурация некорректна` (Configuration invalid)

**Solution**: Run validation to see specific errors:
```bash
ru-smb-it-budget-planner validate infra.yaml
```

Check for:
- YAML syntax errors (indentation, colons, quotes)
- Missing required fields
- Invalid data types (e.g., string instead of number)

---

**Issue**: Cost calculations seem incorrect

**Solution**: Verify your pricing data:
- Check `pricing.yaml` for up-to-date vendor pricing
- Ensure regional names match between `infra.yaml` and `pricing.yaml`
- Validate cloud profile codes

---

**Issue**: Missing cloud profiles or pricing regions

**Solution**: Add missing entries to `pricing.yaml`:
```yaml
cloud_profiles:
  - code: "your_cloud_provider"
    vCPU_price_rub_per_hour: 1.2
    ram_price_rub_per_gb_hour: 0.4
    storage_price_rub_per_gb_month: 4.5
    egress_price_rub_per_gb: 0.8
```

### Enable Debug Logging

For verbose output during development:

```bash
export LOG_LEVEL=DEBUG
ru-smb-it-budget-planner plan infra.yaml pricing.yaml
```

### Running Tests

For developers and contributors:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=ru_smb_it_budget_planner --cov-report=html

# Run specific test module
pytest tests/test_dsl.py
```

---

## Security Notes

> [!IMPORTANT]
> This tool is for cost estimation purposes only. It does not guarantee legal or regulatory compliance.

### Data Privacy

- The tool processes infrastructure metadata locally
- No data is sent to external services
- All calculations are performed offline
- Configuration files may contain business-sensitive information — protect them accordingly

### Regulatory Compliance

- `has_pd` and `has_kii` flags help **identify** compliance requirements
- **You** are responsible for implementing actual compliance measures
- Consult legal and security experts for 152-FZ and 187-FZ compliance
- This tool provides guidance, not legal advice

### Best Practices

- Store `infra.yaml` and `pricing.yaml` in version control with restricted access
- Regularly update pricing data to maintain accuracy
- Review generated reports before sharing with third parties
- Do not commit actual vendor pricing or business-sensitive data to public repositories

---

## Project Structure

```
ru-smb-it-budget-planner/
├── src/
│   └── ru_smb_it_budget_planner/
│       ├── cli.py                      # Main CLI entry point
│       ├── dsl/                        # Configuration parser and validator
│       │   ├── parser.py
│       │   └── schema_generator.py
│       ├── models/                     # Pydantic data models
│       │   ├── infra_model.py
│       │   └── pricing_model.py
│       ├── calculator/                 # TCO calculation engines
│       │   ├── on_prem_calc.py
│       │   ├── cloud_calc.py
│       │   ├── energy_calc.py
│       │   └── scenario_builder.py
│       ├── reporting/                  # Report generators
│       │   ├── tables.py
│       │   └── owner_report_ru.py
│       └── ai_interface/               # AI stub interfaces (future)
│           ├── infra_text_to_yaml_stub.py
│           └── report_text_generator_stub.py
├── tests/                              # Unit and integration tests
├── examples/                           # Sample configurations
│   ├── small_retail_on_prem/
│   └── it_services_hybrid/
├── .github/
│   └── workflows/
│       └── ci.yml                      # CI/CD pipeline
├── pyproject.toml                      # Project metadata and dependencies
├── LICENSE                             # Apache-2.0 license
├── README.md                           # This file (English)
└── README.ru.md                        # Russian version
```

---

## Roadmap / Plans

Future enhancements under consideration:

- **Web UI**: Browser-based interface for non-technical users
- **AI Integration**: Natural language infrastructure description → YAML conversion
- **Multi-year projections**: Long-term TCO forecasting with growth scenarios
- **Advanced reporting**: PDF/Excel export with charts and graphs
- **Vendor integrations**: Direct API pulls for real-time cloud pricing
- **Optimization engine**: Automated recommendations for cost reduction
- **Database backend**: Store historical calculations and track budget over time

Contributions and feature requests are welcome via GitHub Issues.

---

## Contributing

We welcome contributions from the community!

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** with clear, descriptive commits
4. **Add tests** for new functionality
5. **Run linters and tests**:
   ```bash
   ruff check src tests
   mypy src
   pytest
   ```
6. **Submit a Pull Request** with a clear description of your changes

### Code Style

- Follow **PEP 8** Python style guidelines
- Use **type hints** for all function signatures
- Write **docstrings** for public modules, classes, and functions
- Keep functions small and focused
- Maintain **Russian-language** error messages and user-facing text

### Reporting Issues

- Use GitHub Issues to report bugs or request features
- Include steps to reproduce for bugs
- Provide example `infra.yaml` and `pricing.yaml` files when relevant

---

## License

This project is licensed under the **Apache License 2.0**.

See the [LICENSE](LICENSE) file for full terms and conditions.

In summary:
- ✅ Free to use, modify, and distribute
- ✅ Commercial use permitted
- ✅ Must include original license and copyright notice
- ✅ Changes must be documented
- ❌ No warranty or liability

---

## Author and Commercial Support

**Author**: [Ranas Mukminov](https://github.com/ranas-mukminov)

This project is maintained by the team at **[run-as-daemon.ru](https://run-as-daemon.ru)**.

### Professional Services

For production deployments, customizations, and professional support:

- **IT Budget Audits**: Comprehensive analysis of your infrastructure costs with optimization recommendations
- **Migration Planning**: Design and execute cloud migration strategies tailored to Russian regulatory requirements
- **Infrastructure Consulting**: DevOps, monitoring, backup, and SRE services for Russian SMBs
- **Custom Development**: Extend this tool with integrations, custom calculators, or enterprise features

**Contact**: Visit [run-as-daemon.ru](https://run-as-daemon.ru) (in Russian) or reach out via the [GitHub profile](https://github.com/ranas-mukminov).

---

**⭐ If this tool helped you, please star the repository on GitHub!**
