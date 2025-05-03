from http.server import HTTPServer, BaseHTTPRequestHandler
import json # тъй като javascript ще ни праща данни в json формат и ще трябва да ги parse-ваме
import validation
import databaseHandle

class Server(BaseHTTPRequestHandler):

    host = 'localhost' # ще върви само на локален сървър (компютъра, който изпълнява server.py файла)
    port = 8080
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html' # тъй като това е главната страница, искаме при достъп до сайта да ни препраща там
        try:
            file = open(self.path[1:]).read() # отваряме файла <Нещо си>.html, като преди това премахваме водещата '/'
            self.send_response(200) # Ако файла се е отворил успешно на горния ред, изпращаме отговор с код 200
        except:
            file = "File Not Found" 
            self.send_response(404) # ако няма такъв файл, или файла не може да бъде отворен поради някаква друга причина, изпращама error код 404
        self.end_headers()
        self.wfile.write(bytes(file, 'utf-8'))

    def _load_data(self):
        length = self.headers['Content-Length'] # намира дължината на получените данни в байтове
        length = int(length) # защото е стринг
        data = self.rfile.read(length) # прочита толкова байта от json-format данните, който сме изпратили
        data = json.loads(data)
        return data

    def do_POST(self):
        if self.path == '/RegistrationPage.html':
            data = self._load_data()
            validation_results = validation.validate_registration(data)
            if validation_results[0] == False:
                self.send_response(300)
                output = json.dumps(validation_results[1])
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length" , str(len(output)))
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
            else:
                if databaseHandle.check_already_registered(data['emailText']):
                    self.send_response(314)
                    self.end_headers()
                else:
                    databaseHandle.insert_new_user(data)
                    self.send_response(200)
                    self.end_headers()
        elif self.path == '/changeFirstName.html':
            data = self._load_data()
            validation_results = validation.validate_name(data['firstNameText'])
            if validation_results == True:
                databaseHandle.update_value_by_email("FirstName", data['firstNameText'] , data['emailText'])
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(300)
                output = json.dumps({'FirstName' : "Name: Invalid!"})
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length" , str(len(output)))
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
        elif self.path == '/changeLastName.html':
            data = self._load_data()
            validation_results = validation.validate_name(data['lastNameText'])
            if validation_results == True:
                databaseHandle.update_value_by_email("lastName", data['lastNameText'] , data['emailText'])
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(300)
                output = json.dumps({'LastName' : "Name: Invalid!"})
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length" , str(len(output)))
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))

            
server = HTTPServer((Server.host, Server.port), Server)
server.serve_forever()