# Pinecone_TheDefibs
This is a repository for the Pinecone Hackathon submission for Team: The Defibrillators

#  HeartQuest

HeartQuest is a unique game recommendation system that utilizes machine learning to provide personalized game recommendations. It includes a fun, interactive game, and after completion, the system will recommend similar games you might enjoy.

## Features

### Interactive gameplay

Personalized game recommendations using advanced machine learning

### Getting Started

To run the scripts included in this repository, you'll first need to clone it to your local machine. Once that's done, you can install the necessary Python libraries.

### Prerequisites

Ensure you have Python 3.7 or newer installed on your machine.

You will need the following Python libraries:

flask,
pinecone-client,
pandas,
numpy,
keras,
tensorflow

You can install them using pip:

pip install flask pinecone-client pandas numpy tensorflow keras

### Setup

The recommendation system requires an API key for the Pinecone machine learning service. For security reasons, this key is not included in the repository. You will need to sign up for a Pinecone account and obtain an API key. Once you have the key, you can enter it into the script where indicated.

Please note that due to a current issue with the Pinecone Python client during the compilation process, the executable version of the application (app.exe) only includes the interactive game and does not include the machine learning recommendation system.

However, you can still run the full functionality of HeartQuest (including the recommendation system) by running the Python scripts included in this repository. To do so, simply enter your Pinecone API key into the scripts as indicated, then run them using your Python interpreter.

### Usage

To play the game, execute the app.exe file.

To run the full application (including the game and the recommendation system), run the app.py script. Please ensure that all necessary files are in the same directory and that a valid Pinecone API key has been entered into the script.

If running the script for the first time, it may take a while to download the necessary machine learning models and data.
