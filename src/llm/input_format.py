from src.image_encoder.encode import image_to_base64

def format_input(text:str, image_path:str):
    image_data = image_to_base64(image_path)
    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": text,
            },
            {
                "type": "image",
                "source_type": "base64",
                "data": image_data,
                "mime_type": "image/jpeg",
            },
            {
                "type": "text",
                "text": """ I want you to describe the image of the diagram. 
                            Give a very detailed description as you are an expert in AWS. 
                            Answer technically like you are an AWS Cloud Engineer with expertise in designing Cloud Architecture and Workloads.
                            If there is any Bucket names, EC2 machine names, Lambda function names, specified region, AZ and so on... Keep them to the diagram description.

                            """,
            },
        ],
    }

