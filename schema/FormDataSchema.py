from app import ma

# Forms Data Schema
class FormDataSchema(ma.Schema):
  class Meta:
    fields = ('id', 'form_id', 'name', 'description', 'data', 'created_at', 'updated_at')