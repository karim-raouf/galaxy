from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

class TimeFormatField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12  # Adjust the max_length as needed
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None or isinstance(value, str):
            return value
        return value.strftime('%H:%M:%S.%f')[:-3]

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value:
            parts = value.split(':')
            if len(parts) < 2 or len(parts) > 3:
                raise ValidationError('Invalid time format. Use HH:mm or HH:mm:ss.SSS.')

            hour = parts[0]
            minute = parts[1]
            second = parts[2] if len(parts) > 2 else '00'
            microsecond = '000' if len(parts) < 3 else parts[2].ljust(3, '0')

            try:
                datetime.strptime(f'{hour}:{minute}:{second}.{microsecond}', '%H:%M:%S.%f')
            except ValueError:
                raise ValidationError('Invalid time format. Use HH:mm or HH:mm:ss.SSS.')

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        return str(value) if value else value