import base64

def encode_file_to_base64(filename):
    with open(filename, 'rb') as file:
        file_content = file.read()
        base64_string = base64.b64encode(file_content).decode('ascii')
    return base64_string

filename = 'your_file.txt'
base64_encoded = encode_file_to_base64(filename)
print(f"Base64 Encoded String: {base64_encoded}")


def base64_to_filename(base64_string):
    return base64_string.replace('/', '_')

# Example usage:
original_filename = base64_to_filename(base64_encoded)
print(f"Reversible Filename: {original_filename}")
