def test_pagina_inicial(cliente):

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "Buenos dias mi gente. Soy Nacho" in contenido

def test_pagina_health(cliente):

	respuesta=cliente.get("/health")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "OK" in contenido