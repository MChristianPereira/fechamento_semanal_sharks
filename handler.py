from modules import dados_fintz, composicao_ibov, ibov, acoes_semana, enviar_email

def gerando_fechamento_semanal():

    try:
        dados_fintz().iniciar_script_main()
        composicao_ibov()
        ibov().iniciar_script_main()
        acoes_semana().iniciar_script_main()
        enviar_email().enviando_email()
    
        response = {}
        response['statusCode'] = 200
        response['headers'] = {}
        response['headers']['Content-Type'] = 'application/json'
        response['body'] = {'message': 'Fechamento Semanal enviado com sucesso!'}

        return response
    
    except Exception as e:

        response = {}
        response['statusCode'] = 502
        response['headers'] = {}
        response['headers']['Content-Type'] = 'application/json'
        response['body'] = {'message': f'{e}'}
        enviar_email().enviando_erro_email(error = f'Erro ao enviar o Fechamento Semanal: {e}')
  
        return response

if __name__ == "__main__":

    resposta = gerando_fechamento_semanal()    
    print(resposta)