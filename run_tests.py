import unittest

suite = unittest.TestLoader().discover("test")
result = unittest.TextTestRunner(verbosity=2).run(suite)

if result.wasSuccessful():
    exit(0)
else:
    exit(1)
