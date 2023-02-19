import yaml
import json

def deploy():
    with open('todo.yml') as f:
        y = yaml.safe_load(f)
    f.close()
    
    install = []
    packages = y['server']['install_packages']
    pip_pk = ['redis', 'bs4']

    install.append({'name': 'Install packages', 'ansible.builtin.package': {'name': packages}})
    install.append({'name': 'Install pip packages', 'ansible.builtin.pip': {'name': pip_pk}})
    
    copy = []
    files = y['server']['exploit_files']
    for file in files:
        copy.append({'name': 'Copy ' + file, 'ansible.builtin.copy': {'src': '../src/' + file, 'dest': file}})
    
    bad_guys = ""
    for guy in y['bad_guys']:
        bad_guys += guy + ','
    
    run = []
    run.append({'name': 'Run ' + files[0], 'ansible.builtin.script': files[0]})
    run.append({'name': 'Run ' + files[1], 'ansible.builtin.script': files[1] + ' -e ' + bad_guys[:-1]})

    dep = {'name': 'genAnsible', 'hosts': 'localhost', 'connection': 'local', 'tasks': install + copy + run}

    with open('deploy.yml', 'w') as w:
        w.write(yaml.dump([dep], sort_keys=False))

if __name__ == '__main__':
    deploy()
