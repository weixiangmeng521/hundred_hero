
### 启动项目的命令
```bash
# 创建环境
python3 -m venv venv

# 选择环境
source venv/bin/activate
# 运行
python3 main.py
# 生成依赖
pip freeze > requirements.txt
# 结束
deactivate
```

### 配置twilio
https://www.twilio.com/en-us


### 依赖
ORC系:
- pytesseract 对中文支持害行


### python版本选择
- 配置.zshrc, 里面添加下面的内容
```bash
vim ~/.zshrc
# >>> conda initialize >>>
export PATH="/usr/local/anaconda3/bin:$PATH"
. /usr/local/anaconda3/etc/profile.d/conda.sh
# <<< conda initialize <<<
```

- 适配
```bash
# bash
source ~/.bash_profile
# zsh
source ~/.zshrc
```

- 选择pyhon3.12环境
```bash
conda create -n python312 python=3.12
# initilize
conda init
# active
conda activate python312
# deactivate
conda deactivate
```

### MEMO
如果调试cv.imshow函数，需要把设置成单线程
```ini
[THREADS]
EnableDeamon = False
```

BUG


2025-01-04 11:34:49,939 - [百炼英雄] - DEBUG - 是否跳过广告: True...
2025-01-04 11:34:49,940 - [百炼英雄] - DEBUG - 等待游戏加载...
2025-01-04 11:35:00,078 - [百炼英雄] - DEBUG - 加载完毕！
2025-01-04 11:35:00,632 - [百炼英雄] - INFO - 关闭广告。
2025-01-04 11:35:04,981 - [百炼英雄] - DEBUG - cur:(10, 5) tar:(15, 13), path:[(10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (11, 9), (12, 9), (12, 10), (13, 10), (13, 11), (14, 11), (14, 12), (14, 13), (15, 13)]
2025-01-04 11:35:13,489 - [百炼英雄] - INFO - 工会任务已完成，无需再打
2025-01-04 11:35:13,679 - [百炼英雄] - INFO - 准备移动到[竞技场]...
2025-01-04 11:35:13,679 - [百炼英雄] - DEBUG - cur:(15, 13) tar:(0, 9), path:[(15, 13), (14, 13), (14, 12), (14, 11), (13, 11), (13, 10), (12, 10), (12, 9), (11, 9), (10, 9), (9, 9), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9), (0, 9)]