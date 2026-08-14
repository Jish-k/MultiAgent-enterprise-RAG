"use client";
import Link from "next/link";
import { MessageSquare, Clock, User, LogOut } from "lucide-react";
import { useAuth } from "@/components/AuthProvider";

export default function DashboardPage() {
  const { logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <button onClick={logout} className="text-gray-500 hover:text-red-500 flex items-center gap-2 transition-colors">
            <LogOut size={20} />
            Logout
          </button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link href="/chat" className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100 dark:border-gray-700 group flex flex-col items-center text-center">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/50 text-blue-600 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <MessageSquare size={24} />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">New Chat</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm">Start a new reasoning session with the Agentic RAG.</p>
          </Link>

          <Link href="/history" className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100 dark:border-gray-700 group flex flex-col items-center text-center">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/50 text-purple-600 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <Clock size={24} />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Previous Chats</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm">Review past multi-hop reasoning sessions and verified answers.</p>
          </Link>

          <Link href="/profile" className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100 dark:border-gray-700 group flex flex-col items-center text-center">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/50 text-green-600 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <User size={24} />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Profile</h3>
            <p className="text-gray-500 dark:text-gray-400 text-sm">Manage your account settings and preferences.</p>
          </Link>
        </div>
      </div>
    </div>
  );
}
