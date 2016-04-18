from collections import defaultdict

from django_db_sanitizer.updaters.base import BaseUpdater
from django_db_sanitizer.utils import pg_bulk_update


class BatchMultiValuePostgresUpdater(BaseUpdater):
    """Use this updater if you use Postgres and have a very large update where
    all rows of all fields may receive different values.
    """

    update_batch_size = 10000

    def update(self):
        """Iterates through the sanitizer's queryset and updates all fields
        found in the sanitizer's `fields_to_sanitize` in different batches of
        a size configurable with `update_batch_size`. There will be one update
        database query for each field from `fields_to_sanitize` per batch.
        """
        model_class = self.sanitizer.model_class
        pk_field = self.sanitizer.get_pk_field_name()

        update_dict = defaultdict(dict)
        for i, values_row in enumerate(self.item_list.iterator(), 1):
            for field_name in self.sanitizer.fields_to_sanitize:
                field_value = values_row[field_name]
                sanitized_value = \
                    self.sanitizer.sanitize_field_value(field_value)

                pk_value = values_row[pk_field]
                update_dict[field_name][pk_value] = sanitized_value

            if i % self.update_batch_size == 0:
                for field_name in self.sanitizer.fields_to_sanitize:
                    filter_data = list(update_dict[field_name].keys())
                    update_data = list(update_dict[field_name].values())

                    # One query per field per batch
                    pg_bulk_update(model_class, pk_field, field_name,
                                   filter_data, update_data)
                # New batch
                update_dict = defaultdict(dict)

        # Leftovers
        if update_dict:
            for field_name in self.sanitizer.fields_to_sanitize:
                filter_data = list(update_dict[field_name].keys())
                update_data = list(update_dict[field_name].values())

                pg_bulk_update(model_class, pk_field, field_name,
                               filter_data, update_data)
