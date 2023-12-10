import unittest
from islamway import Parser, Types


class IslamwayTestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_search_nasheed(self):
        # Replace 'your_test_query' with an actual search query for testing
        test_query = "your_test_query"
        nasheed_results = self.parser.Anasheed.search_nasheed(test_query, limit=5)

        # Assert that the returned object is a list of Nasheed instances
        self.assertIsInstance(nasheed_results, list)
        self.assertTrue(
            all(isinstance(result, Types.Nasheed) for result in nasheed_results)
        )

        # Add more specific assertions based on your expectations for the search results
        self.assertGreaterEqual(len(nasheed_results), 0)
        for nasheed in nasheed_results:
            self.assertIsNotNone(nasheed.nasheed_url)
            self.assertIsNotNone(nasheed.name)
            self.assertIsNotNone(nasheed.download_url)
            self.assertIsNotNone(nasheed.publisher)

    def test_most_popular_nasheed(self):
        nasheed_results = self.parser.Anasheed.most_popular(limit=5)

        # Assert that the returned object is a list of Nasheed instances
        self.assertIsInstance(nasheed_results, list)
        self.assertTrue(
            all(isinstance(result, Types.Nasheed) for result in nasheed_results)
        )

        # Add more specific assertions based on your expectations for the most popular nasheeds
        self.assertGreaterEqual(len(nasheed_results), 0)
        # Add more assertions as needed

    # Similar tests for other methods like most_recent_nasheed, most_viewed_nasheed, highest_rated_nasheed


if __name__ == "__main__":
    unittest.main()
