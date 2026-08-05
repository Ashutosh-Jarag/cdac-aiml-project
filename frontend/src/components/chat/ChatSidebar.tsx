import { Plus, Trash2, Pencil } from "lucide-react";

type Session = {
    id: string;
    title: string;
};

type Props = {
    sessions: Session[];
    selectedSession: string | null;
    onSelect: (id: string) => void;
    onNewChat: () => void;
    onRename: (id: string) => void;
    onDelete: (id: string) => void;
};

export default function ChatSidebar({
    sessions,
    selectedSession,
    onSelect,
    onNewChat,
    onRename,
    onDelete,
}: Props) {
    return (
        <aside className="flex w-72 flex-col border-r border-slate-800 bg-slate-900">

            <div className="p-4">

                <button
                    onClick={onNewChat}
                    className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 py-3 hover:bg-indigo-500"
                >
                    <Plus size={18} />
                    New Chat
                </button>

            </div>

            <div className="flex-1 overflow-y-auto">

                {sessions.map((chat) => (

                    <div
                        key={chat.id}
                        className={`group flex items-center justify-between px-4 py-3 cursor-pointer transition ${selectedSession === chat.id
                                ? "bg-slate-800"
                                : "hover:bg-slate-800/60"
                            }`}
                        onClick={() => onSelect(chat.id)}
                    >

                        <span className="truncate">

                            {chat.title}

                        </span>

                        <div className="hidden gap-2 group-hover:flex">

                            <Pencil
                                size={15}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    onRename(chat.id);
                                }}
                            />

                            <Trash2
                                size={15}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    onDelete(chat.id);
                                }}
                            />

                        </div>

                    </div>

                ))}

            </div>

        </aside>
    );
}