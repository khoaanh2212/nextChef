class WrappedManager:
    def __init__(self, legacy_model, wrapper):
        self.legacy_model = legacy_model
        self.wrapper = wrapper

    @classmethod
    def new(cls, legacy_model, wrapper):
        return cls(legacy_model, wrapper)

    def __getattr__(self, method_name):
        objects = self.legacy_model.objects
        method = getattr(objects, method_name)
        def call(*args, **kwargs):
            result = method(*args, **kwargs)
            if isinstance(result, self.legacy_model):
                return self.wrapper.from_legacy_model(result)
            else:
                return result
        return call

def legacymodelwrap(legacy_model):
    getattr(legacy_model, 'objects')
    def class_rebuilder(cls):
        cls.objects = WrappedManager(legacy_model, cls)
        getattr(cls, 'from_legacy_model')
        return cls
    return class_rebuilder