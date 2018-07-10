import training_data as td
import json
import requests
import argparse

## Demo of the Training_data object

# rasajs = r'./data/examples/rasa/demo-rasa.json'
# rasamd = r'./data/examples/rasa/demo-rasa.md'
# wit = r'./data/examples/wit/demo-flights.json'
#
# rasajstd = td.load_data(rasajs)
# rasamdtd = td.load_data(rasamd)
# wittd = td.load_data(wit)
# print("==============================")
# print(rasajstd.entities)
# print("==============================")
# print(rasajstd.intents)
# print("==============================")
# x1 = [te.as_dict() for te in rasajstd.training_examples]
# print(json.dumps(x1, indent = 4))
#
#
# print("==============================")
# print(rasamdtd.entities)
# print("==============================")
# print(rasamdtd.intents)
# print("==============================")
# x2 = [te.as_dict() for te in rasamdtd.training_examples]
# print(json.dumps(x2, indent = 4))
#
# print("==============================")
# print(wittd.entities)
# print("==============================")
# print(wittd.intents)
# print("==============================")
# x3 = [te.as_dict() for te in wittd.training_examples]
# print(json.dumps(x3, indent = 4))

def parse_args():
    parser = argparse.ArgumentParser(description='Import a model in a supported format to Articulate.')
    parser.add_argument('file', help='File to import')
    parser.add_argument('agent_name', help='Name to be assigned to the imported agent')
    parser.add_argument('--host', help='Host running articulate if not local host.')
    parser.add_argument('--language', help='Language of the agent')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    training_data = td.load_data(args.file)

    data = {
                "agentName": args.agent_name,
                "description": "string",
                "language": "en",
                "timezone": "string",
                "domainClassifierThreshold": 0,
                "fallbackResponses": [
                    "string"
                ],
                "useWebhook": True,
                "usePostFormat": True,
                "postFormat": {
                    "postFormatPayload": "string"
                },
                "status": "Why must this be a string?",
                "lastTraining": "2018-07-10",
                "extraTrainingData": True,
                "enableModelsPerDomain": True,
                "model": "Why must this be a string?",

                ## why must this be here what webhook applies globally?
                "webhook": {
                    "webhookUrl": "string",
                    "webhookVerb": "GET",
                    "webhookPayloadType": "None",
                    "webhookPayload": "string"
                },

                ## What settings?
                "settings": {

                },

                ## Need to get this from the training data.
                "entities": [
                    {
                        "entityName": "string",
                        "uiColor": "string",
                        "type": "learned",
                        "regex": "string",
                        "examples": [
                            {
                                "value": "string",
                                "synonyms": [
                                    "string"
                                ]
                            },
                            {
                                "value": "string2",
                                "synonyms": [
                                    "string2"
                                ]
                            }
                        ]
                    }
                ],
                "domains": [
                    {
                        "domainName": "string",
                        "enabled": True,
                        "intentThreshold": 0,
                        "lastTraining": "2018-07-10",
                        "model": "string",
                        "status": "string",
                        "extraTrainingData": True,
                        "intents": [
                            {
                                "intentName": "string",
                                "examples": [
                                    {
                                        "userSays": "string",
                                        "entities": [
                                            {
                                                "start": 0,
                                                "end": 0,
                                                "value": "string",
                                                "entity": "string",
                                                "extractor": "string"
                                            }
                                        ]
                                    },
                                    {
                                        "userSays": "string",
                                        "entities": [
                                            {
                                                "start": 0,
                                                "end": 0,
                                                "value": "string",
                                                "entity": "string",
                                                "extractor": "string"
                                            }
                                        ]
                                    }
                                ],
                                "scenario": {
                                    "scenarioName": "string string",
                                    "slots": [
                                        {
                                            "slotName": "string",
                                            "entity": "string",
                                            "isList": True,
                                            "isRequired": True,
                                            "textPrompts": [
                                                "string"
                                            ]
                                        }
                                    ],
                                    "intentResponses": [
                                        "string"
                                    ]
                                },
                                "useWebhook": True,
                                "webhook": {
                                    "webhookUrl": "string",
                                    "webhookVerb": "GET",
                                    "webhookPayloadType": "None",
                                    "webhookPayload": "string"
                                },
                                "usePostFormat": True,
                                "postFormat": {
                                    "postFormatPayload": "string"
                                }
                            }
                        ]
                    }
                ]
            }

    response = requests.post('http://localhost:7500/agent/import', data=json.dumps(data))
    print(json.dumps(json.loads(response.text), indent=4))