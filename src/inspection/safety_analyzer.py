"""
Safety analyzer for elevator inspection results
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger('elevator_safety')


class SafetyAnalyzer:
    """Analyzes inspection results to determine safety status"""
    
    def __init__(self, safety_thresholds: Dict[str, Any]):
        """
        Initialize with safety thresholds from configuration
        
        Args:
            safety_thresholds: Dictionary containing safety threshold configurations
        """
        self.safety_thresholds = safety_thresholds
        logger.debug(f"Initialized safety analyzer with thresholds: {safety_thresholds}")
    
    def analyze(self, inspection_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze inspection results and determine safety status
        
        Args:
            inspection_results: List of inspection result dictionaries
            
        Returns:
            Dictionary containing analysis results
        """
        # Count different types of results
        critical_issues = 0
        warnings = 0
        passed = 0
        errors = 0
        
        # Lists to store specific issues
        critical_items = []
        warning_items = []
        error_items = []
        
        # Analyze each result
        for result in inspection_results:
            if result['status'] == 'fail':
                critical_issues += 1
                critical_items.append({
                    'name': result['name'],
                    'value': result['value'],
                    'category': result.get('category', 'general')
                })
            elif result['status'] == 'warning':
                warnings += 1
                warning_items.append({
                    'name': result['name'],
                    'value': result['value'],
                    'category': result.get('category', 'general')
                })
            elif result['status'] == 'pass':
                passed += 1
            elif result['status'] == 'error':
                errors += 1
                error_items.append({
                    'name': result['name'],
                    'error': result.get('error', 'Unknown error'),
                    'category': result.get('category', 'general')
                })
        
        # Determine overall safety status
        if critical_issues > 0:
            summary = "UNSAFE - Critical issues detected"
            action_required = "Immediate maintenance required. Elevator should not be used until fixed."
            safety_level = "critical"
        elif warnings > 0:
            summary = "CAUTION - Warnings detected"
            action_required = "Schedule maintenance soon to address warnings."
            safety_level = "warning"
        elif errors > 0:
            summary = "INCOMPLETE - Inspection errors"
            action_required = "Some tests failed to complete. Re-inspection recommended."
            safety_level = "incomplete"
        else:
            summary = "SAFE - All checks passed"
            action_required = "Regular maintenance schedule can be followed."
            safety_level = "safe"
        
        # Calculate compliance percentage
        total_checks = critical_issues + warnings + passed
        compliance_percentage = (passed / total_checks * 100) if total_checks > 0 else 0
        
        # Prepare analysis result
        analysis = {
            'summary': summary,
            'safety_level': safety_level,
            'action_required': action_required,
            'critical_issues': critical_issues,
            'warnings': warnings,
            'passed': passed,
            'errors': errors,
            'compliance_percentage': compliance_percentage,
            'critical_items': critical_items,
            'warning_items': warning_items,
            'error_items': error_items,
            'total_checks': len(inspection_results)
        }
        
        logger.info(f"Safety analysis: {summary} - {critical_issues} critical issues, "
                   f"{warnings} warnings, {passed} passed, {errors} errors")
        
        return analysis
