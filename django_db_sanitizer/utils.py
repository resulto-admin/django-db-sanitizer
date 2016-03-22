from django.db import connection


# Based on:
# https://github.com/jfalkner/Efficient-Django-QuerySet-Use/blob/master/demo/django_db_utils/__init__.py
def pg_bulk_update(model, filter_column_name, update_column_name,
                   filter_column_data, update_column_data):
    """Postgres database utility to quickly update an entire column in a table
    with the values provided in update_column_data matched against
    filter_column_data.

    XXX Will not currently work if trying to update a column cell with an
    empty string/value

    :param model: Django model to be updated.
    :param str filter_column_name: Name of the field used to match rows
        to be updated.
    :param str update_column_name: Name of the field to be updated.
    :param list filter_column_data: List of values used for matching rows to
        be updated, using ``filter_column_name``.
    :param list update_column_data: List of values to update
        ``update_column_name`` with for matched rows.
    """
    cursor = connection.cursor()
    # Get table name and column name for filter and update attributes as
    # stored in database.
    db_table = model._meta.db_table
    model_filter = model._meta.get_field(filter_column_name).column
    model_update = model._meta.get_field(update_column_name).column
    # Input data as Django sanitized parameters,
    cursor.execute(
        "UPDATE " + db_table +
        " SET " + model_update + " = input.update" +
        " FROM (SELECT unnest(%s), unnest(%s)) AS input (filter, update)"
        " WHERE " + model_filter + " = input.filter;", [filter_column_data,
                                                        update_column_data])
    cursor.execute("COMMIT;")
