"use client";

import { useRouter } from 'next/navigation';

const InsuranceOption = ({ name, id }) => {
  const router = useRouter();

  const handleClick = () => {
    router.push(`/chatbot/${name.toLowerCase()}`);
  };

  return (
    <div 
      onClick={handleClick} 
      className="cursor-pointer p-6 bg-white text-gray-800 rounded-lg shadow-lg transform transition hover:scale-105 hover:shadow-2xl"
    >
      <h3 className="text-2xl font-semibold">{name}</h3>
    </div>
  );
};

export default InsuranceOption;
