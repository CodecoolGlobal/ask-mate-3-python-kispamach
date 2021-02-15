import os


def delete_pictures(records):
    for record in records:
        if record['image']:
            os.remove('./' + record['image'])
