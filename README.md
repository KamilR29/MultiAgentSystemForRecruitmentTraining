# Recruitment Assistant Web Application

A Streamlit-based web application that provides recruitment assistance through multiple functionalities, including CV analysis, technical review, and interview simulation. Powered by advanced language models, this application helps both candidates and recruiters streamline and enhance the recruitment process.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This project offers a comprehensive recruitment assistant platform built with Streamlit. It integrates advanced language models via custom libraries (e.g., `langchain_openai` and `langgraph`) to perform tasks such as:

- **CV Analysis**: Upload and analyze your CV along with job requirements to receive detailed assessments on technical, soft, and language skills.
- **Technical Review**: Engage in a multi-step, graph-based workflow that simulates technical interviews by asking domain-specific questions, evaluating responses, and providing model answers.
- **Interactive Chat Interface**: Utilize an intuitive chat interface for a seamless user experience during the recruitment process.

## Features

- **Multi-Page Navigation**: Easily switch between different functionalities via a sidebar menu.
- **Custom Styling**: Enhanced UI with custom CSS for a modern and professional look.
- **CV & Requirements Analysis**: Upload `.docx` files to analyze CV content and job requirements.
- **Graph-Based Workflows**: Advanced multi-step workflows to assess skills, compare profiles, and generate tailored model CVs.
- **Interview Simulation**: Interactive recruitment process with LLM-powered questions, answer evaluation, and feedback.
- **Progress Feedback**: Dynamic progress bars and chat-based interactions provide a responsive user experience.

## Project Structure

```
.
├── main.py                       # Main module for page routing and custom styling
├── pages/
│   ├── main_page.py              # Displays an introductory page with progress feedback and LLM interaction
│   ├── analyze_cv_page.py        # Handles CV and job requirements analysis through file uploads and graph-based workflow
│   └── recruitment_process_page.py  # Manages the recruitment workflow and interactive interview simulation
├── images/
│   └── logo.png                  # Logo displayed in the sidebar
├── .env                          # Environment file for storing API keys (not included in version control)
└── README.md                     # Project documentation (this file)
```

### File Descriptions

- **`main.py`**: Routes the application to different pages ("Home", "Analyze CV", "Technical Review") and applies custom sidebar styling.
- **`analyze_cv_page.py`**: Allows users to upload a CV and job requirements in `.docx` format, then performs analysis using an LLM-powered, graph-based workflow.
- **`main_page.py`**: Introduces the application with a progress bar and initial language model interactions, providing an overview of available functionalities.
- **`recruitment_process_page.py`**: Implements the core recruitment workflow where users receive interview questions, submit answers, and get feedback (including ratings and model answers) through a series of graph-based nodes.

## Installation

### Clone the Repository:

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### Create and Activate a Virtual Environment (Optional but Recommended):

```bash
python -m venv venv
source venv/bin/activate      # On Windows use: venv\Scripts\activate
```

### Install Required Dependencies:

If you have a `requirements.txt` file, install dependencies using:

```bash
pip install -r requirements.txt
```

Otherwise, manually install the necessary packages:

```bash
pip install streamlit python-dotenv python-docx pandas typing_extensions
# Additionally, install the custom libraries if available:
pip install langchain_openai langgraph
```

## Configuration

### OpenAI API Key:

Create a `.env` file in the root directory and add your OpenAI API key:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### Logo and Assets:

Ensure that the `images/logo.png` file is in place, as it is used in the sidebar.

## Usage

### Run the Application:

Execute the following command to start the Streamlit server:

```bash
streamlit run main.py
```

### Navigate Through Pages:

Use the sidebar to select the desired functionality:

- **Home**: View introductory information and progress-based interactions.
- **Analyze CV**: Upload your CV and job requirements for a detailed analysis.
- **Technical Review**: Engage in an interactive recruitment process with interview simulations.

### Follow On-Screen Prompts:

Each page provides instructions, file upload widgets, and interactive chat messages to guide you through the process.

## Dependencies

- `streamlit`
- `python-docx`
- `python-dotenv`
- `pandas`
- `typing_extensions`
- `langchain_openai` (Ensure you have access to this or its equivalent)
- `langgraph` (Ensure you have access to this or its equivalent)

**Note**: Some dependencies such as `langchain_openai` and `langgraph` may be proprietary or custom packages. Please refer to the respective documentation or repository for installation details.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Ensure your code follows the project’s style and passes any tests.
4. Submit a pull request with a detailed description of your changes.

For major changes, please open an issue first to discuss what you would like to change.

## License

[Specify your license here]

## Contact

For inquiries or support, please reach out to: [Your Contact Information]


---

## Installation

Follow the steps below to set up and run the application:

### Prerequisites

Ensure you have **Python 3.11** installed on your system.

### Steps


1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
- Add **`OPENAI_API_KEY`** in .env
3. Run the application:

   ```bash
   streamlit run main.py
   ```

---
## Home page
![image](https://github.com/user-attachments/assets/3401654d-a3c6-4d58-ba89-bbdee670f773)

---
##  Analyze CV page
![image](https://github.com/user-attachments/assets/dfb74f05-fbe2-433f-9faf-d7f672078a35)

---
## Technical Review page
![image](https://github.com/user-attachments/assets/5c76dece-d59f-4a0b-9cd4-7afac4f6bb6a)



**Enjoy seamless recruitment support!**
