# -*- coding: utf-8 -*-
import asyncio

from quart import Quart, request

loop = asyncio.get_event_loop()

app = Quart(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/books', methods=['POST'])
async def fetch_books_by_queries():
    from book.services import BookService
    data = await request.json
    service = BookService()
    data = await service.find_books_by_query_list(data.get('queries', []), data.get('k', 0))
    return {'data': data}


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
