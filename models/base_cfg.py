from extensions import db


class BaseCfg(db.Model):
    __tablename__ = 'base_cfg'
    app_id = db.Column(db.String(255), primary_key=True, nullable=False)
    app_secret = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'app_id': self.app_id,
            'app_secret': self.app_secret,
        }
