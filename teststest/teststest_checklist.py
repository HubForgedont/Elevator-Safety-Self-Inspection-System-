"""
Unit tests for the safety checklist module
"""

import unittest
from unittest.mock import MagicMock, patch
from src.inspection.checklist import SafetyChecklist


class TestSafetyChecklist(unittest.TestCase):
    """Tests for the SafetyChecklist class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.checklist_items = [
            {
                "id": "test_sensor",
                "name": "Test Sensor",
                "type": "sensor",
                "sensor_id": "test_sensor_1",
                "category": "test",
                "criticality": "high",
                "thresholds": {
                    "min_warning": 10,
                    "max_warning": 50,
                    "max_critical": 70
                }
            },
            {
                "id": "test_visual",
                "name": "Test Visual",
                "type": "visual",
                "category": "test",
                "criticality": "medium"
            },
            {
                "id": "test_mechanical",
                "name": "Test Mechanical",
                "type": "mechanical",
                "component_id": "test_component",
                "category": "test",
                "criticality": "critical"
            }
        ]
        
        self.checklist = SafetyChecklist(self.checklist_items)
        
        # Create a mock elevator interface
        self.mock_elevator = MagicMock()
        self.mock_elevator.get_sensor_reading.return_value = 30.0
        self.mock_elevator.test_mechanical_component.return_value = True
    
    def test_initialization(self):
        """Test checklist initialization"""
        self.assertEqual(len(self.checklist.checklist_items), 3)
        self.assertEqual(self.checklist.checklist_items[0]['name'], "Test Sensor")
    
    def test_run_inspection(self):
        """Test running a complete inspection"""
        results = self.checklist.run_inspection(self.mock_elevator)
        
        # Check that we got results for all items
        self.assertEqual(len(results), 3)
        
        # Check sensor result
        sensor_result = next(r for r in results if r['item_id'] == 'test_sensor')
        self.assertEqual(sensor_result['status'], 'pass')
        self.assertEqual(sensor_result['value'], 30.0)
        
        # Check visual result
        visual_result = next(r for r in results if r['item_id'] == 'test_visual')
        self.assertEqual(visual_result['status'], 'pass')
        
        # Check mechanical result
        mechanical_result = next(r for r in results if r['item_id'] == 'test_mechanical')
        self.assertEqual(mechanical_result['status'], 'pass')
        
        # Verify method calls
        self.mock_elevator.get_sensor_reading.assert_called_with('test_sensor_1')
        self.mock_elevator.test_mechanical_component.assert_called_with('test_component')
    
    def test_evaluate_sensor_reading_pass(self):
        """Test sensor reading evaluation - pass case"""
        thresholds = {
            "min_warning": 10,
            "max_warning": 50,
            "max_critical": 70
        }
        
        # Value in normal range
        status = self.checklist._evaluate_sensor_reading(30, thresholds)
        self.assertEqual(status, 'pass')
    
    def test_evaluate_sensor_reading_warning(self):
        """Test sensor reading evaluation - warning case"""
        thresholds = {
            "min_warning": 10,
            "max_warning": 50,
            "max_critical": 70
        }
        
        # Value in warning range (too high)
        status = self.checklist._evaluate_sensor_reading(55, thresholds)
        self.assertEqual(status, 'warning')
        
        # Value in warning range (too low)
        status = self.checklist._evaluate_sensor_reading(5, thresholds)
        self.assertEqual(status, 'warning')
    
    def test_evaluate_sensor_reading_fail(self):
        """Test sensor reading evaluation - fail case"""
        thresholds = {
            "min_warning": 10,
            "max_warning": 50,
            "max_critical": 70
        }
        
        # Value in critical range
        status = self.checklist._evaluate_sensor_reading(80, thresholds)
        self.assertEqual(status, 'fail')
    
    def test_error_handling(self):
        """Test error handling during inspection"""
        # Make the sensor reading raise an exception
        self.mock_elevator.get_sensor_reading.side_effect = Exception("Sensor error")
        
        results = self.checklist.run_inspection(self.mock_elevator)
        
        # Check sensor result has error status
        sensor_result = next(r for r in results if r['item_id'] == 'test_sensor')
        self.assertEqual(sensor_result['status'], 'error')
        self.assertEqual(sensor_result['error'], 'Sensor error')


if __name__ == '__main__':
    unittest.main()
