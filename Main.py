from ChatBot import ChatBot
import os
from dotenv import load_dotenv

# Load environment variables from .env file
config_dir = os.path.join(os.path.dirname(__file__), "config")
dotenv_path = os.path.join(config_dir, ".env")
load_dotenv(dotenv_path)


def main():
    query = "What is the best weapon I can use at 70 attack?"

    wise_old_man = ChatBot()
    ans = wise_old_man.answer(query)
    print(ans)

    follow_up_query = "How can I get one?"
    follow_up_ans = wise_old_man.answer(follow_up_query)
    print(follow_up_ans)


if __name__ == "__main__":
    main()