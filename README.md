# Articulate Agent Converter

This is a python utility for converting and importing existing agents defined in Rasa NLU data format (as well as a couple others) to Samtec SPG [Articulate](https://github.com/samtecspg/articulate) conversational agent.

## Getting Started

This utility was developed with Python 3 and utilizes Argparse. The following yields usage documentation:

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

Running the following command from the top level directory will run the script. The file below is an example file which should succeed as long as connecting to Articulate succeeds and you don't already have an agent of the same name.

```
$ python -m agent_data_converter './data/examples/rasa/demo-rasa.json' agent_smith
```

### Prerequisites

To take advantage of this tool, you will need to have an instance of [Articulate](https://github.com/samtecspg/articulate) running either locally or on a server accessible from the localhost.


## Acknowledgments

* This work was derived directly from the Rasa NLU code base.



