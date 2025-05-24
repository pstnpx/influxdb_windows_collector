from libs.ClientIntervalApp import ClientIntervalApp
import logging
from config import LOG_FILENAME

logger = logging.getLogger(LOG_FILENAME) 
app = ClientIntervalApp()
try:
    app.run()
except KeyboardInterrupt:
    logger.info("-------- Collector app stopped by user ---------")
except Exception as final_e:
    logger.critical(f"Unhandled critical exception in main loop: {final_e}", exc_info=True)