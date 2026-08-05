import ReactMarkdown from "react-markdown";

type Props = {
    role: "user" | "assistant";
    content: string;
};

export default function ChatMessage({
    role,
    content,
}: Props) {
    const isUser = role === "user";

    return (
        <div
            className={`flex ${isUser ? "justify-end" : "justify-start"
                }`}
        >
            <div
                className={`max-w-3xl rounded-xl p-4 ${isUser
                        ? "bg-indigo-600 text-white"
                        : "bg-slate-800 text-slate-200"
                    }`}
            >
                <ReactMarkdown>
                    {content}
                </ReactMarkdown>
            </div>
        </div>
    );
}