

def get_route(data):
	"""
	На вход массив, каждый элемент из которого
	это 4 метрики и id маршрутка 
	"""

	outcome = [0,{}]

	disp = []

	avarage = data.get('avarage')
	for route in data:
		s1 = route.get("s1")
		s2 = route.get('s2')
		s3 = route.get('s3')
		s4 = route.get('s4')
		id_route = route.get('id_route')

		coef = s1 * 0.7 + s2 * 1 + s3 * 0.6 + s4 * 0.6
		
		disp.append({id_route:(coef - avarage)})

	disp = sorted(disp, key=lambda k: k['id_route'])
	if disp[len(disp) - 1]  - disp[0] > 0.5:
		return disp.keys()[len(disp) - 1]
	else:
		return 0		

