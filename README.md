# AI Chatbot for Insurance Document Assistance - LLama 3 Hackathon Submission
## Team 0xAGI

## Introduction

Our AI-powered chatbot, leveraging the advanced Llama3 model, is designed to assist university students in navigating and comprehending complex insurance documents. It supports both default university insurance documents and allows students to upload their own documents for personalized queries. By using advanced NLP techniques, the chatbot delivers precise, document-based responses, ensuring accuracy and relevance. Available 24/7, it offers instant and accessible support, particularly benefiting international students unfamiliar with local insurance systems. This solution's versatility extends beyond academia, making it applicable in various industries such as law and finance, where understanding complex documents is crucial.

## Problem

University students, including many international students unfamiliar with local insurance systems, struggle to understand complex insurance documents, lack accessible guidance, and face time-consuming research with inconsistent information and limited personalized assistance.

## Technologies Used

- **Frontend:**
  - Next.js
  - React
  - Tailwind CSS
  - Axios

- **Backend:**
  - Flask
  - Python
  - Llama3 model
  - Together.ai API



## How to Run the Project

### Prerequisites

- Ensure you have Node.js version 18.17.0 installed.
- Set up the `TOGETHER_API_KEY` in a `.env` file.

### Frontend (Next.js)

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name/frontend
    ```

2. **Set up the environment variable:**
    - Create a `.env` file in the `frontend` directory with the following content:
      ```
      TOGETHER_API_KEY=your_api_key_here
      ```

3. **Install dependencies:**
    ```bash
    npm install
    ```

4. **Run the development server:**
    ```bash
    npm run dev
    ```

5. **Open your browser and navigate to:**
    ```
    http://localhost:3000
    ```

### Backend (Flask)

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name/backend
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask app in backend folder:**
    ```bash
    python app.py
    ```

5. **The backend server will be running on:**
    ```
    http://localhost:5000
    ```

## Workflow

1. **User Interaction:**
   - Users interact with the chatbot via the web interface.
   - They can ask questions about default university insurance documents or upload their own.

2. **Document Processing:**
   - Uploaded documents are processed and stored securely.
   - The chatbot analyzes the content using advanced NLP techniques.

3. **Response Generation:**
   - The chatbot generates accurate, document-based responses.
   - It provides clear, concise answers to the users' queries.

4. **Continuous Learning:**
   - The chatbot improves over time with more interactions and feedback.
   - It adapts to provide better and more accurate assistance.

![Workflow Diagram](/images/workflow.jpeg)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Contact

For any questions or inquiries, please contact [your-email@example.com](mailto:your-email@example.com).
