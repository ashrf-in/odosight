from sqlalchemy import Column, Integer, String, JSON, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class UserConfig(Base):
    __tablename__ = 'user_configs'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    odoo_url = Column(String)
    odoo_db = Column(String)
    odoo_user = Column(String)
    odoo_password = Column(String)
    gemini_key = Column(String)
    settings = Column(JSON, default={})

engine = create_engine('sqlite:///data/bot_users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
