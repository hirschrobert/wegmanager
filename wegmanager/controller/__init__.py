from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# imported elsewhere in the code
#import wegmanager.model.bank_user
#import wegmanager.model.transaction

# can be deleted if imported elsewhere in the code
import wegmanager.model.bank
import wegmanager.model.business_partner
import wegmanager.model.invoice
import wegmanager.model.transaction_audited

Base = declarative_base()

db_session = sessionmaker(autocommit=False, autoflush=False)
