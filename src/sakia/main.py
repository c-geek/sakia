"""
Created on 1 févr. 2014

@author: inso
"""
import signal
import sys
import asyncio
import logging
import os
import traceback

# To debug missing spec
import jsonschema

# To force cx_freeze import
import PyQt5.QtSvg

from quamash import QSelectorEventLoop
from PyQt5.QtWidgets import QApplication
from sakia.gui.mainwindow import MainWindow
from sakia.core.app import Application


def async_exception_handler(loop, context):
    """
    An exception handler which exits the program if the exception
    was not catch
    :param loop: the asyncio loop
    :param context: the exception context
    """
    logging.debug('Exception handler executing')
    message = context.get('message')
    if not message:
        message = 'Unhandled exception in event loop'

    try:
        exception = context['exception']
    except KeyError:
        exc_info = False
    else:
        exc_info = (type(exception), exception, exception.__traceback__)

    log_lines = [message]
    for key in [k for k in sorted(context) if k not in {'message', 'exception'}]:
        log_lines.append('{}: {!r}'.format(key, context[key]))

    logging.error('\n'.join(log_lines), exc_info=exc_info)
    for line in log_lines:
        for ignored in ("Unclosed", "socket.gaierror"):
            if ignored in line:
                return
    if exc_info:
        for line in traceback.format_exception(*exc_info):
            for ignored in ("Unclosed", "socket.gaierror"):
                if ignored in line:
                    return
    os._exit(1)


if __name__ == '__main__':
    # activate ctrl-c interrupt
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sakia = QApplication(sys.argv)
    loop = QSelectorEventLoop(sakia)
    loop.set_exception_handler(async_exception_handler)
    asyncio.set_event_loop(loop)

    with loop:
        app = Application.startup(sys.argv, sakia, loop)
        window = MainWindow.startup(app)
        loop.run_forever()
        try:
            loop.run_until_complete(app.stop())
        except asyncio.CancelledError:
            logging.info('CancelledError')
    sys.exit()
