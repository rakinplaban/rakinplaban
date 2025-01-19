import markdown
from bs4 import BeautifulSoup
import json
import chardet
from datetime import datetime

with open("imagelink.json", "r") as f:
    data = json.load(f)

# Get the list of image URLs
images = data["images"]

# Option 1: Rotate images based on the current day
# You can also use hours or minutes if needed
index = datetime.now().day % len(images)

# Option 2: Randomly select an image
# index = random.randint(0, len(images) - 1)

selected_image = images[index]

def get_encoding_type(file_path):
    with open(file_path, 'rb') as f:
        sample = f.read(1024)
        cur_encoding = chardet.detect(sample)['encoding']
        return cur_encoding

with open("README.md", "r", encoding = get_encoding_type("README.md"),errors='ignore') as f:
    
    markdown_content = f.read()


html_content = markdown.markdown(markdown_content)

parser = BeautifulSoup(html_content, "html.parser")



img_id = parser.find("img",{'id':'updatable'})

original_html = str(img_id)

try:
    # img_source = img_id['src']
    # print("Image source: ",img_source)
    img_id['src'] = selected_image
    updated_html = str(img_id)
    print("Updated HTML: ", img_id['src'])
    updated_markdown_content = markdown_content.replace(original_html, updated_html)
    print("Updated Markdown Content: ", updated_markdown_content)
    with open('README.md','w',encoding=get_encoding_type('README.md'),errors='ignore') as file:
        file.write(updated_markdown_content)

    

except:
    print("No image found")