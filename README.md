
### 启动项目的命令
```bash
# 创建环境
python3 -m venv venv

# 选择环境
source venv/bin/activate
# 运行
python3 main.py
# 结束
deactivate
```

### 配置twilio
https://www.twilio.com/en-us


### 依赖
ORC系:
- pytesseract 对中文支持不好，放弃
- CnOCR 中文支持好，轻量

```bash
pip install "cnocr[ort-cpu]"
```


### python版本选择
- 配置.zshrc, 里面添加下面的内容
```bash
vim ~/.zshrc
# >>> conda initialize >>>
export PATH="/usr/local/anaconda3/bin:$PATH"
. /usr/local/anaconda3/etc/profile.d/conda.sh
# <<< conda initialize <<<
```

- 适配他
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