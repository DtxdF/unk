# -*- coding: utf-8 -*-

import logging
import sys
import tornado.ioloop
import app
import config

from tornado.options import define, options

if __name__ == "__main__":
	define("lhost", default=config.API_LHOST, help="La dirección donde escuchará la API")
	define("lport", default=config.API_LPORT, type=int, help="El puerto donde recibirá los datos")
	define("use_curl", default=config.USE_CURL, type=bool, help="Usar la compatibilidad con cURL")
	define("show_trace", default=config.SHOW_TRACE, type=bool, help="Mostrar al cliente la traza de excepciones")
	options.parse_command_line()

	if (options.use_curl):
		# CURL is the best method :D
		tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
		logging.warning("La compatibilidad con cURL ha sido habilitada.")

	if (options.show_trace):
		logging.warning("La traza de excepciones se le mostrará al cliente. Esto puede revelar información sensible.")

	application = app.make_app()
	application.listen(options.lport, options.lhost)

	logging.info("Listening on %s:%d" % (options.lhost, options.lport))
	
	try:
		tornado.ioloop.IOLoop.current().start()
	except KeyboardInterrupt:
		sys.exit(0)
