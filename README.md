# MCQ Generator NLP Project

This project is designed to generate multiple-choice questions (MCQs) from text using advanced Natural Language Processing (NLP) techniques. Initially, it used spaCy, but it has now been enhanced to include the BERT method for more accurate and context-aware question generation.

## Features

- Generate MCQs from any given text.
- Utilize BERT for generating context-aware questions and answers.
- Flask-based web interface for easy interaction.
- Show correct answers only after all questions have been attempted and submitted.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/mcq-generator-nlp.git
    cd mcq-generator-nlp
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main application:
    ```bash
    python main.py
    ```

2. Open your browser and go to `http://localhost:5000` to interact with the MCQ generator.

## File Structure

- `main.py`: The main application file that sets up and runs the Flask server.
- `requirements.txt`: A list of dependencies required for the project.
- `templates/`: Contains the HTML templates for the web interface.
- `static/`: Contains static files like CSS and JavaScript.

## Main.py Overview

The `main.py` file includes the logic for:

- Setting up the Flask application.
- Handling requests to generate MCQs.
- Using the BERT method for question and answer generation.
- Displaying the MCQs on the web interface.

## Future Enhancements

- Integrate more advanced NLP methods and fine-tune the BERT model for better accuracy.
- Add support for different languages.
- Improve the user interface for a better user experience.

## Contributions

Feel free to fork this repository, make improvements, and send a pull request. Contributions are always welcome!

## License

This project is licensed under the MIT License.
