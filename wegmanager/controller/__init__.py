from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# can be deleted if models are loaded elsewhere in the code
import wegmanager.model.apartment
import wegmanager.model.booking
#import wegmanager.model.bank_user
import wegmanager.model.bank
import wegmanager.model.building
import wegmanager.model.business_partner
import wegmanager.model.housing_account
import wegmanager.model.invoice
import wegmanager.model.transaction_audited
#import wegmanager.model.transaction

Base = declarative_base()

db_session = sessionmaker(autocommit=False, autoflush=False)
