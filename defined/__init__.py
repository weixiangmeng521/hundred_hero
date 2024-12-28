# OCR 结果修正字典
CORRECTION_DICT = {
    # '什': '值',  # 例如将识别成 "什" 的词汇替换为 "值"
    # '己': '弓',
    # '马': '弓',
    # '荣': '杀',
    # '茶': '杀',
    # '箱': '霜',
    # '便': '傀',
    # '蝎': '儡',
    # '货': '傀',
    # '晶': '儡',
    # '伪': '儡',
    # '旭': '娜',
    # '边': '迦',
    # '阐': '娜',
    # '迎': '迦',
    # '加': '迦',
    # '是': '师',
    # '共': '杀',
    "粳": "精",
    "电": "蛇",
    "犯独": "猛犸",
    # "昨": "蝙",
    # "崇": "蝙",
    # "白|":"蝙",
    # "蚁": "",
}
# 结果类
IS_UNION_TASK_FINISHED = "1"
IS_DALIY_CASE_FINISHED = "2"
IS_DALIY_ARENA_FINISHED = "3"
IS_DALIY_TOWER_FINISHED = "4"

# 动作类
UP_MOVE_CMD = 0x0001
DOWN_MOVE_CMD = 0x0002
LEFT_MOVE_CMD = 0x0003
RIGHT_MOVE_CMD = 0x0004

# 指令类
FIND_TRAINING_NPC = 0x0010
FIND_RECRUIT_NPC = 0x0011
FIND_PORTAL = 0x0012
FIND_ARENA = 0x0013
FIND_TOWER = 0x0014