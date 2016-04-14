# Trello to Youtrack migration script

The scripts here to provide a way to import from Trello to Youtrack as easy and as quick as possible

## Usage

Edit 'mapping.json' to your own needs and supply your own credentials

The rules for this file:
- All required fields should be there which are:
    - trello.key
    - trello.token
    - youtrack.login
    - youtrack.password
    - youtrack.link
    - trello.board
    - trello.list
    - youtrack.project
    - youtrack.startNumberInProject"
- Some general information
    - youtrack.subsystem
    - users
    - comments
    - attachments
- Mappings
    - You can map field to field, or field to static value
    - The key field has to be youtrack and field value to be trello only
    - You can map to static values best on conditions with value of key as a dictionary
where values are the keys and the values are object containing the conditions, check 'mapping.json' for example.
    - Keys:
        - youtrack.summary
        - youtrack.description
        - youtrack.state
        - youtrack.type
        - trello.name
        - trello.desc
        - trello.closed

How to run:

	$ python TrelloToYoutrack.py



To get Trello key and token:

from here: https://trello.com/1/appKey/generate

the key available at the top and the token you have to request it -only avaiable for certain period of time-
then after allowing it will appear in the link at the bottom most of the page

Dependencies:

- requests


Please report any wanted feature or any inconvenience :)
