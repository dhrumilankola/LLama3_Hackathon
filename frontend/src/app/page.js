"use client";

import Navbar from './components/Navbar';
import WelcomeSection from './components/WelcomeSection';
import InsuranceOption from './components/InsuranceOption';
import UploadInsurance from './components/UploadInsurance';

const HomePage = () => {
  const insuranceOptions = [
    { id: '1', name: 'Dental', imageSrc: '/images/dental.jpg' },
    { id: '2', name: 'Vision', imageSrc: '/images/vision.jpg' },
    { id: '3', name: 'Medical', imageSrc: '/images/medical.jpg' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-r from-gray-100 to-gray-300 text-gray-800 py-10">
      <Navbar />
      <div className="container mx-auto px-4">
        <WelcomeSection />
        <h2 className="text-3xl font-bold text-center my-8 text-gray-800">Choose Your Insurance</h2>
        <div className="flex flex-wrap justify-center gap-8">
          {insuranceOptions.map(option => (
            <InsuranceOption key={option.id} id={option.id} name={option.name} imageSrc={option.imageSrc} />
          ))}
        </div>
        <h2 className="text-3xl font-bold text-center my-8 text-gray-800">Have your own insurance plan? Lean about it and clear your questions with the help of AI.</h2>
        <h2 className="text-xl font-bold text-center  text-gray-800">Upload your insurance.</h2>
        <br />
        <div className="flex justify-center">
          <UploadInsurance />
        </div>
      </div>
    </div>
  );
};

export default HomePage;