import unittest
import sys

sys.path.append(".") # tests use cursesgame.<stuff>
result = unittest.TextTestRunner(verbosity=2)\
    .run(unittest.defaultTestLoader.discover('test'))
exit_code = 0
if result.failures:
    exit_code += 1
if result.errors:
    exit_code += 2
exit(exit_code)
