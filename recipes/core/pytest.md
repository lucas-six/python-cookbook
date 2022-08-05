# PyTest - Testing Framework

## Installation

```python
pipx install pytest
```

or:

```bash
pipenv install --dev pytest
```

## Basic Usage

```python
import pytest

def test_module():
    assert True

class TestClass:

    def test_equal(self):
        assert 'Hello '.capitalize() == 'Hello '

    def test_true(self):
        assert 'HELLO'.isupper()
        assert not 'Hello'.islower()

    def test_in(self):
        assert 'a' in 'abc'
        assert 'd' not in 'abc'

    def test_raise(self):
        with pytest.raises(TypeError):
            'hello'.capitalize(0)
```

## Run

### All Test Cases

```bash
pytest [-q|--quiet]
```

### Specified Modules, Functions, Methods

```bash
pytest <xxx.py>
pytest <xxx.py>::<func_name>
pytest <xxx.py>::<ClassName>::<method_name>
```

### Filter

```bash
pytest -k <containing-expr e.g. "MyClass and not method">

pytest -m <mathing-expr e.g. "MyClass and not method">
```

### Profiling

show `M` slowest (greater than `N` seconds) setup/test durations:

```bash
pytest --durations=<M> --durations-min=<N>
```

### Plugin

```bash
pytest -p <plugin-name>
```

disable:

```bash
pytest -p no:<plugin-name>
```

## Test Fixture

```python
import pytest

@pytest.fixture
def setup():
    return 1

def test_module(setup)
    assert setup == 1

@pytest.fixture(autouse=True)
def setup_for_all():
    return 2
```

### Scope

#### Fixture scopes

```python
# scope: function (default), class, module, package, session
@pytest.fixture(scope='module')
def setup_for_module():
    return 2
```

#### Dynamic scope

```python
def determine_scope(fixture_name, config):
    if config.getoption("--keep-containers", None):
        return "session"
    return "function"

@pytest.fixture(scope=determine_scope)
def setup():
    return 2
```

### Safe Teardown

```python
@pytest.fixture
def setup():
    yield 1
    # code to tear down (clean up).
```

### Pass Data

```python
import pytest

@pytest.fixture
def xxx(request):
    marker = request.node.get_closest_marker("xxx_data")
    if marker is None:
        # Handle missing marker in some way...
        data = None
    else:
        data = marker.args[0]

    # Do something with the data
    return data + 1


@pytest.mark.xxx_data(1)
def test_xxx(xxx):
    assert xxx == 2
```

### Parametrizing

```python
import pytest

@pytest.fixture(params=['127.0.0.1', '192.168.0.1'], autouse=True)
def xxx(request):
    connection = conn(request.param)
    yield connection
    connection.close()


@pytest.fixture
def yyy():
    return 1

@pytest.mark.parametrize('yyy', ['directly-overridden-yyy'])
def test_username(yyy):
    assert yyy == 'directly-overridden-yyy'
```

## Capture Log

```python
import logging

import pytest

class TestClass:

    def test_log(self, caplog):
        # caplog.set_level(logging.INFO)
        # caplog.set_level(logging.INFO, logger='root.xxx')
        with caplog.at_level(logging.INFO, logger='root.xxx'):
            logging.getLogger('root.xxx').info('first message')
            logging.getLogger('root.xxx.yyy').error('second message')

        assert len(caplog.records) == 2
        assert caplog.records[0].message == 'first message'
        assert caplog.records[1].message == 'second message'
        assert caplog.records[0].levelno == logging.INFO
```

## Capture stdout/stderr

```python
import sys

import pytest

def test_output(capsys):  # or use "capfd" for fd-level
    print('hello')
    sys.stderr.write('world\n')

    captured = capsys.readouterr()
    assert captured.out == 'hello\n'
    assert captured.err == 'world\n'

    print('next')
    captured = capsys.readouterr()
    assert captured.out == 'next\n'

    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
```

Run:

```bash
pytest --capture=sys  # fd
```

## Capture Warnings

```python
import warnings

import pytest

class TestClass:

    def test_warning(self):
        with pytest.warns(UserWarning):
            warnings.warn('xxx', UserWarning)

    def test_warning_match(self):
        with pytest.warns(UserWarning, match='must be 0 or None'):
            warnings.warn('value must be 0 or None', UserWarning)

        with pytest.warns(UserWarning, match=r'must be \d+$'):
            warnings.warn('value must be 42', UserWarning)

    def test_warning_record(self):
        with pytest.warns() as record:
            warnings.warn('user', UserWarning)
            warnings.warn('runtime', RuntimeWarning)

        assert len(record) == 2
        assert str(record[0].message) == 'user'
        assert str(record[1].message) == 'runtime'

    def test_warning_recwarn(self, recwarn):
        warnings.warn('hello', UserWarning)
        assert len(recwarn) == 1
        w = recwarn.pop(UserWarning)
        assert issubclass(w.category, UserWarning)
        assert str(w.message) == 'hello'
        assert w.filename
        assert w.lineno
```

## Skip Tests

```python
import sys

import pytest

class TestClass:

    @pytest.mark.skip(reason='demonstrating skipping')
    def test_skip(self):
        pytest.xfail('shouldn\'t happen')

    @pytest.mark.skipif(sys.version_info < (3, 9), 'python 3.9+ required')
    def test_skipif(self):
        # Tests that work for only a certain version of Python.
        pass

    def test_maybe_skipped(self):
        if not external_resource_available():
            pytest.skip('external resource not available')
        # test code that depends on the external resource
        pass
```

## Expected Failure

```python
import pytest

class TestExpectedFailure:

    @pytest.mark.xfail
    def test_fail(self):
        assert False
```

## Temp files

```python
import pytest

def test_tmpfiles(self, tmp_path):
    print(tmp_path)
    assert True
```

## References

- [`pytest` Documentation](https://docs.pytest.org/)
- [`coverage` Documentation](https://coverage.readthedocs.io/)
- [`pytest-cov` Documentation](https://pytest-cov.readthedocs.io/en/latest/)
