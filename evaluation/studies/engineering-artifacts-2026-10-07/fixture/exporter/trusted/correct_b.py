"""Second correct implementation; independently expressed boundary behavior."""

def export_rows(records):
    return dict(items=[dict(zip(('code', 'units'), (row['code'], row.get('units'))))
                       for row in records])


def download_selected(records):
    result = {'items': []}
    for index in range(len(records)):
        row = records[index]
        if row['selected']:
            result['items'].append({'units': row.get('units'), 'code': row['code']})
    return result
