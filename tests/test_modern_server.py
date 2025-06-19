"""Tests for the modern FastMCP-based Project Zomboid server."""

import asyncio
import json
from unittest.mock import Mock, patch

import pytest

from mcp_server.modern_server import (
    get_property_reference,
    get_vanilla_database,
    mcp,
    search_vanilla,
    validate_script,
)


class TestResources:
    """Test resource endpoints."""

    def test_get_vanilla_database_format(self):
        """Test that vanilla database resource returns valid JSON when called properly."""
        # This test would need to be run within a proper FastMCP context
        # For now, we'll test the structure without the actual database call
        with patch('mcp_server.modern_server.mcp.get_context') as mock_get_context:
            mock_context = Mock()
            mock_app_context = Mock()
            mock_app_context.search_service.search_items.return_value = []
            mock_context.request_context.lifespan_context = mock_app_context
            mock_get_context.return_value = mock_context

            result = get_vanilla_database()
            data = json.loads(result)

            assert data["type"] == "vanilla_database"
            assert "total_items" in data
            assert "sample_items" in data
            assert isinstance(data["sample_items"], list)

    def test_get_property_reference_format(self):
        """Test that property reference returns valid JSON with expected structure."""
        result = get_property_reference()
        data = json.loads(result)

        assert data["type"] == "property_reference"
        assert "item_properties" in data
        assert "recipe_properties" in data
        assert "vehicle_properties" in data

        # Check some key properties exist
        assert "DisplayName" in data["item_properties"]
        assert "Weight" in data["item_properties"]
        assert "Result" in data["recipe_properties"]


class TestTools:
    """Test tool implementations."""

    @pytest.mark.anyio
    async def test_validate_script_empty_content(self):
        """Test script validation with empty content."""
        from mcp_server.modern_server import ScriptValidationRequest

        request = ScriptValidationRequest(
            content="",
            script_type="item"
        )

        result = await validate_script(request, Mock())
        assert "Error: Script content is empty" in result

    @pytest.mark.anyio
    async def test_validate_script_invalid_type(self):
        """Test script validation with invalid script type."""
        from mcp_server.modern_server import ScriptValidationRequest

        request = ScriptValidationRequest(
            content="some content",
            script_type="invalid_type"
        )

        result = await validate_script(request, Mock())
        assert "Error: Unknown script type" in result

    @pytest.mark.anyio
    async def test_validate_script_missing_declaration(self):
        """Test script validation detects missing declarations."""
        from mcp_server.modern_server import ScriptValidationRequest

        request = ScriptValidationRequest(
            content="module Test {\n    // missing item declaration\n    // no item statement found\n}",
            script_type="item"
        )

        # Create a proper async mock context
        mock_ctx = Mock()
        mock_ctx.info = Mock()
        mock_ctx.report_progress = Mock(return_value=asyncio.Future())
        mock_ctx.report_progress.return_value.set_result(None)

        result = await validate_script(request, mock_ctx)

        # The validation logic should detect missing item declaration
        assert "Warning: No 'item' declaration found" in result

    @pytest.mark.anyio
    async def test_search_vanilla_no_results(self):
        """Test search with no results."""
        # Mock the app context and search service
        mock_search_service = Mock()
        mock_search_service.search_items.return_value = []

        with patch('mcp_server.modern_server.mcp.get_context') as mock_get_context:
            mock_context = Mock()
            mock_context.request_context.lifespan_context.search_service = mock_search_service
            mock_get_context.return_value = mock_context

            result = await search_vanilla("nonexistent_item")
            assert "No items found matching" in result


# Note: Completion tests will be added when MCP SDK completion API is available


class TestServerIntegration:
    """Integration tests for the MCP server."""

    def test_server_initialization(self):
        """Test that the server initializes correctly."""
        assert mcp.name == "Project Zomboid"
        # FastMCP server should have basic attributes
        assert hasattr(mcp, 'name')
        assert hasattr(mcp, 'dependencies')
        assert len(mcp.dependencies) > 0

    @pytest.mark.anyio
    async def test_server_lifespan_context(self):
        """Test that server lifespan creates proper context."""
        from mcp_server.modern_server import server_lifespan

        # Mock dependencies to avoid actual database operations
        with patch('mcp_server.modern_server.create_db_and_tables'), \
             patch('mcp_server.modern_server.extract_vanilla_data'), \
             patch('mcp_server.modern_server.SearchService') as MockSearchService, \
             patch('mcp_server.modern_server.ScriptGenerator') as MockScriptGenerator, \
             patch('mcp_server.modern_server.ModChecker') as MockModChecker:

            # Setup mocks
            mock_search = MockSearchService.return_value
            mock_search.search_items.return_value = [{"item_name": "TestItem"}]

            async with server_lifespan(mcp) as context:
                assert hasattr(context, 'search_service')
                assert hasattr(context, 'script_generator')
                assert hasattr(context, 'mod_checker')


if __name__ == "__main__":
    pytest.main([__file__])
