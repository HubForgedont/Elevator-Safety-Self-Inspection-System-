"""
Database utilities for storing inspection results
"""

import os
import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger('elevator_safety')


class InspectionDatabase:
    """Database for storing and retrieving elevator inspection data"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file, if None uses default location
        """
        if db_path is None:
            # Use default location in user's home directory
            home_dir = os.path.expanduser("~")
            db_dir = os.path.join(home_dir, ".elevator_safety")
            
            # Create directory if it doesn't exist
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            db_path = os.path.join(db_dir, "inspections.db")
        
        self.db_path = db_path
        self.conn = None
        
        logger.debug(f"Database initialized with path: {db_path}")
        
        # Initialize database schema if needed
        self._initialize_schema()
    
    def _initialize_schema(self) -> None:
        """Create database schema if it doesn't exist"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Create inspections table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inspections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    elevator_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    inspector TEXT,
                    safety_level TEXT NOT NULL,
                    critical_issues INTEGER NOT NULL,
                    warnings INTEGER NOT NULL,
                    passed INTEGER NOT NULL,
                    compliance_percentage REAL NOT NULL,
                    report_path TEXT,
                    notes TEXT
                )
            ''')
            
            # Create inspection_items table for detailed results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inspection_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inspection_id INTEGER NOT NULL,
                    item_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    criticality TEXT NOT NULL,
                    status TEXT NOT NULL,
                    value TEXT,
                    FOREIGN KEY (inspection_id) REFERENCES inspections (id)
                )
            ''')
            
            conn.commit()
            logger.debug("Database schema initialized")
            
        except Exception as e:
            logger.error(f"Error initializing database schema: {str(e)}")
            raise
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection, creating one if needed"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.conn
    
    def close(self) -> None:
        """Close the database connection"""
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            logger.debug("Database connection closed")
    
    def save_inspection(self, elevator_id: str, inspection_results: List[Dict[str, Any]], 
                       analysis: Dict[str, Any], report_path: Optional[str] = None,
                       inspector: Optional[str] = None, notes: Optional[str] = None) -> int:
        """
        Save inspection results to database
        
        Args:
            elevator_id: Identifier for the elevator
            inspection_results: List of inspection result dictionaries
            analysis: Safety analysis results
            report_path: Path to the generated report file
            inspector: Name of the inspector
            notes: Additional notes about the inspection
            
        Returns:
            ID of the saved inspection record
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Insert main inspection record
            cursor.execute('''
                INSERT INTO inspections (
                    elevator_id, timestamp, inspector, safety_level,
                    critical_issues, warnings, passed, compliance_percentage,
                    report_path, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                elevator_id,
                datetime.now().isoformat(),
                inspector or "System",
                analysis['safety_level'],
                analysis['critical_issues'],
                analysis['warnings'],
                analysis['passed'],
                analysis['compliance_percentage'],
                report_path,
                notes
            ))
            
            inspection_id = cursor.lastrowid
            
            # Insert detailed inspection items
            for result in inspection_results:
                cursor.execute('''
                    INSERT INTO inspection_items (
                        inspection_id, item_id, name, category, criticality, status, value
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    inspection_id,
                    result['item_id'],
                    result['name'],
                    result.get('category', 'general'),
                    result.get('criticality', 'normal'),
                    result['status'],
                    json.dumps(result['value']) if result['value'] is not None else None
                ))
            
            conn.commit()
            logger.info(f"Saved inspection {inspection_id} for elevator {elevator_id}")
            
            return inspection_id
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error saving inspection to database: {str(e)}")
            raise
    
    def get_inspection(self, inspection_id: int) -> Dict[str, Any]:
        """
        Retrieve a specific inspection by ID
        
        Args:
            inspection_id: ID of the inspection to retrieve
            
        Returns:
            Dictionary containing inspection data and results
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get main inspection record
            cursor.execute('''
                SELECT * FROM inspections WHERE id = ?
            ''', (inspection_id,))
            
            inspection = dict(cursor.fetchone())
            
            # Get inspection items
            cursor.execute('''
                SELECT * FROM inspection_items WHERE inspection_id = ?
            ''', (inspection_id,))
            
            items = []
            for row in cursor.fetchall():
                item = dict(row)
                # Parse JSON value
                if item['value']:
                    try:
                        item['value'] = json.loads(item['value'])
                    except:
                        pass
                items.append(item)
            
            inspection['items'] = items
            
            return inspection
            
        except Exception as e:
            logger.error(f"Error retrieving inspection {inspection_id}: {str(e)}")
            raise
    
    def get_elevator_history(self, elevator_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get inspection history for a specific elevator
        
        Args:
            elevator_id: Identifier for the elevator
            limit: Maximum number of records to return
            
        Returns:
            List of inspection records for the elevator
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM inspections 
                WHERE elevator_id = ? 
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (elevator_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error retrieving history for elevator {elevator_id}: {str(e)}")
            raise
