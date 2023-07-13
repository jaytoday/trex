# -*- coding: utf-8 -*-
import os
import requests
from dataclasses import dataclass

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
            json={"prompt": prompt, "cfg": Trex.JSON_GRAMMAR, "max_tokens": max_tokens, "language": "json"},
        )
        response_json = response.json()
        return TrexResponse(response=response_json['response'], tokens=response_json['tokens'])
    
    def generate_regex(self, prompt: str, regex: str, max_tokens: int = 512) -> TrexResponse:
        """
        Generate data in valid JSON.

        :param prompt: The prompt / instructions / guidelines to follow when generating the data.
        :param max_tokens: The maximum number of tokens to generate. Defaults to 512.
        """
        response = requests.post(
            f"{Trex.BASE_URL}/generate",
            headers={"X-API-Key": self.api_key},
            json={"prompt": prompt, "regex": regex, "max_tokens": max_tokens, "language": "json"},
        )
        response_json = response.json()
        return TrexResponse(response=response_json['response'], tokens=response_json['tokens'])