#!/usr/bin/env python3
"""
Test script for the Project Zomboid Mod Checker
"""

import os
import tempfile
from pathlib import Path
from mcp_server.core.mod_checker import ModChecker

def create_test_mod():
    """Create a test mod directory with some issues"""
    # Create temporary directory
    test_dir = Path(tempfile.mkdtemp(prefix="pz_test_mod_"))
    
    # Create basic mod structure
    (test_dir / "media" / "scripts").mkdir(parents=True)
    (test_dir / "media" / "textures").mkdir(parents=True)
    
    # Create mod.info
    mod_info = """name=Test Mod
id=TestMod
description=A test mod for validation
author=Test Author
"""
    (test_dir / "mod.info").write_text(mod_info)
    
    # Create a simple item script
    item_script = """module Base
{
    item TestKnife
    {
        Type = Weapon,
        DisplayName = Test Knife,
        Weight = 1.5,
        MaxDamage = 2.0,
        Categories = Blade,
        Icon = Knife,
    }
    
    item OverpoweredSword
    {
        Type = Weapon,
        DisplayName = Overpowered Sword,
        Weight = 0.1,
        MaxDamage = 15.0,
        Categories = Blade,
    }
}
"""
    (test_dir / "media" / "scripts" / "items_weapons.txt").write_text(item_script)
    
    # Create a recipe script with issues
    recipe_script = """module Base
{
    recipe CraftTestKnife
    {
        Result = TestKnife,
        Time = 50000,
        Category = Smithing,
        OnGiveXP = Smithing:10,
    }
}
"""
    (test_dir / "media" / "scripts" / "recipes_test.txt").write_text(recipe_script)
    
    # Create a malformed script
    bad_script = """module Base
{
    item BadItem
    {
        Type = Weapon
        DisplayName = Bad Item,
        Weight = -5.0,
        // Missing closing brace
"""
    (test_dir / "media" / "scripts" / "bad_script.txt").write_text(bad_script)
    
    # Create a large texture file (simulate)
    large_texture = b"fake large texture data" * 100000  # Simulate large file
    (test_dir / "media" / "textures" / "large_texture.png").write_bytes(large_texture)
    
    return test_dir

def main():
    """Test the mod checker"""
    print("🧪 Testing Project Zomboid Mod Checker")
    print("=" * 50)
    
    # Create test mod
    test_mod_path = create_test_mod()
    print(f"Created test mod at: {test_mod_path}")
    
    try:
        # Initialize mod checker
        print("\n📊 Initializing mod checker...")
        checker = ModChecker(vanilla_db_path="mcp_data.db")
        
        # Run mod check
        print(f"\n🔍 Checking mod directory: {test_mod_path}")
        result = checker.check_mod(str(test_mod_path))
        
        # Generate and display report
        print("\n📋 Mod Check Report:")
        print("-" * 50)
        report = checker.generate_report(result, format="text")
        print(report)
        
        # Show auto-fix suggestions
        auto_fixes = checker.get_auto_fix_suggestions(result.issues)
        if auto_fixes:
            print("\n🔧 Auto-Fix Suggestions:")
            print("-" * 30)
            for i, fix in enumerate(auto_fixes, 1):
                print(f"{i}. {fix['issue_title']}")
                print(f"   Fix: {fix['fix_description']}")
                if fix['file_path']:
                    print(f"   File: {fix['file_path']}")
                print()
        
        # Test JSON format
        print("\n📄 JSON Report (first 500 chars):")
        print("-" * 30)
        json_report = checker.generate_report(result, format="json")
        print(json_report[:500] + "..." if len(json_report) > 500 else json_report)
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up test directory
        try:
            import shutil
            shutil.rmtree(test_mod_path)
            print(f"\n🧹 Cleaned up test directory: {test_mod_path}")
        except Exception as e:
            print(f"⚠️  Could not clean up test directory: {e}")

if __name__ == "__main__":
    main()