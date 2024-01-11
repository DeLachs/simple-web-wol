import os
import re
from flask import Flask
from wakeonlan import send_magic_packet


APP = Flask(__name__)
RE_MAC_PATTERN = re.compile("([A-Fa-f0-9]{2}-[A-Fa-f0-9]{2}-[A-Fa-f0-9]{2}-[A-Fa-f0-9]{2}-[A-Fa-f0-9]{2}-[A-Fa-f0-9]{2})")
FROM_IP: str = os.getenv("WEB_WOL_FROM_IP", "0.0.0.0")
REDIRECT_URL: str = os.getenv("WEB_WOL_REDIRECT_URL", "/wol/success")


@APP.route('/wol/<target_mac>')
def wake_device(target_mac):
  if RE_MAC_PATTERN.match(target_mac):
    try:
      send_magic_packet(target_mac, interface=FROM_IP)
    except OSError as e:
      return(str(e))
    return(f"<script type=\"text/javascript\">window.location.replace(\"{REDIRECT_URL}\");</script>")
  else:
    return("Not a valid mac address! Please use the following format: ff-ff-ff-ff-ff-ff")


# Default redirect page if nothing different is supplied by the user.
@APP.route('/wol/success')
def success():
  return("success")


# uncomment the line below to run a local development
#APP.run(host="127.0.0.1", port=8080)
