import js2py

def get_md5(password,token): 
	with open('data/md5.js', 'r') as file:
		js_code = file.read()
	context = js2py.EvalJs()
	context.execute(js_code)
	return context.md5(password, token)