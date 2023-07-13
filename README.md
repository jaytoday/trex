# Trex

### _Transform unstructured to structured data_

Trex transforms your unstructured to structured data—just specify a regex or context free grammar and we'll intelligently ensure your data conforms to that schema.

## Installation

To install the Python client:

```bash
pip install git+https://github.com/automorphic-ai/trex.git
```

## Usage

To use Trex, you'll need an API key, which you can get by signing up for a free account at [automorphic.ai](https://automorphic.ai).

```python
import trex

tx = trex.Trex('<YOUR_AUTOMORPHIC_API_KEY>')
prompt = '''generate a valid json object of the following format:

{
    "name": "string",
    "age": "number",
    "height": "number",
    "pets": pet[]
}

in the above object, name is a string corresponding to the name of the person, age is a number corresponding to the age of the person in inches as an integer, height is a number corresponding to the height of the person, and pets is an array of pets.

where pet is defined as:
{
    "name": "string",
    "species": "string",
    "cost": "number",
    "dob": "string"
}

in the above object name is a string corresponding to the name of the pet, species is a string corresponding to the species of the pet, cost is a number corresponding to the cost of the pet, and dob is a string corresponding to the date of birth of the pet.

given the above, generate a valid json object containing the following data: one human named dave 30 years old 5 foot 8 with a single dog pet named 'trex'. the dog costed $100 and was born on 9/11/2001.
'''

custom_grammar = r"""
    ?start: json_schema

    json_schema: "{" name "," age "," height "," pets "}"

    name: "\"name\"" ":" ESCAPED_STRING
    age: "\"age\"" ":" NUMBER
    height: "\"height\"" ":" NUMBER
    pets: "\"pets\"" ":" "[" [pet ("," pet)*] "]"

    pet: "{" pet_name "," species "," cost "," dob "}"
    pet_name: "\"name\"" ":" ESCAPED_STRING
    species: "\"species\"" ":" ESCAPED_STRING
    cost: "\"cost\"" ":" NUMBER
    dob: "\"dob\"" ":" ESCAPED_STRING

    %import common.ESCAPED_STRING
    %import common.NUMBER
    %import common.WS

    %ignore WS
"""

print(tx.generate_cfg(prompt, cfg=custom_grammar, language='json').response)
# the above produces:
# {
#     "name": "dave",
#     "age": 30,
#     "height": 58,
#     "pets": [
#         {
#             "name": "trex",
#             "species": "dog",
#             "cost": 100,
#             "dob": "2001-09-11"
#         }
#     ]
# }
```

## Roadmap

- [x] Structured JSON generation
- [x] Structured custom CFG generation
- [x] Structured custom regex generation
- [ ] SIGNIFICANT speed improvements (in progress)
- [ ] Auto-prompt generation for unstructured ETL
- [ ] More intelligent models

Join our [Discord](https://discord.gg/E8y4NcNeBe) or [email us](mailto:founders@automorphic.ai), if you're interested in or need help using Trex, have ideas, or want to contribute.

Follow us on [Twitter](https://twitter.com/AutomorphicAI) for updates.
