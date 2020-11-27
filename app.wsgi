#!usr/bin/python3
import sys


sys.path.insert(0, '/var/www/html/stan')
sys.path.append('/var/www/html/stan/venv/bin/python')


from app import app as application
