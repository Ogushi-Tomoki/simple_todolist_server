#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import requests

todolist = []

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]

        # パスの確認
        if path_elements[0] != 'api' or path_elements[1] != 'v1' or path_elements[2] != 'todo':
            self.send_response(404)
            self.end_headers()
            return

        try:
            arguments = [int(x) for x in path_elements[3:]]
        except:
            self.send_response(400)
            self.end_headers()
            return

        # パスの長さが3か4の場合以外はエラー
        if len(arguments) != 1 and len(arguments) != 0:
            self.send_response(404)
            self.end_headers()
            return

        try:
            # パスの長さが4の場合
            if len(arguments) == 1:
                argument = arguments[0]
                response = todolist[argument]
            # パスの長さが3の場合
            elif len(arguments) == 0:
                response = {"todo": todolist}

            self.send_response(200)
            self.send_header('Context-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))
            return
        except Exception as e:
            print("Not Found")
            print(e)
            self.send_response(404)
            self.end_headers()
            return


    def do_POST(self):
        content_len=int(self.headers.get('content-length'))
        requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))

        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]

        # パスの確認
        if path_elements[0] != 'api' or path_elements[1] != 'v1' or path_elements[2] != 'todo':
            self.send_response(404)
            self.end_headers()
            return

        # パスの長さが3の場合以外はエラー
        if len(path_elements) != 3:
            self.send_response(404)
            self.end_headers()
            return

        if len(requestBody) != 3 or "deadline" not in requestBody or "title" not in requestBody or "memo" not in requestBody:
            response = {"status": "failure", "message": "invalid date format"}
            self.send_response(400)
            self.send_header('Context-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))
            return

        try:

            global todolist

            # todoリストに追加する
            idnumber = len(todolist)
            requestBody["id"] = idnumber
            todolist.append(requestBody)

            # レスポンスを返す
            response = {"status": "success", "message": "registered", "id": idnumber}
            self.send_response(200)
            self.send_header('Context-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))
            return

        except Exception as e:
            response = {"status": "failure", "message": "invalid date format"}
            print(e)
            self.send_response(400)
            self.send_header('Context-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))
            return


def main():
    server = HTTPServer(('', 8080), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()