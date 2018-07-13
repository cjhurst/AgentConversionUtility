import training_data as td
import json
import requests
import argparse
from pathlib import Path

## Path to demo files.

# rasajs = r'./data/examples/rasa/demo-rasa.json'
# rasamd = r'./data/examples/rasa/demo-rasa.md'
# wit = r'./data/examples/wit/demo-flights.json'
#

def parse_args():
    parser = argparse.ArgumentParser(description='Convert an agent to articulate format.')
    parser.add_argument('file', help='File to import')
    parser.add_argument('agent_name', help='Name to be assigned to the imported agent')
    parser.add_argument('--host', help='Host running Articulate')
    parser.add_argument('-o', '--out', help='File to which to save the converted agent' )
    parser.add_argument('--language', help='Language of the agent')
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()

    # initial arg processing

    if args.out:
        if Path(args.out).exists():
            raise Exception(args.out + " already exists.")

    # load file

    training_data = td.load_data(args.file)

    # fill out the rest call

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

                ## why must this be here? what webhook applies globally?
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

    # Write out the agent to the file if that was requested.

    if args.out:
        try:
            with open(args.out, 'w') as f:
                f.write(json.dumps(data, indent=4))
            print("Successfully wrote agent to file: " + args.out )

        except Exception as e:
            print(json.dumps({"error": "{}".format(e)}, indent=4))

    # Try to import the agent to a running server if that was requested

    if args.host:

        try:
            response = requests.post('http://' + args.host + ':7500/agent/import', data=json.dumps(data))
            if response.status_code is 200:
                print("Import to host '" + args.host + "' was successful")
            else:
                print("Import to host '" + args.host + "' was unsuccessful: \n " + response.text)

        except Exception as e:

            print(json.dumps({"error": "{}".format(e)}, indent=4))

    print(json.dumps(data, indent=4))


