from app import create_app

app = create_app()

if __name__ == '__main__':
    # O debug=True ajuda-nos a ver os erros no terminal e atualiza sozinho
    app.run(debug=True)