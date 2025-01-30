from datetime import datetime

class MetaWithTimestamp(type):
    def __new__(cls, name, bases, class_dict):
        class_dict['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, class_dict)

class MyClass(metaclass=MetaWithTimestamp):
    pass

class AnotherClass(metaclass=MetaWithTimestamp):
    pass

if __name__ == "__main__":
    obj1 = MyClass()
    obj2 = AnotherClass()
    print(f"MyClass created at: {MyClass.created_at}")
    print(f"AnotherClass created at: {AnotherClass.created_at}")
