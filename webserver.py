from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>Hello!!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>hola!!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h1>Restaurants!!</h1>"
                output += "<a href='/restaurants/new'>Make a new restaurant!!</a><ul>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    # print restaurant.name
                    output += "<li>{name} <a href='/restaurant/{id}/edit'>Edit</a>    <a href='/restaurant/{id}/delete'>Delete</a></li>".format(name=restaurant.name, id=restaurant.id) 
                output += "</ul></body></html>"
                self.wfile.write(output)
                # print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h1>Make a new restaurant!!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name='restaurantName' type='text' placeholder='New restaurant name'><input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return
            if self.path.endswith("/edit"):
                RestaurantId = self.path.split("/")[2]
                Restau = session.query(Restaurant).filter_by(id = RestaurantId).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h1>Make a new restaurant!!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/{id}/edit'><input name='restaurantName' type='text' placeholder='{name}'><input type='submit' value='Edit'></form>".format(id = Restau.id, name=Restau.name)
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return
            if self.path.endswith("/delete"):
                RestaurantId = self.path.split("/")[2]
                Restau = session.query(Restaurant).filter_by(id = RestaurantId).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete {name}?</h1>".format(name=Restau.name)
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/{id}/delete'><input type='submit' value='Delete'></form>".format(id = Restau.id, name=Restau.name)
                output += "</body></html>"
                self.wfile.write(output)
                # print output
                return
        except:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurantName')
                print messagecontent
                #crate a restaurant
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurantName')
                print messagecontent
                RestaurantId = self.path.split("/")[2]
                Restau = session.query(Restaurant).filter_by(id = RestaurantId).one()
                Restau.name = messagecontent[0]
                session.add(Restau)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/delete"):
                RestaurantId = self.path.split("/")[2]
                toDelete = session.query(Restaurant).filter_by(id = RestaurantId).one()
                if toDelete!= []:
                    session.delete(toDelete)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            # self.send_response(301)
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
                # fields=cgi.parse_multipart(self.rfile, pdict)
                # messagecontent = fields.get('message')
            # output = ""
            # output += "<html><body>"
            # output += "<h2>Okay how about this : </h2>"
            # output += "<h1>%s </h1>" % messagecontent[0]
            # output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2> What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='submit'></form>"
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output
        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()



if __name__ == '__main__':
    main()