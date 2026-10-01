import logging 

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(filename)s -> %(funcName)s()] - %(message)s'
)

logger = logging.getLogger(__name__)