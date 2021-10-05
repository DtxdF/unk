
DIR_ROOT = "files"
CONFIG_FILE = f"{DIR_ROOT}/settings.ini"
DEFAULT_HTTP_HEADERS = {
	"Access-Control-Allow-Origin"	: "*",
	"Access-Control-Allow-Headers"	: "*"
}
# Típicamente son los usados (quizá PATCH, inclusive)
DEFAULT_METHODS = "POST, GET, PUT, DELETE, OPTIONS"
