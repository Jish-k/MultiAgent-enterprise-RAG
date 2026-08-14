"use client";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function HistoryPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="flex items-center mb-8 gap-4">
          <Link href="/dashboard" className="text-gray-500 hover:text-gray-900 dark:hover:text-white">
            <ArrowLeft size={24} />
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Chat History</h1>
        </header>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 divide-y divide-gray-100 dark:divide-gray-700">
          <div className="p-6 text-center text-gray-500 dark:text-gray-400">
            No previous chats found.
          </div>
        </div>
      </div>
    </div>
  );
}
