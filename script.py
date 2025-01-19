import json
import chardet
from datetime import datetime
import re

# Load image links from a JSON file
with open("imagelink.json", "r") as f:
    data = json.load(f)

# Get the list of image URLs
images = data["images"]

# Rotate images based on the current day
print(datetime.now().hour, "<- The hour :: The length ->",len(images))
index = datetime.now().hour % len(images)
print(index)
selected_image = images[index]

# Function to detect the encoding type of a file
def get_encoding_type(file_path):
    with open(file_path, 'rb') as f:
        sample = f.read(1024)
        cur_encoding = chardet.detect(sample)['encoding']
        return cur_encoding

# Read the original Markdown file
with open("README.md", "r", encoding=get_encoding_type("README.md"), errors='ignore') as f:
    markdown_content = f.read()

# Regex pattern to find the <img> tag with id="updatable"
img_pattern = r'<img[^>]*id=["\']updatable["\'][^>]*>'

# Search for the tag
match = re.search(img_pattern, markdown_content)

if match:
    original_img_tag = match.group(0)

    # Regex to update the src attribute within the <img> tag
    updated_img_tag = re.sub(
        r'src=["\'][^"\']*["\']',  # Match src="current_link"
        f'src="{selected_image}"',  # Replace with new link
        original_img_tag
    )

    # Replace the original <img> tag with the updated one in the Markdown content
    updated_markdown_content = markdown_content.replace(original_img_tag, updated_img_tag)

    # Write the updated content back to the file
    with open("README.md", "w", encoding=get_encoding_type("README.md"), errors='ignore') as f:
        f.write(updated_markdown_content)

    print("Image link updated successfully!")
    print("Original tag:", original_img_tag)
    print("Updated tag:", updated_img_tag)
else:
    print("No <img> tag with id='updatable' found in the Markdown file.")
