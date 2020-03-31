# -*- coding: utf-8 -*-

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE_PATH = os.path.join(ROOT_DIR, 'data', '_index_data.json')

SOURCE_DATA_FILE_PATH = os.path.join(ROOT_DIR, "data", "data.json")
# SOURCE_DATA_FILE_PATH = os.path.join(ROOT_DIR, "data", "large_data.json")


# Redis Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""
