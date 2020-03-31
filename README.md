## Problem Part 1:
- I have used inverted index to search for summaries.
- I am storing source data in multiple formats to improve search query time:
   1. inverted indices: {word1: [[book_id, index] ...], word2:...}
   1. keyword indices: {book_id1: [word1, word2 ...], book_id2:...}
   1. summary indices: {book_id1: summary_string, book_id2:...}
   
- After processing source data, I can store it in redis for better I/O

## Problem Part 2:
- I am using quart server to make async requests to fetch author details
- We can also cache author api's response to minimize the api and hit and hence reduce overall response time.

## API details:

```
POST http://http://127.0.0.1:5000/books
Request Body: {
                "queries": [
                    "Three Sentences: To become",
                    "The 10X Rule says that 1) you should",
                    "related processes",
                    "Okay this related processes."
                ],
                "k": 5
              }
``` 


### To Run
Run below commands:

1. `pip install -r requirement.txt`

2. `python app.py`
