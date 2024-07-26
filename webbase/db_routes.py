class DBRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    db_list = ["JOBORDER","JOBTOTRACK","TRACK","TRACKPL"]
    app_disabled = ["joborder"]

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.db_table in self.db_list:
            return "itc_inwhouse"

        return "default"

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.db_table in self.db_list:
            return "itc_inwhouse"

        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        # print("Allow relations if a model in the auth or contenttypes apps")
        return None
        

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.app_disabled:
            return False

        return True