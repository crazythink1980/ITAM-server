from .model import AssetType
from app.db import marshmallow


class AssetTypeSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = AssetType
        load_instance = True
