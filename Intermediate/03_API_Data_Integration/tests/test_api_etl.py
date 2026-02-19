import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from api_etl import (
    setup_logger,
    fetch_with_retries,
    fetch_paginated_data,
    normalize_data,
    save_to_csv
)


class TestAPIETL:
    def test_setup_logger(self):
        """Test logger setup"""
        logger = setup_logger()
        assert logger.name == "api_etl"
        assert logger.level == 20  # INFO level

    def test_normalize_data(self):
        """Test data normalization"""
        raw_data = [
            {"id": 1, "title": "Test Post", "body": "Test content", "userId": 1},
            {"id": 2, "title": "Another Post", "body": "More content", "userId": 2}
        ]

        normalized = normalize_data(raw_data)

        assert len(normalized) == 2
        assert normalized[0]["id"] == 1
        assert normalized[0]["title"] == "Test Post"
        assert normalized[0]["content"] == "Test content"
        assert normalized[0]["user_id"] == 1
        assert normalized[0]["api_source"] == "jsonplaceholder"
        assert normalized[0]["valid"] is True
        assert "fetched_at" in normalized[0]

    def test_normalize_data_invalid_record(self):
        """Test normalization with invalid records"""
        raw_data = [
            {"id": None, "title": "", "body": "content", "userId": 1},  # Invalid: no id and empty title
            {"id": 2, "title": "Valid", "body": "content", "userId": 2}  # Valid
        ]

        normalized = normalize_data(raw_data)

        assert len(normalized) == 2
        assert normalized[0]["valid"] is False
        assert normalized[1]["valid"] is True

    @patch('requests.get')
    def test_fetch_with_retries_success(self, mock_get):
        """Test successful API fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response

        result = fetch_with_retries("http://test.com", max_retries=3, timeout=5)

        assert result == {"test": "data"}
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_fetch_with_retries_failure_then_success(self, mock_get):
        """Test API fetch with retry on failure"""
        import requests

        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "data"}

        # First call raises RequestException, second succeeds
        mock_get.side_effect = [requests.exceptions.RequestException("Connection error"), mock_response]

        result = fetch_with_retries("http://test.com", max_retries=3, timeout=5)

        assert result == {"test": "data"}
        assert mock_get.call_count == 2

    @patch('requests.get')
    def test_fetch_with_retries_max_retries_exceeded(self, mock_get):
        """Test API fetch fails after max retries"""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        with pytest.raises(requests.exceptions.RequestException):
            fetch_with_retries("http://test.com", max_retries=2, timeout=5)

        assert mock_get.call_count == 2

    def test_save_to_csv(self):
        """Test CSV saving functionality"""
        data = [
            {"id": 1, "title": "Test", "content": "Content", "user_id": 1,
             "api_source": "test", "fetched_at": "2023-01-01", "valid": True}
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name

        try:
            count = save_to_csv(data, temp_path)
            assert count == 1

            # Verify file contents
            with open(temp_path, 'r') as f:
                lines = f.readlines()
                assert len(lines) == 2  # header + 1 data row
                assert "id,title,content" in lines[0]
                assert "1,Test,Content" in lines[1]
        finally:
            os.unlink(temp_path)

    def test_save_to_csv_empty_data(self):
        """Test CSV saving with empty data"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name

        try:
            count = save_to_csv([], temp_path)
            assert count == 0

            # File should not be created or should be empty
            if os.path.exists(temp_path):
                with open(temp_path, 'r') as f:
                    content = f.read()
                    assert content == ""
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)