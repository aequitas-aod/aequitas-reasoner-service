import unittest

suite = unittest.TestLoader().discover("test")
result = unittest.TextTestRunner(verbosity=2).run(suite)

exit(0) if result.wasSuccessful() else exit(1)
