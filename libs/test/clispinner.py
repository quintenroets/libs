from libs.clispinner import CliSpinner
import time

with CliSpinner("test"):
    time.sleep(4)
