import { useState } from "react";
import { Monitor, Moon, Sun } from "lucide-react";

type Theme = "dark" | "light" | "system";

export default function AppearancePage() {

    const [theme, setTheme] = useState<Theme>("dark");

    return (
        <div className="h-full overflow-y-auto bg-slate-950 p-6">

            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white">
                    Appearance
                </h1>

                <p className="mt-2 text-slate-400">
                    Customize how ResearchAI looks.
                </p>
            </div>

            <div className="max-w-2xl rounded-xl border border-slate-800 bg-slate-900 p-6">

                <h2 className="mb-5 font-semibold text-white">
                    Theme
                </h2>

                <div className="grid gap-3">

                    <ThemeOption
                        title="Dark"
                        description="Use the dark interface."
                        icon={<Moon size={18} />}
                        selected={theme === "dark"}
                        onClick={() => setTheme("dark")}
                    />

                    <ThemeOption
                        title="Light"
                        description="Use the light interface."
                        icon={<Sun size={18} />}
                        selected={theme === "light"}
                        onClick={() => setTheme("light")}
                    />

                    <ThemeOption
                        title="System"
                        description="Follow your system preference."
                        icon={<Monitor size={18} />}
                        selected={theme === "system"}
                        onClick={() => setTheme("system")}
                    />

                </div>

            </div>

        </div>
    );
}

function ThemeOption({
    title,
    description,
    icon,
    selected,
    onClick,
}: {
    title: string;
    description: string;
    icon: React.ReactNode;
    selected: boolean;
    onClick: () => void;
}) {
    return (
        <button
            onClick={onClick}
            className={`flex w-full items-center gap-4 rounded-lg border p-4 text-left transition ${selected
                    ? "border-indigo-500 bg-indigo-500/10"
                    : "border-slate-800 bg-slate-950 hover:border-slate-700"
                }`}
        >
            <div className="text-indigo-400">
                {icon}
            </div>

            <div className="flex-1">
                <p className="font-medium text-white">
                    {title}
                </p>

                <p className="text-sm text-slate-400">
                    {description}
                </p>
            </div>

            {selected && (
                <div className="text-xs font-medium text-indigo-400">
                    Selected
                </div>
            )}
        </button>
    );
}