#coding=utf-8

import os 
import sys
import subprocess
import threading
import time
import argparse

from settings import default

processes = {}


def make_migrations():
    print('**** Check database change, make migrations')

    subprocess.call('python manage.py db upgrade head', shell=True)    
    subprocess.call('python manage.py db migrate', shell=True)    


def start_gunicorn():
    print('**** Start Gunicorn WSGI HTTP Server')

    make_migrations()

    p = subprocess.Popen('python manage.py gunicorn', shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return p


def start_celery():
    print('**** Start Celery as Distributed Task Queue')

    cmd = 'celery -A manage.celery worker -l INFO'
    p = subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return p


def start_beat():
    print('**** Start Beat as Periodic Task Scheduler')
    pidfile = os.path.join(default.TMP_DIR, 'jcywgl_beat.pid')
    if os.path.exists(pidfile):
        print("Beat pid file `{}` exist, remove it".format(pidfile))
        os.unlink(pidfile)
        time.sleep(0.5)

    if os.path.exists(pidfile):
        print("Beat pid file `{}` exist yet, may be something wrong".format(pidfile))
        os.unlink(pidfile)
        time.sleep(0.5)
    
    cmd = 'celery -A manage.celery worker -l INFO --pidfile {} -B'.format(pidfile)
    p = subprocess.Popen(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    return p


def start_service(services):
    print(time.ctime())
    print('welcome to Jcywgl, more see https://jcywgl.jc/')
    print('Quit the server with CONTROL-C.')

    services_all = {
         "gunicorn": start_gunicorn,
         "celery": start_celery,
         "beat": start_beat
    }

    if 'all' in services:
        for name, func in services_all.items():
            processes[name] = func()
    else:
        for name in services:
            func = services_all.get(name)
            processes[name] = func()

    stop_event = threading.Event()
    while not stop_event.is_set():
        for name, proc in processes.items():
            if proc.poll() is not None:
                print('\n\n' + '####'*10 + '  ERROR OCCUR  ' + '####'*10)
                print('Start service {} [FAILED]'.format(name))
                for _, p in processes.items():
                    p.terminate()
                stop_event.set()
                print('Exited'.format(name))
                break
        time.sleep(5)


def stop_service():
    for name, proc in processes.items():
        print("Stop service {}".format(name))
        proc.terminate()

    if os.path.exists(os.path.join(default.TMP_DIR, 'jcywgl_beat.pid')):
        os.unlink(os.path.join(default.TMP_DIR, 'jcywgl_beat.pid'))


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Jcgroup start service")
    parser.add_argument("services", type=str, nargs='+', default="all",
                        choices=("all", "gunicorn", "celery", "beat"),
                        help="The service to start",
                        )
    args = parser.parse_args()
    start_service(args.services)