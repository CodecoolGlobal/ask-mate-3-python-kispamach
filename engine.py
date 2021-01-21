def sort_data(order_by, order_direction, data):
    def modifier(rec):
        rec['submission_time'] = int(rec['submission_time'])
        rec['view_number'] = int(rec['view_number'])
        rec['vote_number'] = int(rec['vote_number'])
        return rec
    data = map(lambda record: modifier(record), data)
    return sorted(data, key=lambda record: record[order_by], reverse=False if order_direction == 'asc' else True)


def sort_answers(order_by, order_direction, data):
    def modifier(rec):
        rec['submission_time'] = int(rec['submission_time'])
        rec['vote_number'] = int(rec['vote_number'])
        return rec
    data = map(lambda record: modifier(record), data)
    return sorted(data, key=lambda record: record[order_by], reverse=False if order_direction == 'asc' else True)
