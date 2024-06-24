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


def score_adder(self, answer: str, file_path: str) -> int:
    """
    Return how much to add to the score based on the answer.
    :return:
    """

    with open(file_path, 'r', encoding="utf-8") as file:
        if (answer in file.read()) and (answer[0] == self.letter):
            return 2
    return 0



tmp_score = 0  # initialize new score
# tmp_score += score_adder(country, "./Client/Answers/Country")
# tmp_score += score_adder(city, "./Client/Answers/CityHeb")
tmp_score += int(score_adder(city, "./Client/Answers/City") / 2)
# tmp_score += score_adder(animal, "./Client/Answers/Animal")
# tmp_score += score_adder(plant, "./Client/Answers/Plant")