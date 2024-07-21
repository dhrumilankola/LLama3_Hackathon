"use client";

import Navbar from '../components/Navbar';

const ContactPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-400 to-indigo-600 text-white py-10">
      <Navbar />
      <div className="container mx-auto px-4 py-10">
        <h1 className="text-5xl font-bold text-center mb-8">Contact Us</h1>
        <p className="text-center text-xl mb-12">
            We would love to hear from you! Write to use if you have any querries or suggestions.
        </p>
        <div className="max-w-lg mx-auto bg-white p-8 rounded-lg shadow-lg text-gray-800">
          <form>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
                Name
              </label>
              <input 
                type="text" 
                id="name" 
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
                placeholder="Your Name" 
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                Email
              </label>
              <input 
                type="email" 
                id="email" 
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
                placeholder="Your Email" 
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="message">
                Message
              </label>
              <textarea 
                id="message" 
                rows="4" 
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
                placeholder="Your Message" 
              ></textarea>
            </div>
            <div className="flex items-center justify-between">
              <button 
                type="submit" 
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Send Message
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
