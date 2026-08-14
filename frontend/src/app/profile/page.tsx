"use client";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { useAuth } from "@/components/AuthProvider";

export default function ProfilePage() {
  const { logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-2xl mx-auto">
        <header className="flex items-center mb-8 gap-4">
          <Link href="/dashboard" className="text-gray-500 hover:text-gray-900 dark:hover:text-white">
            <ArrowLeft size={24} />
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Profile</h1>
        </header>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6 space-y-6">
          <div>
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Email Address</h3>
            <p className="text-lg text-gray-900 dark:text-white">{typeof window !== 'undefined' ? localStorage.getItem('auth_email') : 'User'}</p>
          </div>
          <div className="pt-6 border-t border-gray-100 dark:border-gray-700">
            <button onClick={logout} className="text-red-600 hover:text-red-700 font-medium transition-colors">
              Sign out of all sessions
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
