from ChatBot import ChatBot
from ItemLookUp import LookUpTool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
config_dir = os.path.join(os.path.dirname(__file__), "config")
dotenv_path = os.path.join(config_dir, ".env")
load_dotenv(dotenv_path)


def main():
    # import nltk
    # nltk.download('punkt_tab')

    # # General question: memory test
    # query = "What is the best weapon I can use at 70 attack?"
    
    # wise_old_man = ChatBot()
    # ans = wise_old_man.answer(query)
    # print(ans)

    # follow_up_query = "How can I get one?"
    # follow_up_ans = wise_old_man.answer(follow_up_query)
    # print(follow_up_ans)


    # ItemLookUp general test
    query = "How many clues is the abyssal whip used in?"
    
    whip_look_up_tool = LookUpTool("Abyssal Whip")
    d_scim_look_up_tool = LookUpTool("Dragon Scimitar")
    obby_mail_look_up_tool = LookUpTool("Obby maul")

    wise_old_man = ChatBot()
    ans = wise_old_man.answer_from_html(query)
    print(ans)


if __name__ == "__main__":
    main()