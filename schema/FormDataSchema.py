from app import ma

# Forms Data Schema
class FormDataSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'data', 'created_at', 'updated_at')
