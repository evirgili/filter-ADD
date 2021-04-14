import typing as tp
import string
import sys
import shutil
from pathlib import Path


def add_filter(path: str, filters: tp.Dict[str, tp.Set[str]]) -> None:
    with open(path) as file:
        name = path.rsplit('/', maxsplit=1)[-1][:-4]
        s: tp.Set[str] = set()

        while line := file.readline():
            line = line.rstrip('\n').lower()
            if line:
                s.add(line)
        
        filters[name] = s


def categorize_file(path: str, filters: tp.Dict[str, tp.Set[str]]) -> tp.List[str]:
    result: tp.List[str] = []

    with open(path) as file:
        while line := file.readline():
            line = line.translate(str.maketrans('\n', ' ', string.punctuation)).lower()
            words = line.split()
            for word in words:
                for category in filters:
                    if word in filters[category] and category not in result:
                        result.append(category)
    
    return result


def fill_filters() -> tp.Dict[str, tp.Set[str]]:
    filters: tp.Dict[str, tp.Set[str]] = {}
    directory = Path('filter dictionaries')

    for path in directory.glob('*.txt'):
        add_filter(str(path), filters)

    return filters

def make_destination_name(path: Path, destination: Path) -> str:
    name = str(path).rsplit('/', maxsplit=1)[-1]
    return f'{str(destination)}/{name}'

def filter_files(filters: tp.Dict[str, tp.Set[str]]) -> None:
    files = Path('text files')
    valids = Path('valid files')
    invalids = Path('invalid files')

    with open(f'{str(invalids)}/files categories.txt', 'w') as file:
        for path in files.glob('*.txt'):
            name = str(path).rsplit('/', maxsplit=1)[-1]
            categories = categorize_file(str(path), filters)
            if categories:
                shutil.copy(str(path), make_destination_name(path, invalids))
                file.write(f'{name}: {str(categories)}\n')
            else:
                shutil.copy(str(path), make_destination_name(path, valids))


def main(args=None):
    filters = fill_filters()
    filter_files(filters)
    


if __name__ == '__main__':
    main()

# for key, value in filters.items():
#     print(f'{key}:', end='')
#     for word in value:
#         print(f' {word},', end='')
#     print('')