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
        board_id, list_id = '', ''
        request_url = 'https://api.trello.com/1/members/me/boards?fields=name&lists=all&list_fields=name?members=true' \
                      '&members_fields=&key=%s&token=%s' % (self.trello_key, self.trello_token)
        response = requests.get(request_url)

        for trello_board in response.json():
            if trello_board["name"] == board_name:
                board_id = trello_board["id"]
                for trello_list in trello_board["lists"]:
                    if trello_list["name"] == list_name:
                        list_id = trello_list["id"]
                        return board_id, list_id
                if list_id == '':
                    raise Exception("List %s not found in board %s" % (list_name, board_name))
        raise Exception("Board %s not found", board_name)

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
            users.append( {
                "username": user_dict["username"],
                "fullName": user_dict["fullName"],
                "email": user_dict["email"]
            })
            print user_dict
        return users

    def get_cards(self):
        # Cache results
        if self.cards:
            return self.cards
        # TODO add fields to specs file
        request_url = "https://api.trello.com/1/lists/%s/cards?fields=name,desc,closed" % \
                      (self.trello_list_id,)
        if self.attachments:
            request_url += "&attachments=true"
        # TODO check getting comments too.
        request_url += "&key=%s&token=%s" % (self.trello_key, self.trello_token)
        response = requests.get(request_url)

        self.cards = response.json()
        return response.json()

    def get_attachments_for_card(self, card_id):
        # TODO maybe checking can be done outside of here?
        if self.attachments is True:
            card = None
            for trello_card in self.cards:
                if trello_card["id"] == card_id:
                    card = trello_card
                    break
            if card is None:
                return None

            attachments = []
            for card_attachments in card["attachments"]:
                response = requests.get(card_attachments["url"])
                attachments.append((card_attachments["name"], response.content))
            return attachments
