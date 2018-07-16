import training_data as td
import json
import requests
import argparse
from pathlib import Path
import uuid

uuid.uuid4()
import os

print(os.getcwd())


## Path to demo files.

# rasajs = r'./data/examples/rasa/demo-rasa.json'
# rasamd = r'./data/examples/rasa/demo-rasa.md'
# wit = r'./data/examples/wit/demo-flights.json'
#

def parse_args():
    parser = argparse.ArgumentParser(description='Convert an agent to articulate format.')
    parser.add_argument('file', help='File to import')
    parser.add_argument('agent_name', help='Name to be assigned to the imported agent')
    parser.add_argument('description', help='A description of the agent')
    parser.add_argument('--host', help='Host running Articulate')
    parser.add_argument('-o', '--out', help='File to which to save the converted agent')
    parser.add_argument('--language',
                        help="Language of the agent, can be one of 'en', 'es', 'fr', 'de', 'pt'. Default is 'en'.",
                        default='en')

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    # initial arg processing

    if args.out:
        if Path(args.out).exists():
            raise Exception(args.out + " already exists.")
    if args.language:
        if args.language not in ('en', 'es', 'fr', 'de', 'pt'):
            raise Exception(args.language + " is not a supported language")

    # load file

    training_data = td.load_data(args.file)

    # functions to populate JSON REST elements from training data.

    def intent_dict(intent):

        # set defaults
        intent_dict = {"useWebhook": False, "usePostFormat": False}

        # populate the intent name
        intent_dict['intentName'] = intent

        # if there are examples, create a dictionary entry
        intent_examples = [ex for ex in training_data.intent_examples if ex.data['intent'] == intent]
        if len(intent_examples) > 0:
            intent_dict['examples'] = []

        # iterate through the examples, output needs to be a list
        # each element in output is a dictionary containing entities list and userSays
        # 'example' in training data is a Message object which has relevant properties: 'data' and 'text'

        for example in intent_examples:

            # get only the examples for this intent
            if example.data['intent'] == intent:

                example_dict = {}
                example_dict['userSays'] = example.text

                # needs to be a list, not all examples have entities
                if 'entities' in example.data:
                    example_dict['entities'] = example.data['entities']
                    for each in example.data['entities']:
                        each['extractor'] = 'string'
                else:
                    example_dict['entities'] = []

                # plug in the example to the dict
                intent_dict['examples'].append(example_dict)

        return intent_dict

    def intents_list(): # return the list for inclusion in JSON structure
        intent_list = []

        for intent in list(training_data.intents):
            intent_list.append(intent_dict(intent))
        return intent_list

    def entity_dict(entity):
        entity_dict = {   "entityName": entity,
                            "uiColor": "string",
                            "type": "learned",
                            "examples":[]
         }

        print ("XAMPLE +++++++++++++++++++++++++++\n")
        print(training_data.entity_examples)

        for example in training_data.entity_examples:
            print ("XAMPLE2 +++++++++++++++++++++++++++\n")
            print(example.data['entities'])
            for each in example.data['entities']:
                if each['entity']== entity:
                    entity_dict['examples'].append({'value': each['value']})

        return entity_dict

    def entities_list():

        entities_list = []

        for entity in list(training_data.entities):
            entities_list.append(entity_dict(entity))

        return  entities_list##training_data.entity_examples.data.entities

    settings = {
        "domainClassifierPipeline": [
            {
                "name": "nlp_spacy"
            },
            {
                "name": "tokenizer_spacy"
            },
            {
                "name": "intent_featurizer_spacy"
            },
            {
                "name": "intent_classifier_sklearn"
            }
        ],
        "intentClassifierPipeline": [
            {
                "name": "nlp_spacy"
            },
            {
                "name": "tokenizer_spacy"
            },
            {
                "name": "intent_featurizer_spacy"
            },
            {
                "name": "ner_crf"
            },
            {
                "name": "ner_synonyms"
            },
            {
                "name": "intent_classifier_sklearn"
            },
            {
                "name": "ner_spacy"
            }
        ],
        "entityClassifierPipeline": [
            {
                "name": "nlp_spacy"
            },
            {
                "name": "tokenizer_spacy"
            },
            {
                "name": "ner_crf"
            },
            {
                "name": "ner_synonyms"
            },
            {
                "name": "ner_spacy"
            }
        ],
        "rasaURL": "http://rasa:5000",
        "ducklingURL": "http://duckling:8000",
        "ducklingDimension": [
            "amount-of-money",
            "distance",
            "duration",
            "email",
            "number",
            "ordinal",
            "phone-number",
            "quantity",
            "temperature",
            "time",
            "url",
            "volume"
        ],
        "spacyPretrainedEntities": [
            "PERSON",
            "NORP",
            "FAC",
            "ORG",
            "GPE",
            "LOC",
            "PRODUCT",
            "EVENT",
            "WORK_OF_ART",
            "LAW",
            "LANGUAGE",
            "DATE",
            "TIME",
            "PERCENT",
            "MONEY",
            "QUANTITY",
            "ORDINAL",
            "CARDINAL"
        ]
    }

    # populate JSON data object

    data = {
        "status": "Out of Date",
        "usePostFormat": False,
        "description": args.description,
        "language": args.language,
        "settings": settings,
        "enableModelsPerDomain": True,
        "domainClassifierThreshold": 0.5,
        "extraTrainingData": False,
        "entities": entities_list(),
        "useWebhook": False,
        "agentName": "aaaaaa" + str(uuid.uuid4()),
        "domains": [  ##I haven't see other systems with the concept of domains so this is new
            {
                "status": "Out of Date",  ##Same that agent status, "Out of Date" by default
                "intents": intents_list(),

                "intentThreshold": 0.5,
                "domainName": args.agent_name + "_DefaultDomain",
                "enabled": True,
                "extraTrainingData": False
            }
        ],
        "timezone": "UTC",
        "fallbackResponses": [
            "I didn't understand that. Can you say it in a different way?"
        ]
    }

    # Write out the agent to the file if that was requested.

    if args.out:
        try:
            with open("DeleteMe/aaaaaa" + str(uuid.uuid4()), 'w') as f:
                f.write(json.dumps(data, indent=4))
            print("\nSuccessfully wrote agent to file: " + args.out)

        except Exception as e:
            print("\nWriting to file " + args.out + " was unsuccessful.")
            print("\n" + json.dumps({"error": "{}".format(e)}, indent=4))

    # Try to import the agent to a running server if that was requested

    if args.host:

        try:
            response = requests.post('http://' + args.host + ':7500/agent/import', data=json.dumps(data))
            if response.status_code is 200:
                print("\nImport to host '" + args.host + "' was successful")
            else:
                print("\nImport to host '" + args.host + "' was unsuccessful:" + response.text)

        except Exception as e:

            print("\n" + json.dumps({"error": "{}".format(e)}, indent=4))

    print(json.dumps(data, indent=4))
