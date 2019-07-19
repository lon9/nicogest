import argparse
from nicogest import Nicogest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id')
    parser.add_argument('-o', '--output', default='./')
    parser.add_argument('-t', '--threshold_multiplier', type=float, default=1.2)
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')

    args = parser.parse_args()
    print(args)
    nicogest = Nicogest(args.output, args.threshold_multiplier, args.username, args.password)
    nicogest.do(args.video_id)
