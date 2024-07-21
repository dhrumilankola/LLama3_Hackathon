import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Trash2 } from 'lucide-react';

const ChatInterface = ({ insuranceType }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [dummyTextVisible, setDummyTextVisible] = useState(true);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (dummyTextVisible) {
      const initialMessages = [
        { sender: 'bot', text: `Welcome to the ${insuranceType} insurance chat! How can I assist you today?` },
        { sender: 'bot', text: `You can ask me about coverage details, claim process, and more.` },
      ];
      setMessages(initialMessages);
    }
  }, [dummyTextVisible, insuranceType]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() === '') return;

    const newMessage = { sender: 'user', text: input };
    setMessages([...messages, newMessage]);
    setInput('');
    setDummyTextVisible(false);

    try {
      const response = await axios.post('http://localhost:5000/chat', { query: input, type: insuranceType.toLowerCase() });
      const botMessage = { sender: 'bot', text: response.data.response };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const handleClearChat = async () => {
    try {
      await axios.post('http://localhost:5000/clear_chat');
      setMessages([]);
      setDummyTextVisible(true);
    } catch (error) {
      console.error('Error clearing chat:', error.response ? error.response.data : error.message);
    }
  };

  // Generate the dynamic path for the PDF from the public directory
 const pdfPath = `/docs/${insuranceType.toLowerCase()}/${insuranceType.toLowerCase()}.pdf`;

  return (
    <div className="flex flex-col h-full bg-gradient-to-r from-blue-400 to-indigo-600 text-white p-4">
      <div className="bg-white rounded-lg shadow-lg mb-4 p-4 text-center text-gray-800 flex justify-between items-center">
        <h2 className="text-2xl font-bold">{insuranceType} Chat</h2>
        <button
          onClick={handleClearChat}
          className="p-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition flex items-center"
        >
          <Trash2 className="h-4 w-4 mr-2" />
          Clear Chat
        </button>
      </div>
      <div className="flex flex-grow gap-4">
        <div className="flex-1">
          <iframe
            src={pdfPath}
            width="100%"
            height="800px"
            className="border border-gray-300 rounded-lg"
            title="Insurance Document"
          ></iframe>
        </div>
        <div ref={chatContainerRef} className="flex-1 p-4 overflow-y-auto bg-white rounded-lg shadow-lg">
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <div key={index} className={`p-4 rounded-lg ${msg.sender === 'user' ? 'bg-blue-500 text-white self-end' : 'bg-gray-300 text-gray-800 self-start'}`}>
                {msg.text}
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="p-4 bg-white flex items-center rounded-lg shadow-lg mt-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          className="flex-grow p-2 border border-gray-300 rounded-lg text-gray-800"
          placeholder="Type your message..."
        />
        <button
          onClick={handleSend}
          className="ml-2 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
