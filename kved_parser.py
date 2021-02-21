"""Thid module parses json file for comfortable usage"""
import json
import doctest


def parse_kved(class_code):
    """
    Parses json file
    :param class_code:
    :return:
    >>> print(parse_kved(None))
    None
    """
    if class_code is None:
        return None
    dictionary = find_json_info(class_code)
    with open("kved_results.json", 'w') as outfile:
        json.dump(dictionary, outfile, ensure_ascii=False)


def convert_json(file):
    """
    Reads json file and converts it into dictionary
    :param file:
    :return:
    >>> print(convert_json(None))
    None
    """
    if file is None:
        return None
    with open(file, encoding='utf-8', errors='ignore') as json_data:
        return json.load(json_data, strict=False)


def find_section_code(class_code):
    """
    Returns section code for class code in json file
    :param class_code:
    :return:
    >>> find_section_code('01.11')
    'A'
    """
    indicator = int(class_code[:2])
    dict_codes = {(1, 5): 'A', (5, 10): 'B', (10, 35): 'C',
                  (35, 36): 'D', (36, 41): 'E', (41, 45): 'F',
                  (45, 49): 'G', (49, 55): 'H', (55, 58): 'I',
                  (58, 64): 'J', (64, 68): 'K', (68, 69): 'L',
                  (69, 77): 'M', (77, 84): 'N', (84, 85): 'O',
                  (85, 86): 'P', (86, 90): 'Q', (90, 94): 'R',
                  (94, 97): 'S', (97, 99): 'T', (99, 100): 'U'}
    for key in dict_codes:
        start, end = key
        if indicator in range(start, end):
            return dict_codes[key]


def find_json_info(class_code):
    """
    Returns desirable info from json file
    :param class_code:
    :return:
    >>> print(find_json_info(None))
    None
    """
    if class_code is None:
        return None
    dict_json = convert_json('kved.json')
    dict_results = {"type": "class",
                    "parent": {"type": "group",
                               "parent": {"type": "division",
                                          "parent": {"type": "section"}}}}
    division_code = class_code[:2]
    group_code = class_code[:4]
    section_code = find_section_code(class_code)
    for key in dict_json["sections"][0]:
        if key["sectionCode"] == section_code:
            section_name = key["sectionName"]
            divisions = key["divisions"]
            dict_results["parent"]["parent"]["parent"]["name"] = section_name
            dict_results["parent"]["parent"]["parent"]["num_children"] = len(divisions)
            for division in divisions:
                if division["divisionCode"] == division_code:
                    division_name = division["divisionName"]
                    groups = division["groups"]
                    dict_results["parent"]["parent"]["name"] = division_name
                    dict_results["parent"]["parent"]["num_children"] = len(groups)
                    for group in groups:
                        if group["groupCode"] == group_code:
                            group_name = group["groupName"]
                            classes = group["classes"]
                            dict_results["parent"]["name"] = group_name
                            dict_results["parent"]["num_children"] = len(classes)
                            for class_ in classes:
                                if class_["classCode"] == class_code:
                                    class_name = class_["className"]
                                    dict_results["name"] = class_name
                                    return dict_results

doctest.testmod()
