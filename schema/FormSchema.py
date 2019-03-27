from app import ma

# Forms Schema
class FormSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description')