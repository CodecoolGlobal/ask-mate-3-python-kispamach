import random
import string
import data_handler
from datetime import datetime
import os


def convert_to_date(rec):
    rec['submission_time'] = datetime.utcfromtimestamp(int(rec['submission_time'])).strftime('%Y-%m-%d %H:%M')
    return rec


def date_formatter(database):
    return map(lambda record: convert_to_date(record), database)


def generate_id(start_char, allowed_special_chars=r"_+-!"):
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


def delete_pictures(records):
    for record in records:
        if record['image']:
            os.remove('./' + record['image'])
