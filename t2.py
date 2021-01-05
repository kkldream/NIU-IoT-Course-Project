import requests

my_data = { 'action': 'get_status'}

r = requests.post('http://120.101.8.240:5000/api', data = my_data)

print(r.status_code)
print(r.text)
print(type(eval(r.text)))
print(eval(r.text))
print(eval(r.text)['status'])