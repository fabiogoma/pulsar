import sys
import site

site.addsitedir('/var/www/counter/lib/python3.6/site-packages')

sys.path.insert(0, '/var/www/counter')

from app import app as application