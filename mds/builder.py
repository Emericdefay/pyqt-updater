import os, sys
from bs4 import BeautifulSoup as bs

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)

from app.updater.settings import USER, REPO, APP_NAME


# vars
paths = []
struct = {
    '{logo_name}': f'{APP_NAME} logo',
    '{app_name}': APP_NAME,
    '{USER}': USER,
    '{REPO}': REPO,
}

# init soup
with open(os.path.join(os.path.dirname(__file__), 'main.md'), 'r') as f:
    # search paths
    soup = bs(f, 'html.parser')

# init stub
with open('README.stub','w') as f:
    f.write('')
# create stub
for index, inc_tag in enumerate(soup.find_all('include')):
    path = inc_tag.get('path')
    # template readme
    with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        readme_stub = f.read()
    inc_tag.string = readme_stub
soup.include.replaceWithChildren()
# write out stub
with open('README.stub','w') as f:
    f.write(soup.text)

# init md
with open('README.md','w') as f:
    f.write("")
# template readme
with open('README.stub') as f:
    readme = f.read()
# put potential variables
for key, value in struct.items():
    readme = readme.replace(key, value)
    with open('README.md','w') as f:
        f.write(readme)
