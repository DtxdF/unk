import re
import tornado.web
import applications
import config

def make_app():
	version = config.settings.getfloat("server", "version")
	version = re.escape(str(version))

	return tornado.web.Application([
		(r"/", applications.mainHandler.RequiredResource),
		(rf"/v{version}/?", applications.mainHandler.RequiredResource)
	], **config.tornado_applications_settings)
