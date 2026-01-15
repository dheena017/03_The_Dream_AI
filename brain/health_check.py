"""
Dream AI Health Check and Diagnostics
Monitors system health, detects issues, and provides recommendations
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add brain to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from logger import get_logger
except ImportError:
    # Fallback if logger not available
    import logging
    def get_logger(name):
        return logging.getLogger(name)

logger = get_logger("health_check")

class HealthCheck:
    """System diagnostics and health monitoring"""
    
    def __init__(self):
        self.brain_dir = Path(__file__).parent
        self.issues = []
        self.warnings = []
        
    def check_all(self):
        """Run all health checks"""
        logger.info("🏥 Starting comprehensive health check...")
        
        self.check_imports()
        self.check_directories()
        self.check_memory_system()
        self.check_file_permissions()
        self.check_disk_space()
        
        return self.generate_report()
    
    def check_imports(self):
        """Verify all core modules work"""
        logger.info("Checking core modules...")
        
        try:
            from observation_memory import ObservationMemory
            logger.debug("✅ memory imports OK")
        except Exception as e:
            self.issues.append(f"❌ memory failed: {e}")
        
        try:
            from orchestrator import BrainOrchestrator
            logger.debug("✅ orchestrator imports OK")
        except Exception as e:
            self.issues.append(f"❌ orchestrator failed: {e}")
    
    def check_directories(self):
        """Verify critical directories exist"""
        logger.info("Checking directories...")
        critical_dirs = ['generated', 'memory', 'skills', 'evolution', 'logs']
        
        for dir_name in critical_dirs:
            dir_path = self.brain_dir / dir_name
            if not dir_path.exists():
                self.warnings.append(f"⚠️  Missing directory: {dir_name}")
                logger.warning(f"Creating missing directory: {dir_name}")
                dir_path.mkdir(parents=True, exist_ok=True)
            else:
                logger.debug(f"✅ {dir_name} exists")
    
    def check_memory_system(self):
        """Check if memory database is accessible"""
        logger.info("Checking memory system...")
        try:
            from observation_memory import ObservationMemory
            mem = ObservationMemory()
            # Just verify it can connect to the database
            logger.info("✅ Memory system is functional")
        except Exception as e:
            self.warnings.append(f"⚠️  Memory system issue: {e}")
            logger.warning(f"Memory check failed: {e}")
    
    def check_file_permissions(self):
        """Check if we have write permissions to critical dirs"""
        logger.info("Checking file permissions...")
        critical_dirs = ['generated', 'memory', 'logs']
        
        for dir_name in critical_dirs:
            dir_path = self.brain_dir / dir_name
            test_file = dir_path / '.write_test'
            try:
                test_file.touch()
                test_file.unlink()
                logger.debug(f"✅ Write permission OK: {dir_name}")
            except Exception as e:
                self.issues.append(f"❌ No write permission: {dir_name}")
                logger.error(f"Permission check failed for {dir_name}: {e}")
    
    def check_disk_space(self):
        """Check available disk space"""
        logger.info("Checking disk space...")
        try:
            import shutil
            usage = shutil.disk_usage('.')
            percent_used = (usage.used / usage.total) * 100
            
            logger.info(f"Disk usage: {percent_used:.1f}%")
            
            if percent_used > 90:
                self.issues.append(f"❌ Disk almost full: {percent_used:.1f}%")
            elif percent_used > 80:
                self.warnings.append(f"⚠️  Disk usage high: {percent_used:.1f}%")
        except Exception as e:
            logger.warning(f"Could not check disk space: {e}")
    
    def generate_report(self):
        """Generate health check report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy" if not self.issues else "degraded" if self.warnings else "unhealthy",
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendation": self._get_recommendation()
        }
        
        logger.info(f"Health check complete. Status: {report['status']}")
        return report
    
    def _get_recommendation(self):
        """Provide recommendations based on issues"""
        if self.issues:
            if any("permission" in i.lower() for i in self.issues):
                return "Fix file permissions or run with appropriate privileges"
            if any("import" in i.lower() for i in self.issues):
                return "Run 'pip install -r requirements.txt' to install dependencies"
            return "Contact administrator for support"
        
        if self.warnings:
            if any("disk" in w.lower() for w in self.warnings):
                return "Clean up old backups and generated files"
            return "Monitor system closely"
        
        return "System running normally"

def run_health_check():
    """Quick health check"""
    hc = HealthCheck()
    report = hc.check_all()
    
    print("\n" + "="*60)
    print("🏥 DREAM AI HEALTH CHECK REPORT")
    print("="*60)
    print(f"Status: {report['status'].upper()}")
    print(f"Time: {report['timestamp']}")
    
    if report['issues']:
        print("\n❌ ISSUES:")
        for issue in report['issues']:
            print(f"  {issue}")
    
    if report['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in report['warnings']:
            print(f"  {warning}")
    
    if not report['issues'] and not report['warnings']:
        print("\n✅ All systems operational")
    
    print(f"\n💡 Recommendation: {report['recommendation']}")
    print("="*60 + "\n")
    
    return report

if __name__ == "__main__":
    run_health_check()
