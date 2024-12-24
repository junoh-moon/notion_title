import argparse

import log
import title
import updater

logger = log.init()


def main(args):
    if args.generate:
        title.main(args)
    elif args.watch:
        updater.Updater(*updater.PAGE_ID_MAPPING.values()).watch()
    elif args.update:
        updater.Updater(*updater.PAGE_ID_MAPPING.values()).update()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    sub = parser.add_mutually_exclusive_group(required=True)

    sub.add_argument("--generate", action="store_true")
    sub.add_argument("--watch", action="store_true")
    sub.add_argument("--update", action="store_true")

    raw_args = parser.parse_known_args()
    logger.info(raw_args)
    if raw_args[0].generate:
        title.prepare_args(parser)
        args = parser.parse_args()
    else:
        args = raw_args[0]
    main(args)
