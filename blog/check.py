import base64


def encode_image_to_base64_with_prefix(file_path):
    with open(file_path, "rb") as image_file:
        image_bytes = image_file.read()
    ext = file_path.split('.')[-1].lower()
    b64_data = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/{ext};base64,{b64_data}"


def decode_base64_to_file(b64_string, output_path):
    try:
        # Try to decode full base64 string including prefix
        decoded_bytes = base64.b64decode(b64_string)
        with open(output_path, "wb") as f:
            f.write(decoded_bytes)
        print(f"Decoded file saved to {output_path} (without removing prefix)")
    except Exception as e:
        print(f"Failed to decode with prefix: {e}")


def decode_base64_to_file_proper(b64_string, output_path):
    try:
        # Remove prefix first
        if "," in b64_string:
            b64_string = b64_string.split(",")[1]
        decoded_bytes = base64.b64decode(b64_string)
        with open(output_path, "wb") as f:
            f.write(decoded_bytes)
        print(f"Decoded file saved to {output_path} (after removing prefix)")
    except Exception as e:
        print(f"Failed to decode properly: {e}")


if __name__ == "__main__":
    input_image_path = "./logo.png"  # Change this to your image path
    output_path_wrong = "decoded_wrong.png"
    output_path_correct = "decoded_correct.png"

    b64_with_prefix = encode_image_to_base64_with_prefix(input_image_path)
    print("Base64 with prefix:")
    print(b64_with_prefix[:100] + "...")  # print first 100 chars only

    decode_base64_to_file(b64_with_prefix, output_path_wrong)
    decode_base64_to_file_proper(b64_with_prefix, output_path_correct)
