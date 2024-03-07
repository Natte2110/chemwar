from sqlalchemy import create_engine, exists
from chemwar import db, app
from sqlalchemy.orm import sessionmaker
from chemwar.models import Users, Groups, CBRN, Cordons, Reports
import os

if os.path.exists("env.py"):
    import env  # noqa

engine = create_engine(os.environ.get("DB_URL"))
Session = sessionmaker(bind=engine)
Users.metadata.create_all(engine)

session = Session()


def create_default_user(session):
    # Check if the group "Administrator" already exists
    admin_group_exists = session.query(
        exists().where(Groups.name == "Administrator")).scalar()

    # If the group doesn't exist, add it
    if not admin_group_exists:
        admin_group = Groups(name="Administrator")
        session.add(admin_group)
        session.commit()

    # Check if the user "admin" already exists
    admin_user_exists = session.query(
        exists().where(Users.username == "admin")).scalar()
    
    # If the user doesn't exist, add it
    if not admin_user_exists:
        admin_user = Users(
            username=os.environ.get("DEFAULT_USER_USERNAME"),
            password=os.environ.get("DEFAULT_USER_PASSWORD"),
            level=int(os.environ.get("DEFAULT_USER_LEVEL")),
            group=int(os.environ.get("DEFAULT_USER_GROUP")),
            initial=os.environ.get("DEFAULT_USER_INITIAL"),
            surname=os.environ.get("DEFAULT_USER_SURNAME"),
            blood_group=os.environ.get("DEFAULT_USER_BLOOD"),
            med_tag=bool(os.environ.get("DEFAULT_USER_MED"))
        )
        session.add(admin_user)
        session.commit()

    default_group_exists = session.query(
        exists().where(Groups.name == "Default")).scalar()

    # If the group doesn't exist, add it
    if not default_group_exists:
        default_group = Groups(name="Default")
        session.add(default_group)
        session.commit()

def create_cbrn_types(session):
    
    if session.query(exists().where(CBRN.type == "Chemical")).scalar() == None:
        chemical = CBRN(type="Chemical")
        session.add(chemical)
        session.commit()
    
    if session.query(exists().where(CBRN.type == "Biological")).scalar() == None:
        biological = CBRN(type="Biological")
        session.add(biological)
        session.commit()
    

create_default_user(session)

create_cbrn_types(session)