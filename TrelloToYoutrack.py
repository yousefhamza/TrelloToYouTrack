# coding=UTf-8
from TtY.Migration import Migration
from TtY.Trello import Trello
from TtY.YouTrack import YouTrack


def main():
    with Migration("mapping.json", "specs.json") as migration_dict:

        attachments = migration_dict.get("attachments", False)
        users = migration_dict.get("users", False)
        comments = migration_dict.get("comments", False)

        trello_client = Trello(migration_dict["trello.key"], migration_dict["trello.token"],
                               migration_dict["trello.board"], migration_dict["trello.list"],
                               attachments=attachments, users=users, comments=comments)

        youtrack_client = YouTrack(migration_dict["youtrack.login"], migration_dict["youtrack.password"],
                                   migration_dict["youtrack.link"], migration_dict["youtrack.project"])

        if users:
            print 'Loading users from trello...'
            trello_users = trello_client.get_users()
            print '√ Done loading users\n'

            print 'Importing users to Youtrack...'
            youtrack_client.import_users(trello_users)
            print '√ Done importing users\n'

        print 'Loading cards from trello...'
        trello_cards = trello_client.get_cards()
        print '√ Done loading cards\n'

        print 'Importing issues to Youtrack...'
        youtrack_client.import_issues(trello_cards, migration_dict["mappings"],
                                      int(migration_dict["youtrack.startNumberInProject"]),
                                      attachments=attachments, comments=comments)
        print '√ All done!'
if __name__ == "__main__":
    main()
