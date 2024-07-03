import sqlite3
from pyrogram import Client, filters

# Usando a sessão salva "my_account.session"
app = Client("my_account")

# Conexão com o banco de dados SQLite (será criado se não existir)
conn = sqlite3.connect('messages.db')
cursor = conn.cursor()

# Cria a tabela para armazenar as mensagens, se ainda não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message_text TEXT
    )
''')
conn.commit()

@app.on_message(filters.private)
async def log_message(client, message):
    # Obtém o ID do usuário que enviou a mensagem
    user_id = message.from_user.id
    
    # Obtém o conteúdo da mensagem
    text = message.text
    
    # Registra no console o ID do usuário e a mensagem recebida
    print(f"Usuário ID: {user_id} | Mensagem: {text}")
    
    # Insere a mensagem no banco de dados SQLite
    cursor.execute('''
        INSERT INTO messages (user_id, message_text) VALUES (?, ?)
    ''', (user_id, text))
    conn.commit()
    
    # Responde ao usuário com uma mensagem de confirmação
    await message.reply("Mensagem recebida. Seu ID foi registrado no log!")

# Inicia o bot
app.run()
