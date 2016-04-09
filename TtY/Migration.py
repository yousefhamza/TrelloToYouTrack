import json

SPECS_FILE = "TtY/specs.json"


class Migration:
    def __init__(self, mapping_file, specs_file):
        self.migration_dict = self._load_json(mapping_file)

        specs_dict = self._load_json(specs_file)
        self.required = specs_dict["required"]
        self.supported_keys = self.required + specs_dict["supported_keys"]
        self.types = specs_dict["types"]
        for type_key in self.types:
            if not type(self.types[type_key]) is list:
                self.types[type_key] = eval(self.types[type_key])

    def __enter__(self):
        self.validate_migration_dict()
        return self.migration_dict

    def validate_migration_dict(self):
        migration_dict = self.migration_dict

        # Check required keys
        for required_key in self.required:
            if not migration_dict.has_key(required_key):
                raise Exception("Missing required field %r" % (required_key,))

        # Check Supported keys
        for migration_key in migration_dict.keys():
            if migration_key not in self.supported_keys:
                raise Exception("Not recognized key %r" % (migration_key,))

        # Validate mappings against specs
        mapping_dict = migration_dict["mappings"]
        for mapping_key in mapping_dict.keys():
            if mapping_key not in self.types.keys():
                raise Exception("Not recognized mapping key %r" % (mapping_key,))
            mapping_value = mapping_dict[mapping_key]
            self._verify_keys_and_values_types(mapping_key, mapping_value, mapping_dict)

    def _verify_keys_and_values_types(self, mapping_key, mapping_value, mapping_dict):
        if mapping_value in self.types.keys():
                if not self.types[mapping_value] is self.types[mapping_key]:
                    raise Exception("%r and %r has different types %r %r" % (mapping_key, mapping_value,
                                                                            self.types[mapping_key],
                                                                            self.types[mapping_value]))
                if 'youtrack.' not in mapping_key or 'trello.' not in mapping_value:
                    raise Exception("Mapping keys should be youtrack and values trello, error key %r and value %r" %
                                    (mapping_key, mapping_dict[mapping_key]))

        elif type(self.types[mapping_key]) is list and type(mapping_value) is dict:
            conditions_dict = mapping_value
            for condition_value in conditions_dict.keys():
                if condition_value not in self.types[mapping_key]:
                    raise Exception("Not valid value %r for key %r" % (condition_value, mapping_key))\

                for key in conditions_dict[condition_value].keys():
                    if key not in self.types.keys():
                        raise Exception("Not recognized mapping key %r" % (key,))
                    elif not type(conditions_dict[condition_value][key]) is self.types[key]:
                            raise Exception("%r is not of type %r" % (conditions_dict[condition_value][key],
                                                                      self.types[key]))

        elif type(self.types[mapping_key]) is list and mapping_value not in self.types[mapping_key]:
            raise Exception("%r is not a valid value for %r, valid values are %r" % (mapping_value,
                                                                                     mapping_key,
                                                                                     self.types[mapping_key]))

        elif not type(self.types[mapping_key]) is list and  not type(mapping_value) is self.types[mapping_key]:
            raise Exception("%r is not of type %r" % (mapping_value, self.types[mapping_key]))

    def _load_json(self, file_name):
        json_file = open(file_name)
        json_string = json_file.read()
        json_file.close()
        return json.loads(json_string)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
