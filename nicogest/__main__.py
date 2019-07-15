import argparse
from nicogest import Nicogest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id')

    args = parser.parse_args()
    print(args)
    nicogest = Nicogest()
    nicogest.do(args.video_id)
