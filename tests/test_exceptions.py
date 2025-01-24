import unittest
from blofin.exceptions import BlofinAPIException

class TestExceptions(unittest.TestCase):
    def test_blofin_api_exception(self):
        """Test BlofinAPIException"""
        # Test with message only
        exc = BlofinAPIException("Test error")
        self.assertEqual(str(exc), "Test error")
        self.assertIsNone(exc.code)
        self.assertIsNone(exc.response)

        # Test with message and code
        exc = BlofinAPIException("Test error", code="400")
        self.assertEqual(str(exc), "Test error")
        self.assertEqual(exc.code, "400")
        self.assertIsNone(exc.response)

        # Test with message, code, and response
        response = {"error": "Bad Request"}
        exc = BlofinAPIException("Test error", code="400", response=response)
        self.assertEqual(str(exc), "Test error")
        self.assertEqual(exc.code, "400")
        self.assertEqual(exc.response, response)

if __name__ == '__main__':
    unittest.main()
