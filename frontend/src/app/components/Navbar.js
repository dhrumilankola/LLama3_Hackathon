"use client";

import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className="bg-white text-gray-800 shadow-lg mb-10 rounded-lg mx-10">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-blue-600"><Link href="/" className="hover:text-blue-600">Insurance Info</Link>
        </div>
        <div className="space-x-6">
          <Link href="/" className="hover:text-blue-600">Home</Link>
          <Link href="/contact" className="hover:text-blue-600">Contact Us</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
