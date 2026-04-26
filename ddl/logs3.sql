CREATE TABLE usuario(
	id_usuario SERIAL PRIMARY KEY,
	usuario_tipo INT,
	nome VARCHAR(100) NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	senha VARCHAR(16) NOT NULL
)

SELECT * FROM usuario

CREATE TABLE arquivo(
	id_arquivo SERIAL PRIMARY KEY,
	usuario_uploader INT REFERENCES usuario(id_usuario),
	nome VARCHAR(255) NOT NULL,
	acesso INT NOT NULL DEFAULT 1,   --Publico
	tipo VARCHAR(50) DEFAULT 'application/x-shockwave-flash',
    DataCriacao DATE
)

INSERT INTO usuario
VALUES(1, 1, 'Andressa Urach', 'andressanegocios@CNN.com', '142bbuisbu214321');
