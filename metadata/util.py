import csv
import uuid
from typing import Any

from metadata.models import Music


def read_csv_file(file) -> list:
    data = []
    try:
        with open(file) as csv_infile:
            check_file_extension = file.split('.')
            if check_file_extension[1].lower() != 'csv':
                raise ValueError('Only CSV files are allowed')

            csv_data = csv.DictReader(csv_infile)
            for row in csv_data:
                data.append(row)
            return data
    except (ValueError, FileNotFoundError, Exception):
        raise


def clean_csv_data(file) -> dict:
    unique_dict = {}

    try:
        data_ = read_csv_file(file)

        for data in data_:
            if data.get('title') in unique_dict:
                data_contributor = data.get('contributors').split('|')
                unique_dict_contributor = unique_dict.get(data.get('title')).get('contributors').split('|')
                merge_contributors = '|'.join(list(set(data_contributor + unique_dict_contributor)))

                data_iswc = data.get('iswc').split()
                unique_dict_iswc = unique_dict.get(data.get('title')).get('iswc').split()
                merge_iswc = ''.join(list(set(data_iswc + unique_dict_iswc)))

                unique_dict.get(data.get('title')).update(
                    {'title': data.get('title'), 'contributors': merge_contributors, 'iswc': merge_iswc})
            else:
                unique_dict[data.get('title')] = {
                    'title': data.get('title'),
                    'contributors': data.get('contributors'),
                    'iswc': data.get('iswc'),
                }
        return unique_dict
    except (ValueError, Exception):
        raise


def write_csv_to_database(file) -> Any:
    try:
        dict_response = clean_csv_data(file)

        for v in dict_response.values():
            if not Music.objects.filter(title=v.get('title'), contributors=v.get('contributors'),
                                        iswc=v.get('iswc')).exists():
                Music.objects.create(title=v.get('title'), contributors=v.get('contributors'),
                                     iswc=v.get('iswc'), id=uuid.uuid4())
        return 'Music data loaded successfully'
    except (ValueError, Exception):
        raise


def validate_required_fields(fields: dict):
    return {
        'detail': f'Field {field} is required'
        for field in fields
        if fields.get(field) is None or fields.get(field) == ''
    }
