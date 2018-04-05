import bcrypt
import concurrent.futures
import MySQLdb
import markdown
import os.path
import re
import subprocess
import torndb
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="prod", help="database name")
define("mysql_user", default="prod", help="database user")
define("mysql_password", default="prod", help="database password")


# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/admin", AdminHandler),
            (r"/admin/message", AdminMessageHandler),
            (r"/admin/settings", AdminSettingsHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "assets"),
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

        self.check_migrations()

    def check_migrations(self):
        try:
            self.db.get("SELECT COUNT(*) from settings;")
        except MySQLdb.ProgrammingError:
            subprocess.check_call(['mysql',
                                   '--host=' + options.mysql_host,
                                   '--database=' + options.mysql_database,
                                   '--user=' + options.mysql_user,
                                   '--password=' + options.mysql_password],
                                  stdin=open('schema.sql'))


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    @property
    def db(self):
        return self.application.db


class HomeHandler(BaseHandler):
    def get(self):
        settings = self.db.get("select * from settings where id=1")
        self.render("layout/front.html", settings=settings)


class AdminHandler(BaseHandler):
    def get(self):
        self.render("layout/admin.html")


class AdminMessageHandler(BaseHandler):
    def get(self):
        self.render("message.html")


class AdminSettingsHandler(BaseHandler):
    def get(self):
        settings = self.db.get("select * from settings where id=1")
        self.render("settings.html", settings=settings)

    def post(self):
        first_block_text = self.get_argument("first_block_text")
        second_block_text = self.get_argument("second_block_text")
        tel_num = self.get_argument("tel_num")
        email = self.get_argument("email")
        insta_link = self.get_argument("insta_link")
        youtube_link = self.get_argument("youtube_link")
        facebook_link = self.get_argument("facebook_link")
        self.write(first_block_text)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
