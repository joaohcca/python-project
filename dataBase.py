import sqlite3 as sq3

#criação da tabela
conn = sq3.connect('produtos.db')
prod = conn.cursor()

#prod.execute("""
#CREATE TABLE produtos (
#    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#    tipo TEXT NOT NULL,
#    area FLOAT NOT NULL,
#    perimetro FLOAT NOT NULL,
#    data DATE NOT NULL
#    );
#    """)
#print('Tabela criada com Sucesso')
#conn.close()





 #inicializando tabela com dados pra database
    #rotina de adição na tabela
    #prod.execute(""" INSERT INTO produtos (tipo,area,perimetro,evento_em)
    #VALUES('teste',50000,2500,11-02-2018)
    #""")
prod.execute("""
SELECT * FROM produtos;
""");
#rotina de leitura na tabela
print("database test")
for linha in prod.fetchall():
    print(linha)
conn.close()
    #CREATE TABLE produtos (
    #	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    #	tipo TEXT NOT NULL,
    # 	area FLOAT,
    #	perimetro FLOAT,
    #	evento_em DATE NOT NULL,
    #);
    #"""""")
    #prod.close()

     # inserindo dados na tabela

     #obj é uma tupla com os dados

    #removendo dados da database usando o id como indicador
#     id_produto = 8

     # excluindo um registro da tabela
 #    prod.execute("""
 #    DELETE FROM produtos
 #    WHERE id = ?
 #    """, (id_produto,))
#
#     conn.commit()