import os
from instagrapi import Client


async def load_client(bot, user_id, username, password):
    session_path = os.path.join("sessions", f"{user_id}-{username}.json")

    cli = Client()

    try:
        if os.path.exists(session_path):
            cli.load_settings(session_path)
            print("Logged in using saved session.")
        else:
            cli.login(
                username=username,
                password=password,
                verification_code=lambda user_id, username: await two_factor_handler(
                    bot, user_id, username
                ),
            )
            cli.dump_settings(session_path)
            print("New session saved.")
    except Exception as e:
        print("An error occurred during login:", e)

    return cli


async def two_factor_handler(bot, user_id, username):
    code_2fa = await bot.ask(chat_id=user_id, text=f"Enter your 2fa code for '{username}'")
    return code_2fa.text
