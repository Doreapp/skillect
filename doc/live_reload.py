"""
Python script to live-reload the documentation
"""

import argparse
import logging
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from watchdog import events
from watchdog.observers import Observer

LOGGER = logging.getLogger("live_reload")


class Handler(events.FileSystemEventHandler):
    """Custom file-changed handler"""

    src_directory: str
    output_directory: str

    def __init__(self, src_directory: str, output_directory: str):
        super().__init__()
        self.src_directory = src_directory
        self.output_directory = output_directory

    def on_any_event(self, event: events.FileSystemEvent):
        """Callback on any event"""
        if event.event_type in (
            events.EVENT_TYPE_CREATED,
            events.EVENT_TYPE_DELETED,
            events.EVENT_TYPE_MODIFIED,
            events.EVENT_TYPE_MOVED,
        ):
            self.reload()

    def reload(self):
        """Reload the documentation"""
        LOGGER.info("Reloading...")
        os.system(f"sphinx-build -b html {self.src_directory} {self.output_directory}")


def parse_args() -> argparse.Namespace:
    """Parse arguments from the command line"""
    parser = argparse.ArgumentParser(
        "live_reload",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("directory", help="Directory to watch")
    parser.add_argument("-o", "--output", help="HTML output directory", default="html")
    parser.add_argument(
        "-p", "--port", type=int, help="Port to serve the documentation", default=8000
    )
    parser.add_argument(
        "-l",
        "--level",
        "--log-level",
        help="Logger level",
        choices=("ERROR", "WARNING", "INFO", "DEBUG"),
        default="INFO",
    )
    return parser.parse_args()


def main():
    """Main entrypoint"""
    args = parse_args()
    logging.basicConfig(level=args.level)
    # Update handle
    handler = Handler(args.directory, args.output)
    handler.reload() # Initial build
    LOGGER.info("Start watching '%s'", args.directory)
    # Files watcher
    observer = Observer()
    observer.schedule(handler, args.directory, recursive=True)
    observer.start() # Start watching
    # Simple server
    request_handler = partial(SimpleHTTPRequestHandler, directory=args.output)
    with ThreadingHTTPServer(("0.0.0.0", args.port), request_handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            LOGGER.warning("Stopping...")
            observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
