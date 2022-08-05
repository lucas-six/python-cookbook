# `unittest` - Standard Unit Testing Framework

## Basic Usage

```python
import unittest

class MyTestCase(unittest.TestCase):

    def test_equal(self):
        self.assertEqual('Hello '.capitalize(), 'Hello ')
        self.assertNotEqual(1, 2)

    def test_true(self):
        self.assertTrue('HELLO'.isupper())
        self.assertFalse('Hello'.islower())

    def test_in(self):
        self.assertIn('a', 'abc')
        self.assertNotIn('d', 'abc')

    def test_is_none(self):
        a = None
        self.assertIsNone(a)
        self.assertIsNotNone('a')

    def test_raise(self):
        with self.assertRaises(TypeError):
            'hello'.capitalize(0)

if __name__ == '__main__':
    unittest.main(verbosity=2, catchbreak=True)
```

## Run

### All Test Cases

```bash
python -m unittest
```

### Specified Modules

```bash
python -m unittest [-v] <test_module>
```

### Filter

```bash
python -m unittest -k <containing-expr e.g. "MyClass and not method">
```

## Test Fixture

```python
import unittest

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass
```

## Capture Log

```python
import logging

import unittest

class MyTestCase(unittest.TestCase):

    def test_log(self):
        with self.assertLogs('foo', level='INFO') as cm:
           logging.getLogger('foo').info('first message')
           logging.getLogger('foo.bar').error('second message')
        self.assertEqual(cm.output, ['INFO:foo:first message', 'ERROR:foo.bar:second message'])

if __name__ == '__main__':
    unittest.main(verbosity=2, catchbreak=True)
```

## Capture Warnings

```python
import unittest

class MyTestCase(unittest.TestCase):

    def test_warning(self):
        with self.assertWarns(UserWarning):
            do_something()

    def test_warning_match(self):
        with self.assertWarnsRegex(UserWarning, 'must be 0 or None'):
            warnings.warn('value must be 0 or None', UserWarning)

        with self.assertWarnsRegex(UserWarning, match=r'must be \d+$'):
            warnings.warn('value must be 42', UserWarning)

    def test_warning_cm(self):
        with self.assertWarns(UserWarning) as cm:
            do_something()

        self.assertIn('myfile.py', cm.filename)
        self.assertEqual(320, cm.lineno)

if __name__ == '__main__':
    unittest.main(verbosity=2, catchbreak=True)
```

## Skip Tests

```python
class MyTestCase(unittest.TestCase):

    @unittest.skip('demonstrating skipping')
    def test_skip(self):
        self.fail('shouldn\'t happen')

    @unittest.skipIf(sys.version_info < (3, 9), 'python 3.9+ required')
    def test_skipif(self):
        # Tests that work for only a certain version of Python.
        pass

    @unittest.skipUnless(sys.platform.startswith('win'), 'requires Windows')
    def test_windows_support(self):
        # windows specific testing code
        pass

    def test_maybe_skipped(self):
        if not external_resource_available():
            self.skipTest('external resource not available')
        # test code that depends on the external resource
        pass
```

## Expected Failure

```python
class ExpectedFailureTestCase(unittest.TestCase):

    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")
```

## Subtest itertaion

```python
class NumbersTest(unittest.TestCase):

    def test_even(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
```

Output:

```python
======================================================================
FAIL: test_even (__main__.NumbersTest) (i=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0

======================================================================
FAIL: test_even (__main__.NumbersTest) (i=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0

======================================================================
FAIL: test_even (__main__.NumbersTest) (i=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0
```

## coroutines tests

```python
from unittest import IsolatedAsyncioTestCase

events = []


class MyTest(IsolatedAsyncioTestCase):


    def setUp(self):
        events.append("setUp")

    async def asyncSetUp(self):
        self._async_connection = await AsyncConnection()
        events.append("asyncSetUp")

    async def test_response(self):
        events.append("test_response")
        response = await self._async_connection.get("https://dookbook.info")
        self.assertEqual(response.status_code, 200)
        self.addAsyncCleanup(self.on_cleanup)

    def tearDown(self):
        events.append("tearDown")

    async def asyncTearDown(self):
        await self._async_connection.close()
        events.append("asyncTearDown")

    async def on_cleanup(self):
        events.append("cleanup")

if __name__ == '__main__':
    unittest.main()
```

## Singal Handling

temporarily remove the control-C handler while the test is being executed:

```python
@unittest.removeHandler
def test_signal_handling(self):
    ...
```

or for all (**`-c`**/**`--catch`** option)：

```bash
python -m unittest -c

python -m unittest -c <test_module>
```

## Mock: `unittest.mock`

```python
import unittest
import unittest.mock as mock
from io import StringIO

class MyTestCase(unittest.TestCase):

    @mock.patch('os.remove')
    def test_a(self, mock_os_remove):
        import os
        filename = 'a'

        os_remove_mock.return_value = None
        os_remove_mock.side_effect = OSError
        os.remove(filename)
        mock_os_remove.assert_called_once(filename)
        mock_os_remove.assert_called_with(filename)
        mock_os_remove.assert_any_call(filename)
        self.assertTrue(mock_os_remove.called)
        call = mock.call
        mock_os_remove.assert_has_calls([call(filename)])
        #mock_os_remove.assert_not_called()


    @mock.patch('os.getpid')
    @mock.patch('os.remove')
    def test_b(self, mock_os_remove, mock_os_getpid):
        pass


    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_c(self, mock_stderr):
        text = mock_stderr.getvalue()
        self.assertEqual(text, 'xxx')


    def test_d(self):
        mock_opener = mock.mock_open(read_data='aaa')
        mock_file = mock_opener()
        with mock.patch('builtins.open', mock_opener):
            mock_file.write.assert_not_called()
            self.assertEqual(mock_file.read.return_value, 'aaa')
        mock_opener.assert_called_with(filename, 'w')
        mock_file.close.assert_not_called()
```

## References

- [`unittest` Documentation](https://docs.python.org/3/library/unittest.html)
- [`unittest.mock` Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [`unittest.mock` - Getting Started](https://docs.python.org/3/library/unittest.mock-examples.html)
