# tests/test_profile.py


from upwork_scraper.models.profile import (clean_string,
                                          convert_empty_string_to_none,
                                          strip_whitespace)


def test_clean_string():
    assert clean_string("   example string  ", "e", "l") == "xamp string"
    assert clean_string("abc", "x") == "abc"
    assert clean_string(None, "x") is None


def test_strip_whitespace():
    assert strip_whitespace("   example   string  ") == "example string"
    assert strip_whitespace("  multiple    spaces   ") == "multiple spaces"
    assert strip_whitespace(None) is None


def test_convert_empty_string_to_none():
    assert convert_empty_string_to_none("") is None
    assert convert_empty_string_to_none("example") == "example"
    assert convert_empty_string_to_none(None) is None
