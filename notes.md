### Flask Alembic
- [Docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html#running-our-first-migration)
https://www.programcreek.com/python/example/87970/alembic.op.add_column
- run migration: `alembic upgrade head`
- create new migration `alembic revision -m "Add a column"`


https://medium.com/@romanchvalbo/how-i-set-up-react-and-node-with-json-web-token-for-authentication-259ec1a90352

https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
https://blog.tecladocode.com/jwt-authentication-and-token-refreshing-in-rest-apis/
https://hptechblogs.com/using-json-web-token-react/
https://jasonwatmore.com/post/2019/04/06/react-jwt-authentication-tutorial-example#auth-header-js
https://medium.com/@riken.mehta/full-stack-tutorial-3-flask-jwt-e759d2ee5727

https://flask-jwt-extended.readthedocs.io/en/latest/installation.html

# form_data = db.engine.execute("SELECT form_data.id as form_data_id, form_data.form_id,"\
#                               "form_data.name as name, form_data.description as description,"\
#                               "form_data.data as data, form_data.created_at as created_at, "\
#                               "form_data.updated_at as updated_at, form_data.id as id, "\
#                               "form.user_id as user_id FROM form_data "\
#                               "JOIN form ON form_data.form_id = form.id WHERE "\
#                               "form.user_id={} AND form.unique_id='{}'".format(current_user,form_unique_id))
