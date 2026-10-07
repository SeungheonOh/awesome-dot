"""Dependency-free stock-selection export, revision export-fixture-1."""

def export_rows(records):
    """Create the public payload; order and duplicate occurrences are significant."""
    items = []
    for record in records:
        units = record['units'] if 'units' in record else None
        items.append({'code': record['code'], 'units': units})
    return {'items': items}


def download_selected(records):
    """Public download consumer used by the selection screen."""
    selected = [record for record in records if record['selected'] is True]
    return export_rows(selected)
