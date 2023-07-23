# -*- coding: utf-8 -*-
import os
import requests
from dataclasses import dataclass
from trex.exceptions import InvalidCFGError, InvalidRegexError, InvalidAPIKey

@dataclass
class TrexResponse:
    response: str
    tokens: int

class Trex:
    """Trex API client."""

    BASE_URL = "https://api.automorphic.ai/trex"
    JSON_GRAMMAR = r"""
                    ?start: object

                    ?value: object
                        | array
                        | string
                        | SIGNED_NUMBER      -> number
                        | "true"             -> true
                        | "false"            -> false
                        | "null"             -> null

                    array  : "[" [value ("," value)*] "]"
                    object : "{" [pair ("," pair)*] "}"
                    pair   : string ":" value

                    string : ESCAPED_STRING

                    %import common.ESCAPED_STRING
                    %import common.SIGNED_NUMBER
                    %import common.WS

                    %ignore WS
                """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("AUTOMORPHIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "AUTOMORPHIC_API_KEY must be set in the environment or passed into the client."
            )
        
    def generate(self, prompt: str, max_tokens: int = 512) -> TrexResponse:
        """
        Generate a completion without any restrictions.

        :param prompt: The prompt given to the model to generate the completion.
        :param max_tokens: The maximum number of tokens to generate. Defaults to 512.
        """
        response = requests.post(
            f"{Trex.BASE_URL}/generate",
            headers={"X-API-Key": self.api_key},
            json={"prompt": prompt, "max_tokens": max_tokens},
        )
        response_json = response.json()
        if response.status_code != 201:
            if response.status_code == 401:
                raise InvalidAPIKey(f'Invalid API Key: {self.api_key}')
            else:
                response.raise_for_status()
        return TrexResponse(response=response_json['response'], tokens=response_json['tokens'])
        
    def generate_cfg(self, prompt: str, cfg: str, language: str = None, max_tokens: int = 512) -> TrexResponse:
        """
        Generate data to conform to a [lark](https://github.com/lark-parser/lark) context free grammar.

        :param prompt: The prompt / instructions / guidelines to follow when generating the data.
        :param cfg: The context free grammar to generate data from (specified as a lark DSL).
        :param max_tokens: The maximum number of tokens to generate. Defaults to 512.
        """
        response = requests.post(
            f"{Trex.BASE_URL}/generate",
            headers={"X-API-Key": self.api_key},
            json={"prompt": prompt, "cfg": cfg, "language": language, "max_tokens": max_tokens},
        )
        response_json = response.json()
        if response.status_code != 201:
            message = response_json['detail']
            if 'Invalid cfg' in message:
                raise InvalidCFGError(message)
            elif response.status_code == 401:
                raise InvalidAPIKey(f'Invalid API Key: {self.api_key}')
            else:
                response.raise_for_status()
        return TrexResponse(response=response_json['response'], tokens=response_json['tokens'])


    def generate_json(self, prompt: str, max_tokens: int = 512) -> TrexResponse:
        """
        Generate data in valid JSON.

        :param prompt: The prompt / instructions / guidelines to follow when generating the data.
        :param max_tokens: The maximum number of tokens to generate. Defaults to 512.
        """
        response = requests.post(
            f"{Trex.BASE_URL}/generate",
            headers={"X-API-Key": self.api_key},
            json={"prompt": prompt, "cfg": Trex.JSON_GRAMMAR, "language": 'json', "max_tokens": max_tokens},
        )
        response_json = response.json()
        if response.status_code != 201:
            message = response_json['detail']
            if 'Invalid cfg' in message:
                raise InvalidCFGError(message)
            elif response.status_code == 401:
                raise InvalidAPIKey(f'Invalid API Key: {self.api_key}')
            else:
                response.raise_for_status()
        return TrexResponse(response=response_json['response'], tokens=response_json['tokens'])
    
    def generate_regex(self, prompt: str, regex: str, max_tokens: int = 512) -> TrexResponse:
        """
        Generate data to conform to a particular regex.

        :param prompt: The prompt / instructions / guidelines to follow when generating the data.
        :param max_tokens: The maximum number of tokens to generate. Defaults to 512.
        """
        response = requests.post(
            f"{Trex.BASE_URL}/generate",
            headers={"X-API-Key": self.api_key},
            json={"prompt": prompt, "regex": regex, "max_tokens": max_tokens},
        )
        response_json = response.json()
        if response.status_code != 201:
            message = response_json['detail']
            if 'Invalid regex' in message:
                raise InvalidRegexError(message)
            elif response.status_code == 401:
                raise InvalidAPIKey(f'Invalid API Key: {self.api_key}')
            else:
                response.raise_for_status()
        return TrexResponse(response=response_json['response'], tokens=response_json['tokens'])