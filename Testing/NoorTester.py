import unittest
from Noor_Wrapper import Parser, Types
from icecream import ic


class NoorTestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_book_page(self):
        # Replace 'your_test_url' with an actual book page URL for testing
        test_url = "https://www.noor-book.com/%D9%83%D8%AA%D8%A7%D8%A8-%D9%83%D8%AA%D8%A7%D8%A8-%D8%A7%D9%84%D8%AA%D9%88%D8%AD%D9%8A%D8%AF-pdf"
        book = self.parser.parse_book_page(test_url)

        # Assert that the returned object is an instance of the Book class
        self.assertIsInstance(book, Types.Book)
        # Add more specific assertions based on your expectations for the parsed book data
        self.assertIsNotNone(book.title)
        self.assertIsNotNone(book.author)
        self.assertIsNotNone(book.URL)
        self.assertIsNotNone(book.img_url)
        # Add more assertions as needed

    def test_search(self):
        # Replace 'your_test_query' with an actual search query for testing
        test_query = "التوحيد"
        search_results = self.parser.search(test_query, limit=5)

        # Assert that the returned object is a list of SearchResult instances
        self.assertIsInstance(search_results, list)
        self.assertTrue(
            all(isinstance(result, Types.SearchResult) for result in search_results)
        )

        # Add more specific assertions based on your expectations for the search results
        self.assertGreaterEqual(len(search_results), 0)
        # Add more assertions as needed


if __name__ == "__main__":
    unittest.main()
