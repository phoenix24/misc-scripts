from __future__ import with_statement # needed for python 2.5
from fabric.api import *

from datetime import datetime
import urllib

# globals
env.project_name = 'madduck3'

# environments, development server.
def localhost():
    """ Use the local virtual server """
    env.hosts = ['localhost']
    env.user = 'chaitanya'
    env.path = '/home/%(user)s/Projects/madduck2/%(project_name)s' % env
    env.virtualhost_path = env.path


# environments, staging server.
def staging():
    """ the production server """
    env.hosts = ['192.168.1.4']
    env.user = 'chaitanya'
    env.path = '/home/chaitanya/Projects/madduck2/%(project_name)s' % env
    env.virtualhost_path = env.path


# environments, production server.
def production():
    """ the production server """
    env.hosts = ['icrack.it']
    env.user = 'gopi'
    env.path = '/home/gopi/%(project_name)s' % env
    env.virtualhost_path = env.path

# tasks
def test():
    """ Run the test suite and bail out if it fails """
    result = local("cd %(path)s; python manage.py test" % env)

def upgrade():
   """ deploy the latest codebase on the given server. """
   run('ls %(path)s -l;' % env, pty=True)
   run('cd %(path)s; git pull origin master' % env, pty=True)
   run('cd %(path)s;' % env, pty=True)
#   local('git pull origin master')


# Helpers. These are called by other functions rather than directly
def create_tar():
    """creates an application tar for; labled as release; ready for deployment; """
    local('git archive --format=tar master | gzip > releases/%(release)s.tar.gz' % env)
    print '%(release)s : release tar successfully created.' % env

def upload_tar():
    """ uploads the created tar. """
    run('mkdir -p  %(path)s/releases/%(release)s' % env)
    run('mkdir -p %(path)s/packages/' % env)
    put('releases/%(release)s.tar.gz' % env, '%(path)s/packages' % env)

    print '%(release)s : release tar successfully uploaded.' % env
    run('cd %(path)s/releases/%(release)s/ && tar zxf %(path)s/packages/%(release)s.tar.gz' % env)

def install_requirements():
    """ installing the release requirements. """
    #run('pip install -E . -r %(path)s/releases/%(release)s/requirements/apps.txt' )
    run('source ~/.gopirc; workon madduck2; pip install -r %(path)s/releases/%(release)s/requirements/apps.txt' % env)

def install_site():
    """ install the release; """
    """ @todo, i dont link this approach, will fix later. """
    run('rm -rf %(path)s/../madduck2' % env)
    run('cp -ar %(path)s/releases/%(release)s %(path)s/../madduck2' % env)

def symlink_current_release():
    """ symlinking current/previous releases. """
    run('cp %(path)s/releases/current %(path)s/releases/previous;' % env)
    run('ln -s %(path)s/releases/%(release)s %(path)s/releases/current')

def deploy():
    """ deploy the application on the remote server. """
    env.release = datetime.now().strftime("%Y%m%d.%H%M%S")
    create_tar()
    upload_tar()
#   install_requirements()
    stop_apache2()
    install_site()
#   symlink_current_release()
    restart_apache2()
    shoot_email_notice()
#   shoot_xmpp_notice()

def stop_apache2():
    """ Stopping the web server. """
    sudo('/etc/init.d/apache2 stop', pty=True)

def start_apache2():
    """ Stopping the web server. """
    sudo('/etc/init.d/apache2 start', pty=True)

def restart_apache2():
    """ Restart the web server """
    sudo('/etc/init.d/apache2 restart', pty=True)

def shoot_email_notice():
    subject = "dev.icrack.it is been updated, new release." % env
    payload = "new upgrade '%(release)s' has been deployed at dev.icrack.it;\
             \nthe dev server is ready for inspection, please proceed with your inspection.\
             \n\nplease report the bugs as soon as possible." % env

    params = urllib.urlencode({'subject':subject, 'payload':payload})
    f = urllib.urlopen("http://post-bot.3bandar.org/post/email/prakharkjain@gmail.com", params)
    f = urllib.urlopen("http://post-bot.3bandar.org/post/email/gopi.daiict@gmail.com", params)
    print "successfully sent email notice."

def shoot_xmpp_notice():
    subject = "dev.icrack.it is been updated, new release." % env
    payload = "new upgrade '%(release)s' has been deployed at dev.icrack.it;\
             \n  the dev server is ready for inspection, please proceed with your inspection.\
             \n\n  please report the bugs as soon as possible." % env

    params = urllib.urlencode({'subject':subject, 'payload':payload})
    f = urllib.urlopen("http://post-bot.3bandar.org/post/xmpp/prakharkjain@gmail.com", params)
#    f = urllib.urlopen("http://post-bot.3bandar.org/post/xmpp/gopi.daiict@gmail.com", params)
    print "successfully sent xmpp notice."

