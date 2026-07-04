from src.tools import web_search


def test_web_search_no_query():
    result = web_search("")
    assert isinstance(result, str)


def test_web_search_internet():
    result = web_search("Python programming language")
    assert isinstance(result, str)
    assert len(result) > 0
