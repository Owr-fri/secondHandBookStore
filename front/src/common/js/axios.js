import axios from "axios";

// 构建axios实例
const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/',  // 该处url会根据开发环境进行变化（开发/发布）
  timeout: 10000  // 设置请求超时连接时间
})

instance.interceptors.response.use(response => {
  return response.data
}, error => {
  return error.response.data
})

instance.defaults.withCredentials = true

export default(
  instance
)