import { Routes, Route, Navigate } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Topbar from "../components/layout/Topbar";

import DashboardPage from "../pages/Dashboard/DashboardPage";

import ClassificationPage from "../pages/ML/ClassificationPage";
import RecommendationPage from "../pages/ML/RecommendationPage";
import PublicationPage from "../pages/ML/PublicationPage";
import MLChatPage from "../pages/ML/MLChatPage";

import AIChatPage from "../pages/AIChat/AIChatPage";

import ProfilePage from "../pages/Settings/ProfilePage";
import AppearancePage from "../pages/Settings/AppearancePage";

export default function MainLayout() {
    return (
        <div className="flex h-screen bg-slate-950 text-white">

            <Sidebar />

            <div className="flex flex-1 flex-col">

                <Topbar />

                <main className="flex-1 overflow-y-auto p-8">

                    <Routes>

                        <Route path="/" element={<DashboardPage />} />

                        <Route
                            path="/ml/classification"
                            element={<ClassificationPage />}
                        />

                        <Route
                            path="/ml/recommendation"
                            element={<RecommendationPage />}
                        />

                        <Route
                            path="/ml/publication"
                            element={<PublicationPage />}
                        />

                        <Route
                            path="/ml/chat"
                            element={<MLChatPage />}
                        />

                        <Route
                            path="/chat"
                            element={<AIChatPage />}
                        />

                        <Route
                            path="/settings/profile"
                            element={<ProfilePage />}
                        />

                        <Route
                            path="/settings/appearance"
                            element={<AppearancePage />}
                        />

                        <Route
                            path="*"
                            element={<Navigate to="/" />}
                        />

                    </Routes>

                </main>

            </div>

        </div>
    );
}