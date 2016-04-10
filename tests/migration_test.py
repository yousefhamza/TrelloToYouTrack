from unittest import TestCase
from TtY.Migration import Migration


class MigrationTest(TestCase):
    def setUp(self):
        self.migration_obj = Migration("../mapping.json", "../specs.json")
        self.migration_dict = self.migration_obj.migration_dict

    def test_correct_dict_should_pass(self):
        try:
            self.migration_obj.validate_migration_dict()
        except Exception:
            self.fail()

    def test_missing_required_keys(self):
        del self.migration_dict["trello_key"]
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_not_recongized_key(self):
        self.migration_dict["blabla"] = "blabla"
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

        del self.migration_dict["blabla"]
        self.migration_dict["mappings"]["blabla"] = "blabla"
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_if_comments_true_then_users_is_true(self):
        self.migration_dict["users"] = False
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_key_and_values_are_of_equal_types(self):
        self.migration_dict["mappings"]["youtrack.summary"] = "trello.dateLastActivity"
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_key_is_youtrack_and_value_is_trello(self):
        self.migration_dict["mappings"]["youtrack.summary"] = "youtrack.description"
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_static_values_for_list_types(self):
        self.migration_dict["mappings"]["youtrack.state"] = "NOT_VALID"
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_static_values_for_list_types_pass(self):
        self.migration_dict["mappings"]["youtrack.state"] = "Open"
        try:
            self.migration_obj.validate_migration_dict()
        except Exception:
            self.fail("Exception thrown when valid static value supplied")

    def test_values_are_valid_for_choices(self):
        self.migration_dict["mappings"]["youtrack.state"]["INVALID_VALUE"] = dict()
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_conditions_are_of_valid_keys(self):
        self.migration_dict["mappings"]["youtrack.state"]["Open"]["INVALID_KEY"] = "BLA"
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_conditions_values_are_of_wrong_type(self):
        self.migration_dict["mappings"]["youtrack.state"]["Open"]["trello.closed"] = "NOT_BOOL"
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)

    def test_static_value_is_of_correct_type(self):
        self.migration_dict["mappings"]["youtrack.summary"] = 123
        self.assertRaises(Exception, self.migration_obj.validate_migration_dict)
