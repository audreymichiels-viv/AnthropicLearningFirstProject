**Setup (one time)**

`cd /Users/audrey.michiels/Documents/Projects/AnthropicLearningFirstProject`

`python3 -m venv venv`               # create an isolated Python environment

`source venv/bin/activate`           # activate it

`pip install -r requirements.txt`    # install the anthropic library

`export ANTHROPIC_API_KEY="xxx"`   # paste your real API key here

**Run it**

`python main.py "Je voudrais un café s'il vous plait"`

You should see something like:

Original language: French

Corrected: Je voudrais un café, s'il vous plaît.

Translation: I would like a coffee, please.

Try also: `python main.py "I goed to the store yesterday" to see the correction in action.`
