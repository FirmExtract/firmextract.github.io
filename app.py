import os
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

env = Environment(loader=FileSystemLoader('templates'))
cwd = os.getcwd()

POST_PATH = os.path.join(cwd, 'posts')
HTML_BASE = 'static'

os.makedirs(os.path.join(HTML_BASE, 'posts'), exist_ok=True)

file_cnt = 0
post_list = []
head_list = []
prev_list = []

for filename in os.listdir(os.path.join(cwd, HTML_BASE, 'posts/')):
    if os.path.splitext(filename)[-1] == '.html':
        prev_list.append(os.path.splitext(filename)[0])

for filename in os.listdir(POST_PATH):
    if os.path.splitext(filename)[-1] == '.set':
        post_list.append(os.path.splitext(filename)[0])

for filename in post_list:
    with open(os.path.join(POST_PATH, filename + '.md'), 'r', encoding='utf-8') as fh:
        text = markdown.markdown(fh.read(), extensions=['extra'])
        head = []

        with open(os.path.join(POST_PATH, filename + '.set'), 'r', encoding='utf-8') as fh:
            for line in fh.readlines():
                line = line.strip()
                if line != '':
                    head.append(line)
        
        head[3] = datetime.strptime(head[3], '%Y-%m-%d').strftime('%B %d, %Y')

        template = env.get_template('post.html')
        with open(os.path.join(cwd, HTML_BASE, 'posts/', f'{filename}.html'), 'w', encoding='utf-8') as fh:
            fh.write(template.render(head=head, text=text))

        head_list.append([filename] + head)

        if filename not in prev_list:
            print(f'+ {filename}')
        else:
            print(f'{filename}')

        file_cnt += 1

head_list.sort(reverse=True, key=lambda x: datetime.strptime(x[4], '%B %d, %Y'))

template = env.get_template('index.html')    
with open(os.path.join(cwd, HTML_BASE, 'index.html'), 'w', encoding='utf-8') as fh:
    fh.write(template.render(headlist=head_list))

print(f'create {file_cnt - len(prev_list)} posts, {file_cnt} posts, done.')