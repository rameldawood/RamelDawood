import unittest
from query_process import QueryProcess, DocumentStore, BaseIndex

class TestQueryProcess(unittest.TestCase):
    def setUp(self):
        # Assuming DocumentStore and BaseIndex are properly implemented and can be instantiated
        self.document_store = DocumentStore()
        self.index = BaseIndex()
        self.query_process = QueryProcess(self.document_store, self.index)

    def test_expandQueries(self):
        # Mock thesaurus for testing
        mock_thesaurus = {
            'test': ['exam', 'assessment'],
            'queries': ['inquiries', 'questions']
        }
        # The query to expand
        query = 'test queries'
        # Expected result after expansion
        expected_result = {
            'test': ['test', 'exam', 'assessment'],
            'queries': ['queries', 'inquiries', 'questions']
        }
        # Run the expandQueries function
        result = self.query_process.expandQueries(query, mock_thesaurus)
        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
