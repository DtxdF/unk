import configparser
import constants

from applications import mainHandler

settings = configparser.ConfigParser()
settings.read(constants.CONFIG_FILE)

API_LHOST = settings.get("server", "lhost")
API_LPORT = settings.getint("server", "lport")
USE_CURL = settings.getboolean("server", "use_curl")
SHOW_TRACE = settings.getboolean("server", "show_trace")

tornado_applications_settings = {
	"default_handler_class" : mainHandler.NotFoundHandler,
	"default_handler_args"  : {
		"status_code" : 404,
		"message"     : "Resource not found"
	},
	"compress" : True
}
