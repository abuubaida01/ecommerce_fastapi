# this is created, so that alembic can create migration for each of our models
# so, in whole app, if I create any model, I will mention here 
# these models are being imported in the alembic/env.py file

from account.models import User, RefreshToken