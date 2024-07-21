import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

const UploadInsurance = () => {
  const router = useRouter();
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    setFile(acceptedFiles[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false
  });

  const handleSubmit = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      router.push('/chatbot/custom');
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col items-center w-full max-w-md mx-auto">
      <div 
        {...getRootProps()} 
        className={`w-full p-6 mb-4 border-2 border-dashed rounded-lg text-center cursor-pointer
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${file ? 'bg-green-50' : ''}`}
      >
        <input {...getInputProps()} />
        {
          file
            ? <p className="text-green-600">File selected: {file.name}</p>
            : isDragActive
              ? <p>Drop the PDF file here ...</p>
              : <p>Drag 'n' drop a PDF file here, or click to select a file</p>
        }
      </div>
      <button 
        onClick={handleSubmit}
        disabled={!file || isUploading}
        className={`w-full py-2 px-4 rounded-lg shadow-lg transform transition
          ${file && !isUploading 
            ? 'bg-blue-600 text-white hover:bg-blue-700 hover:scale-105' 
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
      >
        {isUploading ? 'Uploading...' : 'Submit'}
      </button>
    </div>
  );
};

export default UploadInsurance;