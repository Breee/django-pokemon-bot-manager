class ModelDatabaseRouter(object):
    """Allows each model to set its own destiny"""

    def db_for_read(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def db_for_write(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def allow_syncdb(self, db, model):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the monocle app's models get created on the right database."""
        if app_label == 'scannerdb':
            # The scannerdb app should be migrated only on the rocketmap database.
            return db == 'rocketdb'
        elif db == 'rocketdb':
            # Ensure that all other apps don't get migrated on the rocketmap database.
            return False

        # No opinion for all other scenarios
        return None