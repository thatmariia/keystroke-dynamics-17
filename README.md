# Keystroke Dynamics

This repository consists of code and data used for testing a model of ideantification a user by their typing behavior. 

The model has been developed for a course 2WH20 at TU/e by Christian van den Berg, Finn Devlin, Mariia Turchina, Sanderijn van Loosdrecht.

  ## Files description

  * DataCollection.py - collects raw information about each entry and stores it in a .xlsx file designated for the user.

  * DataProcessing.ipynb - processes the raw data of all users and prepares it for the evaluation

  * Evaluation.ipynb - evaluates the model

  * .xlsx files starting with "check" - raw data used for evaluation

  * other .xlsx files - raw data used for model construction

# Usage

  ## To run with existing data

  1. Run DataProcessing.ipynb
  2. Run Evaluation.ipynb
  
  ## To generate new data and run
  
  1. Make users run DataCollection.py as many times as possible (perform multiple entering sessions)
  2. After all the entering sessions are done, separate the file of each user into 2:
    * Bigger one for model construction: delete "password_" in front of the file name
    * Smaller one for model evaluation: substritute "password_" to "check " in the file name
  3. In the DataProcessing.ipynb and Evaluation.ipynb files manually put the names of the users in "names" list
    (Also consider adding more matplotlib color to the "colors" list in ataProcessing.ipynb so that len(color) >= len(names) so that the graphs are distinguishable for each user)
  4. Run DataProcessing.ipynb
  5. Run Evaluation.ipynb
  

