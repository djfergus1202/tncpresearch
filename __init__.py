"""
Utilities Module
===============

Common utility functions and helpers.
"""

import logging
import random
import numpy as np
import torch
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json
import yaml
import psutil
import platform
from datetime import datetime
from functools import wraps
import time


class Logger:
    """
    Custom logger wrapper for consistent logging across the platform.
    """
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name
            
        Returns:
            Logger instance
        """
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            ch.setFormatter(formatter)
            
            # Add handler if not already present
            if not logger.handlers:
                logger.addHandler(ch)
                
            cls._loggers[name] = logger
            
        return cls._loggers[name]
        
    @classmethod
    def set_level(cls, level: str):
        """Set logging level for all loggers."""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        log_level = level_map.get(level.upper(), logging.INFO)
        
        for logger in cls._loggers.values():
            logger.setLevel(log_level)
            for handler in logger.handlers:
                handler.setLevel(log_level)


# Create logger instance
logger = Logger()


def set_seed(seed: int = 42):
    """
    Set random seed for reproducibility.
    
    Args:
        seed: Random seed value
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        
    # Set deterministic behavior for CUDA
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    
    os.environ['PYTHONHASHSEED'] = str(seed)
    
    logger.get_logger(__name__).info(f"Random seed set to {seed}")


def device_info() -> Dict[str, Any]:
    """
    Get device information.
    
    Returns:
        Dictionary with device information
    """
    info = {
        'platform': platform.platform(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'cpu_count': os.cpu_count(),
        'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
    }
    
    # Check for GPU
    if torch.cuda.is_available():
        info['gpu_available'] = True
        info['gpu_count'] = torch.cuda.device_count()
        info['gpu_name'] = torch.cuda.get_device_name(0)
        info['cuda_version'] = torch.version.cuda
        
        # Memory info for first GPU
        memory_info = torch.cuda.mem_get_info(0)
        info['gpu_memory_total_gb'] = round(memory_info[1] / (1024**3), 2)
        info['gpu_memory_free_gb'] = round(memory_info[0] / (1024**3), 2)
    else:
        info['gpu_available'] = False
        
    return info


def memory_usage() -> Dict[str, float]:
    """
    Get current memory usage.
    
    Returns:
        Dictionary with memory usage in GB
    """
    memory = psutil.virtual_memory()
    
    usage = {
        'total_gb': round(memory.total / (1024**3), 2),
        'used_gb': round(memory.used / (1024**3), 2),
        'free_gb': round(memory.free / (1024**3), 2),
        'percent': memory.percent,
    }
    
    # GPU memory if available
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.mem_get_info(0)
        usage['gpu_used_gb'] = round((gpu_memory[1] - gpu_memory[0]) / (1024**3), 2)
        usage['gpu_free_gb'] = round(gpu_memory[0] / (1024**3), 2)
        
    return usage


def timer(func):
    """
    Decorator to time function execution.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        elapsed = end_time - start_time
        logger.get_logger(func.__module__).info(
            f"{func.__name__} took {elapsed:.2f} seconds"
        )
        
        return result
        
    return wrapper


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: Union[str, Path]) -> Any:
    """
    Load JSON file.
    
    Args:
        path: Path to JSON file
        
    Returns:
        Loaded data
    """
    with open(path) as f:
        return json.load(f)


def save_json(data: Any, path: Union[str, Path], indent: int = 2):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        path: Output path
        indent: JSON indentation
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent, default=str)


def load_yaml(path: Union[str, Path]) -> Any:
    """
    Load YAML file.
    
    Args:
        path: Path to YAML file
        
    Returns:
        Loaded data
    """
    with open(path) as f:
        return yaml.safe_load(f)


def save_yaml(data: Any, path: Union[str, Path]):
    """
    Save data to YAML file.
    
    Args:
        data: Data to save
        path: Output path
    """
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def get_timestamp() -> str:
    """
    Get current timestamp string.
    
    Returns:
        Timestamp string
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_size(size_bytes: int) -> str:
    """
    Format byte size to human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def batch_iterator(data: List[Any], batch_size: int):
    """
    Create batches from a list.
    
    Args:
        data: Input data list
        batch_size: Size of each batch
        
    Yields:
        Batches of data
    """
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flatten nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key for recursion
        sep: Separator for keys
        
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten_dict(d: Dict, sep: str = '.') -> Dict:
    """
    Unflatten dictionary.
    
    Args:
        d: Flattened dictionary
        sep: Separator used in keys
        
    Returns:
        Nested dictionary
    """
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


class ProgressTracker:
    """
    Track and report progress of long-running operations.
    """
    
    def __init__(self, total: int, description: str = "Processing"):
        """
        Initialize progress tracker.
        
        Args:
            total: Total number of items
            description: Description of operation
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.logger = logger.get_logger(__name__)
        
    def update(self, n: int = 1):
        """Update progress."""
        self.current += n
        self._report()
        
    def _report(self):
        """Report current progress."""
        percent = (self.current / self.total) * 100
        elapsed = time.time() - self.start_time
        
        if self.current > 0:
            rate = self.current / elapsed
            eta = (self.total - self.current) / rate
        else:
            eta = 0
            
        self.logger.info(
            f"{self.description}: {self.current}/{self.total} "
            f"({percent:.1f}%) - ETA: {eta:.1f}s"
        )
        
    def finish(self):
        """Mark operation as finished."""
        self.current = self.total
        elapsed = time.time() - self.start_time
        self.logger.info(
            f"{self.description} completed in {elapsed:.1f} seconds"
        )


# Validation utilities
def validate_file_exists(path: Union[str, Path]) -> Path:
    """
    Validate that a file exists.
    
    Args:
        path: File path
        
    Returns:
        Path object
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path


def validate_dir_exists(path: Union[str, Path]) -> Path:
    """
    Validate that a directory exists.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
        
    Raises:
        NotADirectoryError: If directory doesn't exist
    """
    path = Path(path)
    if not path.is_dir():
        raise NotADirectoryError(f"Directory not found: {path}")
    return path


# Export main utilities
__all__ = [
    'logger',
    'Logger',
    'set_seed',
    'device_info',
    'memory_usage',
    'timer',
    'ensure_dir',
    'load_json',
    'save_json',
    'load_yaml',
    'save_yaml',
    'get_timestamp',
    'format_size',
    'batch_iterator',
    'flatten_dict',
    'unflatten_dict',
    'ProgressTracker',
    'validate_file_exists',
    'validate_dir_exists',
]