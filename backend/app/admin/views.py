from app import models
from app.admin.converters import UserConverter
from sqladmin import ModelView


class UserAdmin(ModelView, model=models.User):
    form_converter = UserConverter
    column_list = [models.User.id, models.User.email]
    form_excluded_columns = ["password"]
    icon = "fa-solid fa-user"


class InboundAdmin(ModelView, model=models.Inbound):
    form_excluded_columns = ["session_token"]


class ClientAdmin(ModelView, model=models.Client):
    pass
