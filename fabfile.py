from fabric.api import env, local, run, sudo
import os

env.user = 'ubuntu'
env.key_filename = ['~/.ssh/chefbox.pem']

#put in your public ip address for your aws box
#env.hosts = ['54.171.201.222'] #chefbox

env.hosts = ['52.51.12.92']
project_root = "~/uwotmate"
activate_script = os.path.join(project_root, 'env/bin/activate')

#  hardcoded for now
repo_name = "django_one_nine_project"
repo_root = os.path.join(project_root, repo_name)


def update():
    sudo('apt-get -y update', pty=True)


def upgrade():
    sudo('apt-get -y upgrade', pty=True)


def make_proj_root():
    run("mkdir -p %s " % project_root)


def virtualenv(command, use_sudo=False):
    if use_sudo:
        func = sudo
    else:
        func = run
    func(". %s && %s" % (activate_script, command))


def makemigrations():
    virtualenv("cd %s && python manage.py makemigrations" % repo_root)

def freeze():
    virtualenv("pip freeze")

def migrate():
    virtualenv("cd %s && python manage.py migrate" % repo_root)

def collectstatic():
    virtualenv("cd %s && python manage.py collectstatic" % repo_root)



def createsuperuser():
    virtualenv("cd %s && python manage.py createsuperuser" % repo_root)


def startproject(name):
    virtualenv("cd %s && django-admin startproject %s" % (project_root, name))


def setup_gunicorn():
    pass

def pull():
    run('cd %s && git pull' % repo_root)

def restart():
    sudo("supervisorctl restart testapp")


def basic_code_reload():
    pull()
    restart()


def setup_mysql():
    sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password password lululu1'")
    sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password lululu1'")
    sudo("apt-get install libmysqlclient-dev mysql-client-core-5.5 -y", pty=True)
    virtualenv("pip install MySQL-python==1.2.3")
    sudo("apt-get -y install mysql-server", pty=True)
    run('mysql -u root -p%s -e "create database IF NOT EXISTS dbname";' % ("'lululu1'"))
    run('mysql -u root -p%s -e "grant all on dbname.* to root@localhost identified by %s ";' % ("'lululu1'", "'lululu1'"))


def setup_postgres():
    sudo("apt-get -y install postgresql-9.3 postgresql-server-dev-9.3")


def make_logs():
    run("cd %s && mkdir -p logs && touch logs/gunicorn_supervisor.log" % repo_root )
    sudo("touch %s " % (repo_root + '/logs/nginx-access.log'))
    sudo("touch %s " % (repo_root + '/logs/nginx-error.log'))


def update_supervisor():
    sudo('supervisorctl reread && supervisorctl update')


def install_nginx():
    sudo('apt-get install nginx -y')


def restart_ngninx():
    sudo('service nginx restart')

def pipinstall():
    virtualenv("pip install -r %s --upgrade" % (repo_root + '/requirements.txt'))

def delete_existing_proj():
    try:
        sudo('rm -R {}'.format(project_root))
    except:
        pass

def setup_django():
    delete_existing_proj()
    update()
    upgrade()
    #going with mysql for now, will leave postgres stuff in there anyway
    sudo('apt-get -y install python-pip git python-virtualenv python-dev mercurial meld sqlite supervisor libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk')
    make_proj_root()
    run('cd %s && virtualenv env' % project_root)
    #setup_postgres()
    ###setup_mysql()

    run('cd {} && git clone https://charlesfaustin@bitbucket.org/charlesfaustin/{}.git'.format(project_root, repo_name) )
    #'{} {}'.format('one', 'two')
    virtualenv("pip install -r %s " % (repo_root + '/requirements.txt'))
    virtualenv("pip install setproctitle")

    #running fab to install locally on remote machine is pretty easy
    # http://stackoverflow.com/a/6769071/2049067

    makemigrations()
    migrate()
    collectstatic()
    #createsuperuser()
    setup_gunicorn()
    #will have to copy supervisor config & gunicorn_start file from repo, into the right places
    # then change permissions etc
    # need ot make /home/ubuntu/uwotmate/testapp/run/ & put gunicorn.sock file in it
    run("cp %s /home/ubuntu/uwotmate/env/bin" % (repo_root + '/configs/gunicorn_start'))
    sudo ("chmod u+x /home/ubuntu/uwotmate/env/bin/gunicorn_start")

    make_logs()

    install_nginx()

    sudo("cp %s /etc/nginx/sites-available" % (repo_root + '/configs/testapp'))
    try:
        sudo("rm /etc/nginx/sites-enabled/default")
    except:
        pass

    try:
        sudo("rm /etc/nginx/sites-enabled/testapp")
    except:
        pass
         
    sudo("ln -s /etc/nginx/sites-available/testapp /etc/nginx/sites-enabled/testapp")

    restart_ngninx()

    #copy supervisor files into place

    try:
        sudo("rm /etc/supervisor/conf.d/testapp.conf")
    except:
        pass

    sudo("cp %s /etc/supervisor/conf.d" % (repo_root + '/configs/testapp.conf'))

    update_supervisor()
    restart()

    #also look at https://github.com/jcalazan/ansible-django-stack

