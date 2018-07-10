# Articulate Agent Translator

This is a python utility for translating and importing existing agents defined in Rasa NLU data format (as well as a couple others) to Samtec SPG Articulate conversational agent.

## Getting Started

This utility was developed with Python 3 and utilizes argparse. The following yields usage documentation:

```
$ python -m agent_data_converter -h

usage: agent_data_converter.py [-h] [--host HOST] [--language LANGUAGE]
                               file agent_name

Import an agent in a supported format to Articulate.

positional arguments:
  file                 File to import
  agent_name           Name to be assigned to the imported agent

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          Host running Articulate if not localhost.
  --language LANGUAGE  Language of the agent

```

Running the following command from the top level directory will run the script. 

```
$ python -m agent_data_converter './data/examples/rasa/demo-rasa.json' agent_smith
```

## Acknowledgments

* This work was derived directly from the Rasa NLU code base.



