
#! run the server
from flaskblog import create_app  # exist in __init__.py
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# TODO 
# add and wether api to the home screen ! 
# https://www.youtube.com/watch?v=InoAIgBZIEA    ===> https://openweathermap.org/api