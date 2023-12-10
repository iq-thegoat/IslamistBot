import unittest
from DorrarTester import DorrarTestParser
from IslamwayTester import IslamwayTestParser
from NoorTester import NoorTestParser

if __name__ == "__main__":
    # Create a test loader
    test_loader = unittest.TestLoader()

    # Load tests from test case classes
    dorrar_test_suite = test_loader.loadTestsFromTestCase(DorrarTestParser)
    islamway_test_suite = test_loader.loadTestsFromTestCase(IslamwayTestParser)
    noor_test_suite = test_loader.loadTestsFromTestCase(NoorTestParser)

    # Create a test suite and add the loaded test suites
    test_suite = unittest.TestSuite(
        [dorrar_test_suite, islamway_test_suite, noor_test_suite]
    )

    # Run the test suite using TextTestRunner
    unittest.TextTestRunner().run(test_suite)
