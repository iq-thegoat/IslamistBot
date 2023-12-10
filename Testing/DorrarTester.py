import unittest
from dorrar import Types, Parser


class DorrarTestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_search(self):
        # Replace 'your_test_query' with an actual search query for testing
        test_query = "your_test_query"
        hadith_results = self.parser.search(test_query, limit=5)

        # Assert that the returned object is a list of Hadith instances
        self.assertIsInstance(hadith_results, list)
        self.assertTrue(
            all(isinstance(result, Types.Hadith) for result in hadith_results)
        )

        # Add more specific assertions based on your expectations for the search results
        self.assertGreaterEqual(len(hadith_results), 0)
        for hadith in hadith_results:
            self.assertIsNotNone(hadith.text)
            self.assertIsNotNone(hadith.url)
            self.assertIsNotNone(hadith.ruling)
            self.assertIsNotNone(hadith.muhadith)

        # Add more assertions as needed


if __name__ == "__main__":
    unittest.main()
