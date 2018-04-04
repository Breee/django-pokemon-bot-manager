import requests
import json


class PokemonDataToJson:
    data_types = ['pokemon', 'type', 'move', 'pokestop', 'gym']
    raw_data_types = ['pokestop', 'gym']
    mappings_file = 'mappings.json'

    pokemon_go_pokedex_url = 'https://raw.githubusercontent.com/BrunnerLivio/' \
                             + 'pokemongo-json-pokedex/master/output/'
    pokemon_go_pokedex_type = ['pokemon', 'type', 'move']

    pokemon_translations_url = 'https://raw.githubusercontent.com/sindresorhus/pokemon/master/' +\
                               'data/'
    pokemon_languages = ['de', 'fr', 'en']
    pokemon_translations = {}
    json_data = {}

    def __init__(self):
        self.type_colors = self.get_type_colors()

        for data_type in self.data_types:
            if data_type in self.pokemon_go_pokedex_type:
                pokemon_go_pokedex_json = requests.get(
                    self.pokemon_go_pokedex_url + data_type + '.json').text
                pokemon_go_pokedex = json.loads(pokemon_go_pokedex_json)
            elif data_type in self.raw_data_types:
                with open(data_type + '_raw.json') as raw_data_json:
                    pokemon_go_pokedex = json.load(raw_data_json)
            else:
                raise NotImplementedError

            with open(self.mappings_file, 'r') as mappings_file:
                self.mappings = json.load(mappings_file)

            for lang in self.pokemon_languages:
                translations = requests.get(self.pokemon_translations_url + lang + '.json').text
                self.pokemon_translations[lang] = json.loads(translations)

            if data_type == 'pokemon':
                self.json_data[data_type] = self.get_pokemon_from_data(pokemon_go_pokedex)
            elif data_type == 'move':
                self.json_data[data_type] = self.get_moves_from_data(pokemon_go_pokedex)
            elif data_type == 'type':
                self.json_data[data_type] = self.get_types_from_data(pokemon_go_pokedex)
            elif data_type == 'pokestop':
                self.json_data[data_type] = self.get_pokestop_from_data(pokemon_go_pokedex)
            elif data_type == 'gym':
                self.json_data[data_type] = self.get_gym_from_data(pokemon_go_pokedex)

            with open(data_type + '.json', 'w') as output_file:
                if data_type in self.json_data:
                    json.dump(self.json_data[data_type], output_file, indent=4)

    def get_pokemon_from_data(self, pokemon_list):
        pokemon_rest_data = []
        index = 0
        for pokemon in pokemon_list:
            number = pokemon['dex']
            if index > 0:
                if number == pokemon_rest_data[index - 1]['number']:
                    """
                    TODO: Find a solution for pokemon with multiple entries like castform and
                    deoxys
                    """
                    continue

            rest_pokemon = self.extract_object_from_data(pokemon, 'pokemon')

            # get data from other sources
            rest_pokemon['name_english'] = self.pokemon_translations['en'][index]
            rest_pokemon['name_german'] = self.pokemon_translations['de'][index]
            rest_pokemon['name_french'] = self.pokemon_translations['fr'][index]
            pokemon_rest_data.append(rest_pokemon)
            index += 1
        return pokemon_rest_data

    def get_moves_from_data(self, move_list):
        moves_rest_data = []
        for move in move_list:
            rest_move = self.extract_object_from_data(move, 'move')
            moves_rest_data.append(rest_move)
        return moves_rest_data

    def get_types_from_data(self, type_list):
        types_rest_data = []
        for pokemon_type in type_list:
            rest_type = self.extract_object_from_data(pokemon_type, 'type')

            rest_type['color'] = rest_type['name']
            rest_type['name_german'] = rest_type['name_german']

            types_rest_data.append(rest_type)
        return types_rest_data

    def get_pokestop_from_data(self, pokestop_list):
        pokestop_rest_data = []
        for pokestop in pokestop_list['pstops']:
            rest_pokestop = self.extract_object_from_data(pokestop, 'pokestop')
            rest_pokestop['type'] = "pokestop"
            pokestop_rest_data.append(rest_pokestop)
        return pokestop_rest_data

    def get_gym_from_data(self, gym_list):
        gym_rest_data = []
        for gym in gym_list['gyms']:
            rest_gym = self.extract_object_from_data(gym, 'gym')
            rest_gym['type'] = "gym"
            gym_rest_data.append(rest_gym)
        return gym_rest_data

    def extract_object_from_data(self, data, data_type):
        rest_data = {}
        # generate data from pokemon_go_pokedex with mappings
        for key in self.mappings[data_type]:
            value = self.safe_get_dict_value(self.mappings[data_type], key)
            if value is None:
                rest_data[key] = None
                continue
            split_value: list = value.split('.')
            rest_data[key] = self.safe_get_dict_value(data, split_value[0])
            # if value is in sublist, extract it
            if len(split_value) > 0:
                for i in range(1, len(split_value), 1):
                    # if value consists of multiple values, store them as list of values
                    if isinstance(rest_data[key], list):
                        rest_data[key] = [self.extract_sub_value(sub_value, split_value) for
                                          sub_value in rest_data[key]]
                    else:
                        rest_data[key] = self.safe_get_dict_value(rest_data[key], split_value[i])
        return self.clean_data(rest_data)


    @staticmethod
    def extract_sub_value(sub_value, split_value):
        value = sub_value[split_value.copy().pop()]
        return value

    @staticmethod
    def get_type_colors():
        with open('type_colors.json', 'r') as data_file:
            data = json.load(data_file)
            return data

    @staticmethod
    def safe_get_dict_value(dictionary, key):
        if isinstance(dictionary, dict):
            if key in dictionary:
                return dictionary[key]
        return None

    def clean_data(self, dictionary):
        for key in dictionary:
            value = dictionary[key]
            if isinstance(value, str):
                value = self.clean_data_str(value)
            elif isinstance(value, list):
                for index, data in enumerate(value):
                    if isinstance(data, str):
                        value[index] = self.clean_data_str(data)
            dictionary[key] = value

        return dictionary

    def clean_data_str(self, value):
        # clean prefixes from value string
        for data_type in self.data_types:
            value = value.replace(data_type.upper(), '')
        value = value.lstrip('_')       # clean left over underscores of prefixes
        value = value.lower()           # make it lowercase to prevent errors
        value = value.replace('_', ' ')  # replace underscores for better readability
        return value


PokemonDataToJson()
