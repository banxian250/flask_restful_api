from models.miniprogram_member import MiniProgramMember
from extensions import db


class MiniProgramMemberRepository():
    @classmethod
    def create(cls, id, openid, create_time):
        member = MiniProgramMember(id=id, openid=openid, create_time=create_time)
        db.session.add(member)
        db.session.commit()
        return member
