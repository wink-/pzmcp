from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, JSON, insert, DDL, event
from sqlalchemy.engine import Connection
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement

# Pydantic models for type hinting and data structure
from .models import ItemModuleData, RecipeModuleData, VehicleModuleData

DATABASE_URL = "sqlite:///./mcp_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()


# --- FTS5 Helper Class and Compiler ---
class CreateFTS5Table(Executable, ClauseElement):
    def __init__(self, table_name, columns, options=None):
        self.table_name = table_name
        self.columns = columns  # List of column names for FTS
        self.options = options or {} # e.g., {'tokenize': 'porter'}

@compiles(CreateFTS5Table)
def _compile_create_fts5_table(element, compiler, **kw):
    columns_def = ", ".join(element.columns)
    options_def = ""
    if element.options:
        options_def = ", " + ", ".join(f"{k} = {v}" if not isinstance(v, str) else f"{k} = '{v}'"
                                      for k, v in element.options.items())
    # Using 'UNINDEXED' for columns we don't want to search directly but want in the table.
    # The columns listed in the FTS5 definition are the columns of the virtual table.
    # Those not marked UNINDEXED are part of the full-text index.
    # `content=` option can be used if the FTS table is an external content table, but not here.
    # `columnsize=` can be 0 for FTS5 to not store the text, if content is elsewhere. Here we store.
    return f"CREATE VIRTUAL TABLE {element.table_name} USING fts5(" \
           f"id UNINDEXED, " \
           f"module_name, " \
           f"item_name, " \
           f"display_name, " \
           f"properties_json UNINDEXED{options_def})"
           # Columns to be indexed by FTS5 are those not marked UNINDEXED.


# --- Table Definitions ---
# This 'items_table' is now effectively a definition for SQLAlchemy ORM/Core to be aware of the structure.
# The actual FTS table is created by the DDL.
# For data insertion, we will target 'items_fts_table' directly.
# The original 'items_table' definition can be removed or repurposed if we need a non-FTS version.
# For simplicity, we'll define items_fts_table for SQLAlchemy's awareness and use it for inserts.

items_fts_table = Table(
    "items_fts", # This is the FTS5 virtual table name
    metadata,
    Column("id", Integer, primary_key=True), # FTS5 rowid, can be aliased
    Column("module_name", String, nullable=True),
    Column("item_name", String), # 'name' from ParsedItem
    Column("display_name", String, nullable=True), # Extracted from properties
    Column("properties_json", JSON) # Stores the full properties dict
)

# Other tables remain as before
recipes_table = Table(
    "recipes",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("module_name", String, nullable=True),
    Column("name", String, index=True),
    Column("inputs", JSON),       # Stores List[RecipeInputItem]
    Column("properties", JSON),   # Stores Dict[str, Any]
    Column("result", JSON)        # Stores RecipeResult
)

vehicles_table = Table(
    "vehicles",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("module_name", String, nullable=True),
    Column("name", String, index=True),
    Column("inherits", String, nullable=True),
    Column("properties", JSON),   # Stores Dict[str, Any] for vehicle's direct properties
    Column("model_data", JSON, nullable=True),    # Stores VehicleModel properties
    Column("skins_data", JSON, nullable=True),    # Stores List[VehicleSkin properties]
    Column("sound_data", JSON, nullable=True),    # Stores VehicleSound properties
    Column("parts_data", JSON, nullable=True)     # Stores List[VehiclePart]
)

# Could add templates_table here if it's distinct enough from vehicles,
# or if templates are just a type of vehicle data.
# For now, assuming templates might be stored similarly or in a separate table if needed.
# The request implies they are parsed, but not explicitly how they are stored vs vehicles.
# Let's assume for now templates might be handled by a similar table or a type field in vehicles_table.
# For simplicity, I'll omit a separate templates_table unless it becomes clear it's needed.
# We can store templates in the vehicles_table with a 'type' field if necessary, or add templates_table later.

def create_db_and_tables():
    """Creates the database and all defined tables."""
    print(f"Creating database and tables at {DATABASE_URL}")

    with engine.connect() as conn:
        # Explicitly drop the items_fts table (regular or virtual) to ensure clean setup
        conn.execute(DDL("DROP TABLE IF EXISTS items_fts"))
        conn.commit()

    # Create non-FTS tables (recipes, vehicles) using metadata.create_all
    # Filter out items_fts_table from direct creation by metadata.create_all
    tables_to_create_directly = [
        table for table_name, table in metadata.tables.items() if table_name != "items_fts"
    ]
    if tables_to_create_directly:
        # If you had other tables, pass them: metadata.create_all(engine, tables=tables_to_create_directly)
        # For now, this might be empty if only items_fts, recipes, vehicles were defined in metadata
        # and items_fts is excluded.
        # Let's be more explicit: create specific tables.
        recipes_table.create(engine, checkfirst=True)
        vehicles_table.create(engine, checkfirst=True)
        # Any other regular tables would be created here.
        print("Regular tables (recipes, vehicles) created (if they didn't exist).")
    else:
        print("No other regular tables to create besides items_fts.")


    # Explicitly create the FTS5 virtual table
    with engine.connect() as connection:
        # The CreateFTS5Table helper compiles to the "CREATE VIRTUAL TABLE..." DDL string.
        # The columns specified in CreateFTS5Table are those to be indexed by FTS5.
        # The actual schema of the FTS5 table (all its columns) is defined within _compile_create_fts5_table.
        stmt = CreateFTS5Table("items_fts", ["module_name", "item_name", "display_name"])
        connection.execute(stmt)
        connection.commit()

    print("FTS5 virtual table 'items_fts' created (if it didn't exist).")
    print("Database schema initialization complete.")

# --- Data Insertion Functions ---

def insert_item_module_data(conn: Connection, module_data: ItemModuleData):
    """Inserts item data from a ItemModuleData object into the items_fts_table."""
    if module_data.items:
        for item_obj in module_data.items:
            # Extract DisplayName, default to item_name if not found
            display_name = item_obj.properties.get("DisplayName", item_obj.name)
            if not display_name: # Further fallback if DisplayName was empty string
                display_name = item_obj.name

            stmt = insert(items_fts_table).values(
                # id is handled by FTS5 rowid automatically if not specified,
                # but for consistency or if we manage IDs elsewhere, it can be included.
                # For now, let's let FTS5 handle its rowid.
                # If items_fts_table has an explicit PK 'id', we might need to provide it or ensure it's auto.
                # The FTS5 table defined via CreateFTS5Table has 'id UNINDEXED'.
                # We don't need to insert 'id' if it's meant to be the FTS rowid.
                # However, if we want our own auto-incrementing PK for items_fts_table for SQLAlchemy's sake,
                # that's a different setup.
                # The current items_fts_table Table object has 'id' as PK.
                # FTS5 virtual tables have a built-in 'rowid'. We can alias it or use it.
                # For simplicity with SQLAlchemy Table object, let's assume we are not inserting 'id' and it's rowid.
                # Or, if 'id' is a regular column in FTS (even if UNINDEXED), it needs a value or default.
                # Let's remove 'id' from values() for now and rely on FTS rowid.
                # The 'id' in items_fts_table can serve as an alias for rowid if defined as INTEGER PRIMARY KEY.
                # In FTS5, any INTEGER PRIMARY KEY column becomes an alias for the rowid.
                module_name=module_data.module,
                item_name=item_obj.name,
                display_name=display_name,
                properties_json=item_obj.properties
            )
            conn.execute(stmt)
        print(f"Inserted {len(module_data.items)} items into FTS table from module '{module_data.module or 'Unknown'}'.")

def insert_recipe_module_data(conn: Connection, module_data: RecipeModuleData):
    """Inserts recipe data from a RecipeModuleData object into the recipes_table."""
    if module_data.recipes:
        for recipe_obj in module_data.recipes:
            # For complex fields like inputs (list of Pydantic models) or result (Pydantic model),
            # convert them to dicts for JSON storage. Pydantic's .model_dump() is good here.
            inputs_data = [input_item.model_dump() for input_item in recipe_obj.inputs]
            result_data = recipe_obj.result.model_dump() if recipe_obj.result else None

            stmt = insert(recipes_table).values(
                module_name=module_data.module,
                name=recipe_obj.name,
                inputs=inputs_data,
                properties=recipe_obj.properties, # Already a dict
                result=result_data
            )
            conn.execute(stmt)
        print(f"Inserted {len(module_data.recipes)} recipes from module '{module_data.module or 'Unknown'}'.")

def insert_vehicle_module_data(conn: Connection, module_data: VehicleModuleData):
    """Inserts vehicle data from a VehicleModuleData object into the vehicles_table."""
    if module_data.vehicles:
        for vehicle_obj in module_data.vehicles:
            # Similar to recipes, convert complex nested Pydantic models/lists of models to dict/list of dicts
            model_data_dict = vehicle_obj.model # Parser returns dict
            skins_data_list = vehicle_obj.skins # Parser returns list of dicts
            sound_data_dict = vehicle_obj.sound # Parser returns dict
            parts_data_list = [part.model_dump() for part in vehicle_obj.parts]

            stmt = insert(vehicles_table).values(
                module_name=module_data.module,
                name=vehicle_obj.name,
                inherits=vehicle_obj.inherits,
                properties=vehicle_obj.properties, # Already a dict
                model_data=model_data_dict,
                skins_data=skins_data_list,
                sound_data=sound_data_dict,
                parts_data=parts_data_list
            )
            conn.execute(stmt)
        print(f"Inserted {len(module_data.vehicles)} vehicles from module '{module_data.module or 'Unknown'}'.")

    if module_data.templates:
        # Example: Storing templates in the same vehicles_table with a flag or different handling.
        # Or, if you had a separate templates_table, you would call its insert function.
        # For now, just printing a message.
        print(f"Found {len(module_data.templates)} templates in module '{module_data.module or 'Unknown'}' (not inserted in this example).")


if __name__ == "__main__":
    create_db_and_tables()
    print("Database schema initialized directly via database.py")

    # Example of direct insertion (for testing database.py independently)
    # from .models import ParsedItem
    # test_item_data = ItemModuleData(
    #     module="TestItems",
    #     items=[
    #         ParsedItem(name="TestItem1", properties={"Type": "Test", "Weight": 1.0}),
    #         ParsedItem(name="TestItem2", properties={"Type": "Another", "DisplayName": "My Test Item"})
    #     ]
    # )
    # with engine.connect() as connection:
    #     insert_item_module_data(connection, test_item_data)
    #     connection.commit()
    #     print("Test item data inserted directly.")
