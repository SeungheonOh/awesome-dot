"""Five isolated plausible faults; original fixtures, not candidate programs."""
from correct_a import export_rows as baseline


def run(name, boundary, records):
    selected = records
    if boundary == 'download_selected' and name != 'consumer_filter_bypass':
        selected = [r for r in records if r['selected'] is True]
    result = baseline(selected)
    if name == 'duplicate_collapse':
        result['items'] = [item for n, item in enumerate(result['items'])
                           if item not in result['items'][:n]]
    elif name == 'zero_as_missing':
        for item in result['items']:
            if item['units'] == 0:
                item['units'] = None
    elif name == 'sort_instead_of_stable_order':
        result['items'].sort(key=lambda item: item['code'])
    elif name == 'wrong_empty_representation' and not result['items']:
        result = {'items': None}
    return result

NAMES = ('duplicate_collapse', 'zero_as_missing', 'sort_instead_of_stable_order',
         'wrong_empty_representation', 'consumer_filter_bypass')
