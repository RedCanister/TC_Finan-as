## Uso

O projeto utiliza Streamlit para criar uma interface interativa, permitindo que os usuários insiram dados de entrada, vejam previsões geradas pelo modelo LSTM e acompanhem o histórico de entradas e saídas.

### Funcionalidades principais

- **Interface interativa:**  
  Usuários podem inserir os valores de `Open`, `High` e `Low` na barra lateral.
  
- **Previsão do preço de fechamento:**  
  Com base nos dados fornecidos, o modelo LSTM realiza previsões para o preço de fechamento (`Close`) das ações da NVIDIA.

- **Histórico de previsões:**  
  O histórico de entradas e saídas é mantido durante a sessão e exibido em formato de tabela.

### Endpoints e Recursos

- **Entrada de dados:**  
  Os valores `Open`, `High` e `Low` são inseridos via barra lateral, com validação e escalonamento dos valores.

- **Modelo LSTM carregado dinamicamente:**  
  O modelo e o escalador (`scaler`) são carregados usando `pickle` para realizar previsões em tempo real.

- **Gráfico e tabela:**  
  - Tabela dinâmica com as entradas do usuário e a previsão correspondente.
  - Exibição do valor previsto diretamente na interface.

### Fluxo de execução

1. O usuário insere valores para `Open`, `High` e `Low` na barra lateral.  
2. Após clicar em "Enviar", o sistema:
   - Escala os valores para o formato esperado pelo modelo.
   - Utiliza uma sequência de 20 valores repetidos como entrada para o modelo LSTM.
   - Calcula a previsão de `Close` e reverte a normalização para exibição.
3. O resultado é exibido diretamente na interface.
4. O histórico de entradas e previsões é atualizado e mostrado como uma tabela.

