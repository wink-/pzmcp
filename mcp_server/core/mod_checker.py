"""
Project Zomboid Mod Checker - Comprehensive mod validation and analysis
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3

from ..parsers import ItemParser, RecipeParser, VehicleParser
# Database connection will be handled by direct sqlite3 connection

logger = logging.getLogger(__name__)

class IssueSeverity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    SUGGESTION = "suggestion"

class IssueCategory(Enum):
    STRUCTURE = "structure"
    CONTENT = "content"
    PERFORMANCE = "performance"
    COMPATIBILITY = "compatibility"
    BALANCE = "balance"

@dataclass
class ModIssue:
    """Represents a single issue found in a mod"""
    severity: IssueSeverity
    category: IssueCategory
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'severity': self.severity.value,
            'category': self.category.value,
            'title': self.title,
            'description': self.description,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'suggestion': self.suggestion,
            'auto_fixable': self.auto_fixable
        }

@dataclass
class ModCheckResult:
    """Complete mod validation result"""
    mod_path: str
    mod_name: str
    overall_score: float
    issues: List[ModIssue]
    file_count: int
    script_count: int
    asset_count: int
    total_size_mb: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'mod_path': self.mod_path,
            'mod_name': self.mod_name,
            'overall_score': self.overall_score,
            'issues': [issue.to_dict() for issue in self.issues],
            'file_count': self.file_count,
            'script_count': self.script_count,
            'asset_count': self.asset_count,
            'total_size_mb': self.total_size_mb,
            'issues_by_severity': self._count_by_severity(),
            'issues_by_category': self._count_by_category()
        }
    
    def _count_by_severity(self) -> Dict[str, int]:
        counts = {severity.value: 0 for severity in IssueSeverity}
        for issue in self.issues:
            counts[issue.severity.value] += 1
        return counts
    
    def _count_by_category(self) -> Dict[str, int]:
        counts = {category.value: 0 for category in IssueCategory}
        for issue in self.issues:
            counts[issue.category.value] += 1
        return counts

class ModChecker:
    """Comprehensive Project Zomboid mod validation system"""
    
    def __init__(self, vanilla_db_path: str = "mcp_data.db"):
        self.vanilla_db_path = vanilla_db_path
        self.vanilla_items: Set[str] = set()
        self.vanilla_recipes: Set[str] = set()
        self.vanilla_sounds: Set[str] = set()
        self._load_vanilla_data()
    
    def _load_vanilla_data(self):
        """Load vanilla game data for reference checking"""
        try:
            with sqlite3.connect(self.vanilla_db_path) as conn:
                cursor = conn.cursor()
                
                # Load vanilla items
                cursor.execute("SELECT item_name FROM items_fts")
                self.vanilla_items = {row[0] for row in cursor.fetchall()}
                
                # Load vanilla recipes (if table exists)
                try:
                    cursor.execute("SELECT item_name FROM recipes_fts")
                    self.vanilla_recipes = {row[0] for row in cursor.fetchall()}
                except sqlite3.OperationalError:
                    logger.warning("Recipes table not found, skipping recipe validation")
                
                logger.info(f"Loaded {len(self.vanilla_items)} vanilla items for validation")
                
        except Exception as e:
            logger.error(f"Failed to load vanilla data: {e}")
    
    def check_mod(self, mod_path: str) -> ModCheckResult:
        """
        Perform comprehensive mod validation
        
        Args:
            mod_path: Path to the mod directory
            
        Returns:
            ModCheckResult with all validation findings
        """
        mod_path = Path(mod_path)
        
        if not mod_path.exists():
            return ModCheckResult(
                mod_path=str(mod_path),
                mod_name="Unknown",
                overall_score=0.0,
                issues=[ModIssue(
                    severity=IssueSeverity.CRITICAL,
                    category=IssueCategory.STRUCTURE,
                    title="Mod directory not found",
                    description=f"The specified mod directory '{mod_path}' does not exist"
                )],
                file_count=0,
                script_count=0,
                asset_count=0,
                total_size_mb=0.0
            )
        
        # Initialize tracking variables
        issues: List[ModIssue] = []
        mod_name = mod_path.name
        
        # Get mod statistics
        file_count, script_count, asset_count, total_size = self._get_mod_stats(mod_path)
        
        # Run all validation checks
        issues.extend(self._check_structure(mod_path))
        issues.extend(self._check_mod_info(mod_path))
        issues.extend(self._check_scripts(mod_path))
        issues.extend(self._check_assets(mod_path))
        issues.extend(self._check_performance(mod_path, total_size))
        
        # Calculate overall score
        overall_score = self._calculate_score(issues, file_count)
        
        # Try to get mod name from mod.info
        mod_info_path = mod_path / "mod.info"
        if mod_info_path.exists():
            try:
                mod_name = self._parse_mod_info(mod_info_path).get('name', mod_name)
            except:
                pass
        
        return ModCheckResult(
            mod_path=str(mod_path),
            mod_name=mod_name,
            overall_score=overall_score,
            issues=issues,
            file_count=file_count,
            script_count=script_count,
            asset_count=asset_count,
            total_size_mb=total_size / (1024 * 1024)
        )
    
    def _get_mod_stats(self, mod_path: Path) -> Tuple[int, int, int, int]:
        """Get basic mod statistics"""
        file_count = 0
        script_count = 0
        asset_count = 0
        total_size = 0
        
        script_extensions = {'.txt'}
        asset_extensions = {'.png', '.jpg', '.jpeg', '.wav', '.ogg', '.mp3'}
        
        for file_path in mod_path.rglob('*'):
            if file_path.is_file():
                file_count += 1
                total_size += file_path.stat().st_size
                
                if file_path.suffix.lower() in script_extensions:
                    script_count += 1
                elif file_path.suffix.lower() in asset_extensions:
                    asset_count += 1
        
        return file_count, script_count, asset_count, total_size
    
    def _check_structure(self, mod_path: Path) -> List[ModIssue]:
        """Check mod directory structure"""
        issues = []
        
        # Required files/directories
        required_items = [
            ('mod.info', 'file'),
            ('media', 'directory'),
            ('media/scripts', 'directory')
        ]
        
        for item_name, item_type in required_items:
            item_path = mod_path / item_name
            if not item_path.exists():
                issues.append(ModIssue(
                    severity=IssueSeverity.CRITICAL,
                    category=IssueCategory.STRUCTURE,
                    title=f"Missing {item_type}: {item_name}",
                    description=f"Required {item_type} '{item_name}' not found in mod directory",
                    suggestion=f"Create the {item_type} '{item_name}' in your mod directory"
                ))
            elif item_type == 'directory' and not item_path.is_dir():
                issues.append(ModIssue(
                    severity=IssueSeverity.CRITICAL,
                    category=IssueCategory.STRUCTURE,
                    title=f"Invalid {item_type}: {item_name}",
                    description=f"'{item_name}' exists but is not a directory",
                    suggestion=f"Remove the file and create a directory named '{item_name}'"
                ))
            elif item_type == 'file' and not item_path.is_file():
                issues.append(ModIssue(
                    severity=IssueSeverity.CRITICAL,
                    category=IssueCategory.STRUCTURE,
                    title=f"Invalid {item_type}: {item_name}",
                    description=f"'{item_name}' exists but is not a file",
                    suggestion=f"Remove the directory and create a file named '{item_name}'"
                ))
        
        # Check for common optional directories
        optional_dirs = ['media/textures', 'media/sounds', 'media/lua']
        for dir_name in optional_dirs:
            dir_path = mod_path / dir_name
            if dir_path.exists() and not dir_path.is_dir():
                issues.append(ModIssue(
                    severity=IssueSeverity.WARNING,
                    category=IssueCategory.STRUCTURE,
                    title=f"Invalid directory: {dir_name}",
                    description=f"'{dir_name}' exists but is not a directory",
                    suggestion=f"Remove the file and create a directory if you need '{dir_name}'"
                ))
        
        # Check for suspicious files in root
        root_files = [f for f in mod_path.iterdir() if f.is_file()]
        allowed_root_files = {'mod.info', 'poster.png', 'preview.png', 'README.md', 'README.txt'}
        
        for file_path in root_files:
            if file_path.name not in allowed_root_files:
                issues.append(ModIssue(
                    severity=IssueSeverity.INFO,
                    category=IssueCategory.STRUCTURE,
                    title=f"Unexpected root file: {file_path.name}",
                    description=f"File '{file_path.name}' found in mod root - consider organizing in subdirectories",
                    suggestion="Move non-essential files to appropriate subdirectories"
                ))
        
        return issues
    
    def _check_mod_info(self, mod_path: Path) -> List[ModIssue]:
        """Check mod.info file"""
        issues = []
        mod_info_path = mod_path / "mod.info"
        
        if not mod_info_path.exists():
            return issues  # Already handled in structure check
        
        try:
            mod_info = self._parse_mod_info(mod_info_path)
            
            # Required fields
            required_fields = ['name', 'id', 'description']
            for field in required_fields:
                if field not in mod_info or not mod_info[field].strip():
                    issues.append(ModIssue(
                        severity=IssueSeverity.CRITICAL,
                        category=IssueCategory.STRUCTURE,
                        title=f"Missing mod.info field: {field}",
                        description=f"Required field '{field}' is missing or empty in mod.info",
                        file_path="mod.info",
                        suggestion=f"Add a {field} field to your mod.info file"
                    ))
            
            # Validate mod ID
            if 'id' in mod_info:
                mod_id = mod_info['id']
                if not re.match(r'^[a-zA-Z0-9_-]+$', mod_id):
                    issues.append(ModIssue(
                        severity=IssueSeverity.WARNING,
                        category=IssueCategory.STRUCTURE,
                        title="Invalid mod ID format",
                        description="Mod ID contains invalid characters (use only letters, numbers, underscore, hyphen)",
                        file_path="mod.info",
                        suggestion="Use only alphanumeric characters, underscores, and hyphens in mod ID"
                    ))
            
            # Check for recommended fields
            recommended_fields = ['author', 'url', 'poster']
            for field in recommended_fields:
                if field not in mod_info or not mod_info[field].strip():
                    issues.append(ModIssue(
                        severity=IssueSeverity.INFO,
                        category=IssueCategory.STRUCTURE,
                        title=f"Missing recommended field: {field}",
                        description=f"Field '{field}' is recommended for better mod presentation",
                        file_path="mod.info",
                        suggestion=f"Consider adding a {field} field to your mod.info"
                    ))
            
        except Exception as e:
            issues.append(ModIssue(
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.STRUCTURE,
                title="Cannot parse mod.info",
                description=f"Failed to parse mod.info file: {str(e)}",
                file_path="mod.info",
                suggestion="Check mod.info syntax - each line should be 'field=value'"
            ))
        
        return issues
    
    def _parse_mod_info(self, mod_info_path: Path) -> Dict[str, str]:
        """Parse mod.info file into dictionary"""
        mod_info = {}
        
        with open(mod_info_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if '=' not in line:
                    continue
                
                key, value = line.split('=', 1)
                mod_info[key.strip()] = value.strip()
        
        return mod_info
    
    def _check_scripts(self, mod_path: Path) -> List[ModIssue]:
        """Check all script files for syntax and content issues"""
        issues = []
        scripts_path = mod_path / "media" / "scripts"
        
        if not scripts_path.exists():
            return issues
        
        # Find all .txt files in scripts directory
        script_files = list(scripts_path.rglob("*.txt"))
        
        # Track item IDs to detect duplicates
        all_item_ids = {}
        all_recipe_names = {}
        
        for script_file in script_files:
            rel_path = script_file.relative_to(mod_path)
            issues.extend(self._check_single_script(script_file, rel_path, all_item_ids, all_recipe_names))
        
        # Check for duplicate IDs across files
        for item_id, files in all_item_ids.items():
            if len(files) > 1:
                issues.append(ModIssue(
                    severity=IssueSeverity.CRITICAL,
                    category=IssueCategory.CONTENT,
                    title=f"Duplicate item ID: {item_id}",
                    description=f"Item ID '{item_id}' is defined in multiple files: {', '.join(files)}",
                    suggestion="Each item must have a unique ID - rename one of the items"
                ))
        
        for recipe_name, files in all_recipe_names.items():
            if len(files) > 1:
                issues.append(ModIssue(
                    severity=IssueSeverity.WARNING,
                    category=IssueCategory.CONTENT,
                    title=f"Duplicate recipe name: {recipe_name}",
                    description=f"Recipe '{recipe_name}' is defined in multiple files: {', '.join(files)}",
                    suggestion="Consider using unique recipe names to avoid conflicts"
                ))
        
        return issues
    
    def _check_single_script(self, script_file: Path, rel_path: Path, 
                           all_item_ids: Dict, all_recipe_names: Dict) -> List[ModIssue]:
        """Check a single script file"""
        issues = []
        
        try:
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse with appropriate parser
            if 'item' in script_file.name.lower():
                issues.extend(self._check_item_script(content, rel_path, all_item_ids))
            elif 'recipe' in script_file.name.lower():
                issues.extend(self._check_recipe_script(content, rel_path, all_recipe_names))
            elif 'vehicle' in script_file.name.lower():
                issues.extend(self._check_vehicle_script(content, rel_path))
            else:
                # Generic script check
                issues.extend(self._check_generic_script(content, rel_path))
                
        except UnicodeDecodeError:
            issues.append(ModIssue(
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.CONTENT,
                title="File encoding error",
                description="Cannot read script file - check file encoding",
                file_path=str(rel_path),
                suggestion="Save the file with UTF-8 encoding"
            ))
        except Exception as e:
            issues.append(ModIssue(
                severity=IssueSeverity.WARNING,
                category=IssueCategory.CONTENT,
                title="Script parsing error",
                description=f"Error reading script file: {str(e)}",
                file_path=str(rel_path)
            ))
        
        return issues
    
    def _check_item_script(self, content: str, rel_path: Path, all_item_ids: Dict) -> List[ModIssue]:
        """Check item script content"""
        issues = []
        
        try:
            parser = ItemParser(content)
            parsed_data = parser.parse()
            
            # Check for items and validate
            items = parsed_data.get('items', [])
            for item in items:
                item_name = item.get('itemName')
                if item_name:
                    # Track for duplicate detection
                    if item_name not in all_item_ids:
                        all_item_ids[item_name] = []
                    all_item_ids[item_name].append(str(rel_path))
                    
                    # Check if item references vanilla items improperly
                    if item_name in self.vanilla_items:
                        issues.append(ModIssue(
                            severity=IssueSeverity.WARNING,
                            category=IssueCategory.COMPATIBILITY,
                            title=f"Overrides vanilla item: {item_name}",
                            description=f"Item '{item_name}' has the same name as a vanilla item",
                            file_path=str(rel_path),
                            suggestion="Consider using a unique name or prefix for custom items"
                        ))
                    
                    # Validate item properties
                    issues.extend(self._validate_item_properties(item, rel_path))
        
        except Exception as e:
            issues.append(ModIssue(
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.CONTENT,
                title="Item script syntax error",
                description=f"Cannot parse item script: {str(e)}",
                file_path=str(rel_path),
                suggestion="Check script syntax for missing braces, quotes, or semicolons"
            ))
        
        return issues
    
    def _validate_item_properties(self, item: Dict, rel_path: Path) -> List[ModIssue]:
        """Validate individual item properties for balance and correctness"""
        issues = []
        item_name = item.get('itemName', 'Unknown')
        
        # Check weapon balance
        if item.get('Type') == 'Weapon':
            max_damage = item.get('MaxDamage')
            if max_damage:
                try:
                    damage_value = float(max_damage)
                    if damage_value > 10.0:
                        issues.append(ModIssue(
                            severity=IssueSeverity.WARNING,
                            category=IssueCategory.BALANCE,
                            title=f"Overpowered weapon: {item_name}",
                            description=f"Weapon damage {damage_value} is very high (vanilla max ~3.0)",
                            file_path=str(rel_path),
                            suggestion="Consider reducing damage to maintain game balance"
                        ))
                    elif damage_value <= 0:
                        issues.append(ModIssue(
                            severity=IssueSeverity.WARNING,
                            category=IssueCategory.BALANCE,
                            title=f"Invalid weapon damage: {item_name}",
                            description=f"Weapon damage {damage_value} is zero or negative",
                            file_path=str(rel_path),
                            suggestion="Set weapon damage to a positive value"
                        ))
                except ValueError:
                    issues.append(ModIssue(
                        severity=IssueSeverity.WARNING,
                        category=IssueCategory.CONTENT,
                        title=f"Invalid damage value: {item_name}",
                        description=f"MaxDamage '{max_damage}' is not a valid number",
                        file_path=str(rel_path),
                        suggestion="Use a decimal number for MaxDamage (e.g., 1.5)"
                    ))
        
        # Check weight
        weight = item.get('Weight')
        if weight:
            try:
                weight_value = float(weight)
                if weight_value > 50.0:
                    issues.append(ModIssue(
                        severity=IssueSeverity.WARNING,
                        category=IssueCategory.BALANCE,
                        title=f"Very heavy item: {item_name}",
                        description=f"Item weight {weight_value} is very high",
                        file_path=str(rel_path),
                        suggestion="Consider if this weight is intentional and balanced"
                    ))
                elif weight_value < 0:
                    issues.append(ModIssue(
                        severity=IssueSeverity.WARNING,
                        category=IssueCategory.CONTENT,
                        title=f"Invalid weight: {item_name}",
                        description=f"Item weight {weight_value} is negative",
                        file_path=str(rel_path),
                        suggestion="Set weight to a positive value"
                    ))
            except ValueError:
                issues.append(ModIssue(
                    severity=IssueSeverity.WARNING,
                    category=IssueCategory.CONTENT,
                    title=f"Invalid weight value: {item_name}",
                    description=f"Weight '{weight}' is not a valid number",
                    file_path=str(rel_path),
                    suggestion="Use a decimal number for Weight (e.g., 1.5)"
                ))
        
        return issues
    
    def _check_recipe_script(self, content: str, rel_path: Path, all_recipe_names: Dict) -> List[ModIssue]:
        """Check recipe script content"""
        issues = []
        
        try:
            parser = RecipeParser(content)
            parsed_data = parser.parse()
            
            recipes = parsed_data.get('recipes', [])
            for recipe in recipes:
                recipe_name = recipe.get('recipeName')
                if recipe_name:
                    # Track for duplicate detection
                    if recipe_name not in all_recipe_names:
                        all_recipe_names[recipe_name] = []
                    all_recipe_names[recipe_name].append(str(rel_path))
                    
                    # Validate recipe properties
                    issues.extend(self._validate_recipe_properties(recipe, rel_path))
        
        except Exception as e:
            issues.append(ModIssue(
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.CONTENT,
                title="Recipe script syntax error",
                description=f"Cannot parse recipe script: {str(e)}",
                file_path=str(rel_path),
                suggestion="Check script syntax for missing braces, quotes, or semicolons"
            ))
        
        return issues
    
    def _validate_recipe_properties(self, recipe: Dict, rel_path: Path) -> List[ModIssue]:
        """Validate recipe properties"""
        issues = []
        recipe_name = recipe.get('recipeName', 'Unknown')
        
        # Check for reasonable time values
        time_value = recipe.get('Time')
        if time_value:
            try:
                time_int = int(time_value)
                if time_int > 10000:
                    issues.append(ModIssue(
                        severity=IssueSeverity.WARNING,
                        category=IssueCategory.BALANCE,
                        title=f"Very long recipe time: {recipe_name}",
                        description=f"Recipe time {time_int} is very long (>10 seconds game time)",
                        file_path=str(rel_path),
                        suggestion="Consider if this crafting time is balanced"
                    ))
                elif time_int <= 0:
                    issues.append(ModIssue(
                        severity=IssueSeverity.WARNING,
                        category=IssueCategory.CONTENT,
                        title=f"Invalid recipe time: {recipe_name}",
                        description=f"Recipe time {time_int} is zero or negative",
                        file_path=str(rel_path),
                        suggestion="Set recipe time to a positive value"
                    ))
            except ValueError:
                issues.append(ModIssue(
                    severity=IssueSeverity.WARNING,
                    category=IssueCategory.CONTENT,
                    title=f"Invalid time value: {recipe_name}",
                    description=f"Time '{time_value}' is not a valid number",
                    file_path=str(rel_path),
                    suggestion="Use an integer for Time (e.g., 100)"
                ))
        
        return issues
    
    def _check_vehicle_script(self, content: str, rel_path: Path) -> List[ModIssue]:
        """Check vehicle script content"""
        issues = []
        
        try:
            parser = VehicleParser(content)
            parsed_data = parser.parse()
            # Add vehicle-specific validation here
            
        except Exception as e:
            issues.append(ModIssue(
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.CONTENT,
                title="Vehicle script syntax error",
                description=f"Cannot parse vehicle script: {str(e)}",
                file_path=str(rel_path),
                suggestion="Check script syntax for missing braces, quotes, or semicolons"
            ))
        
        return issues
    
    def _check_generic_script(self, content: str, rel_path: Path) -> List[ModIssue]:
        """Check generic script file for basic syntax"""
        issues = []
        
        # Basic syntax checks
        brace_count = content.count('{') - content.count('}')
        if brace_count != 0:
            issues.append(ModIssue(
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.CONTENT,
                title="Mismatched braces",
                description=f"Script has {abs(brace_count)} unmatched {'opening' if brace_count > 0 else 'closing'} braces",
                file_path=str(rel_path),
                suggestion="Check that every opening brace { has a matching closing brace }"
            ))
        
        return issues
    
    def _check_assets(self, mod_path: Path) -> List[ModIssue]:
        """Check mod assets (textures, sounds, etc.)"""
        issues = []
        
        # Check textures
        textures_path = mod_path / "media" / "textures"
        if textures_path.exists():
            for texture_file in textures_path.rglob("*"):
                if texture_file.is_file():
                    issues.extend(self._check_texture_file(texture_file, mod_path))
        
        # Check sounds
        sounds_path = mod_path / "media" / "sounds"
        if sounds_path.exists():
            for sound_file in sounds_path.rglob("*"):
                if sound_file.is_file():
                    issues.extend(self._check_sound_file(sound_file, mod_path))
        
        return issues
    
    def _check_texture_file(self, texture_file: Path, mod_path: Path) -> List[ModIssue]:
        """Check individual texture file"""
        issues = []
        rel_path = texture_file.relative_to(mod_path)
        
        # Check file size
        file_size = texture_file.stat().st_size
        if file_size > 2 * 1024 * 1024:  # 2MB
            issues.append(ModIssue(
                severity=IssueSeverity.WARNING,
                category=IssueCategory.PERFORMANCE,
                title=f"Large texture file: {texture_file.name}",
                description=f"Texture file is {file_size / (1024*1024):.1f}MB (large textures can impact performance)",
                file_path=str(rel_path),
                suggestion="Consider compressing or resizing the texture"
            ))
        
        # Check file format
        if texture_file.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
            issues.append(ModIssue(
                severity=IssueSeverity.WARNING,
                category=IssueCategory.COMPATIBILITY,
                title=f"Unsupported texture format: {texture_file.name}",
                description=f"File format '{texture_file.suffix}' may not be supported",
                file_path=str(rel_path),
                suggestion="Use PNG or JPG format for textures"
            ))
        
        return issues
    
    def _check_sound_file(self, sound_file: Path, mod_path: Path) -> List[ModIssue]:
        """Check individual sound file"""
        issues = []
        rel_path = sound_file.relative_to(mod_path)
        
        # Check file size
        file_size = sound_file.stat().st_size
        if file_size > 5 * 1024 * 1024:  # 5MB
            issues.append(ModIssue(
                severity=IssueSeverity.WARNING,
                category=IssueCategory.PERFORMANCE,
                title=f"Large sound file: {sound_file.name}",
                description=f"Sound file is {file_size / (1024*1024):.1f}MB (large sounds can impact performance)",
                file_path=str(rel_path),
                suggestion="Consider compressing the audio file"
            ))
        
        # Check file format
        if sound_file.suffix.lower() not in ['.wav', '.ogg', '.mp3']:
            issues.append(ModIssue(
                severity=IssueSeverity.WARNING,
                category=IssueCategory.COMPATIBILITY,
                title=f"Unsupported sound format: {sound_file.name}",
                description=f"File format '{sound_file.suffix}' may not be supported",
                file_path=str(rel_path),
                suggestion="Use WAV, OGG, or MP3 format for sounds"
            ))
        
        return issues
    
    def _check_performance(self, mod_path: Path, total_size: int) -> List[ModIssue]:
        """Check for potential performance issues"""
        issues = []
        
        # Check total mod size
        size_mb = total_size / (1024 * 1024)
        if size_mb > 100:
            issues.append(ModIssue(
                severity=IssueSeverity.WARNING,
                category=IssueCategory.PERFORMANCE,
                title="Large mod size",
                description=f"Mod is {size_mb:.1f}MB (large mods can slow game loading)",
                suggestion="Consider optimizing assets or splitting into multiple mods"
            ))
        
        # Check number of script files
        scripts_path = mod_path / "media" / "scripts"
        if scripts_path.exists():
            script_count = len(list(scripts_path.rglob("*.txt")))
            if script_count > 50:
                issues.append(ModIssue(
                    severity=IssueSeverity.INFO,
                    category=IssueCategory.PERFORMANCE,
                    title="Many script files",
                    description=f"Mod has {script_count} script files (many files can slow loading)",
                    suggestion="Consider consolidating related scripts into fewer files"
                ))
        
        return issues
    
    def _calculate_score(self, issues: List[ModIssue], file_count: int) -> float:
        """Calculate overall mod quality score (0-10)"""
        if file_count == 0:
            return 0.0
        
        # Score starts at 10 and is reduced based on issues
        score = 10.0
        
        for issue in issues:
            if issue.severity == IssueSeverity.CRITICAL:
                score -= 2.0
            elif issue.severity == IssueSeverity.WARNING:
                score -= 0.5
            elif issue.severity == IssueSeverity.INFO:
                score -= 0.1
        
        # Bonus points for having many files (indicates completeness)
        if file_count > 10:
            score += 0.5
        if file_count > 50:
            score += 0.5
        
        return max(0.0, min(10.0, score))
    
    def get_auto_fix_suggestions(self, issues: List[ModIssue]) -> List[Dict[str, Any]]:
        """Generate auto-fix suggestions for fixable issues"""
        auto_fixes = []
        
        for issue in issues:
            if issue.auto_fixable:
                auto_fixes.append({
                    'issue_title': issue.title,
                    'file_path': issue.file_path,
                    'fix_description': issue.suggestion,
                    'fix_type': 'automatic'
                })
        
        return auto_fixes
    
    def generate_report(self, result: ModCheckResult, format: str = 'text') -> str:
        """Generate a comprehensive mod check report"""
        if format == 'json':
            return json.dumps(result.to_dict(), indent=2)
        
        # Text format report
        report = []
        report.append(f"=== Project Zomboid Mod Check Report ===")
        report.append(f"Mod: {result.mod_name}")
        report.append(f"Path: {result.mod_path}")
        report.append(f"Overall Score: {result.overall_score:.1f}/10.0")
        report.append("")
        
        report.append(f"📊 Statistics:")
        report.append(f"  Files: {result.file_count}")
        report.append(f"  Scripts: {result.script_count}")
        report.append(f"  Assets: {result.asset_count}")
        report.append(f"  Total Size: {result.total_size_mb:.1f} MB")
        report.append("")
        
        if result.issues:
            report.append(f"🔍 Issues Found ({len(result.issues)}):")
            
            # Group by severity
            issues_by_severity = result._count_by_severity()
            for severity in ['critical', 'warning', 'info', 'suggestion']:
                count = issues_by_severity.get(severity, 0)
                if count > 0:
                    icon = {'critical': '❌', 'warning': '⚠️', 'info': 'ℹ️', 'suggestion': '💡'}[severity]
                    report.append(f"  {icon} {severity.title()}: {count}")
            
            report.append("")
            
            # List all issues
            for i, issue in enumerate(result.issues, 1):
                icon = {'critical': '❌', 'warning': '⚠️', 'info': 'ℹ️', 'suggestion': '💡'}[issue.severity.value]
                report.append(f"{i:2d}. {icon} {issue.title}")
                report.append(f"     {issue.description}")
                if issue.file_path:
                    location = f"File: {issue.file_path}"
                    if issue.line_number:
                        location += f", Line: {issue.line_number}"
                    report.append(f"     {location}")
                if issue.suggestion:
                    report.append(f"     💡 {issue.suggestion}")
                report.append("")
        else:
            report.append("✅ No issues found!")
        
        return "\n".join(report)