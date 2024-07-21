"use client";

import { useRouter } from 'next/navigation';
import Image from 'next/image';

const InsuranceOption = ({ name, id, imageSrc }) => {
  const router = useRouter();

  const handleClick = () => {
    router.push(`/chatbot/${name.toLowerCase()}`);
  };

  return (
    <div className="max-w-sm rounded overflow-hidden shadow-lg bg-white">
      <Image className="w-full h-48 object-cover" src={imageSrc} alt={`${name} Insurance`} width={300} height={200} />
      <div className="px-6 py-4">
        <div className="font-bold text-xl mb-2">{name} Insurance</div>
        <p className="text-gray-700 text-base mb-4">
          Get information about our {name.toLowerCase()} insurance plans and coverage options.
        </p>
        <button 
          onClick={handleClick}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300"
        >
          Start Chat!
        </button>
      </div>
    </div>
  );
};

export default InsuranceOption;