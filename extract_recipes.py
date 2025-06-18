from mcp_server.parsers import RecipeParser
from mcp_server.core.models import RecipeModuleData
from mcp_server.core.database import engine, insert_recipe_module_data
import os

scripts_dir = '/mnt/c/Users/winkk/code/pzmcp/media/scripts'
processed_count = 0

# Process recipes from the recipes/ subdirectory
recipes_dir = os.path.join(scripts_dir, 'recipes')
if os.path.exists(recipes_dir):
    for filename in os.listdir(recipes_dir):
        if filename.endswith('.txt') and filename != 'recipes.txt':
            filepath = os.path.join(recipes_dir, filename)
            print(f'Processing {filename}...')
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                parser = RecipeParser(content)
                raw_data = parser.parse()
                
                if raw_data.get('recipes'):
                    recipe_data = RecipeModuleData(**raw_data)
                    
                    with engine.connect() as connection:
                        insert_recipe_module_data(connection, recipe_data)
                        connection.commit()
                    
                    recipes_count = len(raw_data.get('recipes', []))
                    print(f'  ✓ Inserted {recipes_count} recipes from {filename}')
                    processed_count += recipes_count
                else:
                    print(f'  - No recipes found in {filename}')
                    
            except Exception as e:
                print(f'  ✗ Error processing {filename}: {e}')

print(f'\nTotal recipes processed: {processed_count}')