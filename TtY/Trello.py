# coding=UTF-8
import requests


class Trello:
    def __init__(self, trello_key, trello_token, trello_board, trello_list,
                 attachments=False, users=False, comments=False):
        self.trello_key = trello_key
        self.trello_token = trello_token

        self.trello_board_id, self.trello_list_id = self._get_board_and_list_id(trello_board, trello_list)
        self.cards = None

        self.attachments = attachments
        self.users = users
        self.comments = comments

    def _get_board_and_list_id(self, board_name, list_name):
        request_url = 'https://api.trello.com/1/members/me/boards?fields=name&lists=all&list_fields=name?members=true' \
                      '&members_fields=&key=%s&token=%s' % (self.trello_key, self.trello_token)
        response = requests.get(request_url)

        boards = response.json()
        trello_board = [board for board in boards if board["name"] == board_name]
        if not trello_board:
            raise Exception("Board %s not found" % (board_name,))
        trello_board = trello_board[0]

        trello_list = [_list for _list in trello_board["lists"] if _list["name"] == list_name]
        if not trello_list:
            raise Exception("list %s not found in board %s", (list_name, board_name))
        trello_list = trello_list[0]

        return trello_board["id"], trello_list["id"]

    def get_users(self):
        users = []
        request_url = "https://api.trello.com/1/boards/%s/members?key=%s&token=%s" % (self.trello_board_id,
                                                                                      self.trello_key,
                                                                                      self.trello_token)
        response = requests.get(request_url)
        for user in response.json():
            member_request_url = "https://api.trello.com/1/members" \
                                 "/%s?fields=username,fullName,email,lala&key=%s&token=%s" % (user["username"],
                                                                                              self.trello_key,
                                                                                              self.trello_token)
            user_response = requests.get(member_request_url)
            user_dict = user_response.json()
            users.append({
                "username": user_dict["username"],
                "fullName": user_dict["fullName"],
                "email": user_dict["email"]
            })
        return users

    def get_cards(self):
        # Cache results
        if self.cards:
            return self.cards
        # TODO add fields from specs file
        request_url = "https://api.trello.com/1/lists/%s/cards?fields?fields=all" % \
                      (self.trello_list_id,)
        if self.attachments:
            request_url += "&attachments=true"
        # TODO check getting comments too.
        request_url += "&key=%s&token=%s" % (self.trello_key, self.trello_token)
        response = requests.get(request_url)

        self.cards = response.json()
        if self.users:
            print 'Loading members for cards...'
            self._get_members(self.cards)
            print '√ Done loading members for cards\n'
        if self.comments:
            print 'Loading comments for cards...'
            self._get_comments(self.cards)
            print '√ Done loading comments for cards\n'
        return self.cards

    def _get_members(self, cards):
        for card in cards:
            if card["idMembers"]:
                members_response = requests.get('https://api.trello.com/1/cards/%s/members'
                                                '?fields=username&key=%s&token=%s' % (card["id"],
                                                                                      self.trello_key,
                                                                                      self.trello_token))
                card["members"] = members_response.json()

    def _get_comments(self, cards):
        for card in cards:
            comments_response = requests.get("https://api.trello.com/1/cards/%s/actions?"
                                             "filter=commentCard&key=%s&token=%s" % (card["id"],
                                                                                     self.trello_key,
                                                                                     self.trello_token))
            comments = comments_response.json()
            card["comments"] = [{"author": comment["memberCreator"]["username"], "created": comment["date"],
                                 "text": comment["data"]["text"]} for comment in comments]

    def get_attachments_for_card(self, card_id):
        # TODO maybe checking can be done outside of here?
        if self.attachments is True:
            card = [card for card in self.cards if card["id"] == card_id]
            if card is None:
                return None
            card = card[0]

            attachments = []
            for card_attachments in card["attachments"]:
                response = requests.get(card_attachments["url"])
                attachments.append((card_attachments["name"], response.content))
            return attachments
