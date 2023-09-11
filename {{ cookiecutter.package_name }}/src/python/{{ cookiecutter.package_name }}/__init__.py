from {{ cookiecutter.package_name }}._{{ cookiecutter.package_name }} import is_foobar

__version__ = "{{ cookiecutter.version }}"

__all__ = [
    "is_foobar",
]
