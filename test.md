# 测试直连示例
curl http://192.168.88.12:50008/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-30b-a3b",
    "messages": [{"role": "user", "content": "Draw a login page with username, password, and submit button"}],
    "stream": true
  }'

## 成功

# 测试中间件
curl http://192.168.88.12:8086 \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Draw a login page with username, password, and submit button"
  }'


  ## 中间件返回结果

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   296    0   214  100    82     35     13  0:00:06  0:00:06 --:--:--    53{
  "generatedResponse": "graph TD\n    subgraph Login_Page\n        Username[Username] --> Input_Username\n        Password[Password] --> Input_Password\n        Submit_Button[Submit] --> Action_Submit\n    end"
}


# 测试通过Apache转发


curl https://xxx.xxx.com/whiteboardgejiesoftcomsupercalifragilisticexpiadocious \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Draw a login page with username, password, and submit button"
  }'

## 返回成功
