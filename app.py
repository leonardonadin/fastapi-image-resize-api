from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
import cv2
import os

app = FastAPI()

@app.post('/')
def resize(file: UploadFile = File(...), ratio_resize: int = Form(...)):
    try:
        file_name = gen_random_string() + '.jpg'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        request_file_path = os.path.join(current_dir, 'tmp/files', file_name)

        contents = file.file.read()
        with open(request_file_path, 'wb') as f:
            f.write(contents)

        file = cv2.imread(request_file_path)

        new_width = int(file.shape[1] / ratio_resize)
        new_height = int(file.shape[0] / ratio_resize)

        resized_file = cv2.resize(file, (new_width, new_height))

        new_file_path = os.path.join(current_dir, 'tmp/resized', file_name)

        cv2.imwrite(new_file_path, resized_file)
        
        return FileResponse(new_file_path)


    except Exception as e:
        return e.args

def gen_random_string():
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

@app.route('/clean_up')
def clean_up():
    import os
    for file in os.listdir('./tmp/files'):
        if file.endswith('.jpg'):
            os.remove(file)
    for file in os.listdir('./tmp/resized'):
        if file.endswith('.jpg'):
            os.remove(file)

if __name__ == '__main__':
    app.run(debug=True)
