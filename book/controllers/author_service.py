# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import asyncio
from concurrent.futures import ThreadPoolExecutor

import requests


class AuthorService(object):
    def __init__(self):
        """
        This class fetches authors of list of books parallely to improve performance
        :rtype: list({'id': 1})
        """

    @staticmethod
    def _fetch_author(session, book_id):
        """
        This function fetch author detail of a book id
        :type book_id: id of a book
        :type session: Session
        :return: book data
        :rtype: int
        """
        url = "https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding"

        payload = '{"book_id": ' + str(book_id) + '}'
        headers = {
            'Content-Type': 'application/json'
        }

        with session.post(url, data=payload, headers=headers) as response:
            if response.status_code != 200:
                print(f"Author Fetch Failure::{response.text}")
            else:
                data = response.json()
                book = {
                    'author': data['author'],
                    'id': book_id
                }
        return book

    @staticmethod
    async def _get_multiple_books_author(book_id_list):
        """
        This function call fetch author using Thread pool executor for give parralelism
        :param book_id_list: List of book ids
        :type book_id_list: list(int)
        """
        data = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `fetch`
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        AuthorService._fetch_author,
                        *(session, book_id)  # Allows us to pass in multiple arguments to `fetch`
                    )
                    for book_id in book_id_list
                ]
                for response in await asyncio.gather(*tasks):
                    data.append(response)
        return data

    async def get_authors(self, book_id_list):
        """
        This function is gets called to fetch author
        """
        return await self._get_multiple_books_author(book_id_list)
