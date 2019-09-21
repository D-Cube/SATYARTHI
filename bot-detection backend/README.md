# twitter-bot-detection

## Install

  * Update the configuration file `config\app_config.py.dist` and rename it to `config\app_config.py`
  * Install the dependencies `pip install -r requirements.txt`
    
## Usage

One script is used to import the data `import.py` and the other is used to generate the report `report.py`.

```shell
# drop/create the database and import all the tweets from the user FranckBrignoli
$ python import.py FranckBrignoli --create-db  

# import all the tweets from FranckBrignoli and his followers
$ python import.py FranckBrignoli --followers 

# import all the tweets from the user LOUDBOT and flag it as bot
$ python import.py LOUDBOT --is-bot 

# generate report
$ python report.py
```
