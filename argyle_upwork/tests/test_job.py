# tests/test_job.py

from datetime import datetime, timedelta

from argyle_upwork.models.job import (clean_numeric_string,
                                      validate_client_spendings,
                                      validate_posted_on)


def test_clean_numeric_string():
    assert clean_numeric_string("abc123") == "123"
    assert clean_numeric_string("xyz456") == "456"
    assert clean_numeric_string(None) is None


def test_validate_client_spendings():
    assert validate_client_spendings("5K") == "5000.0"
    assert validate_client_spendings("2k") == "2000.0"
    assert validate_client_spendings(None) is None


def test_validate_posted_on():
    current_time = datetime.now()
    days_ago = (current_time - timedelta(days=5)).isoformat()
    minutes_ago = (current_time - timedelta(minutes=30)).isoformat()

    assert validate_posted_on("5 days ago")[20] == days_ago[20]
    assert validate_posted_on("30 minutes ago")[20] == minutes_ago[20]
    assert validate_posted_on(None) is None
