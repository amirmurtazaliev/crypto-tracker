from .database import sessionlocal, Password
from sqlalchemy import select, delete
from .models import User, ConfirmCode, FavoutiteCrypto

pwdacts = Password()

class UserActions:
    async def email_is_busy(self, email: str):
        async with sessionlocal() as session:
            result = await session.execute(
                select(User)
                .where(User.email == email)
                .limit(1)
            )
            user = result.scalar_one_or_none()
            if user:
                return {"msg": "email is busy", "employment": True}
            return {"msg": "email is not busy", "employment": False}
        
    async def find_user(self, email: str, password: str):
        async with sessionlocal() as session:
            result= await session.execute(
                select(User)
                .where(User.email == email)
            )
            
            user=result.scalar_one_or_none()
            if user and pwdacts.verify_password(password, user.password):
                return {"msg": "user found", "user_id": user.id}
            return {"msg": "user not found", "user_id": None}
     
    async def add_user(self, email: str, password: str):
        new_user=User(
            email = email,
            password = pwdacts.get_password_hash(password)
        )
        try:
            async with sessionlocal() as session:
                session.add(new_user)  
                await session.commit()
            return {"msg": "user added"}
        
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}
        
    async def delete_user(self, email: str, password: str):
        try:
            async with sessionlocal() as session:
                stmt = delete(User).where(
                    User.email == email
                )
                result = await session.execute(stmt)
                rows_deleted = result.rowcount
                await session.commit()
                
                if rows_deleted > 0:
                    return {"msg": "user deleted"}
                else:
                    return {"msg": "User not found or credentials incorrect"}
                    
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}
        
class CodeActions:
    async def add_conf_code(self, email: str, code: str):
        new_conf_code = ConfirmCode(
            email = email,
            code = code
        )
        try:
            async with sessionlocal() as session:
                session.add(new_conf_code)
                await session.commit()
            return {"msg": "user added"}
        
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}
    
    async def find_conf_code(self, email: str):
        async with sessionlocal() as session:
            result = await session.execute(
                select(ConfirmCode)
                .where(ConfirmCode.email == email)
                .order_by(ConfirmCode.id.desc())
                .limit(1)
            )
            
            code = result.scalar_one_or_none()
            return {"msg": "code found", "conf_code": code.code}
        
class CryptoActions:
    async def get_all_user_crypto(self, user_id: int):
        async with sessionlocal() as session:
            result = await session.execute(
                select(FavoutiteCrypto)
                .where(FavoutiteCrypto.user_id == user_id)
            )
            
            user_crypto = result.all()
            return {"user_cryptocurrencies": user_crypto}
    
    async def add_favourite_crypto(self, cmc_id: int, user_id: int, crypto_name: str):
        new_favourite_crypto = FavoutiteCrypto(
                cmc_id = cmc_id,
                user_id = user_id,
                crypto_name = crypto_name
            )
        try:
            async with sessionlocal() as session:
                session.add(new_favourite_crypto)
                await session.commit()
            return {"msg": "user added"}
        
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}
    
    async def delete_favourite_crypto(self, user_id: int, crypto_name: str):
        try:
            async with sessionlocal() as session:
                stmt = delete(FavoutiteCrypto).where(
                    FavoutiteCrypto.user_id == user_id,
                    FavoutiteCrypto.crypto_name ==crypto_name
                )
                result = await session.execute(stmt)
                rows_deleted = result.rowcount
                await session.commit()
                
                if rows_deleted > 0:
                    return {"msg": "user deleted"}
                else:
                    return {"msg": "User not found or credentials incorrect"}
                    
        except Exception as e:
            return {"msg": f"Error: {str(e)}"}