from database import engine
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
print("Tables recreated successfully")
