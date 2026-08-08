import { useState } from "react";
import { NavLink } from "react-router-dom";

import {
    LayoutDashboard,
    BrainCircuit,
    Bot,
    Settings,
    ChevronDown,
    ChevronRight,
} from "lucide-react";

export default function Sidebar() {
    const [mlOpen, setMlOpen] = useState(true);
    const [settingsOpen, setSettingsOpen] = useState(false);

    return (
        <aside className="flex w-72 flex-col border-r border-slate-800 bg-slate-900">

            <div className="border-b border-slate-800 p-6">

                <h1 className="text-2xl font-bold text-indigo-400">
                    ResearchAI
                </h1>

            </div>

            <nav className="flex-1 overflow-y-auto p-4 space-y-2">

                <NavLink
                    to="/"
                    className="flex items-center gap-3 rounded-lg px-4 py-3 hover:bg-slate-800"
                >
                    <LayoutDashboard size={20} />
                    Dashboard
                </NavLink>

                <button
                    onClick={() => setMlOpen(!mlOpen)}
                    className="flex w-full items-center justify-between rounded-lg px-4 py-3 hover:bg-slate-800"
                >
                    <div className="flex items-center gap-3">
                        <BrainCircuit size={20} />
                        Machine Learning
                    </div>

                    {mlOpen ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                </button>

                {mlOpen && (
                    <div className="ml-10 flex flex-col">

                        <NavLink to="/ml/classification" className="py-2 text-sm hover:text-indigo-400">
                            Classification
                        </NavLink>

                        <NavLink to="/ml/recommendation" className="py-2 text-sm hover:text-indigo-400">
                            Recommendation
                        </NavLink>

                        <NavLink to="/ml/publication" className="py-2 text-sm hover:text-indigo-400">
                            Publication
                        </NavLink>

                        <NavLink to="/ml/chat" className="py-2 text-sm hover:text-indigo-400">
                            ML Chat
                        </NavLink>

                    </div>
                )}

                <NavLink
                    to="/chat"
                    className="flex items-center gap-3 rounded-lg px-4 py-3 hover:bg-slate-800"
                >
                    <Bot size={20} />
                    AI Chat
                </NavLink>

            </nav>

            <div className="border-t border-slate-800 p-4">

                <button
                    onClick={() => setSettingsOpen(!settingsOpen)}
                    className="flex w-full items-center justify-between rounded-lg px-4 py-3 hover:bg-slate-800"
                >
                    <div className="flex items-center gap-3">
                        <Settings size={20} />
                        Settings
                    </div>

                    {settingsOpen ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                </button>

                {settingsOpen && (
                    <div className="ml-10 mt-2 flex flex-col">

                        <NavLink to="/settings/profile" className="py-2 text-sm hover:text-indigo-400">
                            Profile
                        </NavLink>

                        <NavLink to="/settings/appearance" className="py-2 text-sm hover:text-indigo-400">
                            Appearance
                        </NavLink>

                    </div>
                )}

            </div>

        </aside>
    );
}