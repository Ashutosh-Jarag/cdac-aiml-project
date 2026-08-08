import { useState } from "react";
import { RefreshCw, Send } from "lucide-react";
import client from "../../api/client";

type Message = {
    role: "user" | "assistant";
    content: string;
};

export default function MLChatPage() {

    const [messages, setMessages] = useState<Message[]>([]);
    const [question, setQuestion] = useState("");
    const [loading, setLoading] = useState(false);

    const handleRefresh = () => {
        setMessages([]);
        setQuestion("");
    };

    const handleSend = async () => {

        if (!question.trim() || loading) {
            return;
        }

        const userQuestion = question.trim();

        setMessages((prev) => [
            ...prev,
            {
                role: "user",
                content: userQuestion,
            },
        ]);

        setQuestion("");
        setLoading(true);

        try {

            const response = await client.post(
                "/ml/chat",
                {
                    question: userQuestion,
                }
            );

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content:
                        response.data.data.answer,
                },
            ]);

        } catch (error) {

            console.error(error);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content:
                        "Unable to generate a response.",
                },
            ]);

        } finally {

            setLoading(false);

        }
    };

    return (
        <div className="flex h-full flex-col">

            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-800 p-4">

                <div>
                    <h2 className="text-xl font-semibold">
                        ML Research Chat
                    </h2>

                    <p className="text-xs text-slate-400">
                        Chat with the research paper dataset
                    </p>
                </div>

                <button
                    onClick={handleRefresh}
                    className="flex items-center gap-2 rounded-lg bg-slate-700 px-4 py-2 text-sm hover:bg-slate-600"
                >
                    <RefreshCw size={16} />
                    Refresh Chat
                </button>

            </div>


            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6">

                {!messages.length && (
                    <div className="mt-40 text-center text-slate-400">

                        <h3 className="mb-2 text-lg font-semibold">
                            ML Research Chat
                        </h3>

                        <p>
                            Ask questions about research papers
                            from the arXiv dataset.
                        </p>

                    </div>
                )}

                <div className="mx-auto max-w-4xl space-y-4">

                    {messages.map((message, index) => (

                        <div
                            key={index}
                            className={`flex ${message.role === "user"
                                    ? "justify-end"
                                    : "justify-start"
                                }`}
                        >

                            <div
                                className={`max-w-[75%] rounded-xl px-4 py-3 ${message.role === "user"
                                        ? "bg-indigo-600 text-white"
                                        : "bg-slate-800 text-slate-200"
                                    }`}
                            >
                                {message.content}
                            </div>

                        </div>

                    ))}

                    {loading && (
                        <div className="text-sm text-slate-400">
                            Searching research papers...
                        </div>
                    )}

                </div>

            </div>


            {/* Input */}
            <div className="border-t border-slate-800 p-4">

                <div className="mx-auto flex max-w-4xl gap-3">

                    <input
                        value={question}
                        onChange={(e) =>
                            setQuestion(e.target.value)
                        }
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                handleSend();
                            }
                        }}
                        placeholder="Ask about research papers..."
                        className="flex-1 rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm outline-none focus:border-indigo-500"
                    />

                    <button
                        onClick={handleSend}
                        disabled={loading || !question.trim()}
                        className="rounded-lg bg-indigo-600 px-5 py-3 text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        <Send size={18} />
                    </button>

                </div>

            </div>

        </div>
    );
}