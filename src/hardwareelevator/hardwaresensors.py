"""
Sensor interface for elevator safety inspection
"""

import logging
import random
from typing import Dict, Any, Optional, Union

logger = logging.getLogger('elevator_safety')


class SensorManager:
    """Manages connections to and readings from elevator sensors"""
    
    def __init__(self, sensor_config: Dict[str, Any]):
        """
        Initialize with sensor configuration
        
        Args:
            sensor_config: Dictionary containing sensor configurations
        """
        self.sensor_config = sensor_config
        self.connected_sensors = {}
        logger.debug(f"Initialized sensor manager with {len(sensor_config)} sensors")
    
    def connect_sensors(self) -> bool:
        """
        Connect to all configured sensors
        
        Returns:
            True if all sensors connected successfully, False otherwise
        """
        success = True
        for sensor_id, config in self.sensor_config.items():
            try:
                # In a real implementation, this would establish actual connections
                # to physical sensors or sensor APIs
                logger.info(f"Connecting to sensor: {sensor_id} ({config['type']})")
                
                # Simulate connection success
                self.connected_sensors[sensor_id] = {
                    "type": config['type'],
                    "connected": True,
                    "config": config
                }
                
                logger.debug(f"Successfully connected to sensor: {sensor_id}")
            except Exception as e:
                logger.error(f"Failed to connect to sensor {sensor_id}: {str(e)}")
                success = False
        
        return success
    
    def get_reading(self, sensor_id: str) -> Optional[Union[float, bool, str]]:
        """
        Get a reading from a specific sensor
        
        Args:
            sensor_id: Identifier for the sensor
            
        Returns:
            Sensor reading value, or None if sensor not available
        """
        if sensor_id not in self.connected_sensors:
            logger.warning(f"Attempted to read from unknown sensor: {sensor_id}")
            return None
        
        sensor = self.connected_sensors[sensor_id]
        
        try:
            # In a real implementation, this would get actual readings from sensors
            # For simulation, generate reasonable values based on sensor type
            if sensor['type'] == 'temperature':
                value = self._simulate_temperature_reading(sensor['config'])
            elif sensor['type'] == 'pressure':
                value = self._simulate_pressure_reading(sensor['config'])
            elif sensor['type'] == 'vibration':
                value = self._simulate_vibration_reading(sensor['config'])
            elif sensor['type'] == 'speed':
                value = self._simulate_speed_reading(sensor['config'])
            elif sensor['type'] == 'weight':
                value = self._simulate_weight_reading(sensor['config'])
            elif sensor['type'] == 'door_sensor':
                value = self._simulate_door_sensor_reading(sensor['config'])
            elif sensor['type'] == 'emergency_button':
                value = self._simulate_emergency_button_reading(sensor['config'])
            else:
                logger.warning(f"Unknown sensor type: {sensor['type']}")
                value = 0
            
            logger.debug(f"Sensor {sensor_id} reading: {value}")
            return value
            
        except Exception as e:
            logger.error(f"Error reading from sensor {sensor_id}: {str(e)}")
            return None
    
    def _simulate_temperature_reading(self, config: Dict[str, Any]) -> float:
        """Simulate a temperature sensor reading"""
        # Normal range for elevator machinery temperature in Celsius
        base_value = 35.0
        variation = 15.0
        return base_value + (random.random() * variation)
    
    def _simulate_pressure_reading(self, config: Dict[str, Any]) -> float:
        """Simulate a pressure sensor reading"""
        # Hydraulic pressure in PSI for hydraulic elevators
        base_value = 500.0
        variation = 200.0
        return base_value + (random.random() * variation)
    
    def _simulate_vibration_reading(self, config: Dict[str, Any]) -> float:
        """Simulate a vibration sensor reading"""
        # Vibration in mm/s
        base_value = 2.0
        variation = 3.0
        return base_value + (random.random() * variation)
    
    def _simulate_speed_reading(self, config: Dict[str, Any]) -> float:
        """Simulate an elevator speed reading"""
        # Speed in m/s
        base_value = 1.5
        variation = 0.5
        return base_value + (random.random() * variation)
    
    def _simulate_weight_reading(self, config: Dict[str, Any]) -> float:
        """Simulate a weight sensor reading"""
        # Weight in kg
        capacity = config.get('capacity', 1000)
        return random.random() * capacity
    
    def _simulate_door_sensor_reading(self, config: Dict[str, Any]) -> bool:
        """Simulate a door sensor reading"""
        # True = door closed properly, False = door issue
        return random.random() > 0.1  # 90% chance doors are fine
    
    def _simulate_emergency_button_reading(self, config: Dict[str, Any]) -> bool:
        """Simulate an emergency button check"""
        # True = button working, False = button malfunction
        return random.random() > 0.05  # 95% chance button is working
