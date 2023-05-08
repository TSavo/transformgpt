from __future__ import annotations
from dataclasses import dataclass
import dataclasses
from typing import List, Optional
import unittest
import openai
import os
import sys
# add .. to the path so we can import transformgpt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from transformgpt import TransformGPT


openai.api_key = os.getenv("OpenAIAPI")
transformer = TransformGPT(openai.ChatCompletion)


class TestClassify(unittest.TestCase):
    def setUp(self):
        # initialize any objects or variables needed for the tests
        pass
    def test_classify(self):
        # test case with a single request and constraints
        message = "Please clone https://github.com/tsavo/image-processor, specifically the main branch. Then scan it for viruses."
        categories = ["Ask a question about the president",
                                  "Open a file",
                                  "Choose a hat to wear",
                                  "Clone a git repository",
                                  "Eat soup for lunch",
                                  "Delete a git repository",
                                  "None of the above"]
        result = transformer.classify_string(message, categories)
        assert(result == "Clone a git repository")

if __name__ == '__main__':
    unittest.main()