import argparse
import collections
import csv
import simplejson as json
import os


def read_and_write_file(json_file_path, csv_file_path, column_names):
    """Read in the json dataset file and write it out to a csv file, given the column names."""
    print(csv_file_path)
    with open(csv_file_path, 'w+') as fout:
        csv_file = csv.writer(fout)
        csv_file.writerow(list(column_names))
        with open(json_file_path) as fin:
            for line in fin:
                line_contents = json.loads(line)
                csv_file.writerow(get_row(line_contents, column_names))

def get_superset_of_column_names_from_file(json_file_path):
    """Read in the json dataset file and return the superset of column names."""
    column_names = set()
    with open(json_file_path) as fin:
        for line in fin:
            line_contents = json.loads(line)
            column_names.update(
                    set(get_column_names(line_contents))
                    )
    return column_names

def get_column_names(line_contents, parent_key=''):
    """Return a list of flattened key names given a dict.
    Example:
        line_contents = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        will return: ['a.b', 'a.c']
    These will be the column names for the eventual csv file.
    """
    column_names = []
    # print(line_contents)
    for k in line_contents.keys():
        column_names.append(k)
    return column_names

def get_nested_value(d, key):
    """Return a dictionary item given a dictionary `d` and a flattened key from `get_column_names`.
    
    Example:
        d = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        key = 'a.b'
        will return: 2
    
    """
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    return get_nested_value(sub_dict, sub_key)

def get_row(line_contents, column_names):
    """Return a csv compatible row given column names and a dict."""
    row = []
    for column_name in column_names:
        line_value = get_nested_value(
                        line_contents,
                        column_name,
                        )
        if isinstance(line_value, str):
            row.append('{0}'.format(line_value.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row

if __name__ == '__main__':
    """Convert a yelp dataset file from json to csv."""

    parser = argparse.ArgumentParser(
            description='Convert Yelp Dataset Challenge data from JSON format to CSV.',
            )

    parser.add_argument(
            'json_file',
            type=str,
            help='The json file to convert.',
            )
    
    parser.add_argument(
            'csv_file',
            type=str,
            help='The directory to store csv.',
            )

    args = parser.parse_args()

    json_file = args.json_file
    # csv_file = '{0}.csv'.format(json_file.split('.json')[0])
    csv_file_path = args.csv_file
    csv_file = '{0}.csv'.format(os.path.join(csv_file_path,os.path.basename(json_file).split('.json')[0]))
    
    column_names = get_superset_of_column_names_from_file(json_file)
    print("json-",json_file)
    print("csv-",csv_file)
    read_and_write_file(json_file, csv_file, column_names)