"""
Reusable SQLAlchemy column types.
"""

from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

String50 = String(50)

String100 = String(100)

String150 = String(150)

String255 = String(255)

LongText = Text()

IntegerType = Integer()

FloatType = Float()


def EnumType(enum_cls):
    return Enum(
        enum_cls,
        native_enum=False,
        create_constraint=True,
    )