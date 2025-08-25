# 🛗 Elevator Safety Self-Inspection System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive system for performing automated safety inspections on elevators. This tool helps maintenance personnel conduct thorough checks, ensuring elevator systems meet safety standards.

## ✨ Features

- 🔍 **Comprehensive Inspection Checklist**: Pre-configured safety checks based on industry standards
- 📊 **Sensor Integration**: Connect to elevator sensors to collect real-time data
- 🚨 **Safety Analysis**: Automatic evaluation of inspection results with clear pass/fail criteria
- 📝 **Detailed Reports**: Generate professional PDF, HTML or JSON reports
- 📱 **Easy to Use**: Simple command-line interface for technicians
- 💾 **Historical Data**: Store and retrieve inspection history for trend analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/elevator-safety-inspector.git
   cd elevator-safety-inspector
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment (optional):
   ```bash
   cp config/config.example.yaml config/config.yaml
   # Edit config.yaml with your specific configuration
   ```

## 📖 Usage

### Basic Inspection

Run a basic inspection on an elevator:

```bash
python -m src.main --elevator-id ELEVATOR123
```

### Advanced Options

Specify report format and config file:

```bash
python -m src.main --elevator-id ELEVATOR123 --report-format pdf --config path/to/custom/config.yaml
```

Enable verbose logging:

```bash
python -m src.main --elevator-id ELEVATOR123 --verbose
```

## 🔧 Configuration

The system is configured through YAML files. The default configuration file is `config/config.yaml`, which includes:

- Hardware specifications
- Sensor configurations
- Inspection checklist items and thresholds
- Reporting preferences

Example configuration snippet:

```yaml
inspection:
  checklist_items:
    - id: "motor_temp"
      name: "Motor Temperature"
      type: "sensor"
      sensor_id: "motor_temperature"
      category: "mechanical"
      criticality: "high"
      thresholds:
        min_warning: 50
        max_warning: 75
        max_critical: 85
```

## 📊 Report Examples

### Safety Report Summary

The system generates reports with clear summaries:

- ✅ **SAFE**: All checks passed
- ⚠️ **CAUTION**: Some warnings detected
- ❌ **UNSAFE**: Critical issues detected

Each report includes detailed measurements and recommendations for addressing any issues found.

## 🧪 Running Tests

Run the test suite to ensure everything is working correctly:

```bash
python -m unittest discover tests
```

For more verbose test output:

```bash
python -m unittest discover tests -v
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📬 Contact

Project Link: [https://github.com/yourusername/elevator-safety-inspector](https://github.com/yourusername/elevator-safety-inspector)

---

Built with ❤️ by the elevator safety community
