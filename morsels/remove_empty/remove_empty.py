import os


def remove_empty(start_dir):
    removed_dirs = set()
    for root, dirs, files in os.walk(start_dir, topdown=False):
        if not any(files):
            if not any(dirs) or all(os.path.join(root, i) in removed_dirs for i in dirs):
                print(f'Deleting directory {os.path.split(root)[1]}')
                os.rmdir(root)
                removed_dirs.add(root)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('root')
    args = parser.parse_args()

    remove_empty(args.root)
