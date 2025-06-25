from models.number_generator import NumberGenerator
from extensions import db


class NumberGeneratorRepository():
    @classmethod
    def create(cls, table_name, current_number):
        number = NumberGenerator(table_name=table_name, current_number=current_number)
        db.session.add(number)
        db.session.commit()
        return number

    @classmethod
    def update(cls, filters: dict, update_fields: dict):
        query = db.session.query(NumberGenerator)
        for key, value in filters.items():
            query = query.filter(getattr(NumberGenerator, key) == value)

        real_update_fields = {}
        for key, value in update_fields.items():
            if isinstance(key, str):
                real_update_fields[getattr(NumberGenerator, key)] = value
            else:
                real_update_fields[key] = value

        updated_rows = query.update(real_update_fields)
        db.session.commit()
        return updated_rows
