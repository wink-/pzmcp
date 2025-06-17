from fastapi import FastAPI, HTTPException, Query
from mcp_server.core.database import create_db_and_tables
from mcp_server.core.data_extractor import DataExtractor
from mcp_server.core.script_generator import ScriptGenerator
from mcp_server.core.models import ItemTemplateParams, RecipeTemplateParams # Add other relevant params
from mcp_server.core.search_service import SearchService # Import SearchService
import os

app = FastAPI(title="MCP Server")
script_gen_service = ScriptGenerator()
# Instantiate SearchService with the global engine from database.py
# This ensures it uses the same engine as the rest of the app.
search_service_instance = SearchService(engine=db_engine)

@app.on_event("startup")
def on_startup():
    print("Initializing database...")
    create_db_and_tables()
    print("Database initialization complete.")

@app.get("/")
async def root():
    return {"message": "MCP Server is running"}

@app.get("/extract-vanilla-data")
async def extract_data_endpoint():
    # Construct path relative to this main.py file (mcp_server/main.py)
    # So, ./data/vanilla_scripts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vanilla_scripts_path = os.path.join(current_dir, "data", "vanilla_scripts")
    vanilla_scripts_path = os.path.normpath(vanilla_scripts_path)

    print(f"Extracting data from: {vanilla_scripts_path}")

    # Note: For easier re-testing, you might want to clear relevant tables before extraction.
    # Example (crude, clears ALL tables defined in metadata):
    # from mcp_server.core.database import engine, metadata
    # print("Clearing database tables for fresh extraction...")
    # metadata.drop_all(engine)
    # metadata.create_all(engine) # Recreate them
    # print("Database tables cleared and recreated.")

    extractor = DataExtractor(vanilla_scripts_path)
    # Validate with Pydantic models during extraction, which also triggers DB insertion
    data = extractor.extract_all_data(validate_with_models=True)

    if data:
        response_message = "Data extracted and validated."
        if "items" in data and data["items"]: # Check if item data was processed (data["items"] would be the model_dump)
            # Check if the items list within the ItemModuleData (which is now a dict after model_dump) is not empty
            items_module_data = data.get("items", {})
            if isinstance(items_module_data, dict) and items_module_data.get("items"):
                 response_message += " Item data populated into FTS5-enabled table."
            elif isinstance(items_module_data, list) and items_module_data: # Should not happen if model_dump was used
                 response_message += " Item data (list format) populated into FTS5-enabled table."
            else:
                 response_message += " Data populated into database (items data might be empty or not processed)."

        elif "items" in data and not data["items"]: # items key exists but is empty
            response_message += " Item data was empty or not processed; other data populated into database."
        else: # no "items" key in data
            response_message += " Data populated into database."

        return {
            "status": "success",
            "source": vanilla_scripts_path,
            "message": response_message,
            "extracted_data_summary": {
                 k: f"{len(v.get(k[:-1] if k.endswith('s') else k, [])) if isinstance(v, dict) else (len(v) if isinstance(v, list) else '1 entry (object)')} entries processed"
                 for k, v in data.items()
            }
        }
    else:
        return {"status": "error", "message": "No data extracted or an error occurred during extraction/DB population.", "source": vanilla_scripts_path}


@app.post("/generate/item/{template_name}", response_model=str, tags=["Script Generation"])
async def generate_item_script_endpoint(template_name: str, params: ItemTemplateParams):
    """Generates an item script from a given template and parameters."""
    try:
        # Return as plain text script
        script = script_gen_service.generate_script_from_template(template_name, params)
        return script
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Log the exception details for debugging on the server
        print(f"Error generating item script: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating script: {str(e)}")

@app.post("/generate/recipe/{template_name}", response_model=str, tags=["Script Generation"])
async def generate_recipe_script_endpoint(template_name: str, params: RecipeTemplateParams):
    """Generates a recipe script from a given template and parameters."""
    try:
        script = script_gen_service.generate_script_from_template(template_name, params)
        return script
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error generating recipe script: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating script: {str(e)}")

# To run this FastAPI app (from the project root /app directory):
# uvicorn mcp_server.main:app --reload
# Then access http://localhost:8000/extract-vanilla-data to test.
# Check mcp_data.db with an SQLite browser.
# Test generation endpoints via Swagger UI at http://localhost:8000/docs

@app.get("/search/items", tags=["Search"])
async def search_items_endpoint(q: str = Query(..., min_length=1, description="Search query for items.")):
    """
    Searches for items in the database using FTS5.
    The query string can use FTS5 syntax (e.g., "term1 term2", "term1 NEAR term2", "term*").
    """
    if not q or q.isspace(): # Query validation also handled by min_length in Query
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    try:
        results = search_service_instance.search_items(q)
        return {"query": q, "results_count": len(results), "results": results}
    except Exception as e:
        print(f"Error during item search endpoint for query '{q}': {e}")
        # Consider logging the full exception e for server-side debugging
        raise HTTPException(status_code=500, detail=f"An error occurred during search: {str(e)}")
