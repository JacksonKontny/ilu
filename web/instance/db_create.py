# Check the PYTHONPATH environment variable before beginning to ensure that the
# top-level directory is included.  If not, append the top-level.  This allows
# the modules within the .../project/ directory to be discovered.
import sys
import os

print('Creating database tables for app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    sys.path.append(os.path.abspath(os.curdir))

from project import db
from project.models import *

# Create the database tables, add some initial data, and commit to the database
# Drop all of the existing database tables
db.drop_all()

# Create the database and the database table
db.create_all()

# Commit the changes
db.session.commit()

print('...done!')
