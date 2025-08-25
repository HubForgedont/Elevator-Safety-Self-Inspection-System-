"""
Safety checklist module for elevator inspection
"""

import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger('elevator_safety')


class SafetyChecklist:
    """Manages the safety inspection checklist for elevators"""
    
    def __init__(self, checklist_items: List[Dict[str, Any]]):
        """
        Initialize with checklist items from configuration
        
        Args:
            checklist_items: List of checklist item configurations
        """
        self.checklist_items = checklist_items
        logger.debug(f"Initialized safety checklist with {len(checklist_items)} items")
    
    def run_inspection(self, elevator_interface) -> List[Dict[str, Any]]:
        """
        Run through the complete safety checklist
        
        Args:
            elevator_interface: Interface to the elevator hardware
            
        Returns:
            List of inspection results
        """
        results = []
        
        for item in self.checklist_items:
            logger.info(f"Checking: {item['name']}")
            
            try:
                # Get sensor data or manual input based on check type
                if item['type'] == 'sensor':
                    value = elevator_interface.get_sensor_reading(item['sensor_id'])
                    status = self._evaluate_sensor_reading(value, item['thresholds'])
                elif item['type'] == 'visual':
                    # For visual inspections, we'd typically have a UI prompt
                    # Here we're simulating with a default "pass" for demonstration
                    value = "SIMULATED VISUAL INSPECTION"
                    status = "pass"
                elif item['type'] == 'mechanical':
                    value = elevator_interface.test_mechanical_component(item['component_id'])
                    status = "pass" if value else "fail"
                else:
                    logger.warning(f"Unknown check type: {item['type']}")
                    value = None
                    status = "skipped"
                
                result = {
                    "item_id": item['id'],
                    "name": item['name'],
                    "type": item['type'],
                    "value": value,
                    "status": status,
                    "timestamp": datetime.now().isoformat(),
                    "category": item.get('category', 'general'),
                    "criticality": item.get('criticality', 'normal')
                }
                
                results.append(result)
                logger.debug(f"Check result: {item['name']} - {status}")
                
            except Exception as e:
                logger.error(f"Error during check {item['name']}: {str(e)}")
                results.append({
                    "item_id": item['id'],
                    "name": item['name'],
                    "type": item['type'],
                    "value": None,
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "category": item.get('category', 'general'),
                    "criticality": item.get('criticality', 'normal'),
                    "error": str(e)
                })
        
        return results
    
    def _evaluate_sensor_reading(self, value: float, thresholds: Dict[str, Any]) -> str:
        """
        Evaluate a sensor reading against defined thresholds
        
        Args:
            value: The sensor reading value
            thresholds: Dictionary containing threshold values
            
        Returns:
            Status string: 'pass', 'warning', or 'fail'
        """
        if 'min_critical' in thresholds and value < thresholds['min_critical']:
            return 'fail'
        if 'max_critical' in thresholds and value > thresholds['max_critical']:
            return 'fail'
        if 'min_warning' in thresholds and value < thresholds['min_warning']:
            return 'warning'
        if 'max_warning' in thresholds and value > thresholds['max_warning']:
            return 'warning'
        return 'pass'
