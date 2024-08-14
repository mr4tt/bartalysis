class BartRouter:
    def db_for_read(self, model, **hints):
        """
        Attempts to read models from a specific database.
        """
        if model._meta.app_label == 'bartapp':
            return 'bart'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write models to a specific database.
        """
        if model._meta.app_label == 'bartapp':
            return 'bart'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allows relations if both objects are in the same database.
        """
        if obj1._state.db == obj2._state.db:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensures that apps' models get created on the correct database.
        """
        if app_label == 'bartapp':
            return db == 'bart'
        return db == 'default'