from app import ma

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'email', 'api_key', 'timezone', 'created_at', 'updated_at')
