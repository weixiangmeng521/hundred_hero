// 去除年
const removeYear = (date) => {
    const list = date.split("-")
    list.shift()
    return list.join("-")
}

// 封装的请求函数
const request = (url, method = 'GET', headers = {}, body = null) => {
    // 设置请求参数
    const requestOptions = {
        method: method, // 默认为 GET 方法
        headers: {
            'Content-Type': 'application/json', // 默认发送 JSON 格式数据
            ...headers, // 合并传入的 headers
        },
        body: body ? JSON.stringify(body) : null, // 如果有请求体则将其转为 JSON 字符串
    };

    // 创建请求对象
    const request = new Request(url, requestOptions);

    // 使用 fetch 发送请求
    return fetch(request)
        .then(response => {
            // 检查响应是否成功
            if (!response.ok) {
                return Promise.reject('请求失败: ' + response.statusText);
            }
            return response.json(); // 解析 JSON 格式的响应
        })
        .then(data => {
            return data; // 返回数据
        })
        .catch(error => {
            console.error('Error:', error); // 处理错误
            throw error; // 抛出错误以便进一步处理
        });
}


// 初始化chart
const init_last7days_cards_chart = (data) => {
    for(const key in data){
        const value = data[key];
        data[removeYear(key)] = value;
        delete data[key];
    }

    // 提取日期和卡片类型
    const labels = Object.keys(data);  // 日期
    const cardTypes = ['蓝卡', '紫卡', '橙卡', '垃圾', '红卡'];  // 可能的卡片类型
    // 定义卡片类型与颜色的映射
    const cardTypeColors = {
        '蓝卡': 'rgb(105, 187, 255)',  // 蓝色
        '紫卡': 'rgb(209, 6, 131)',  // 紫色
        '橙卡': '#FFA500',  // 橙色
        '垃圾': 'rgb(204, 204, 204)',  // 灰色
        '红卡': '#FF0000'   // 红色
    };

    // 数据准备：每个卡片类型的数量
    const datasets = cardTypes.map(cardType => ({
        label: cardType,
        data: labels.map(date => {
            return data[date][cardType] || 0
        }),  // 获取每个日期对应卡片类型的数量，若没有则为0
        borderColor: getColor(cardType),
        backgroundColor: getColor(cardType),
        fill: false
    }));

    // 随机颜色生成函数
    function getColor(cardType) {
        return cardTypeColors[cardType];
    }

    // 创建图表
    const ctx = document.getElementById('last7days_cards_chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',  // 折线图
        data: {
            labels: labels,  // X 轴为日期
            datasets: datasets  // Y 轴为不同的卡片类型
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,  // 取消保持比例
            plugins: {
                title: {
                    display: true,  // 显示标题
                    text: '近7日的抽卡情况',  // 标题内容
                    font: {
                        size: 18,  // 标题字体大小
                        weight: 'bold',  // 标题字体加粗
                    },
                    color: '#333',  // 标题颜色
                    padding: {
                        top: 20,  // 上边距
                        bottom: 20  // 下边距
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '日期'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '数量'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}


// 初始化chart
const init_last7days_coins_chart = (data) => {
    for(const key in data){
        const value = data[key];
        data[removeYear(key)] = value;
        delete data[key];
    }    
    // 提取日期和金币数量
    const labels = Object.keys(data);  // 日期
    // 数据准备：每个日期的金币数量
    const datasets = [{
        label: "金币",
        data: labels.map(date => data[date] || 0),  // 获取每个日期对应金币数量，若没有则为0
        borderColor: '#FFA500',
        backgroundColor: '#FFA500',
        fill: false
    }];

    // 创建图表
    const ctx = document.getElementById('last7days_coin_chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',  // 折线图
        data: {
            labels: labels,  // X 轴为日期
            datasets: datasets  // Y 轴为不同的卡片类型
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,  // 取消保持比例
            plugins: {
                title: {
                    display: true,  // 显示标题
                    text: '近7日的打金情况',  // 标题内容
                    font: {
                        size: 18,  // 标题字体大小
                        weight: 'bold',  // 标题字体加粗
                    },
                    color: '#333',  // 标题颜色
                    padding: {
                        top: 20,  // 上边距
                        bottom: 20  // 下边距
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '日期'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '金币'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}


// 初始化当天错误data信息
const init_today_error_data = (data) => {
    // 提取日期和金币数量
    const labels = Object.keys(data);  // 日期
    // 数据准备：每个日期的金币数量
    const datasets = [{
        label: "故障",
        data: labels.map(date => data[date] || 0),  // 获取每个日期对应金币数量，若没有则为0
        borderColor: 'rgba(255, 0, 0, 1)',
        backgroundColor: 'rgba(255, 0, 0, 1)',
        fill: false
    }];

    // 创建图表
    const ctx = document.getElementById('today_error_message').getContext('2d');
    new Chart(ctx, {
        type: 'line',  // 折线图
        data: {
            labels: labels,  // X 轴为日期
            datasets: datasets  // Y 轴为不同的卡片类型
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,  // 取消保持比例
            plugins: {
                title: {
                    display: true,  // 显示标题
                    text: '今日系统故障情况',  // 标题内容
                    font: {
                        size: 18,  // 标题字体大小
                        weight: 'bold',  // 标题字体加粗
                    },
                    color: '#333',  // 标题颜色
                    padding: {
                        top: 20,  // 上边距
                        bottom: 20  // 下边距
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '日期'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '故障次数'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}