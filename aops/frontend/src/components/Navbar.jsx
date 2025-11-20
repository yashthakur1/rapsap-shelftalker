import React from 'react';
import { Link, useLocation } from 'react-router-dom';

/**
 * Navbar Component
 * Navigation header for the application
 */
export default function Navbar() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-800';

  return (
    <header className="bg-white shadow-md sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Logo & Title */}
          <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div className="text-3xl">🏷️</div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">AOPS</h1>
          </Link>

          {/* Navigation Links */}
          <nav className="flex items-center space-x-6">
            <Link
              to="/"
              className={`pb-2 font-semibold transition-colors ${isActive('/')}`}
            >
              Dashboard
            </Link>
            <Link
              to="/settings"
              className={`pb-2 font-semibold transition-colors ${isActive('/settings')}`}
            >
              Settings
            </Link>
          </nav>

          {/* Subtitle */}
          <p className="text-sm md:text-base text-gray-600 hidden md:block">
            Automated Offer Print System
          </p>
        </div>
      </div>
    </header>
  );
}
