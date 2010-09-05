from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.files import *
from unipath import Path

import datetime
import fabric
import os
import random

me = 'yourname'

def run(*args, **kwargs):
    return fabric.api.run(*args, pty=True, **kwargs)

def sudo(*args, **kwargs):
    return fabric.api.run(*args, pty=True, **kwargs)

def h():
    print('Installation:')
    print('linode_prep')
    print('root@remote system_setup')
    print('%s@remote user_setup' % me)
    print('root@remote project_setup:li,dev_domain.com,stage_domain.com')
    print('root@localhost initialize:li-dev,/home/yourname/Dropbox/li,/srv/li-dev,sqlite')
    print('After installation:')
    print('root@remote,root@localhost rf:li')
    print('root@remote stage:li')

def linode_setup():
    messages = (
        "Did you choose Fremont for your Linode's datacenter?",
        "Did you deploy 32-bit Ubuntu 10.04 to your Linode?",
        "Did you record your Linode's root password?",
        "Did you boot up your Linode?",
        "Did you record your Linode's IP address ('eth0') in :c and :accounts?",
        "Did you log in to your Linode via the AJAX console, run 'ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub', and record the output in :c and :accounts?",
        "Did you attempt ssh in to your linode and make sure you were given the right RSA key fingerprint?",
        "If localhost is not a known host, did you ssh in to localhost with your internet off and confirm the key fingerprint?",
    )
    for message in messages:
        if not confirm(message):
            quit()

def system_setup():
    sudo('aptitude update -y')
    sudo('aptitude full-upgrade -y')
    etckeeper_setup()
    hostname = raw_input('What do you want to name your new system? ')
    sudo('echo "%s" > /etc/hostname' % hostname)
    sudo('hostname -F /etc/hostname')
    ensure_single_sub('/etc/hosts', '^$', '%s\\t%s\\n' % ('127.0.0.1', hostname), use_sudo=True)
    etc('Configure hostname')
    if confirm("Would you like to ensure your new server's hostname is in your local /etc/hosts?"):
        ip = env.host
        if not confirm("Is %s is your Linode's IP address?" % ip):
            ip = raw_input("Please enter your Linode's IP address: ")
        with settings(host='localhost'):
            ensure_single_sub('/etc/hosts', '^$', '%s\\t%s\\n' % (ip, hostname), use_sudo=True)

    sudo('ln -sf /usr/share/zoneinfo/UTC /etc/localtime')
    etc('Set local time')

    packages = (
        'ack-grep',
        'less',
        'python-setuptools',
        'vim-nox', 
        'wget',
        'zsh',
    )
    sudo('aptitude -y install %s' % ' '.join(packages))
    etc('Install various packages with aptitude')

    sudo('easy_install pip')
    sudo('pip install ipython virtualenv')
    etc('Install various packages with pip')

    sudo('virtualenv --no-site-packages /srv/base-py-env')

    with settings(warn_only=True):
        sudo('update-alternatives --set pager /bin/less')
        sudo('git config --system --bool color.ui true')
        sudo('git config --system --path core.pager less')
        sudo('git config --system diff.renames copy')
    etc('Change various preferences')

    with settings(warn_only=True):
        sudo("adduser --shell=/usr/bin/zsh --gecos='%s,,,' --disabled-login %s" % (me, me))
        sudo("adduser " + me + " sudo")
        etc('Add user ' + me)
    
    sudo("wget 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'")
    sudo('unzip compiler-latest.zip -d compiler-latest')
    sudo('mv compiler-latest/compiler.jar /usr/local/bin/closure-compiler.jar')
    sudo('chmod a+r /usr/local/bin/closure-compiler.jar')
    sudo('rm -r compiler-latest')
    print("Log in as root and run \npasswd " + me + "\n to set " + me + "'s password, then run user_setup with " + me + " as the user")

def etckeeper_setup():
    if not exists('/etc/.git'):
        packages = (
            'bzr',
            'etckeeper',
            'git-core',
        )
        sudo('aptitude -y install %s' % ' '.join(packages))
        with settings(warn_only=True):
            sudo('etckeeper init')
        if not exists('/etc/.git'):
            sudo('etckeeper uninit -f')
            comment('/etc/etckeeper/etckeeper.conf', 'VCS="bzr"', use_sudo=True, char='# ', backup='.bak')
            uncomment('/etc/etckeeper/etckeeper.conf', 'VCS="git"', use_sudo=True, backup='.bak')
            sudo('rm /etc/etckeeper/etckeeper.conf.bak')
            sudo('etckeeper init')
        append('*.bak', '/etc/.gitignore', use_sudo=True)
        sudo('chmod -R a+rx /etc/.git')
        sudo('chmod a+w /etc/.git')
        sudo('chmod -R a+rx /etc/.etckeeper')
        sudo('aptitude -y remove bzr')
        etc('Initial commit')

def etc(message):
    with settings(warn_only=True):
        sudo('etckeeper commit "%s"' % message)

def ensure_single_sub(filename, before, after, use_sudo=False, **kwargs):
    search_pattern = after
    while search_pattern.endswith('\\n'):
        search_pattern = search_pattern[:len('\\n')]
    if not contains(search_pattern, filename, use_sudo):
        single_sub(filename, before, after, use_sudo, **kwargs)

def single_sub(filename, before, after, use_sudo=False, backup='.bak'):
    before = re.sub('/', '\\/', before)
    after = re.sub('/', '\\/', after)
    command = "sed -i%s -r -e '0,/%s/s//%s/' %s" % (backup, before, after, filename)
    if use_sudo:
        sudo(command, shell=False)
    else:
        run(command, shell=False)

def user_setup():
    with cd('~'):
        run('wget -O dropbox.tar.gz http://www.dropbox.com/download/?plat=lnx.x86')
        run('tar -zxof dropbox.tar.gz')
        run('rm dropbox.tar.gz')
        run('mkdir -p ~/tpe')
        run("wget -P ~/tpe 'http://www.dropbox.com/download?dl=packages/dropbox.py'")
        run('chmod +x ~/tpe/dropbox.py')
        run('touch ~/.cli-only')
        run('mkdir tb')
        run('mkdir .trashinfo')
        print('Visit the url in the output of the following command:')
        run('~/.dropbox-dist/dropboxd &')
        print("When you first log in, run")
        print("~/tpe/dropbox.py start")
        print("chmod +x ~/Dropbox/bin/*")
        print("~/Dropbox/bin/db-symlinks.py")
        print("Then log out.")
        print("Then run")
        print("~/tpe/ssh_keygen.sh")

public_media = ['uploads', 'v1']

def project_setup(name, dev_domain=None, stage_domain=None, error_email='xylowolf@gmail.com'):
    dev_name = '%s-dev' % name
    stage_name = '%s-stage' % name
    dev_repo = '/home/yourname/Dropbox/%s' % name
    stage_repo = '/srv/%s-stage/%s' % (name, name)
    dev_install = '/srv/%s-dev' % name
    stage_install = '/srv/%s-stage' % name
    initialize(dev_name, dev_repo, dev_install, 'sqlite3')
    push(dev_repo, dev_name, dev_repo, dev_install)
    initialize(stage_name, stage_repo, stage_install, 'postgres')
    push(dev_repo, stage_name, stage_repo, stage_install)
    for d in public_media:
        sudo('mkdir -p %s' % Path('/srv/%s-dev' % name).child('media', 'public', d))
        sudo('chmod a+w %s' % Path('/srv/%s-dev' % name).child('media', 'public', d))
        sudo('mkdir -p %s' % Path('/srv/%s-stage' % name).child('media', 'public', d))
        sudo('chmod a+w %s' % Path('/srv/%s-stage' % name).child('media', 'public', d))
    sudo('a2enmod rewrite')
    with settings(warn_only=True):
        if confirm('Autogenerate httpd.conf files based on /home/yourname/Dropbox/%s/setup/httpd.conf on your local filesystem?' % name):
            def upload_conf(fullname, repo, install, domain, error_email, versioned_alias):
                upload_template('/home/yourname/Dropbox/%s/setup/httpd.conf' % name, '/tmp/%s.conf' % fullname, context = {
                    'fullname': fullname,
                    'repo': repo,
                    'install': install,
                    'domain': domain,
                    'error_email': error_email,
                    'versioned_alias': versioned_alias,
                })
                sudo('chmod a+r /tmp/*.conf')
                sudo('cat /tmp/%s.conf >> /etc/apache2/httpd.conf' % fullname)
            upload_conf(dev_name, dev_repo, dev_install, dev_domain, error_email, 'Alias /versioned/ %s/media/versioned/' % dev_install)
            upload_conf(stage_name, stage_repo, stage_install, stage_domain, error_email, '')
            etc('Upload naive httpd.conf files')
    print('# fix apache configuration with')
    print('se /etc/apache2/httpd.conf')
    print('# after changing etc run')
    print('sudo etckeeper commit')
    print('# to run management commands')
    print('source %s; cd %s' % (Path(dev_install).child('bin', 'activate'), Path(dev_repo).child('my')))
    print('source %s; cd %s' % (Path(stage_install).child('bin', 'activate'), Path(stage_repo).child('my')))
    print('# to gracefully restart the server')
    print('sudo /etc/init.d/apache2 graceful')

def stage(name):
    ensure_relative_symlinks('/home/yourname/Dropbox/%s' % name)
    if confirm('Is DJANGO_STATIC True?') and confirm('Is DEBUG False?') and confirm('Did you test on other browsers?') and confirm('Did you git commit?'):
        push('/home/yourname/Dropbox/%s' % name, '%s-stage' % name, '/srv/%s-stage/%s' % (name, name), '/srv/%s-stage' % name)
        for d in public_media:
            sudo('mkdir -p %s' % Path('/srv/%s-stage' % name).child('media', 'public', d))
            sudo('chmod -R a+w %s' % Path('/srv/%s-stage' % name).child('media', 'public', d))
        sudo('mkdir -p %s' % Path('/srv/%s-stage' % name).child('media', 'public', 'build'))
        sudo('chmod -R a+w %s' % Path('/srv/%s-stage' % name).child('media', 'public', 'build'))

def rf(name):
    sudo("killall -SIGSTOP '/home/yourname/.dropbox-dist/dropbox'")
    ensure_relative_symlinks('/home/yourname/Dropbox/%s' % name)
    push('/home/yourname/Dropbox/%s' % name, '%s-dev' % name, '/home/yourname/Dropbox/%s' % name, '/srv/%s-dev' % name)
    for d in public_media:
        sudo('mkdir -p %s' % Path('/srv/%s-dev' % name).child('media', 'public', d))
        sudo('chmod -R a+w %s' % Path('/srv/%s-dev' % name).child('media', 'public', d))
    sudo('mkdir -p %s' % Path('/srv/%s-dev' % name).child('media', 'public', 'build'))
    sudo('chmod -R a+w %s' % Path('/srv/%s-dev' % name).child('media', 'public', 'build'))
    sudo("killall -SIGCONT '/home/yourname/.dropbox-dist/dropbox'")

def initialize(name, repo, install, database):
    '''
    Initialize an installation.
    
    name -- the codename of the installation
    repo -- the path to the repository associated with this installation
    install -- the path to the root of this installation
    database -- a string representing the database backend for this installation
    
    '''
    with settings(warn_only=True):
        sudo("adduser --gecos=',,,' --disabled-login %s" % name)
    repo, install = [Path(path) for path in (repo, install)]
    sudo('virtualenv --no-site-packages %s' % install)
    sudo('mkdir -p %s' % install.child('media', 'public', 'build'))
    with settings(warn_only=True):
        sudo('ln -s %s %s' % (install.child('lib', 'python2.6', 'site-packages', 'django', 'contrib', 'admin', 'media'), install.child('media', 'public', 'admin')))
        sudo('ln -s %s %s' % (repo.child('media'), install.child('media', 'versioned')))
    for kind in ('application', 'error', 'request'):
        sudo('touch %s' % install.child(kind + '.log'))
    sudo('chmod a+w %s' % install.child('*.log'))
    if database.startswith('sqlite'):
        sudo('mkdir -p %s' % install.child('db'))
        sudo('touch %s' % install.child('db', 'db.sqlite3'))
        sudo('chmod -R a+w %s' % install.child('db'))
    elif database.startswith('postgres'):
        sudo('aptitude install -y postgresql')
        print('# commands to initialize postgresql')
        print('sudo -u postgres psql postgres')
        print('sudo -u postgres createuser -D -A -P %s' % name)
        print('sudo -u postgres createdb -O %s %s' % (name, name))
        print('se /etc/postgresql/8.4/main/pg_hba.conf')
        print('# change this line')
        print('localhost   all   all   ident')
        print('# to this')
        print('localhost   all   all   md5')
        print('sudo /etc/init.d/postgresql-8.4 restart')
        confirm("Did you get that?")
    else:
        raise AssertionError('invalid database string')
    with settings(warn_only=True):
        sudo('chown -R %s:%s %s %s' % (me, me, repo, install))

def push(source, name, dest, install):
    '''
    Push changes from one installation to another--or, if source and dest are the same, refresh an installation.
    
    source -- the path to the repository that is being pushed
    name -- the codename of the installation receiving the push
    dest -- the path to the repository receiving the push
    install -- the path to the root of the installation receiving the push
    
    '''
    def change_etc(etc, print_only=False):
        '''Change the etc in the destination directory'''
        sudo('mkdir -p /root/tb')
        sudo('mkdir -p /root/.trashinfo')
        sudo('chmod a+x /home/%s/bin/*' % me)
        commands = [
            'touch %s' % dest.child('etcs', etc, 'apache', 'django.wsgi'),
            '/home/%s/bin/t -f %s' % (me, dest.child('my', 'etc')),
            'ln -s %s %s' % (dest.child('etcs', etc), dest.child('my', 'etc')),
        ]
        if print_only:
            print '; '.join(commands)
        else:
            for command in commands:
                sudo(command)

    source, dest, install = [Path(path) for path in (source, dest, install)]
    change_etc('maint')
    if source.norm() != dest.norm():
        sudo('mkdir -p %s' % install.child('old-repos'))
        sudo('mkdir -p %s' % dest)
        sudo('cp -r %s %s' % (dest, install.child('old-repos', datetime.datetime.now().isoformat())))
        sudo('rsync -ahvEP %s %s' % (source.child('*'), dest))
    sudo('aptitude install -y `python -c \'with open("%s") as f: print " ".join([line.rstrip("\\n") for line in f.readlines()])\'`' % dest.child('setup', 'apt-requirements.txt'))
    sudo('pip install -E %s -r %s' % (install, dest.child('setup', 'pypi-requirements.txt')))
    sudo('chmod a+x %s' % dest.child('my', 'manage.py'))
    sudo('chgrp -R %s %s %s %s' % (me, source, dest, install))
    if confirm('Do you need to do any database migrations?'):
        print('# source the virtualenv and manage the installation with')
        print('source %s; cd %s' % (install.child('bin', 'activate'), dest.child('my')))
        print('# migration syntax is')
        print('manage.py migrate')
        print("# (make sure you haven't created any destructive migrations")
        print("# when you've run all the migrations, execute")
        change_etc(name, print_only=True)
        confirm("Did you get that?")
    else:
        change_etc(name)

def ensure_relative_symlinks(directory):
    # Will only work on local machine due to use of os module.
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames + dirnames:
            try:
                target = os.readlink(os.path.join(dirpath, filename))
            except OSError:
                target = None
            if target:
                if target.startswith(os.path.sep) and 'etcs' not in target:
                    raise AssertionError("%s points to %s (an absolute path)" % (filename, target))
