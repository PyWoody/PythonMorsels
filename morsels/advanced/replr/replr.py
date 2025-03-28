import os
import code
import pickle


def run(session, auto=False):
    session_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), f'{session}.pickle'
    )
    globals()['save'] = save_session(session_file)
    globals()['restore'] = restore_session(session_file)
    if auto:
        globals()['restore']()
    try:
        code.interact(local=globals(), banner='', exitmsg='')
    finally:
        if auto:
            globals()['save']()


def save_session(session_file):

    def save():
        with open(session_file, 'wb') as f:
            data = {}
            for k, v in globals().items():
                try:
                    p = pickle.dumps(v)
                except Exception:
                    pass
                else:
                    data[k] = p
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    return save


def restore_session(session_file):

    def restore():
        if os.path.isfile(session_file):
            with open(session_file, 'rb') as f:
                try:
                    data = pickle.load(f)
                except EOFError:
                    pass
                else:
                    for k, p in data.items():
                        globals()[k] = pickle.loads(p)

    return restore


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('session')
    parser.add_argument('--auto', action='store_true', default=False)
    args = parser.parse_args()

    run(args.session, auto=args.auto)
