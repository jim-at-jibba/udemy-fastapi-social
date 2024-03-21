import databases
import sqlalchemy
from config import config

metatdata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    "posts",
    metatdata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
)

comments = sqlalchemy.Table(
    "comments",
    metatdata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column(
        "post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"), nullable=False
    ),
)

engine = sqlalchemy.create_engine(config.DATABASE_URL)

metatdata.create_all(engine)

database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
