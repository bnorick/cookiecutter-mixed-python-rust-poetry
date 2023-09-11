import {{ cookiecutter.package_name }}
from expecter import expect


def describe_nominal() -> None:
    def with_foobar() -> None:
        expect({{ cookiecutter.package_name }}.is_foobar("foobar")).is_(True)
        expect({{ cookiecutter.package_name }}.is_foobar("foodbard")).is_(False)
