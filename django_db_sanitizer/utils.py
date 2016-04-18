# The MIT License (MIT)
#
# Copyright (c) 2013 Jayson Falkner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from django.db import connection


# Last modified by Martin Gingras from Resulto on 2016-03-22
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
