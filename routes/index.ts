import app = require("teem");

//**********************************************************************************
// Se por acaso ocorrer algum problema de conexão, autenticação com o MySQL,
// por favor, execute este código abaixo no MySQL e tente novamente!
//
// ALTER USER 'USUÁRIO'@'localhost' IDENTIFIED WITH mysql_native_password BY 'SENHA';
//
// * Assumindo que o usuário seja root e a senha root, o comando ficaria assim:
//
// ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
//
//**********************************************************************************

class IndexRoute {
	public async index(req: app.Request, res: app.Response) {
		let jogos: any[];

		await app.sql.connect(async (sql) => {

			// Todas os comandos SQL devem ser executados aqui dentro do app.sql.connect().

			jogos = await sql.query(`
				SELECT jogo.id_jogo, jogo.titulo, genero.nome_genero
				FROM jogo
				INNER JOIN genero ON genero.id_genero = jogo.id_genero
				ORDER BY genero.nome_genero ASC, jogo.titulo ASC
			`);

		});

		let opcoes = {
			jogos: jogos
		};

		res.render("index/index", opcoes);
	}

	@app.route.methodName("jogo/:id_jogo")
	public async jogo(req: app.Request, res: app.Response) {
		const id_jogo = parseInt(req.params["id_jogo"]) || 0;

		let leituras: any[];

		await app.sql.connect(async (sql) => {

			// Todas os comandos SQL devem ser executados aqui dentro do app.sql.connect().

			leituras = await sql.query(`
				SELECT jogo.id_jogo, jogo.titulo, jogo.preco, jogo.review, raspagem.acessos, date_format(raspagem.data, '%d/%m') data
				FROM jogo
				INNER JOIN raspagem ON raspagem.id_jogo = jogo.id_jogo
				WHERE jogo.id_jogo = ?
				ORDER BY raspagem.data ASC
			`, [id_jogo]);

		});

		let opcoes = {
			leituras: leituras
		};

		res.render("index/jogo", opcoes);
	}
}

export = IndexRoute;
