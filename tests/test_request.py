from unittest import mock

import pytest

from meteobeguda.request import (
    URL_TWO_DAYS,
    URL_EIGHT_DAYS,
    get_last_two_days,
    get_last_eight_days,
)


@pytest.mark.parametrize(
    "url,method",
    [(URL_TWO_DAYS, get_last_two_days), (URL_EIGHT_DAYS, get_last_eight_days)],
)
def test_fetcher_returns_none_if_status_code_not_200(url, method, requests_mock):
    requests_mock.get(url, status_code=404)
    assert method() is None
    assert requests_mock.call_count == 1
    request = requests_mock.request_history[0]
    assert request.method == "GET"
    assert request.url == url


@pytest.mark.parametrize(
    "url,method",
    [(URL_TWO_DAYS, get_last_two_days), (URL_EIGHT_DAYS, get_last_eight_days)],
)
def test_fetcher_forms_request_to_meteobeguda(url, method, requests_mock):
    requests_mock.get(url, content=b"some content")
    assert b"some content" == method()
    assert requests_mock.call_count == 1
    request = requests_mock.request_history[0]
    assert request.method == "GET"
    assert request.url == url
