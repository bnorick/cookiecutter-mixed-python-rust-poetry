use pyo3::prelude::*;

#[pyfunction]
fn is_foobar(data: String) -> PyResult<bool> {
    Ok(data == "foobar")
}

#[pymodule]
#[pyo3(name="_{{ cookiecutter.package_name }}")]
fn _{{ cookiecutter.package_name }}(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(is_foobar))?;
    Ok(())
}
