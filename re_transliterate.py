import re

def word_replace(re_map, word):
    """Regex replace all occurrences of keys in re_map with their value."""
    for key, value in re_map.items():
        word = re.sub(key, value, word, flags=re.UNICODE)
    return word

def word_list_replace(re_map, words):
    """Apply word_replace to a list of words."""
    return [word_replace(re_map, word) for word in words]

def transliterate(re_maps, word):
    """Apply a list of character mappings to transliterate word."""
    for mapping in re_maps:
        word = word_replace(mapping, word)
    return word

def transliterate_all(re_maps, words):
    """Apply a list of character mappings to transliterate a list of words."""
    for mapping in re_maps:
        words = [word_replace(mapping, word) for word in words]
    return words