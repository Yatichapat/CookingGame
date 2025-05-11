# Description about the Project

## ⏳ Project Overview
Apocalypse Cooker is a cooking game with an apocalypse theme, where the chef opens the restaurant to send food to the 
survivors of a zombie horde in the quarantine zone around the city. The chef, who is a player, must avoid zombies who 
burst into the restaurants as possible while he has to cook food for the survivors.

## 🎯 Features
The game includes the following features:
- **Cooking**: Players can cook various dishes using different ingredients.
- **Ingredient Management**: Players can manage their ingredients, including adding, removing, and checking the status of ingredients.
- **Cooking Process**: Players can follow a cooking process to create dishes, cutting, and cooking.
- **Zombie Encounters**: Players must avoid zombies that burst into the restaurant while cooking.

## Algorithms Involved
- ### Order Generation Algorithm (Queue System)
Randomly generates a customer's menu with different ingredients and complexity such as chicken fried, sandwich or just fried egg.
- ### Ingredients Matching Algorithm
Checks if the player has selected the correct ingredients for a recipe
- ### Timer Algorithm
Tracks how long an ingredient or dish is being cooked and determines if it is perfectly cooked, uncooked, or burnt


## 🎮 About the Gameplay
- Ingredients are contained in fridge. Press **E** to open the fridge and add ingredients to the cooking pan by pressing the 
  **Enter key**.
- To drop item, you can press **Shift** on either of both side on your keyboard.
- Wait for the food to be cooked. The cooking time will show on the green bar above the pan.
- Once it's done, you can take the food out of the pan and put it on the plate by pressing **Enter key**
- You can also put the food back in the pan, in the fridge or throw it away.
- The food will be served on the blue pad.
- You can add more ingredients in the fridge by pressing the **Enter key** at the red button and take the paper bag to the fridge.
- When bring the paper bag to the fridge, you can add the ingredients in the bag to the fridge by pressing the **E** key
- The Zombie will chase the player around, you must try to avoid them as much as possible.

## 🧩 UML
The UML diagram below illustrates the main classes and their relationships in the game. 

![UML Diagram](UML.png)

## Graph Representation
| Feature Name        | Graph Objective                                                | Graph Type   | X-axis                                     | Y-axis            |
|---------------------|----------------------------------------------------------------|--------------|--------------------------------------------|-------------------|
| Total time per dish | Compare cooking efficiency across dishes                     | Boxplot      | Dish Types (sandwich, chicken fried, etc.) | Average Time      |
| Ingredients used    | Show the proportional distribution of ingredients across all dishes | Pie Chart    | Ingredient Names                           | Percentage         |
| Mistakes per order  | Measures how accurately players complete orders               | Bar Graph    | The type of accident the player made       | Mistake Count      |
| Keystrokes per dish | Analyze input efficiency distribution                         | Line Chart   | Keystroke bins                             | Frequency          |
| Orders per session  | Measure engagement vs. session duration                       | Scatter Plot | Session duration (min)                     | Orders Completed   |


## 📦 GitHub Link
### → [Link](https://github.com/Yatichapat/CookingGame.git)

## 🎬 YouTube Link 
### → [LINK](https://youtu.be/HM9LTVeIe7g)



