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
    parser.add_argument('description', help='A description of the agent')
    parser.add_argument('--host', help='Host running Articulate')
    parser.add_argument('-o', '--out', help='File to which to save the converted agent')
    parser.add_argument('--language', help="Language of the agent, can be one of 'en', 'es', 'fr', 'de', 'pt'. Default is 'en'.", default='en')

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

    # fill out the rest call

    data =  {
    "status": "Out of Date",
    "usePostFormat": False,
    "description": args.description,
    "language": args.language,
    "settings": {},
    "enableModelsPerDomain": True,
    "domainClassifierThreshold": 0.5,
    "extraTrainingData": False,
    "entities": [
        {
            "uiColor": "string",
            "regex": "string",
            "entityName": "string",
            "type": "learned",
            "examples": [
                {
                    "synonyms": [
                        "string"
                    ],
                    "value": "string"
                },
                {
                    "synonyms": [
                        "string2"
                    ],
                    "value": "string2"
                }
            ]
        }
    ], ##You need to import this values form the training data
    "useWebhook": False,
    "agentName": args.agent_name,
    "domains": [ ##I haven't see other systems with the concept of domains so this is new
        {
            "status": "Out of Date", ##Same that agent status, "Out of Date" by default
            "intents": [ ##I was expecting the intents of the file I sent to the conversion tool here
                {
                    "scenario": { ##Scenario is how the agent will respond if this scenario happens
                        "slots": [ ##Systems like Dialogflow have this element, we should import that, I will explain the attributes of an slot
                            {
                                "isRequired": True, ##If the slots must be filled
                                "textPrompts": [
                                    "string" ##What the agent should ask if the slot is not filled. In example, if your order a pizza without toppings, then a value here will be "What toppings would you like"
                                ],
                                "slotName": "string", ##The slot name given by the user in other system
                                "isList": True, ##If the slot could take the form of a list, like toppings: chicken, mushrooms, and ham
                                "entity": "string" ##The entity that is going to fill this slot
                            }
                        ],
                        "intentResponses": [
                            "string" ##These are the responses from the agent, like "Cool, I will prepare your pizza", or, "Hi, how are you?"
                        ],
                        "scenarioName": "string string" ## By default use the same name that was given to the intent
                    },
                    "useWebhook": False,
                    "intentName": "string", ##The intent given by the user in the input file
                    "examples": [ ##These are the examples, basically the training data
                        {
                            "entities": [
                                {
                                    "start": 0,
                                    "extractor": "string",
                                    "end": 0,
                                    "value": "string",
                                    "entity": "string"
                                }
                            ],
                            "userSays": "string"
                        },
                        {
                            "entities": [
                                {
                                    "start": 0,
                                    "extractor": "string",
                                    "end": 0,
                                    "value": "string",
                                    "entity": "string"
                                }
                            ],
                            "userSays": "string"
                        }
                    ],
                    "usePostFormat": False
                }
            ],
            "intentThreshold": 0.5,
            "domainName": args.agent_name + "DefaultDomain",
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
            with open(args.out, 'w') as f:
                f.write(json.dumps(data, indent=4))
            print("\nSuccessfully wrote agent to file: " + args.out)

        except Exception as e:
            print("\nWriting to file " + args.out + " was unsuccessful.")
            print("\n"+json.dumps({"error": "{}".format(e)}, indent=4))

    # Try to import the agent to a running server if that was requested

    if args.host:

        try:
            response = requests.post('http://' + args.host + ':7500/agent/import', data=json.dumps(data))
            if response.status_code is 200:
                print("\nImport to host '" + args.host + "' was successful")
            else:
                print("\nImport to host '" + args.host + "' was unsuccessful:" + response.text)

        except Exception as e:

            print("\n"+json.dumps({"error": "{}".format(e)}, indent=4))

    print(json.dumps(data, indent=4))


