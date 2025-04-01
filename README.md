# 百炼英雄挂机系统

本仓库仅供学习，请勿用于非法用途

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

### 贡献
欢迎贡献代码、报告问题或提供改进建议。我们相信您的参与将使这个app变得更好！