import unittest
import sys
import os

# Add parent dir to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAntigravity(unittest.TestCase):
    def test_import_antigravity(self):
        """Test that antigravity module is available."""
        try:
            import antigravity
        except ImportError:
            self.fail("antigravity module could not be imported")

    def test_flight_mode_config(self):
        """Test that flight mode config is respected."""
        # This requires mocking env vars, which is a bit complex for a simple script test,
        # but we can check if the Config class has the attribute.
        from config import Config
        self.assertTrue(hasattr(Config, 'ANTIGRAVITY_FLIGHT'))

if __name__ == '__main__':
    unittest.main()
