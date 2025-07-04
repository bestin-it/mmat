import markdown

with open('README.md', 'r', encoding='utf-8') as input_file:
    text = input_file.read()

html = markdown.markdown(text)

with open('readme.html', 'w', encoding='utf-8') as output_file:
    output_file.write(html)

print("README.md converted to readme.html")
