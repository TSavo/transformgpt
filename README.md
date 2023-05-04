TransformGPT is a python library for interpreting unstructured (or structured) data into Python objects using ChatGPT. Given a Python class hierarchy, it can take arbitrary data and structure in into the class hierarchy as a series of objects. This is useful for convertung natural language into structured data, or for converting one data type into another without specifying the mapping schema.

For example:

```python
import transformgpt
import openai
import os

openai.api_key = "YOUR OPENAI TOKEN"
transformer = transformgpt.TransformGPT(openai.ChatCompletion)

class Message:
    def __init__(self, message: str, data : dict[str, str]):
        self.message = message
        self.data = data

incoming_message = "The message is tell Joey Tracy is cheating on him with maid. The data to include is Orange is the new black, and the only way to get the job done is to do it yourself."

print(transformer.transform_string(incoming_message, Message))
```

Yields:
```
Message(message="Tell Joey Tracy is cheating on him with the maid.", data={"Orange": "The new black.", "The only way to get the job done": "Do it yourself."})
```

It handles @dataclasses, and nested class hierarcharies as well:

```python
from __future__ import annotations
from dataclasses import dataclass
import dataclasses
from typing import List, Optional
import openai
import os
import transformgpt
import yaml

openai.api_key = "YOUR OPENAI TOKEN"
transformer = transformgpt.TransformGPT(openai.ChatCompletion)

@dataclass
class MessageClassification:
  original_message:str
  message_part:str
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

incoming_message = "The message is tell Joey Tracy is cheating on him with maid. The data to include is Orange is the new black, and the only way to get the job done is to do it yourself."

print(yaml.dump(transformer.transform_string(incoming_message, MessageClassification)))
```

Yields:

```
- !!python/object:__main__.MessageClassification
  categories:
  - Relationships
  - Infidelity
  follow_up_items:
  - !!python/object:__main__.MessageClassification
    categories:
    - Entertainment
    - Motivation
    follow_up_items: []
    intent: null
    justifications_for_reply:
    - !!python/object:__main__.Justification
      action: null
      description: Orange is the new black is a popular TV show.
      intent: null
      object: null
      subject: null
    - !!python/object:__main__.Justification
      action: null
      description: Doing it yourself is the best way to ensure it gets done right.
      intent: null
      object: null
      subject: null
    message_part: The data to include is Orange is the new black, and the only way
      to get the job done is to do it yourself.
    original_message: The data to include is Orange is the new black, and the only
      way to get the job done is to do it yourself.
    parameters: []
    reply: null
  intent: null
  justifications_for_reply:
  - !!python/object:__main__.Justification
    action: null
    description: null
    intent: Cheating
    object: Joey
    subject: Tracy
  - !!python/object:__main__.Justification
    action: Involved in cheating
    description: null
    intent: null
    object: null
    subject: Maid
  message_part: Tell Joey Tracy is cheating on him with maid.
  original_message: The message is tell Joey Tracy is cheating on him with maid.
  parameters: []
  reply: null
  ```

