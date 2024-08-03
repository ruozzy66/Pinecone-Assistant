# Pinecone Assistant Chat (Twilight Imperium IV Edition Rules Bot)

A modern web-based chatbot interface for interacting with Pinecone's AI assistant. I connected it to Twilight Imperium IV Edition board game rules knowledge base, but you can create your own knoledge base using Pinecone Assistant. 

## 🌟 Features

- Real-time chat interface with Pinecone's AI assistant
- Modern, responsive design using React and Chakra UI
- Seamless integration with Pinecone's API
- Error handling and user-friendly messages
- Easy deployment to Heroku

## 🚀 Getting Started

### Prerequisites

- Node.js (v18.x or later)
- npm (comes with Node.js)
- A Pinecone API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/ruozzy66/pinecone-assistant-chat.git
   cd pinecone-assistant-chat
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file in the root directory and add your Pinecone API key:
   ```
   PINECONE_API_KEY=your_api_key_here
   ```

### Running Locally

1. Start the development server:
   ```
   npm run dev
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Deployment to Heroku

1. [Create a Heroku account](https://dashboard.heroku.com/) and install the Heroku CLI.

2. Log in to Heroku:
   ```
   heroku login
   ```

3. Create a new Heroku app:
   ```
   heroku create
   ```

4. Set your Pinecone API key as a Heroku config var:
   ```
   heroku config:set PINECONE_API_KEY=your_api_key_here
   ```

5. Deploy to Heroku:
   ```
   git push heroku main
   ```

6. Open your app:
   ```
   heroku open
   ```

## 📖 Usage

Once the application is running, you can start chatting with the you own Pinecone Assistant. Simply type your question into the input field and press Enter or click the Send button.

## 🛠 Tech Stack

- Frontend: React, Chakra UI
- Backend: Node.js, Express
- API Integration: Axios
- Deployment: Heroku

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/ruozzy66/pinecone-assistant-chat/issues).

## 📝 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## 👏 Acknowledgements

- [Pinecone](https://www.pinecone.io/) for their amazing AI assistant API
- [Twilight Imperium](https://www.fantasyflightgames.com/en/products/twilight-imperium-fourth-edition/) for being an awesome game
- [BoardGameGeek community](https://boardgamegeek.com/boardgame/233078/twilight-imperium-fourth-edition) for their extensive discussions and rule clarifications
- [Twilight Imperium Fandom Wiki community](https://twilight-imperium.fandom.com/wiki/Twilight_Imperium_Wiki) for maintaining a comprehensive knowledge base
- Both the BoardGameGeek and Twilight Imperium Fandom communities for providing the vast knowledge base used in training the LLM for this project
