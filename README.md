# TransformGPT

TransformGPT is a python library for interpreting unstructured (or structured) data into Python objects using ChatGPT. Given a Python class hierarchy, it can take arbitrary data and structure in into the class hierarchy as a series of objects. This is useful for convertung natural language into structured data, or for converting one data type into another without specifying the mapping schema.

## Installation:

```
pip install transformgpt
```

### Optional:
Set an environment variable called ```OpenAIAPI-Token``` to your OpenAI API token.

## Command line:
```
usage: transformgpt [-h]
                    [-k KEY]
                    [-m MODEL]
                    [-t TEMPERATURE]
                    description
```

KEY: OpenAI API Token if it's not set as an environment variable.
MMDEL: OpenAI Model, defaults to 'gpt-3.5-turbo'
TEMPERATURE: Temperature for the ChatCompletion, defaults to 0, increase towards 1 to make the answers more creative
Description: A description of how you want the data to be transformed.

Takes input from STDIN and returns on STDOUT the transformed data.

### Example:
```
> echo "Hello World.\nHow are you today?\nI am fine.\nIf you don't respond I will blackmail you." | transformgpt "An object with the fields original_message, intent, and response, where intent is one of greeting, inquiry, response, threat, informative."    
```

#### Yields:
```yaml
- original_message: "Hello World."
  intent: greeting
  response: "Hi there!"

- original_message: "How are you today?"
  intent: inquiry
  response: "I'm doing well, thank you. How about 
you?"

- original_message: "I am fine."
  intent: response
  response: "Glad to hear that!"

- original_message: "If you don't respond I will blackmail you."
  intent: threat
  response: "I'm sorry, I didn't mean to ignore you. Is there something you need help with?"
```

### Python usage:

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

#### Yields:
```
Message(message="Tell Joey Tracy is cheating on him with the maid.", data={"Orange": "The new black.", "The only way to get the job done": "Do it yourself."})
```

### Datalasses/Nested Structures

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

#### Yields:

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

### It also supports transforming one object into another:

```python

result = transformer.transform_object(myListOfObjects, MyDataTypeToTransformInto) #Returns a list[MyDataTypeToTransformInto]
```
