from __future__ import annotations
from dataclasses import dataclass
import dataclasses
from typing import List, Optional
import unittest
import openai
import os
from transformgpt import TransformGPT


openai.api_key = os.getenv("OpenAIAPI-Token")
transformer = TransformGPT(openai.ChatCompletion)

@dataclass
class MessageClassification:
  original_message:Optional[str] = None
  message_part:Optional[str] = None
  intent:Optional[str] = None
  categories:List[str] = dataclasses.field(default_factory=list)
  parameters:List[str] = dataclasses.field(default_factory=list)
  reply:Optional[str] = None
  justifications_for_reply:List[Justification] = dataclasses.field(default_factory=list)
  follow_up_items:List[MessageClassification] = dataclasses.field(default_factory=list)

@dataclass
class Justification:
    subject:Optional[str] = None
    object:Optional[str] = None
    intent:Optional[str] = None
    action:Optional[str] = None
    description:Optional[str] = None

class TestInterpretString(unittest.TestCase):
    def setUp(self):
        # initialize any objects or variables needed for the tests
        pass
    
    def test_empty_message(self):
        # test case when message is empty
        message = ""
        cls = MessageClassification
        constraints = {}
        result = transformer.transform_string(message, cls, constraints)
        print(result)
    
    def test_single_request_with_constraints(self):
        # test case with a single request and constraints
        message = "Please clone https://github.com/tsavo/image-processor, specifically the main branch. Then scan it for viruses."
        cls = MessageClassification
        constraints = {"intent": ["Ask a question about the president",
                                  "Open a file",
                                  "Choose a hat to wear",
                                  "Clone a git repository",
                                  "Eat soup for lunch",
                                  "Delete a git repository",
                                  "None of the above"]}
        result = transformer.transform_string(message, cls, constraints)
        assert(len(result) > 0)
        assert(isinstance(result[0], MessageClassification))
        assert(result[0].intent == "Clone a git repository")
        assert(result[0].original_message == message)
        assert(len(result[0].justifications_for_reply) > 0)
        print(result)
if __name__ == '__main__':
    unittest.main()