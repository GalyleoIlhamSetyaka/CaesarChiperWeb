from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

def encrypt(text, key):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            ascii_val = ord(char)
            if char.islower():
                encrypted_ascii = ((ascii_val - 97 + key) % 26) + 97
            else:
                encrypted_ascii = ((ascii_val - 65 + key) % 26) + 65
            encrypted_text += chr(encrypted_ascii)
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, key):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            ascii_val = ord(char)
            if char.islower():
                decrypted_ascii = ((ascii_val - 97 - key + 26) % 26) + 97
            else:
                decrypted_ascii = ((ascii_val - 65 - key + 26) % 26) + 65
            decrypted_text += chr(decrypted_ascii)
        else:
            decrypted_text += char
    return decrypted_text

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    key = int(request.form['key'])
    file = request.files['file']
    filename = file.filename
    file_ext = filename.split('.')[-1]
    if file_ext not in ['txt']:
        return 'File format not supported.'
    text = file.read().decode('utf-8')
    encrypted_text = encrypt(text, key)
    encrypted_filename = 'encrypted_' + filename
    encrypted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
    with open(encrypted_filepath, 'w') as encrypted_file:
        encrypted_file.write(encrypted_text)
    return send_from_directory(app.config['UPLOAD_FOLDER'], encrypted_filename, as_attachment=True)


@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    key = int(request.form['key'])
    file = request.files['file']
    filename = file.filename
    file_ext = filename.split('.')[-1]
    if file_ext not in ['txt']:
        return 'File format not supported.'
    text = file.read().decode('utf-8')
    decrypted_text = decrypt(text, key)
    decrypted_filename = 'decrypted_' + filename
    decrypted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], decrypted_filename)
    with open(decrypted_filepath, 'w') as decrypted_file:
        decrypted_file.write(decrypted_text)
    return send_from_directory(app.config['UPLOAD_FOLDER'], decrypted_filename, as_attachment=True)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
