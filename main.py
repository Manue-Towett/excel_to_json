import json
import pandas as pd
from logs import Logger

class ExcelToJson:
    """Converts Excel file containing menu items into a json file"""
    def __init__(self) -> None:
        self.logger = Logger(self.__class__.__name__)
        self.logger.info("*****ExcelToJson converter started*****")

        try:
            self.xls = pd.ExcelFile("./input/Restaurant Menu Nutrients.xlsx")
            self.sheet_names = self.xls.sheet_names
        except:
            self.logger.error("Cannot locate file 'Restaurant Menu Nutrients.xlsx'")

        self.results = []

    def __update_df_headers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Updates the headers of the dataframe
           
           Arg:
             - df: the dataframe to be updated
           Return:
             - A dataframe with the updated headers
        """
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                if df.iat[row, col] == "Menu Item":        
                    df.columns = df.iloc[row]

                    return df.drop(df.index[row])
    
    def __update_ingredients(self, 
                             data: dict[str, str], 
                             menu_item: dict[str, str|list]) -> None:
        """Updates the list of ingredients for a given menu item
        
           Args:
             - data: a dictionary with the list of ingredients
             - menu_item: a dictionary to be updated with ingredients
        """
        value = data["Key Ingredients"]

        if value:
            if "," in value:
                menu_item["KeyIngredients"].extend(value.split(", "))
            else:
                menu_item["KeyIngredients"].append(value)

    
    def __update_nutrients(self, 
                           data: dict[str, str],
                           menu_item: dict[str, str|list]) -> None:
        """Updates the list of nutrients for a given menu item
        
           Args:
             - data: a dictionary with the list of nutrients
             - menu_item: a dictionary to be updated with nutrients
        """
        is_nutrient = False

        for key, value in data.items():
            if value and is_nutrient:
                menu_item["Nutrients"].append(key)

            if key == "Key Ingredients":
                is_nutrient = True

    
    def __generate_item(self,
                        cuisine_type: str,
                        data_dict: dict[str, str]) -> None:
        """Generate a menu item to be inserted into json
           
           Args:
             - cuisine_type: cuisine type of the menu item
             - data_dict: dictionary to be used in generating menu item
        """
        menu = {"CuisineType": cuisine_type,
                "MenuItem": data_dict["Menu Item"],
                "KeyIngredients": [],
                "Nutrients": [],
                "ImageURL": ""}
        
        self.__update_ingredients(data_dict, menu)
        self.__update_nutrients(data_dict, menu)

        self.results.append(menu)
    
    def run(self) -> None:
        """Entry point to the scraper"""
        for sheet_name in self.sheet_names:
            self.logger.info(f"Converting sheet '{sheet_name}' to json...")

            df = self.__update_df_headers(self.xls.parse(sheet_name))

            if df.empty:
                self.logger.warn(f"{sheet_name} sheet has no records...")
                continue

            records = df.fillna(False).to_dict("records")

            self.logger.info(f"Records found: {len(records)}")

            [self.__generate_item(sheet_name, data) for data in records]
        
        self.logger.info("Done converting excel to json. Saving records...")

        with open("./output/results.json", "w") as file:
            json.dump(self.results, file, indent=4)
        
        self.logger.info("Records saved.")

if __name__ == "__main__":
    converter = ExcelToJson()
    converter.run()