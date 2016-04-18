from django_db_sanitizer.updaters.base import BaseUpdater


class BatchMultiValuePostgresUpdater(BaseUpdater):

    update_batch_size = 1000

    def update(self):
        """

        """
        pass
        # TODO
        # update_batch = []
        # for i, item in enumerate(self.item_list.iterator()):
        #
        #     if len(update_batch) % self.update_batch_size == 0:
        #         pass
