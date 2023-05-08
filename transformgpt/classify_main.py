import argparse
import os
import sys
import openai
from transformgpt.transformgpt import TransformGPT, DataType

def main():
    parser = argparse.ArgumentParser(description='Transform input string to YAML gives a description of the desired output.')
    parser.add_argument('categories', type=str, help='A comma seperated list of possible classification categories.')
    parser.add_argument('-k', '--key', type=str, default="", help='OpenAI API key (or set OpenAIAPI-Token environment variable)')
    parser.add_argument('-m', '--model', type=str, default='gpt-3.5-turbo', help='OpenAI model to use')
    parser.add_argument('-t', '--temperature', type=float, default=0, help='OpenAI temperature')
    args = parser.parse_args()

    # Read input from stdin
    message = sys.stdin.read()

    openai.api_key = args.key if args.key else os.getenv("OpenAIAPI")
    transformer = TransformGPT(openai.ChatCompletion)
    categories = args.categories.split(",")
    categories = [category.strip() for category in categories]
    result = transformer.classify_string(message, categories, model=args.model, temperature=args.temperature)
    print(result)

if __name__ == '__main__':
    main()