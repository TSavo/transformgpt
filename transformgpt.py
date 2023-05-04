from __future__ import annotations
from typing import Any, Generator, List, Optional, Type
import yaml
from source_utils import DataType, deserialize, get_source
default_model = "gpt-3.5-turbo"

#define a type alias for a callable that takes a list of dictionaries and returns a string
from typing import Optional, List, Protocol

class ChatCompletion(Protocol):
    @classmethod
    def create(cls, *args, **kwargs) -> Generator[None | list[Any] | dict[Any, Any], None, None] | None | list[Any] | dict[Any, Any]:
        pass

class TransformGPT:
    def __init__(self, chatCompletion : ChatCompletion, model=default_model):
        self.chatCompletion = chatCompletion
        self.model = model

    def __get_chat_completion(self, messages : list[dict[str,str]], model:Optional[str]=None, temperature=0, **kwargs) -> str:
        if model is None:
            model = self.model
        response = self.chatCompletion.create(
                messages=messages,
                model=model,
                temperature=temperature,
                **kwargs)
        if response is None:
            raise Exception("No response from OpenAI")
        return response.choices[0]['message']['content'] # type: ignore

    @staticmethod
    def __get_body(message : str) -> str:
        try:
            message = message.split('```')[1]
            if message.lower().startswith('yaml'):
                message = message[4:]
            return message.strip()
        except:
            return message.strip()


    def transform_raw(self, message: str, description:str, constraints:dict[str, List[Any]] = {}, **kwargs) -> str:
        con = "".join((f"The \"{k}\" parameter MUST be of the following values:\n```yaml\n"
                    + "\n".join(f"- {str(x)}" for x in v)
                    + "\n```\n")
                    for k, v in constraints.items())
        convo = [{"role": "system", "content": "You are a helpful AI assistant who knows how to extract structured data from a message or messages, and return the results as a blockquoted yaml array of object shaped dictionaries, one for each part of what is said."}]
        convo += [{"role": "system", "content": "The message may contain multiple requests, in which case you should return an object for each portion of the message."}]
        convo += [{"role":"system","content": description}]
        if constraints:
            convo += [{"role":"system","content": f"Here are the required values for the parameters:\n{con}"}]
        convo += [{"role": "user", "content": f'Please convert the following into a blockquoted YAML array of dictionaries that follows the above constraints: "{message}"\n'}]
        return self.__get_body(self.__get_chat_completion(convo, **kwargs))

    def transform_string(self, message: str, cls: Type[DataType], constraints:dict[str, List[Any]] = {}, **kwargs) -> List[DataType]:
        return deserialize(self.transform_raw(message, f"Here are the Python classes that the YAML object must deserialize to:\n```python\n{get_source(cls)}\n```\nThe main class to start with is: {cls.__name__}\n", constraints, **kwargs), cls)
        
    def transform_object(self, obj : Any, cls: Type[DataType], constraints:dict[str, List[Any]] = {}, **kwargs) -> List[DataType]:
        return deserialize(self.transform_string(f"```yaml\n{yaml.dump(obj)}\n```\n", cls))
        