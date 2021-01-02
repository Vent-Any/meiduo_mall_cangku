from django.urls import converters


class UsernameConverter:
    # 正则判断
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return value
