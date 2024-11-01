import os

def init_login_ig(cli, user_id, username, password):
    session_path = os.path.join("sessions", f"{user_id}-{username}.json")

    try:
        if os.path.exists(session_path):
            cli.load_settings(session_path)
            print("Logged in using saved session.")
        else:
            cli.login(
                username=username,
                password=password,
                
            )
            cli.dump_settings(session_path)
            print("New session saved.")
    except Exception as e:
        print("An error occurred during login:", e)


# def two_factor_handler(bot, user_id, username):
#     code_2fa = bot.ask(chat_id=user_id, text=f"Enter your 2fa code for '{username}'")
#     return code_2fa.text
