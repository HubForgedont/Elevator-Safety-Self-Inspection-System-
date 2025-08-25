"""
Interface for interacting with elevator hardware
"""

import logging
import time
from typing import Dict, Any, Optional, Union

from src.hardware.sensors import SensorManager

logger = logging.getLogger('elevator_safety')


class ElevatorInterface:
    """Interface for interacting with elevator hardware systems"""
    
    def __init__(self, elevator_id: str, hardware_config: Dict[str, Any]):
        """
        Initialize the elevator interface
        
        Args:
            elevator_id: Unique identifier for the elevator
            hardware_config: Configuration for hardware components
        """
        self.elevator_id = elevator_id
        self.hardware_config = hardware_config
        self.connected = False
        
        # Initialize sensor manager
        self.sensor_manager = SensorManager(hardware_config.get('sensors', {}))
        
        # Connect to elevator systems
        self._connect()
    
    def _connect(self) -> bool:
        """
        Establish connection to elevator systems
        
        Returns:
            True if connection successful, False otherwise
        """
        logger.info(f"Connecting to elevator {self.elevator_id}...")
        
        try:
            # Connect to sensors
            sensor_success = self.sensor_manager.connect_sensors()
            
            # In a real implementation, would connect to other systems:
            # - Control system
            # - Motor controllers
            # - Door mechanisms
            # - Emergency systems
            
            # Simulate connection delay
            time.sleep(0.5)
            
            self.connected = sensor_success
            if self.connected:
                logger.info(f"Successfully connected to elevator {self.elevator_id}")
            else:
                logger.error(f"Failed to connect to all systems for elevator {self.elevator_id}")
            
            return self.connected
            
        except Exception as e:
            logger.exception(f"Error connecting to elevator {self.elevator_id}: {str(e)}")
            self.connected = False
            return False
    
    def get_sensor_reading(self, sensor_id: str) -> Optional[Union[float, bool, str]]:
        """
        Get a reading from a specific sensor
        
        Args:
            sensor_id: Identifier for the sensor
            
        Returns:
            Sensor reading value, or None if sensor not available
        """
        if not self.connected:
            logger.warning("Attempted to get sensor reading while disconnected")
            return None
        
        return self.sensor_manager.get_reading(sensor_id)
    
    def test_mechanical_component(self, component_id: str) -> bool:
        """
        Test a mechanical component of the elevator
        
        Args:
            component_id: Identifier for the component
            
        Returns:
            True if component passes test, False otherwise
        """
        if not self.connected:
            logger.warning("Attempted to test component while disconnected")
            return False
        
        logger.info(f"Testing mechanical component: {component_id}")
        
        # In a real implementation, this would send commands to test
        # actual mechanical components and analyze their responses
        
        # For simulation, we'll return a mostly positive result
        import random
        result = random.random() > 0.1  # 90% pass rate
        
        status = "passed" if result else "failed"
        logger.info(f"Component {component_id} test {status}")
        
        return result
    
    def get_elevator_info(self) -> Dict[str, Any]:
        """
        Get general information about the elevator
        
        Returns:
            Dictionary containing elevator information
        """
        # In a real implementation, this would query the elevator's
        # control system for actual information
        
        return {
            "id": self.elevator_id,
            "type": self.hardware_config.get("type", "unknown"),
            "manufacturer": self.hardware_config.get("manufacturer", "unknown"),
            "model": self.hardware_config.get("model", "unknown"),
            "installation_date": self.hardware_config.get("installation_date", "unknown"),
            "last_maintenance": self.hardware_config.get("last_maintenance", "unknown"),
            "capacity_kg": self.hardware_config.get("capacity_kg", 1000),
            "floors_serviced": self.hardware_config.get("floors_serviced", []),
            "connected": self.connected
        }
    
    def disconnect(self) -> None:
        """Safely disconnect from elevator systems"""
        if self.connected:
            logger.info(f"Disconnecting from elevator {self.elevator_id}")
            
            # In a real implementation, would properly close connections
            # to all hardware systems
            
            self.connected = False
        else:
            logger.debug(f"Already disconnected from elevator {self.elevator_id}")
