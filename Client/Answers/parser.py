# path = "Plant"
# 
# file = open(path, "a", encoding="utf-8")
# 
# while True:
#     a = input()
#     b = a.split(" ")
#     c = [" ".join(b[i].split(sep="-")) for i in range(len(b))]
#     d = "\n".join(c) + "\n"
#     file.write(d)
from binary_file_search.BinaryFileSearch import BinaryFileSearch

heb_to_eng: dict[str, str] = {"א": "a", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "v", "ז": "z", "ח": "h",
                              "ט": "t", "י": "y", "כ": "k", "ל": "l", "מ": "m", "נ": "n", "ס": "s", "ע": "a",
                              "פ": "p", "צ": "c", "ק": "k", "ר": "r", "ש": "s", "ת": "t"
                              }

def camel_case(string: str) -> str:
    """
    Convert the string to camel case.
    :param string: the string to convert.
    :return: the string in camel case.
    """

    res = ""
    for word in string.split(" "):
        res += word.capitalize()
        res += " "
    return res.strip()

def eng_score_adder(answer: str, file_path: str, letter) -> int:
    """
    Return how much to add to the score based on the answer, answer in English.
    :param answer: the answer to check.
    :param file_path: the path of the file to check the answer in.
    :return: the score of the answer.
    """

    if answer == "":
        return 0

    if answer[0].lower() != heb_to_eng[letter]:  # the first letter is not correct
        return 0

    with open(file_path, 'r', encoding="utf-8") as file:  # check in dataset
        for line in file:
            if camel_case(answer) in line:
                return 1

    return 0  # answer not found


city = "Zywiec"


tmp_score = 0  # initialize new score
# tmp_score += score_adder(country, "./Client/Answers/Country")
# tmp_score += score_adder(city, "./Client/Answers/CityHeb")
tmp_score += eng_score_adder(city, "City", "ז")
# tmp_score += score_adder(animal, "./Client/Answers/Animal")
# tmp_score += score_adder(plant, "./Client/Answers/Plant")

print(tmp_score)