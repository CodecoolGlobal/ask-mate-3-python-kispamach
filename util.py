import os
import data_handler


def delete_pictures(records):
    for record in records:
        if record['image']:
            os.remove('./' + record['image'])


def repu_modifier(record_type, id, vote_type):
    weights = {
        'question': {
            'upvote': 5,
            'downvote': -2
        },
        'answer': {
            'upvote': 10,
            'downvote': -2
        }
    }
    user_id = data_handler.get_one_by_id(record_type, id)['user_id']
    data_handler.reputation_modifier(user_id, weights[record_type][vote_type])