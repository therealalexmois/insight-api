import tomllib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from src.app.domain.constants import AppEnv, LogLevel
from src.app.infrastructure.config import _extract_project_field, Settings


@pytest.fixture
def sample_pyproject(tmp_path: 'Path') -> 'Path':
    """Создает временный pyproject.toml с базовой конфигурацией."""
    content = """
    [project]
    name = "insight-api"
    version = "1.2.3"
    """
    file_path = tmp_path / 'pyproject.toml'
    file_path.write_text(content.strip())
    return file_path


@pytest.mark.unit
def test_extract_project_field__returns_correct_name(sample_pyproject: 'Path') -> None:
    """Проверяет корректное извлечение поля name из pyproject.toml."""
    result = _extract_project_field('name', sample_pyproject)
    assert result == 'insight-api'


@pytest.mark.unit
def test_extract_project_field__returns_correct_version(sample_pyproject: 'Path') -> None:
    """Проверяет корректное извлечение поля version из pyproject.toml."""
    result = _extract_project_field('version', sample_pyproject)
    assert result == '1.2.3'


@pytest.mark.unit
def test_extract_project_field__raises_key_error(sample_pyproject: 'Path') -> None:
    """Проверяет, что возникает KeyError при отсутствии поля."""
    with pytest.raises(KeyError):
        _extract_project_field('description', sample_pyproject)


@pytest.mark.unit
def test_extract_project_field__raises_toml_error(tmp_path: 'Path') -> None:
    """Проверяет, что возникает TOMLDecodeError при неправильном синтаксисе."""
    bad_file = tmp_path / 'pyproject.toml'
    bad_file.write_text('this is not valid TOML')

    with pytest.raises(tomllib.TOMLDecodeError):
        _extract_project_field('name', bad_file)


@pytest.mark.unit
def test_settings__load_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет, что настройки загружаются из переменных окружения."""
    monkeypatch.setenv('APP_ENV', 'dev')
    monkeypatch.setenv('APP_HOST', '0.0.0.0')
    monkeypatch.setenv('APP_PORT', '9000')
    monkeypatch.setenv('APP_LOG_LEVEL', 'info')
    monkeypatch.setenv('APP_SECRET_KEY', 'supersecret')

    settings = Settings()

    test_port = 9000

    assert settings.app.env == AppEnv.DEV
    assert settings.app.host == '0.0.0.0'
    assert settings.app.port == test_port
    assert settings.app.secret_key.get_secret_value() == 'supersecret'
    assert settings.logging.level == LogLevel.INFO
