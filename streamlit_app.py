import os
import streamlit as st
import requests
from PIL import Image
from typing import Tuple, Optional
from dotenv import load_dotenv
import base64

load_dotenv()

# ---------------------------- Configuration ---------------------------- #

# Load backend URL from environment variable
BACKEND_URL = os.environ.get("BACKEND_URL")

# Logos
TERRAFORM_LOGO = "https://upload.wikimedia.org/wikipedia/commons/0/04/Terraform_Logo.svg"
AWS_LOGO = "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg"

# Page setup
st.set_page_config(page_title="Terraform Code Generator", page_icon="🛠️", layout="wide")

# ---------------------------- Utility Functions ---------------------------- #

def split_text_and_code(markdown_str: str) -> Tuple[str, Optional[str]]:
    """Splits markdown into descriptive text and Terraform code."""
    start_tag = "```terraform"
    end_tag = "```"
    start_idx = markdown_str.find(start_tag)
    end_idx = markdown_str.rfind(end_tag)

    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        return markdown_str.strip(), None

    text = markdown_str[:start_idx].strip()
    code = markdown_str[start_idx + len(start_tag):end_idx].strip()
    return text, code

def display_header():
    """Displays the header with logos and title."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image(TERRAFORM_LOGO, width=200)
    with col2:
        st.title("📐 Terraform Code Generator")
    with col3:
        st.image(AWS_LOGO, width=50)

def upload_inputs() -> Tuple[Optional[Image.Image], Optional[str]]:
    """Renders file uploader and description input fields."""
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        image_file = st.file_uploader("🖼️ Upload your architecture diagram (PNG/JPG)", type=["png", "jpg", "jpeg"])
        image = Image.open(image_file) if image_file else None
        if image:
            st.image(image, caption="Uploaded Diagram", use_container_width=True)
    
    with col2:
        description = st.text_area(
            "📝 Project Description",
            height=150,
            placeholder="Describe your infrastructure here..."
        )
    
    return image_file, description

def request_terraform_code(image_file, description: str) -> Tuple[str, Optional[str]]:
    """Sends request to backend API and returns parsed text and code."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key not set in environment.")

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    # Convert image to base64
    image_bytes = image_file.getvalue()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = requests.post(
        f"{BACKEND_URL.rstrip('/')}/generate-code",
        json={
            "image_base64": image_b64,
            "project_description": description
        },
        headers=headers,
        timeout=60
    )

    if response.status_code == 200:
        output_str = response.json().get("terraform_code", {}).get("code", "")
        return split_text_and_code(output_str)
    else:
        raise ValueError(response.json().get("error", "Unknown error"))

def display_output(text: Optional[str], code: Optional[str]):
    """Displays the returned text and code from API."""
    if text:
        st.markdown(text)
    if code:
        st.code(code, language="hcl")

# ---------------------------- App Logic ---------------------------- #

def main():
    display_header()
    image_file, description = upload_inputs()

    if st.button("🚀 Generate Terraform Code"):
        if image_file is None or not description.strip():
            st.error("Please upload an image and provide a description.")
        else:
            with st.spinner("Generating Terraform code..."):
                try:
                    text, code = request_terraform_code(image_file, description)
                    st.session_state["output_text"] = text
                    st.session_state["output_code"] = code
                    st.success("✅ Code generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    if "output_text" in st.session_state or "output_code" in st.session_state:
        display_output(st.session_state.get("output_text"), st.session_state.get("output_code"))

# ---------------------------- Run App ---------------------------- #

if __name__ == "__main__":
    main()
