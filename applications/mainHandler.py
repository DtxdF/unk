import json
import logging
import traceback
import tornado.escape
import tornado.web
from tornado.options import options

class RequireArg(Exception):
	pass

_require_arg = RequireArg()

class JsonHandler(tornado.web.RequestHandler):
	async def prepare(self):
		self.request.json_arguments = {}
		body = self.request.body

		if (body):
			try:
				json_data = tornado.escape.json_decode(body)
			except json.decoder.JSONDecodeError:
				self.write_template({
					"message" : "The message must be in JSON format"
				}, status_code=400)
				self.finish()

			self.request.json_arguments.update(json_data)

	def _check_argument(
		self,
		value,
		value_type=None,
		valid_func=None,
		exceptions=(TypeError, ValueError)
	):
		if (value_type is not None):
			try:
				value = value_type(value)
			except exceptions:
				raise tornado.web.HTTPError(400, reason="The value's type isn't expected")

		if (valid_func is not None) and not (valid_func(value)):
			raise tornado.web.HTTPError(400, reason="A value isn't correct")

		return value

	def get_json_argument(
		self,
		name,
		default=_require_arg,
		strip=True,
		value_type=None,
		valid_func=None,
		exceptions=(TypeError, ValueError)
	):
		try:
			value = self.request.json_arguments[name]
		except KeyError:
			if (isinstance(default, RequireArg)):
				raise tornado.web.HTTPError(400, reason=f"`{name}` is required")
			return default

		if (strip and isinstance(value, str)):
			value = value.strip()

		value = self._check_argument(
			value, value_type, valid_func, exceptions
		)

		return value

	def __get_argument(
		self,
		get_arg_func,
		name,
		default=_require_arg,
		strip=True,
		**kwargs
	):
		try:
			value = get_arg_func(name, strip=strip)
		except tornado.web.MissingArgumentError:
			if (isinstance(default, RequireArg)):
				raise tornado.web.HTTPError(400, reason=f"`{name}` is required")
			return default

		value = self._check_argument(
			value, **kwargs
		)

		return value

	def get_argument(self, *args, **kwargs):
		return self.__get_argument(super().get_argument, *args, **kwargs)

	def get_query_argument(self, *args, **kwargs):
		return self.__get_argument(super().get_query_argument, *args, **kwargs)

	def get_body_argument(self, *args, **kwargs):
		return self.__get_argument(super().get_body_argument, *args, **kwargs)

	def write_error(self, status_code, **kwargs):
		body = {}
		trace = []
		body["message"] = self._reason

		for err in traceback.format_exception(*kwargs["exc_info"]):
			err = err.rstrip()

			logging.error(err)
			if (options.show_trace):
				trace.append(err)
		
		if (trace != []):
			body["trace"] = "\n".join(trace)

		self.write_template(body, status_code)

	def write_template(self, chunk, status_code=200, *args, **kwargs):
		response = {
			"status_code" : status_code
		}
		response.update(chunk)
		self.write_json(response, status_code, *args, **kwargs)

	def write_json(self, chunk, status_code=200):
		self.set_status(status_code)
		self.write(tornado.escape.json_encode(chunk))

	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "*")
		self.set_header("Content-Type", "application/json")

	async def options(self, *args, **kwargs):
		self.set_header("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE, OPTIONS")

class NotFoundHandler(JsonHandler):
	def initialize(self, status_code, message):
		self.set_status(status_code, message)

	def prepare(self):
		raise tornado.web.HTTPError(
			self._status_code, self._reason
		)

class RequiredResource(JsonHandler):
	def prepare(self):
		self.write_template({
			"message" : "El recurso es necesario para poder continuar"
		}, status_code=400)

	async def get(self):
		pass

	async def post(self):
		pass

	async def put(self):
		pass

	async def delete(self):
		pass
