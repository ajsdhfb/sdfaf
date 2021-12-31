# @botfather 申请到的机器人token
TOKEN = "5088843307:AAEZdVOI6sFwVAxD7ZjZincPX6dATo6OrWA"

# 机器人超级管理员，即使你是普通用户，也和群组管理员权限相同
ADMIN = [1431084652, 1431084653]

# 欢迎入群消息配置
WELCOME_MESSAGE = "欢迎入群👏，请仔细阅读群组内的置顶消息\n"

# 欢迎入群消息冷却时间。同时多人入群，欢迎信息只会发送一遍，单位：秒(s)
WELCOME_MESSAGE_CD = 60

# 发送违禁词警告次数，超过次数即踢出
AD_WARN_COUNT = 1

# 群内提及次数最多的关键词 Top n
DISPLAY_KEYWORD_AMOUNT = 7

# 显示最活跃用户数量
TOP_ACTIVE_USER_AMOUNT = 3

# Redis 相关设置
REDIS_HOSTNAME = "127.0.0.1"
REDIS_PORT = 6379
