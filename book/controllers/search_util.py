# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import os
import re
from functools import reduce

import constants


class SearchUtil(object):
    def __init__(self):
        pass
        """

        :rtype: object
        """
        self._build_indices()

    def _build_indices(self):
        """
        Builds inverted index, list of uniques words in summary
        and saves it to json file for future use.
        :rtype: None
        """
        # Check if we have already created inverted indices and source data is not modified:
        # then load already created indices
        # otherwise: create and store indices

        if os.path.exists(constants.INDEX_FILE_PATH) and os.path.getmtime(
                constants.SOURCE_DATA_FILE_PATH) < os.path.getmtime(
            constants.INDEX_FILE_PATH):
            with open(constants.INDEX_FILE_PATH, 'r') as fop:
                _data = json.load(fop)
                self.keyword_indices = _data['keyword_indices']
                self.inverted_indices = _data['inverted_indices']
                self.summary_indices = _data['summary_indices']
        else:
            with open(constants.SOURCE_DATA_FILE_PATH, 'r') as fop:
                _raw_data = json.load(fop)
                summaries = _raw_data.get('a', [])

            self.keyword_indices = dict()
            self.inverted_indices = dict()
            self.summary_indices = dict()

            self.summary_indices = dict({str(a['id']): a['summary'] for a in summaries})

            self.keyword_indices, self.inverted_indices = self._build_partial_indices(summaries)

            # # Save the processed data for future usages
            # with open(constants.INDEX_FILE_PATH, 'w+') as fop:
            #     _data = {
            #         'inverted_indices': self.inverted_indices,
            #         'keyword_indices': self.keyword_indices,
            #         'summary_indices': self.summary_indices
            #     }
            #     json.dump(_data, fop)

    @staticmethod
    def _build_partial_indices(summaries):
        keyword_indices = dict()
        inverted_indices = dict()
        for summary in summaries:
            # Replace all non-ascii or special characters or punctuations character with space
            _words = re.sub(r'[^\x00-\x7F]+|[^A-Za-z0-9 ]+', ' ', summary['summary']).lower().split()
            # make all characters lower case
            keyword_indices[summary.get("id", -1)] = _words
            for i, w in enumerate(_words):
                if inverted_indices.get(w):
                    inverted_indices[w].append([summary['id'], i])
                else:
                    inverted_indices[w] = [[summary['id'], i]]
        return keyword_indices, inverted_indices

    def term_search(self, sentence):
        """
        This function performs key word wise search of sentence in summaries of source data
        :param sentence:
        :type sentence: string
        :return:
        :rtype:
        """
        # Replace all non-ascii or special characters or punctuations character with space
        _words = re.sub(r'[^\x00-\x7F]+|[^A-Za-z0-9 ]+', ' ', sentence).lower().split()

        list_of_set = []
        for term in _words:
            list_of_set.append(set(a[0] for a in self.inverted_indices.get(term) or []))
        _res = reduce(set.intersection, list_of_set)
        return list(_res)

    def sentence_search(self, sentence, k):
        """
        This function perform exact search for sentence in summaries of source data
        :param sentence: sentence to search for
        :type sentence: string
        :return: list of book ids where sentence found in summary
        :rtype: list(int)
        """
        _words = re.sub(r'[^\x00-\x7F]+|[^A-Za-z0-9 ]+', ' ', sentence).lower().split()
        firstword, *otherwords = _words
        found = []
        for _id in self.term_search(sentence):
            _words = self.keyword_indices.get(str(_id)) or []
            for f_index, _word in enumerate(_words):
                if firstword == _word:
                    _found = True
                    for o_index, o_word in enumerate(otherwords):
                        if o_word != _words[f_index + 1 + o_index]:
                            _found = False
                            break
                    if _found:
                        found.append(_id)
                        if len(found) >= k:
                            break
        return list(set(found))
