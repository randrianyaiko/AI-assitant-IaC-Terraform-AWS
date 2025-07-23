import logging
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from src.agent.agent import get_code

def create_app():
    app = Flask(__name__)

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @app.route('/generate-code', methods=['POST'])
    def generate_code():
        try:
            data = request.get_json(force=True)

            image_path = data.get('image_path')
            project_description = data.get('project_description')

            if not image_path or not project_description:
                logger.warning("Missing 'image_path' or 'project_description'")
                raise BadRequest("Missing 'image_path' or 'project_description'")

            # Process the input and get Terraform code
            terraform_code = get_code(image_path=image_path, text=project_description)
            logger.info("Terraform code generated successfully.")

            return jsonify({"terraform_code": terraform_code}), 200

        except BadRequest as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            logger.exception("Unexpected error during code generation.")
            return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == '__main__':
    # Use a production WSGI server like gunicorn in real deployments
    app.run(host='0.0.0.0', port=5000, debug=False)
