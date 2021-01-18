import random
import string
import data_handler


def generate_id(start_char,
                number_of_small_letters=4,
                number_of_capital_letters=2,
                number_of_digits=2,
                number_of_special_chars=2,
                allowed_special_chars=r"_+-!"):
    id = (random.choices(string.ascii_lowercase, k=2) +
          random.choices(string.ascii_uppercase, k=2) +
          random.choices(string.digits, k=2) +
          random.choices(allowed_special_chars, k=1))
    if start_char == 'q':
        listdict = data_handler.reader('question')
    else:
        listdict = data_handler.reader('answer')
    random.shuffle(id)
    final_id = start_char + "".join(id)
    for i in listdict:
        if i['id'] == final_id:
            return generate_id(start_char)
    return final_id
