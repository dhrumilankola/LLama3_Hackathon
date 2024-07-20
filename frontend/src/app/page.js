"use client";

import Navbar from './components/Navbar';
import WelcomeSection from './components/WelcomeSection';
import InsuranceOption from './components/InsuranceOption';
import UploadInsurance from './components/UploadInsurance';

const HomePage = () => {
  const insuranceOptions = [
    { id: '1', name: 'Dental' },
    { id: '2', name: 'Vision' },
    { id: '3', name: 'Medical' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-r from-gray-100 to-gray-300 text-gray-800 py-10">
      <Navbar />
      <div className="container mx-auto px-4">
        <WelcomeSection />
        <h2 className="text-3xl font-bold text-center my-8 text-gray-800">Choose Your Insurance</h2>
        <div className="flex flex-wrap justify-center gap-6">
          {insuranceOptions.map(option => (
            <InsuranceOption key={option.id} id={option.id} name={option.name} />
          ))}
        </div>
        <h2 className="text-3xl font-bold text-center my-8 text-gray-800">Upload Your Insurance Details</h2>
        <div className="flex justify-center">
          <UploadInsurance />
        </div>
      </div>
    </div>
  );
};

export default HomePage;