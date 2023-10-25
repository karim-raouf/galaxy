
class GalaxyRouter:
    route_app_labels = {'galaxy' , 'auth' , 'contenttypes' , 'admin' , 'sessions'}
    
    # def datab_name(request):
    #     user = request.user
    #     if user.is_authenticated:
    #         username = str(request.user.username)

    #         return username
    #     else:
    #         return "no username"
    
    # @staticmethod
    # def connected_db(request):
    #     db_name = datab_name(request)
    #     return db_name
    
    # @classmethod
    # def get_target_database(cls, request):
    #     return cls.connected_db(request)
    
    # target_database = None
    
    # def __init__(self, request=None):
    #     if request is not None:
    #         self.target_database = self.get_target_database(request)
    
    target_database = 'default'
    
    def db_for_read(self, model, **hints):
        """ Attempts to read auth and contenttypes models go to galaxy_db. """
        
        if model._meta.app_label in self.route_app_labels:
            return self.target_database
               
        return None

    
    def db_for_write(self, model, **hints):
        """ Attempts to write auth and contenttypes models go to galaxy_db. """
        
        if model._meta.app_label in self.route_app_labels:
                return self.target_database
        return None

    
    def allow_relation(self, obj1, obj2, **hints):
        """ Allow relations if a model in the auth or contenttypes or admin or sessions or galaxy apps is involved. """
        
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ Make sure the auth and contenttypes , admin , sessions and galaxy apps only appear in the 'galaxy_db' database. """
        
        if app_label in self.route_app_labels:
                return db == self.target_database
        
        return None
    
    
    
class AppRouter:
    route_app_labels = {'App'}
    
    def datab_name(request):
        user = request.user
        if user.is_authenticated:
            username = str(request.user.username)

            return username
        else:
            return "no username"
    
    @staticmethod
    def connected_db(request):
        db_name = datab_name(request)
        return db_name
    
    @classmethod
    def get_target_database(cls, request):
        return cls.connected_db(request)
    
    target_database = None
    
    def __init__(self, request=None):
        if request is not None:
            self.target_database = self.get_target_database(request)
    
    
    
    def db_for_read(self, model, **hints):
        """ Attempts to read auth and contenttypes models go to galaxy_db. """
        
        if model._meta.app_label in self.route_app_labels:
            return self.target_database
               
        return None

    
    def db_for_write(self, model, **hints):
        """ Attempts to write auth and contenttypes models go to galaxy_db. """
        
        if model._meta.app_label in self.route_app_labels:
                return self.target_database
        return None

    
    def allow_relation(self, obj1, obj2, **hints):
        """ Allow relations if a model in the auth or contenttypes or admin or sessions or galaxy apps is involved. """
        
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ Make sure the auth and contenttypes , admin , sessions and galaxy apps only appear in the 'galaxy_db' database. """
        
        if app_label in self.route_app_labels:
                return db == self.target_database
        
        return None