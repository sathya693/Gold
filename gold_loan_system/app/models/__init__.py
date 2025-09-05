# This file makes the 'models' directory a Python package.
# We will import all models here to make them easily accessible.

from .user import User, UserRoles
from .customer import Customer
from .loan import Loan
from .payment import Payment
from .gold_item import GoldItem
# The following will be created and uncommented as we build the system
# from .audit import AuditLog
# from .interest_calculation import InterestCalculation
# from .gold_rate import GoldRate
# from .penalty import Penalty
