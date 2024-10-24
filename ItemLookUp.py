import requests
import regex as re
import os
from bs4 import BeautifulSoup


class LookUpTool():
    """
    """
    def __init__(self, item: str) -> None:
        """
        """
        self.item = self._get_item_title(item)
        self.page = self._get_page_data(self.item)
        self.soup = BeautifulSoup(self.page, "lxml")
        self._save_page_as_html()

    def _get_page_data(self, item: str) -> str:
        """
        """
        url = f"https://oldschool.runescape.wiki/api.php?action=query&prop=revisions&format=json&rvprop=content&titles={item}"
        # Get the response
        response = requests.get(url)
        # Parse as a json
        data = response.json()
        # Navigate to the page info from the given page id
        page_id = list(data["query"]["pages"].keys())[0]
        page = data["query"]["pages"][page_id]["revisions"][0]["*"]
        
        return page

    def _save_page_as_html(self) -> None:
        """"""
        out_dir = "webpages/"
        file_name = f"{self.item.replace(' ', '-')}-page.html"
        path = os.path.join(out_dir, file_name)
        with open(path, "w") as file:
            file.write(self.page)

    def _get_item_title(self, item: str) -> str:
        """
        """
        # Get the page info
        page = self._get_page_data(item)

        # Check for a redirect for item formatting issues
        redirect_check = re.findall(r"(?<=#REDIRECT \[\[)(.*)(?=\]\])", page)
        if redirect_check:
            item = redirect_check[0]
            
        return item
        



