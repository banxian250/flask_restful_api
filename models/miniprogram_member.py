from extensions import db


class MiniProgramMember(db.Model):
    __tablename__ = 'miniprogram_member'
    id = db.Column(db.BigInteger, primary_key=True)
    openid = db.Column(db.String(255), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'create_time': self.create_time
        }
