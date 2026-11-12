import os, requests, json

# 1. 你的选股逻辑在这里（先留空，后续填充）
# 示例：手动写几只备选，或者从某个免费接口拉取
stocks = ["莱绅通灵(603900)", "百洋股份(002696)", "乔治白(002687)"]

# 2. 调用 DeepSeek 做简要分析
api_key = os.environ.get("DEEPSEEK_API_KEY")
prompt = f"请对以下股票做一句话简评，每只不超过30字：{', '.join(stocks)}"

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 500
}
try:
    r = requests.post("https://api.deepseek.com/v1/chat/completions", 
                      headers=headers, json=payload, timeout=30)
    analysis = r.json()["choices"][0]["message"]["content"]
except Exception as e:
    analysis = f"AI分析失败：{e}"

# 3. 推送到微信（PushPlus）
token = os.environ.get("PUSHPLUS_TOKEN")
content = f"## 今日尾盘候选\n\n{chr(10).join(stocks)}\n\n## AI简评\n\n{analysis}"
requests.post("https://www.pushplus.plus/send", json={
    "token": token,
    "title": "尾盘选股结果",
    "content": content,
    "template": "markdown"
})
print("推送完成")
