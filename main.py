#!/usr/bin/python3

import argparse
import logging

import log
import db
import ui
import ctrl
import config

def createParser():
    parser = argparse.ArgumentParser(description='Python photo gallery')
    parser.add_argument(
        '-v,', '--verbose', dest='verbosity',
        action='count', default=0,
        help='Enable verbosity')
    parser.add_argument(
        '-l', '--log', dest='log_file',
        action='store', type=str, default=None,
        help='Log file')
    parser.add_argument(
        '-d', '--dir', dest='dir_list',
        action='append', type=str, required=True,
        help='Directory to search for photos')
    parser.add_argument(
        '-p', '--pattern', dest='file_pattern_list',
        action='append', type=str, default=['.*\.JPG', '.*\.jpg'],
        help='Photo file pattern')
    parser.add_argument(
        '-c', '--config', dest='config_file',
        action='store', type=str, default='config.json',
        help='Config file')
    return parser


def main():
    parser = createParser()
    args = parser.parse_args()

    log.init('root', args.verbosity, args.log_file)
    logger = logging.getLogger('root')
    logger.info('Python photo gallery started!')
    logger.debug('Args: %s', str(args))

    cfg = config.Config(args.config_file)

    dbase = db.Db(args.dir_list, args.file_pattern_list)
    dbase.build()

    #view = mainview.MainView()
    view = ui.NavUi()

    controller = ctrl.Controller(cfg, dbase, view)
    controller.populate_view()

    view.main()

if __name__ == "__main__":
    main()