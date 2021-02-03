# Desafio Nox Bitcoin | Desenvolvedor: Sandro Regis Cardoso

## Domínio do problema

Conforme especificado nos requisitos do desafio o sistema possui apenas duas entradas de dados:
1) A escolha do tipo de operação (compra ou venda);
2) A quantidade de bitcoins a ser adquirida/comprada ou vendida;


## Procedimentos abordados para resolução do desafio

1) Instanciação do serviço de gravação de log de eventos;


-   **Incluir imagem**


2) Instanciação do serviço Redis para armazenamento dos dados recebidos da fonte de dados ou das fontes de dados;


3) Acesso via API ao endpoint principal mercadobitcoin para recuperar os dados de ofertas de venda (asks) e ofertas de compra (bids);


4) Foi adicionado no arquivo de configuração uma fonte de dados alternativa (endpoint) em caso de falha do serviço principal (mercadobitcoin);


5) Todos valores recebidos da fonte de dados, passam por uma verificação para certificar de não existem valores vazios e ou zerados;


6) Após a verificação da integridade dos dados as informações são armazenadas separadamente em duas filas no Redis sendo uma para vendas (asks) e outra para compra (bids). Os dados da fila serão atualizados a cada 30 segundos conforme solicitado no requisito do desafio;


7) Após a carga de dados nas filas do Redis (asks e bids) o sistema executa algumas tarefas Cálculo do preço médio de venda, Cálculo do preço médio nas ofertas de compra, todas de bitcoins disponíveis no mercado e total de bitcoins das ofertas de compra;


8) Uma vez concluído o processamento de todos os métodos/rotinas de inicialização e preparação de dados será apresentada no console de execução a mensagem de boas vindas e a solicitação para que o cliente da NoxBitcoin faça a escolha da operação que deseja efeturar venda (opção 1) ou compra (opção 2) e após a escolha é solicitada a entrada de dado referente a quantidade de Bitcoins que deseja vender ou comprar;


9) Está prevista uma verificação (dummy) sobre a quantidade de Bitcoins solicitadas para compra, no intuito de uma possível e ou eventual restrição relacionado ao total de Bitcoins disponível na fila de ofertas de venda no momento da solicitação de transação do cliente;


-   **Incluir imagem**


10) Será possível também que o cliente faça a aquisição ou a venda de Bitcoins informando o valor em real brasileiro, em produção este cenário deverá consultar o saldo de crypto moedas do cliente;


11) Para cada uma  das transações confirmadas de venda ou compra os dados serão gravados em novas filas do Redis para operação interna da NoxBitcoin;


12) Para cada transação das filas de trading que forem concluídas os dados serão movimentados para transações concluídas;


13) A execução do modulo "NoxBitcoin Orders" se dá através da chamada do programa manage.py que por sua vez inicializa os serviços base do servidor de aplicação e do módulo e então da interação de console com o cliente da NoxBitcoin;


## Vídeo demonstrativo

- https://www.youtube.com/watch?v=KVVj9XT8G1Y


## Notas

- O programa possui sua arquitetura inicial concebida para a expansão para operações de trading com outros tipos de crypto moedas alé do bitcoin;
- Os dados armazenados nas filas "asks" e "bids" do Redis, que são oriundos das fontes de dados externas (endpoints) poderão ser gravados no sistema de arquivos como procedimento preventivo a possíveis e ou eventuais falhas nos endpoints, não interferindo nas consultas e analytics sob as necessidades da NoxBitcoin;
- A alteração de parametros no arquivo de configuração nos dá condições de utilizarmos os arquivos sample*.json para o processo de desenvolvimento, formato do dicionário, rótulos, dados, etc;
- Todos os códigos fontes foram escritos em sua maior parte em inglês norte americano, no intuito de facilitar a interação com profissionais fora do Brasil e possível necessidade de homologação com o mercado internacional global;


## Tecnologias utilizadas

- Linguagem de programação Python versão 3.7;
- Servidor de aplicação Django versão 3.0.4;
- Python/Django REST;
- Timeoutdecorator versão 0.5.0 : Este módulo colaborativo é utilizado para determinar o tempo de resposta de falha nos testes de consulta ao(s) endpoint(s), para testes de performance de execução dos métodos e para rastreamento do tempo de processamento de métodos onde se espera um limite de resposta. Ele simplifica o uso de Thread.Timeout;
- Este módulo timeout-decorator precisa ser incluso no python-path de execução do programa ou pode ser instalado através do comando pip;


## @TODO

-   **Revisão dos Testes**
-   **Criar Suite de Testes**
-   **Implementar codificação Thread.Timer (update dos dados asks e bids)**
-   **Criar interface web**
-   **Implementar envio de e-mails e serviço Push (mobile)**: https://github.com/rs/pushd
-   **Testar execução e chamada independente dos serviços backend e console**: Refinamento do pacote console;
-   **Testes de performance global**
-   **Documentação técnica do módulo**


## Desenvolvimento:

- Sandro Regis Cardoso | Engenheiro de Software
- Mobile/W.App: +55 11 9 4669-9296
- Email: projetaty@gmail.com
