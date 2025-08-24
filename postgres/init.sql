CREATE TABLE paises (Pais VARCHAR(50) PRIMARY KEY,
					PaisIngles VARCHAR(50));

COPY paises (Pais, PaisIngles) FROM '/docker-entrypoint-initdb.d/paises.csv' WITH CSV HEADER;

CREATE TABLE ciudades (CodCiudad SERIAL PRIMARY KEY,
						Ciudad VARCHAR(50),
						Latitud VARCHAR(50),
						Longitud VARCHAR(50),
						Pais VARCHAR(50),
						Siglas CHAR(3),
						Tipo VARCHAR(50),
						Poblacion INT,
						FOREIGN KEY (Pais) REFERENCES paises (Pais) ON DELETE CASCADE);

COPY ciudades (Ciudad, Latitud, Longitud, Pais, Siglas, Tipo, Poblacion) FROM '/docker-entrypoint-initdb.d/ciudades.csv' WITH CSV HEADER;

CREATE TABLE usuarios (Usuario VARCHAR(255) PRIMARY KEY,
						Correo VARCHAR(255),
						Contrasena VARCHAR(255),
						Nombre VARCHAR(255),
						Apellido VARCHAR(255),
						Fecha_Nacimiento DATE,
						CodCiudad INT,
						Admin BOOl DEFAULT FALSE,
						FOREIGN KEY (CodCiudad) REFERENCES ciudades (CodCiudad));

DELETE FROM paises WHERE pais IN ('Anguila', 'Antigua y Barbuda', 'Aruba', 'Bahamas', 'Barbados', 'Bermudas', 'Cabo Verde', 
    'Comoras', 'Dominica', 'Fiyi', 'Granada', 'Guadalupe', 'Guam', 'Guayana Francesa', 'Isla de Man', 'Isla de Navidad', 
    'Isla Norfolk', 'Islas Caimán', 'Islas Cook', 'Islas Feroe', 'Islas Malvinas (Islas Falkland)', 'Islas Marianas del Norte', 
    'Islas Marshall', 'Islas Pitcairn', 'Islas Turcas y Caicos', 'Islas Vírgenes Británicas', 'Islas Vírgenes de EE.UU', 'Jersey', 
    'Kiribati', 'Lesoto', 'Liechtenstein', 'Macau', 'Maldivas', 'Martinica', 'Montserrat', 'Nauru', 'Niue', 'Nueva Caledonia', 
    'Palaos', 'Polinesia Francesa', 'Reunión', 'Samoa', 'Samoa Americana', 'San Bartolomé', 'San Cristóbal y Nieves', 'San Marino', 
    'San Pedro y Miquelón', 'San Vicente y las Granadinas', 'Santa Lucía', 'Santo Tomé y Príncipe', 'Seychelles', 'Solomon Islands', 
    'Suazilandia', 'Surinam', 'Svalbard', 'Tonga', 'Tuvalu', 'Vanuatu', 'Wallis y Futuna', 
    'Benín', 'Burkina Faso', 'Burundi', 'Chad', 'Djibouti', 'Eritrea', 'Gabón', 'Gambia', 'Guinea', 'Guinea Ecuatorial', 'Guinea-Bissau', 
    'Liberia', 'Malawi', 'Malí', 'Mauritania', 'Mozambique', 'Namibia', 'Níger', 'Ruanda', 'Sierra Leona', 'Somalia', 'Sudán del Sur', 'Togo', 'Zambia',
    'Afganistán', 'Bután', 'Brunei', 'Camboya', 'Laos', 'Mongolia', 'Nepal', 'Timor Oriental', 'Uzbekistán', 'Tayikistán', 'Turkmenistán',
    'Papúa Nueva Guinea', 'Belice', 'Guyana', 'Haití', 'Surinam', 'Trinidad y Tobago', 'Artículo 1', 'Mayotte');

DELETE FROM ciudades
WHERE (ciudad, pais, CodCiudad) IN (SELECT ciudad, pais, CodCiudad FROM ciudades
								    WHERE (ciudad, pais) IN (SELECT ciudad, pais FROM ciudades
													        GROUP BY ciudad, pais HAVING COUNT(*)>1)
AND CodCiudad NOT IN (SELECT MIN(CodCiudad) FROM ciudades
				        GROUP BY ciudad, pais HAVING COUNT(*)>1));