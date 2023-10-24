import argparse

import title
import updater


def main(args):
    if args.generate:
        title.main(args)
    elif args.watch:
        updater.Updater(updater.twenty_twenty_three_id).watch()
    elif args.update:
        updater.Updater(updater.twenty_twenty_three_id).update()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    sub = parser.add_mutually_exclusive_group(required=True)
    sub.add_argument("--generate", action="store_true")
    sub.add_argument("--watch", action="store_true")
    sub.add_argument("--update", action="store_true")

    args = parser.parse_args()
    if args.generate:
        title.prepare_args(parser)
        args = parser.parse_args()
    main(args)
