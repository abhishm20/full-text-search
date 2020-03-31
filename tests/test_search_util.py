# -*- coding: utf-8 -*-

import os
import unittest

import constants
from book.controllers.search_util import SearchUtil

instance = None


class TestSearchUtil(unittest.TestCase):
    def get_instance(self):
        global instance
        if instance:
            return instance
        else:
            instance = SearchUtil()
            return instance

    def test_source_data_exists(self):
        self.assertTrue(os.path.exists(constants.SOURCE_DATA_FILE_PATH))

    def test_index_file_parsed_after_data_modification(self):
        if os.path.exists(constants.INDEX_FILE_PATH):
            self.assertTrue(os.path.getmtime(constants.SOURCE_DATA_FILE_PATH)
                            < os.path.getmtime(constants.INDEX_FILE_PATH))

    def test_term_search(self):
        i = self.get_instance()
        queries = self.get_sample_queries()
        for s, results in queries.items():
            self.assertSetEqual(set(i.term_search(s)), set(results[0]))

    def test_sentence_search(self):
        i = self.get_instance()
        queries = self.get_sample_queries()
        for s, results in queries.items():
            self.assertSetEqual(set(i.sentence_search(s)), set(results[1]))

    @staticmethod
    def get_sample_queries():
        return {
            "Three Sentences: To become": [[10, 49], [10]],
            "The 10X Rule says that 1) you should": [[1], [1]],
            "related processes.": [[17], [17]],
            "Okay this related processes.": [[], []]
        }
