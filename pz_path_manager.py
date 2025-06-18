import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PZPathManager:
    """Manages Project Zomboid installation paths with priority-based fallback"""
    
    def __init__(self, config_file: str = "pz_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self._cached_path = None
        self._cache_timestamp = None
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_file} not found, using defaults")
            return self._default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "project_zomboid": {
                "script_paths": [
                    {
                        "name": "local_copy",
                        "path": "./media/scripts",
                        "priority": 99,
                        "description": "Local copied scripts (fallback)"
                    }
                ],
                "custom_paths": [],
                "cache_enabled": True,
                "auto_refresh": True,
                "check_interval_hours": 24
            }
        }
    
    def _convert_wsl_path(self, windows_path: str) -> str:
        """Convert Windows path to WSL path if running in WSL"""
        if os.path.exists('/proc/version'):
            try:
                with open('/proc/version', 'r') as f:
                    if 'microsoft' in f.read().lower():
                        # Running in WSL, convert Windows path
                        if windows_path.startswith('C:\\'):
                            return windows_path.replace('C:\\', '/mnt/c/').replace('\\', '/')
                        elif windows_path.startswith('D:\\'):
                            return windows_path.replace('D:\\', '/mnt/d/').replace('\\', '/')
            except:
                pass
        return windows_path
    
    def find_pz_scripts_directory(self) -> Optional[Tuple[str, str]]:
        """
        Find the best available Project Zomboid scripts directory
        Returns: (path, source_name) or None if not found
        """
        # Check cache first
        if self._should_use_cache():
            if self._cached_path and os.path.exists(self._cached_path):
                return self._cached_path, "cached"
        
        # Get all paths sorted by priority
        all_paths = []
        
        # Add configured paths
        for path_config in self.config["project_zomboid"]["script_paths"]:
            all_paths.append(path_config)
        
        # Add custom paths
        for custom_path in self.config["project_zomboid"].get("custom_paths", []):
            all_paths.append(custom_path)
        
        # Sort by priority (lower number = higher priority)
        all_paths.sort(key=lambda x: x.get("priority", 50))
        
        # Check each path
        for path_config in all_paths:
            original_path = path_config["path"]
            
            # Try original path first
            if os.path.exists(original_path):
                logger.info(f"Found PZ scripts at: {original_path} ({path_config['name']})")
                self._update_cache(original_path)
                return original_path, path_config["name"]
            
            # Try WSL-converted path
            wsl_path = self._convert_wsl_path(original_path)
            if wsl_path != original_path and os.path.exists(wsl_path):
                logger.info(f"Found PZ scripts at: {wsl_path} ({path_config['name']} - WSL)")
                self._update_cache(wsl_path)
                return wsl_path, f"{path_config['name']}_wsl"
        
        logger.warning("No Project Zomboid scripts directory found")
        return None, None
    
    def _should_use_cache(self) -> bool:
        """Check if cached path should be used"""
        if not self.config["project_zomboid"].get("cache_enabled", True):
            return False
        
        if not self._cached_path or not self._cache_timestamp:
            return False
        
        if not self.config["project_zomboid"].get("auto_refresh", True):
            return True
        
        # Check if cache is still valid
        check_interval = self.config["project_zomboid"].get("check_interval_hours", 24)
        cache_expiry = self._cache_timestamp + timedelta(hours=check_interval)
        
        return datetime.now() < cache_expiry
    
    def _update_cache(self, path: str):
        """Update cached path"""
        self._cached_path = path
        self._cache_timestamp = datetime.now()
    
    def add_custom_path(self, name: str, path: str, priority: int = 50, description: str = ""):
        """Add a custom path to the configuration"""
        custom_path = {
            "name": name,
            "path": path,
            "priority": priority,
            "description": description or f"Custom path: {name}"
        }
        
        self.config["project_zomboid"]["custom_paths"].append(custom_path)
        self._save_config()
        logger.info(f"Added custom path: {name} -> {path}")
    
    def _save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def list_available_paths(self) -> List[Dict]:
        """List all configured paths with their availability status"""
        paths = []
        
        all_configs = (self.config["project_zomboid"]["script_paths"] + 
                      self.config["project_zomboid"].get("custom_paths", []))
        
        for path_config in all_configs:
            original_path = path_config["path"]
            wsl_path = self._convert_wsl_path(original_path)
            
            status = {
                "name": path_config["name"],
                "path": original_path,
                "wsl_path": wsl_path if wsl_path != original_path else None,
                "priority": path_config.get("priority", 50),
                "description": path_config.get("description", ""),
                "exists": os.path.exists(original_path),
                "wsl_exists": os.path.exists(wsl_path) if wsl_path != original_path else False
            }
            paths.append(status)
        
        return sorted(paths, key=lambda x: x["priority"])
    
    def get_scripts_directory(self) -> str:
        """Get the best available scripts directory, with fallback"""
        path, source = self.find_pz_scripts_directory()
        
        if path:
            logger.info(f"Using PZ scripts from: {path} (source: {source})")
            return path
        
        # Fallback to local copy
        fallback_path = "./media/scripts"
        if os.path.exists(fallback_path):
            logger.warning(f"Using fallback scripts directory: {fallback_path}")
            return fallback_path
        
        raise FileNotFoundError(
            "No Project Zomboid scripts directory found. "
            "Please install the game or copy scripts to ./media/scripts/"
        )

def main():
    """CLI tool for testing path manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Project Zomboid Path Manager")
    parser.add_argument("--list", action="store_true", help="List all configured paths")
    parser.add_argument("--find", action="store_true", help="Find best available path")
    parser.add_argument("--add", nargs=3, metavar=("NAME", "PATH", "PRIORITY"), 
                       help="Add custom path")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    manager = PZPathManager()
    
    if args.list:
        paths = manager.list_available_paths()
        print("\nConfigured Project Zomboid script paths:")
        print("-" * 80)
        for path in paths:
            status = "✓" if path["exists"] or path.get("wsl_exists") else "✗"
            print(f"{status} [{path['priority']:2d}] {path['name']}")
            print(f"    Path: {path['path']}")
            if path.get("wsl_path"):
                wsl_status = "✓" if path.get("wsl_exists") else "✗"
                print(f"    WSL:  {path['wsl_path']} {wsl_status}")
            print(f"    Desc: {path['description']}")
            print()
    
    elif args.find:
        try:
            path = manager.get_scripts_directory()
            print(f"Best available path: {path}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
    
    elif args.add:
        name, path, priority = args.add
        try:
            priority = int(priority)
            manager.add_custom_path(name, path, priority)
            print(f"Added custom path: {name}")
        except ValueError:
            print("Priority must be an integer")

if __name__ == "__main__":
    main()