import { useState } from "react";
import { Send } from "lucide-react";

type Props = {
    onSend: (message: string) => void;
};

export default function ChatInput({
    onSend,
}: Props) {
    const [message, setMessage] = useState("");

    const send = () => {
        if (!message.trim()) return;

        onSend(message);

        setMessage("");
    };

    return (
        <div className="flex items-center gap-3 border-t border-slate-800 p-4">

            <input
                className="flex-1 rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 outline-none"
                placeholder="Ask something..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") send();
                }}
            />

            <button
                onClick={send}
                className="rounded-lg bg-indigo-600 p-3 hover:bg-indigo-500"
            >
                <Send size={18} />
            </button>

        </div>
    );
}