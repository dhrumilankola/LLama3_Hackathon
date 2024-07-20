"use client";

import { useRouter } from 'next/navigation';

const UploadInsurance = () => {
  const router = useRouter();

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Handle file upload logic here
      router.push(`/chatbot/uploaded`);
    }
  };

  return (
    <div className="flex flex-col items-center">
      <label className="cursor-pointer bg-blue-600 text-white py-2 px-4 rounded-lg shadow-lg transform transition hover:scale-105 hover:shadow-2xl">
        <input 
          type="file" 
          onChange={handleFileUpload} 
          className="hidden"
        />
        Upload Insurance File
      </label>
    </div>
  );
};

export default UploadInsurance;
