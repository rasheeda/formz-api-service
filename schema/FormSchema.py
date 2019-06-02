from app import ma

# Forms Schema
class FormSchema(ma.Schema):
  class Meta:
    fields = ('id', 'unique_id', 'name', 'description', 'created_at', 'updated_at')