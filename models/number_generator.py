from extensions import db


class NumberGenerator(db.Model):
    __tablename__ = 'number_generator'
    table_name = db.Column(db.String, primary_key=True)
    current_number = db.Column(db.BigInteger)

    def to_dict(self):
        return {
            'table_name': self.table_name,
            'current_number': self.current_number
        }
