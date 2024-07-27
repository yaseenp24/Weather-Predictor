# make_project3_submission.py
#
# ICS 32A Fall 2023
# Project 3
# SUBMISSION-BUILDING AUTOMATION
#
# [last updated: 2023-11-05 20:05]

from pathlib import Path
import zipfile


SUBMISSION_NAME = 'project3.zip'
FILES_TO_IGNORE = ['make_project3_submission.py']


def verify_format_py(file_path: Path) -> bool:
    with file_path.open('r', encoding = 'utf-8') as py_file:
        try:
            for line in py_file:
                continue
        except ValueError:
            print()
            print(f'The file named {file_path.name} was expected to be a Python script.')
            print('  However, it contains characters that cannot be read as text, which means')
            print('  it also may not be possible for us to run the program.  If, for example,')
            print('  this is an image or a document you wrote in a word processor, but that')
            print('  you renamed so its filename ends in .py, you\'ll need to instead ensure')
            print('  that the file contains only readable text.')
            print()
            return False

    return True


def can_create(submission_path: Path) -> bool:
    if submission_path.exists():
        print(f'The submission named {submission_path.name} already exists.')
        print('  Do you want to replace it with a new version?')
        print('  If so, type Y and press the Enter key.')
        print('  If not, type N and press the Enter key.')

        what_to_do = input('    What would you like to do? ').upper()

        if what_to_do.startswith('Y'):
            print(f'  A new version of {submission_path.name} will be created,')
            print('  replacing the old one.')
            return True
        else:
            return False
    else:
        return True


def is_submittable(file_path: Path) -> bool:
    return file_path.is_file() \
           and file_path.suffix == '.py' \
           and file_path.name not in FILES_TO_IGNORE


def create_submission(submission_path: Path, script_dir_path: Path) -> bool:
    files_to_submit = [file for file in script_dir_path.iterdir() if is_submittable(file)]
    files_to_skip = [file for file in script_dir_path.iterdir() if file.name in FILES_TO_IGNORE]

    if len(files_to_submit) == 0:
        print('There are no other .py files in the same directory as this script.')
        print('  Put this script into the same directory as the rest of your program')
        print('  and run it again.')
        return False

    any_issues = False

    for file in files_to_submit:
        if not verify_format_py(file):
            any_issues = True

    if any_issues:
        return False

    with zipfile.ZipFile(submission_path, mode = 'w') as submission_zip:
        print()
        print(f'Creating {submission_path.name} ...')

        for file in files_to_submit:
            print(f'  Adding {file.name} to it ...')
            submission_zip.write(file.name)

        for file in files_to_skip:
            print(f'  Skipping {file.name}, because it should not be submitted')

    return True


def run() -> None:
    submission_path = Path.cwd() / SUBMISSION_NAME
    
    if can_create(submission_path) and create_submission(submission_path, Path.cwd()):
        print(f'Submission named {SUBMISSION_NAME} was created.')
    else:
        print('No submission was created.')


if __name__ == '__main__':
    run()