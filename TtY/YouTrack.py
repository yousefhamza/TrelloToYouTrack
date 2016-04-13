from datetime import datetime
import requests

class YouTrack:
    def __init__(self, youtrack_login, youtrack_password, youtrack_link, youtrack_project,
                 youtrack_subsystem=None):
        self.youtrack_login = youtrack_login
        self.youtrack_password = youtrack_password
        self.youtrack_link = youtrack_link
        self.youtrack_project = youtrack_project
        self.youtrack_subsystem = youtrack_subsystem

    def import_issues(self, trello_cards, mapping_dict, number_in_project, attachments=False):
        xml_string = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        xml_string += '<issues>\n'
        xml_string += self._issues_string(trello_cards, mapping_dict, attachments, number_in_project)
        xml_string += '</issues>'

        import_url = '%s/rest/import/%s/issues?test=true' % (self.youtrack_link, self.youtrack_project)
        headers = {'Content-Type': 'application/xml'}
        print xml_string
        print import_url
        response = requests.put(import_url, auth=(self.youtrack_login, self.youtrack_password), headers=headers,
                                data=xml_string.decode('utf-8'))
        print response.status_code
        print response.content

    def _issues_string(self, trello_cards, mapping_dict, attachments, number_in_project):
        issue_string = '\n'
        for card in trello_cards:
            issue_string += '<issue>\n'
            issue_string += self._get_issue_fields(mapping_dict, card, number_in_project)
            issue_string += '</issue>\n'
            number_in_project += 1
        return issue_string

    def _get_issue_fields(self, mapping_dict, card, number_in_project):
        fields = ''
        fields += self._field_string('created', int(datetime.now().strftime("%s")) * 1000) + '\n'
        fields += self._field_string('reporterName', self.youtrack_login) + '\n'
        fields += self._field_string('numberInProject', number_in_project)
        for mapping_key in mapping_dict.keys():
            mapping_value = mapping_dict[mapping_key]
            # TODO make sure that no trello. exist without being in the supported keys
            if 'trello.' in mapping_value:
                trello_key = mapping_value[len('trello.'):]
                fields += self._field_string(mapping_key[len('youtrack.'):], card[trello_key])

            elif type(mapping_value) is dict:
                for value in mapping_value.keys():
                    conditions_dict = mapping_value[value]
                    all_conditions_satisfied = True
                    for condition in conditions_dict.keys():
                        condition_value = conditions_dict[condition]
                        trello_condition_key = condition[len('trello.'):]
                        if card[trello_condition_key] != condition_value:
                            all_conditions_satisfied = False
                            break
                    if all_conditions_satisfied:
                        fields += self._field_string(mapping_key[len('youtrack.'):], value)
            else:
                fields += self._field_string(mapping_key[len('youtrack.'):], mapping_value)
            fields += '\n'
        if self.youtrack_subsystem:
            fields += self._field_string('subsystem', self.youtrack_subsystem) + '\n'
        return fields

    def _field_string(self, name, value):
        return ('<field name="%s">\n'
                '   <value>%s</value>\n'
                '</field>' % (name, value))
