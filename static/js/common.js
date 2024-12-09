// 封装的请求函数
const request = (url, method = 'GET', headers = {}, body = null)  => {
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