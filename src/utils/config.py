"""
Configuration utilities for elevator safety inspection system
"""

import os
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger('elevator_safety')


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary containing configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config file is invalid
    """
    if not os.path.exists(config_path):
        logger.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        logger.debug(f"Loaded configuration from {config_path}")
        return config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {str(e)}")
        raise ValueError(f"Invalid configuration file: {str(e)}")
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration if no config file is provided
    
    Returns:
        Dictionary containing default configuration
    """
    return {
        "hardware": {
            "sensors": {
                "temp_motor": {
                    "type": "temperature",
                    "location": "motor",
                    "unit": "celsius"
                },
                "temp_control": {
                    "type": "temperature",
                    "location": "control_panel",
                    "unit": "celsius"
                },
                "vibration_1": {
                    "type": "vibration",
                    "location": "motor",
                    "unit": "mm/s"
                },
                "speed": {
                    "type": "speed",
                    "unit": "m/s"
                },
                "weight": {
                    "type": "weight",
                    "capacity": 1000,
                    "unit": "kg"
                },
                "door_sensor": {
                    "type": "door_sensor"
                },
                "emergency_button": {
                    "type": "emergency_button"
                }
            }
        },
        "inspection": {
            "checklist_items": [
                {
                    "id": "motor_temp",
                    "name": "Motor Temperature",
                    "type": "sensor",
                    "sensor_id": "temp_motor",
                    "category": "mechanical",
                    "criticality": "high",
                    "thresholds": {
                        "min_warning": 50,
                        "max_warning": 70,
                        "max_critical": 85
                    }
                },
                {
                    "id": "control_temp",
                    "name": "Control Panel Temperature",
                    "type": "sensor",
                    "sensor_id": "temp_control",
                    "category": "electrical",
                    "criticality": "medium",
                    "thresholds": {
                        "min_warning": 30,
                        "max_warning": 60,
                        "max_critical": 75
                    }
                },
                {
                    "id": "vibration",
                    "name": "Motor Vibration",
                    "type": "sensor",
                    "sensor_id": "vibration_1",
                    "category": "mechanical",
                    "criticality": "high",
                    "thresholds": {
                        "max_warning": 4.0,
                        "max_critical": 7.0
                    }
                },
                {
                    "id": "speed_check",
                    "name": "Speed Regulation",
                    "type": "sensor",
                    "sensor_id": "speed",
                    "category": "operational",
                    "criticality": "high",
                    "thresholds": {
                        "min_warning": 0.5,
                        "max_warning": 2.0,
                        "max_critical": 2.5
                    }
                },
                {
                    "id": "weight_sensor",
                    "name": "Weight Sensor Calibration",
                    "type": "sensor",
                    "sensor_id": "weight",
                    "category": "operational",
                    "criticality": "high",
                    "thresholds": {
                        "max_critical": 1050
                    }
                },
                {
                    "id": "door_operation",
                    "name": "Door Operation",
                    "type": "sensor",
                    "sensor_id": "door_sensor",
                    "category": "safety",
                    "criticality": "critical"
                },
                {
                    "id": "emergency_button",
                    "name": "Emergency Button",
                    "type": "sensor",
                    "sensor_id": "emergency_button",
                    "category": "safety",
                    "criticality": "critical"
                },
                {
                    "id": "brake_test",
                    "name": "Emergency Brake Test",
                    "type": "mechanical",
                    "component_id": "emergency_brake",
                    "category": "safety",
                    "criticality": "critical"
                },
                {
                    "id": "cables_visual",
                    "name": "Cables Visual Inspection",
                    "type": "visual",
                    "category": "mechanical",
                    "criticality": "critical"
                },
                {
                    "id": "guide_rails",
                    "name": "Guide Rails Inspection",
                    "type": "visual",
                    "category": "mechanical",
                    "criticality": "high"
                }
            ],
            "safety_thresholds": {
                "max_critical_issues": 0,
                "max_warnings": 2
            }
        },
        "reporting": {
            "default_format": "pdf",
            "include_images": True,
            "company_name": "Elevator Safety Inspections Inc.",
            "company_logo": "assets/logo.png",
            "contact_email": "safety@example.com"
        }
    }
