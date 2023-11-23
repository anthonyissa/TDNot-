from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64


KEY = os.urandom(32)  # Générer une clé de 32 octets (256 bits) pour AES

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length'))
        # print(length)
        body = self.rfile.read(length).decode('utf-8')
        # print(body)
        data = parse_qs(body)
        hashed_password = data['hashed_password'][0]
        print(hashed_password)
        hashed_password_bytes = hashed_password.encode('utf-8')  # Si hashed_password est une chaîne normale
        # ou hashed_password_bytes = bytes.fromhex(hashed_password) si c'est une chaîne hexadécimale
        encrypted_password = self.encrypt_aes(hashed_password_bytes)

        base64_encrypted_password = base64.b64encode(encrypted_password)
        print(base64_encrypted_password)
        
        self.send_response(200)
        #self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(base64_encrypted_password)

    def encrypt_aes(self, data):
        cipher = Cipher(algorithms.AES(KEY), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        return encryptor.update(padded_data) + encryptor.finalize()
    
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}')
    httpd.serve_forever()

run()