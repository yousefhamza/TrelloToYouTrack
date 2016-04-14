from TtY.Migration import Migration
from TtY.Trello import Trello
from TtY.YouTrack import YouTrack


def main():
    with Migration("mapping.json", "specs.json") as migration_dict:

        attachments = migration_dict["attachments"] if migration_dict["attachments"] else False
        users = migration_dict["users"] if migration_dict["users"] else False
        comments = migration_dict["comments"] if migration_dict["comments"] else False

        trello_client = Trello(migration_dict["trello.key"], migration_dict["trello.token"],
                               migration_dict["trello.board"], migration_dict["trello.list"],
                               attachments=attachments, users=users, comments=comments)

        youtrack_client = YouTrack(migration_dict["youtrack.login"], migration_dict["youtrack.password"],
                                   migration_dict["youtrack.link"], migration_dict["youtrack.project"])

        if users:
            youtrack_client.import_users(trello_client.get_users())

        cards = trello_client.get_cards()
        youtrack_client.import_issues(cards, migration_dict["mappings"],
                                      int(migration_dict["youtrack.startNumberInProject"]),
                                      attachments=attachments, comments=comments)
if __name__ == "__main__":
    main()
