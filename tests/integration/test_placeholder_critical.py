import pytest


@pytest.mark.critical
def test_placeholder__always_passes() -> None:
    """Временный критичный тест-заглушка, всегда проходит."""
    assert True
