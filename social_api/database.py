import databases
import sqlalchemy
from social_api.config import config

metatdata = sqlalchemy.MetaData()
post_table = sqlalchemy.Table(
    "posts",
    metatdata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
)

user_table = sqlalchemy.Table(
    "users",
    metatdata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

comment_table = sqlalchemy.Table(
    "comments",
    metatdata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column(
        "post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"), nullable=False
    ),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
)

engine = sqlalchemy.create_engine(config.DATABASE_URL)

metatdata.create_all(engine)

database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
