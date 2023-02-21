from bs4 import BeautifulSoup as bs
import os, sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)

from app.updater.settings import USER, REPO, APP_NAME


with open(os.path.join(os.path.dirname(__file__), 'main.md'), 'r') as f:
    # search paths
    soup = bs(f, 'html.parser')

paths = []

for inc_tag in soup.find_all('include'):
    path = inc_tag.get('path')
    paths.append(path)

# init stub
with open('README.stub','w') as f:
    f.write('')

# # construct base
for path in paths:
    # template readme
    with open(os.path.join(os.path.dirname(__file__), path), 'r') as f:
        readme_stub = f.read()

    with open('README.stub','a') as f:
        f.write(readme_stub)

# init md
with open('README.md','w') as f:
    f.write("")

struct = {
    '{logo_name}': f'{APP_NAME} logo',
    '{app_name}': APP_NAME,
    '{USER}': USER,
    '{REPO}': REPO,
}

# template readme
with open('README.stub') as f:
    readme = f.read()
# put potential variables
for key, value in struct.items():
    readme = readme.replace(key, value)
    with open('README.md','w') as f:
        f.write(readme)
