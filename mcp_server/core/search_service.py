from typing import List, Dict, Any
from sqlalchemy import text, Engine # Import Engine
from mcp_server.core.database import engine as global_engine # Default engine

class SearchService:
    def __init__(self, engine: Engine = None):
        self.engine = engine or global_engine

    def search_items(self, query: str) -> List[Dict[str, Any]]:
        """
        Performs an FTS5 search on the items_fts_table.
        Returns a list of items matching the query, ordered by relevance (rank).
        """
        if not query or query.isspace():
            return []

        # The FTS5 query needs to be formatted correctly.
        # For user input, it's common to append '*' for prefix searches
        # or use FTS5 query syntax like "term1 NEAR term2".
        # For simplicity, we'll use the raw query, but consider sanitizing/enhancing it.
        # Example: fts_query = f'"{query}"*' # for phrase prefix query
        # For now, direct query, assuming user knows FTS syntax or simple terms

        # rank is an auxiliary function of FTS5
        # Ensure all selected columns exist in your items_fts_table definition
        # and in the CREATE VIRTUAL TABLE statement (including UNINDEXED ones).
        # Reverted to using table name in MATCH and selecting rank, and ordering by rank.
        # This is the standard way it should work.
        sql_query = text("""
            SELECT id, module_name, item_name, display_name, properties_json, rank
            FROM items_fts
            WHERE items_fts MATCH :query
            ORDER BY rank DESC;
        """)
        # Using DESC for rank is common as higher rank usually means more relevant.

        results = []
        try:
            with self.engine.connect() as connection:
                db_results = connection.execute(sql_query, {"query": query})
                for row in db_results:
                    results.append(dict(row._mapping))
            # print(f"Search for '{query}' found {len(results)} items.") # Reduced verbosity for tests
        except Exception as e:
            print(f"Error during item search for query '{query}': {e}")
            return []

        return results

if __name__ == '__main__':
    # This block is for basic, direct testing of SearchService.
    # It requires the database mcp_data.db to exist and items_fts table to be populated.
    # To test:
    # 1. Run main.py once to create the DB and tables.
    # 2. Call the /extract-vanilla-data endpoint to populate data.
    # 3. Then you can run this script directly (python -m mcp_server.core.search_service).

    print("--- SearchService Direct Test ---")
    search_service = SearchService()

    # Example queries to test with (assuming vanilla_scripts items.txt was loaded):
    test_queries = ["Screwdriver", "hammer", "apple", "base", "food", "nonexistent"]

    # Before running this, ensure your DB is populated.
    # You might need to run the data extraction process first.
    # print("NOTE: Ensure mcp_data.db is populated before running these tests.")
    # print("Example: Run main.py, then hit /extract-vanilla-data endpoint via browser/curl.")

    # for t_query in test_queries:
    #     print(f"\nSearching for: '{t_query}'")
    #     items = search_service.search_items(t_query)
    #     if items:
    #         for item in items:
    #             print(f"  Found: ID={item['id']}, Module={item['module_name']}, Name={item['item_name']}, Display={item['display_name']}")
    #             # print(f"     Properties: {item['properties_json']}") # Optional: print properties
    #     else:
    #         print(f"  No results for '{t_query}'.")

    print("\nSearchService direct test block finished.")
    print("Uncomment the loop above and ensure DB is populated to perform actual searches.")
