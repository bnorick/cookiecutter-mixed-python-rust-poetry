# {{ cookiecutter.project_name }}

### To develop
1. Install python dependencies with `poetry install` from the `{{ cookiecutter.package_name }}` project folder
2. Install rust component with `poetry run maturin develop --skip-install` (optionally add `--release` for a release build)
3. Make changes
    - If only changing python, move to step 4.
    - If changing rust, update the rust build using step 2. then move to step 4.
4. Test
5. Back to 3, if needed.
6. Bump the version, e.g., `poetry version minor`
7. Publish a branch and submit a PR to main