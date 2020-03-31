# -*- coding: utf-8 -*-
import time

from book.controllers.author_service import AuthorService
from book.controllers.search_util import SearchUtil


class BookService(object):
    def __init__(self):
        self.search_util = SearchUtil()
        self.author_service = AuthorService()

    async def find_books_by_query_list(self, query_list, k):
        """

        :param query_list: list of queries
        :type query_list: list(str)
        :param k: max record to be retured per query
        :type k: int
        :return: reponse containing author, summary
        :rtype: list({id: int, summary: str, author: str, query: str})
        """
        response = []
        book_id_list = []
        st = time.time()
        for query in query_list:
            query_response = []
            results = self.search_util.sentence_search(query, k)
            if len(results) < k:
                results += self.search_util.term_search(query)

            results = results[:k]
            results = set(results)
            book_id_list.extend(results)
            for r in results:
                d = {
                    'summary': self.search_util.summary_indices[str(r)],
                    'id': r,
                    'query': query
                }
                query_response.append(d)
            response.append(query_response)
        print(f"Time taken in querying: {round(time.time()-st, 4)}s")
        st = time.time()
        book_author_list = await self.author_service.get_authors(book_id_list)
        print(f"Time taken in fetching authors: {round(time.time()-st, 4)}s")
        st = time.time()
        for arr in response:
            for obj in arr:
                for author in book_author_list:
                    if author['id'] == obj['id']:
                        obj['author'] = author['author']
        print(f"Time taken in making response: {round(time.time()-st, 4)}s")
        return response
