# this is created, so that alembic can create migration for each of our models
# so, in whole app, if I create any model, I will mention here 
# these models are being imported in the alembic/env.py file

from cart import models as cart_models
from product import models as product_models
from account import models as account_models
from shipping import models as shipping_models