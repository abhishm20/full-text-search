# -*- coding: utf-8 -*-


class BookModel(object):
    def __init__(self, _id, summary=None, author=None):
        self.id = _id
        self.summary = summary
        self.author = author
