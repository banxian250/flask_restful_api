class Config:
    # MySQL 配置 (根据实际情况修改)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@101.43.65.120:3306/travel_china'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # 显示生成的SQL语句 (调试用)
