# -*- coding: utf-8 -*-
import os
import requests


class Trex:
    """Trex API client."""

    BASE_URL = "https://api.automorphic.ai/trex"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TREX_API_KEY")
        if not self.api_key:
            raise ValueError(
                "TREX_API_KEY must be set in the environment or passed into the client."
            )

    def restructure_to_cfg(self, data: str, prompt: str, context_free_grammar: str):
        """
        Restructure some data to conform to a [lark](https://github.com/lark-parser/lark) context free grammar.

        :param data: The data to restructure.
        :param prompt: The prompt / instructions / guidelines to follow when restructuring the data.
        :param context_free_grammar: The context free grammar to conform to (specified as a lark DSL).
        """
        response = requests.post(
            f"{Trex.BASE_URL}/restructure",
            headers={"X-API-Key": self.api_key},
            json={"data": data, "prompt": prompt, "cfg": context_free_grammar},
        )
        return response.json()

    def restructure(self, data: str, prompt: str, regex_pattern: str):
        """
        Restructure some data to conform to a regex pattern.

        :param data: The data to restructure.
        :param prompt: The prompt / instructions / guidelines to follow when restructuring the data.
        :param regex_schema: The regex schema to conform to.
        """
        try:
            import re

            re.compile(regex_pattern)
        except re.error:
            raise ValueError("Invalid regex pattern provided.")

        response = requests.post(
            f"{Trex.BASE_URL}/restructure",
            headers={"X-API-Key": self.api_key},
            json={"data": data, "prompt": prompt, "regex": regex_pattern},
        )
        return response.json()
