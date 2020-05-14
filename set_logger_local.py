import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

## refer https://docs.python.org/3.7/library/logging.html#logging.getLogger
## if nothing is specified within getLogger() function the name of the root
## if __name__ is specified 
logger = logging.getLogger(name=__name__)

## refer https://docs.python.org/3.7/library/logging.html#logging.Logger.setLevel
## set logger level to DEBUG so that anything above this level such as INFO, WARNING, CRITICAL gets logged
logger.setLevel('DEBUG')

## define handler
handler = AzureLogHandler(
    connection_string='InstrumentationKey=da28f1e4-5abb-4563-a583-d7d20066cdd7'
    )

## optionally you can define a format for the log message and add this to the handler
# format_str = '%(asctime)s - %(levelname)-8s - %(message)s'
# date_format = '%Y-%m-%d %H:%M:%S'
# formatter = logging.Formatter(format_str, date_format)
# handler.setFormatter(formatter)

logger.addHandler(handler)

## define custom dimensions to the logs
custom_properties = {
    'custom_dimensions': 
    {
        'key_1': 'value_1', 
        'key_2': 'value_2'
    }
}
print("hello OpenCensus")

## this will provide the effective log level for this logger
print('get effective log level:', logger.getEffectiveLevel())

print("hello debug")
logger.debug('debug from vscode completed.', extra=custom_properties)

print("hello info")
logger.info('info from vscode completed.', extra=custom_properties)

print("hello warning")
logger.warning('warning from vscode completed.', extra=custom_properties)

print("hello error")
logger.error('error from vscode completed.', extra=custom_properties)

#print("hello exception")
#logger.exception('error from vscode completed.', extra=custom_properties)