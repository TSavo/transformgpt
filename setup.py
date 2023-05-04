from setuptools import setup, find_packages
setup(
    name='transformgpt',
    version='0.0.1',
    packages=find_packages(),
    author='T Savo',
    author_email="evilgenius@nefariousplan.com",
    description="A library for transforming unstructured text into structured data without context/mappings using ChatGPT.",
    long_description="A library for transforming unstructured text into structured data without context/mappings using ChatGPT.",
    keywords="openai gpt3 chatgpt nlp chatbot transformers structruing text",
    url="https://github.com/TSavo/transformgpt",
    requires=["openai"],
)