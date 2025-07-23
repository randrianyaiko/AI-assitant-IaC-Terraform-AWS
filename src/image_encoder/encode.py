import base64

def image_to_base64(imagepath:str):
    with open(imagepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')

