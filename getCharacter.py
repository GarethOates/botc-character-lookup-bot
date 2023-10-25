import requests;
import json;
import re;
import os;

from dotenv import load_dotenv

SUMMARY_PATTERN = r'== Summary ==\n(.*?)\n'
TYPE_PATTERN = r'\[\[Character Types ?#([^|\]]+)\|([^|\]]+)\]\]'
EDITION_PATTERN = r'\[\[Category:(.*?)\]\]'

load_dotenv()

WIKI_BASE = os.getenv('WIKI_BASE')

color_dictionary = {
    'Townsfolk': 0x004EA1,
    'Outsider': 0x4EA4CB,
    'Minion': 0x521116,
    'Demon': 0x8F0E13,
    'Traveller': 0x260E27,
    'Fabled': 0xD3AA24
}


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def capitalize_words_around_symbol(input_str, symbol):
    if not symbol in input_str: return input_str

    parts = input_str.split(symbol)
    capitalized_parts = [part.strip().capitalize() for part in parts]

    return symbol.join(capitalized_parts)


def sanitize_string(input_str):
    result = input_str.capitalize()
    result = capitalize_words_around_symbol(result, " ")
    result = capitalize_words_around_symbol(result, "-")

    return result


def get_part_by_pattern(text, pattern):
    match = re.search(pattern, text, re.DOTALL)

    if match:
        result = match.group(1).strip()
        result = result.replace('"', '')
        result = result.replace("Experimental Characters", "Experimental")

        return result


def get_info_for_character(character):
    character = sanitize_string(character)
    encodedCharacter = character.replace(' ', '_')

    url = WIKI_BASE.format(encodedCharacter)

    response = requests.get(url)
    jsonObject = json.loads(response.content)

    if "error" in jsonObject:
        return { 'error': f'Found no results for "{character}"' }
    else:
        wikiText = remove_html_tags(jsonObject["parse"]["wikitext"])

        summary = get_part_by_pattern(wikiText, SUMMARY_PATTERN)
        type = get_part_by_pattern(wikiText, TYPE_PATTERN)
        edition = get_part_by_pattern(wikiText, EDITION_PATTERN)

        dictionary = {
            'name': character,
            'type': type,
            'ability': summary,
            'found': edition,
            'color': color_dictionary[type]
        }

        return dictionary