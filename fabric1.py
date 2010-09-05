from __future__ import with_statement
from fabric.api import env, run, sudo, local, cd, hosts, runs_once, prompt
from fabric.contrib.files import exists

env.bzr_push_url = "bzr+ssh://%(user)s@%(host)s%(path)s"
env.hosts = []
env.user = "username"

@runs_once
def production():
    """The production server."""
    env.remote_app_dir = "/home/username/path/"
    env.hosts.append("server:port")

def update():
    """Update the latest copy on the server."""
    bzr_push_url = env.bzr_push_url % {"host": env.host_string,
                                       "user": env.user,
                                       "path": env.remote_app_dir}
    local("bzr push --no-strict --overwrite %s" % bzr_push_url)
    with cd(env.remote_app_dir):
        run("bzr revert")
        run("bzr up")
        run("./manage.py migrate")
        run("yui-compressor media/js/file.js > media/js/file.min.js")
        run("sass --style compressed sass/main.sass media/css/main.css")
        run("pip -E env/ install -r dependencies.txt")

def flush():
    """Flush varnish."""
    sudo("varnishadm -S /etc/varnish/secret -T :6082 purge.url \"^/\"")

def reload():
    """Reload apache."""
    sudo("/etc/init.d/apache2 reload")

