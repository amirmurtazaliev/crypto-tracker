import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass
 
class User(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(default = "Guest")
    email: Mapped[str] = mapped_column(unique = True)
    password: Mapped[str]
    
class ConfirmCode(Base):
    __tablename__ = "codes"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    email: Mapped[str] = mapped_column(ForeignKey("users.email", ondelete = "CASCADE"))
    code: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(default = datetime.datetime.now())
    
class FavoutiteCrypto(Base):
    __tablename__ = "favcrypto"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    cmc_id: Mapped[int] = mapped_column(unique = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"))
    crypto_name: Mapped[str] = mapped_column(unique = True)
    
