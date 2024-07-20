"use client";

import { useParams } from 'next/navigation';
import Navbar from '../../components/Navbar';
import ChatInterface from '../../components/ChatInterface';

const ChatbotPage = () => {
  const params = useParams();
  const { type } = params;
  const insuranceType = type.charAt(0).toUpperCase() + type.slice(1); // Capitalize the first letter

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-400 to-indigo-600 text-white py-10">
      <Navbar />
      <div className="container mx-auto px-4">
        <ChatInterface insuranceType={insuranceType} />
      </div>
    </div>
  );
};

export default ChatbotPage;
