import streamlit as st
import pyzipper
from io import BytesIO
import base64

def create_encrypted_zip_base64(password, password_padding_pattern, file_name, file_content):
    password += password_padding_pattern[len(password):]
    output_stream = BytesIO()
    with pyzipper.AESZipFile(output_stream, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zip_file:
        zip_file.setpassword(password.encode('utf-8'))
        zip_file.writestr(file_name, file_content)
    output_stream.seek(0)
    zip_bytes = output_stream.read()
    base64_zip = base64.b64encode(zip_bytes).decode('utf-8')
    return base64_zip

st.title("Encrypted Zip File Creator (Base64 Output)")

password = st.text_input("Enter Password", type="password")
password_padding_pattern = st.text_input("Enter Password Padding Pattern (Salt)")
uploaded_file = st.file_uploader("Upload a file")

if st.button("Generate Encrypted Zip (Base64)") and uploaded_file and password and password_padding_pattern:
    file_name = uploaded_file.name
    file_content = uploaded_file.read()
    base64_zip = create_encrypted_zip_base64(password, password_padding_pattern, file_name, file_content)
    st.text_area("Base64 Encoded Encrypted Zip", base64_zip, height=200)
