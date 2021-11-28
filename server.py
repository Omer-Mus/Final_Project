
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# app = Flask(__name__, template_folder=tmpl_dir)
app = Flask(__name__)

#
#
# DATABASEURI = "postgresql://user:password@34.74.246.148/proj1part2"
#                   # om2349    xxxxx
#
# #
# # This line creates a database engine that knows how to connect to the URI above.
# #
# engine = create_engine(DATABASEURI)
#
#
# @app.before_request
# def before_request():
#   """
#   This function is run at the beginning of every web request
#   (every time you enter an address in the web browser).
#   We use it to setup a database connection that can be used throughout the request.
#
#   The variable g is globally accessible.
#   """
#   try:
#     g.conn = engine.connect()
#   except:
#     print("uh oh, problem connecting to database")
#     import traceback; traceback.print_exc()
#     g.conn = None
#
# @app.teardown_request
# def teardown_request(exception):
#   """
#   At the end of the web request, this makes sure to close the database connection.
#   If you don't, the database could run out of memory!
#   """
#   try:
#     g.conn.close()
#   except Exception as e:
#     pass
#


@app.route('/')
def index():


  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  # context = dict(data = names)

  # return render_template("index.html", **context)
  return render_template("index.html")



@app.route('/register')
def another():
  return render_template("another.html")


# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   # name = request.form['name']
#   # g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#   return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":

  import click
  # @click.command()
  # @click.option('--debug', is_flag=True)
  # @click.option('--threaded', is_flag=True)
  # @click.argument('HOST', default='0.0.0.0')
  # @click.argument('PORT', default=8111, type=int)
  #
  # def run(debug, threaded, host, port):
  #   HOST, PORT = host, port
  #   print("running on %s:%d" % (HOST, PORT))
  #   app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  #
  # run()
  app.run(debug=True)