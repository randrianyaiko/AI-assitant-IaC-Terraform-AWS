import os
import logging
import base64
import tempfile
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, Unauthorized
from dotenv import load_dotenv
from src.agent.agent import get_code

load_dotenv()
API_KEY = os.getenv("API_KEY")

def create_app():
    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("app")

    def require_api_key(f):
        from functools import wraps
        @wraps(f)
        def decorated(*args, **kwargs):
            key = request.headers.get("X-API-KEY")
            if key != API_KEY:
                logger.warning("Unauthorized access attempt.")
                raise Unauthorized("Invalid or missing API key.")
            return f(*args, **kwargs)
        return decorated

    @app.route('/generate-code', methods=['POST'])
    @require_api_key
    def generate_code():
        try:
            data = request.get_json(force=True)
            image_base64 = data.get('image_base64')
            project_description = data.get('project_description')

            if not image_base64 or not project_description:
                raise BadRequest("Missing 'image_base64' or 'project_description'")

            # Decode base64 image to a temp file
            image_data = base64.b64decode(image_base64)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(image_data)
                tmp_path = tmp.name

            terraform_code = get_code(image_path=tmp_path, text=project_description)
            logger.info("Terraform code generated successfully.")
            os.remove(tmp_path)

            return jsonify({"terraform_code": terraform_code}), 200

        except BadRequest as e:
            return jsonify({"error": str(e)}), 400
        except Unauthorized as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            logger.exception("Unexpected error during code generation.")
            return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
