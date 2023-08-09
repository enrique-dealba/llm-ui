import unittest

from code_splitter import CodeSplitter
from test_files.code_texts import code_text

class CodeSplitterTestCase(unittest.TestCase):
    def setUp(self):
        self.code_splitter = CodeSplitter(language='python', max_chars=1500)
        self.actual_chunk_sizes = [449, 45, 42, 383, 1483, 716, 29,
                                   1287, 178, 1450, 1356, 1401, 1416]
        
    def error_setUp(self):
        self.error_splitter = CodeSplitter(language='ERROR-LANG', max_chars=1500)
        
    def test_code_splitter(self):
        chunks = self.code_splitter.split_text(code_text)
        self.assertEqual(len(chunks), len(self.actual_chunk_sizes))
        for i in range(len(chunks)):
            self.assertEqual(len(chunks[i]), self.actual_chunk_sizes[i])

    def test_errors(self):
        # Tests the try / except Exception as e...
        self.error_setUp()
        with self.assertRaises(AttributeError) as context:
            chunks = self.error_splitter.split_text(code_text)

if __name__ == '__main__':
    unittest.main()