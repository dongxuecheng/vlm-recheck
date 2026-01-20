import requests

files = {"image": open("test.png", "rb")}
data = {"task_description": "出现人员拥挤的情况。"}

response = requests.post(
    "http://36.7.84.146:23576/api/v1/verify", files=files, data=data
)

result = response.json()
if result["match"]:
    print("继续post到平台")

else:
    print("跳过")

print(f"Match: {result['match']}")
print(f"Reason: {result['reason']}")
print(f"Processing time: {result['processing_time']}s")
