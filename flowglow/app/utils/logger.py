import logging
from datetime import datetime
from typing import Any, Dict
from pathlib import Path

class FlowGlowLogger:
    """Custom logger for FlowGlow application"""
    
    def __init__(self, name: str = "FlowGlow"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
        
    def _setup_logger(self):
        """Configure logger settings"""
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create handlers
        file_handler = logging.FileHandler(
            log_dir / f"flowglow_{datetime.now().strftime('%Y%m%d')}.log"
        )
        console_handler = logging.StreamHandler()
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)
    
    def log_request(self, request: Dict[str, Any]):
        """Log content generation request"""
        self.logger.info(f"Content Request: {request}")
    
    def log_response(self, response: Dict[str, Any]):
        """Log content generation response"""
        self.logger.info(f"Content Response: {response}")
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with context"""
        self.logger.error(f"Error: {str(error)}", extra={"context": context})
    
    def log_performance(self, operation: str, duration: float):
        """Log performance metrics"""
        self.logger.info(f"Performance - {operation}: {duration:.2f}s")