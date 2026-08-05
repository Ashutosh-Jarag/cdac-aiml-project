import { useEffect, useRef, useState } from "react";

import {
    deleteSession,
    getHistory,
    getSessions,
    renameSession,
    sendMessage,
    summarizeChat,
    uploadDocument,
} from "../../api/ai";

import ChatSidebar from "../../components/chat/ChatSidebar";
import ChatInput from "../../components/chat/ChatInput";
import ChatMessage from "../../components/chat/ChatMessage";
import UploadButton from "../../components/chat/UploadButton";
import ReferenceSidebar from "../../components/chat/ReferenceSidebar";
import TypingIndicator from "../../components/chat/TypingIndicator";
import SummaryPanel from "../../components/chat/SummaryPanel";

type Message = {
    role: "user" | "assistant";
    content: string;
};

type Session = {
    id: string;
    title: string;
};

type Reference = {
    page: number;
    text: string;
};

export default function AIChatPage() {
    const [sessions, setSessions] = useState<Session[]>([]);
    const [selectedSession, setSelectedSession] = useState<string | null>(null);
    const [referenceOpen, setReferenceOpen] = useState(true);
    const [messages, setMessages] = useState<Message[]>([]);
    const [references, setReferences] = useState<Reference[]>([]);
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState("");
    const [error, setError] = useState("");
    const [uploading, setUploading] = useState(false);

    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        loadSessions();
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages]);

    async function loadSessions() {
        const res = await getSessions();
        setSessions(res.data);

        if (res.data.length && !selectedSession) {
            loadHistory(res.data[0].id);
        }
    }

    async function loadHistory(sessionId: string) {
        setSelectedSession(sessionId);
        setError("");
        setSummary("");
        const res = await getHistory(sessionId);
        setMessages(res.data);
    }

    async function handleUpload(file: File) {
        try {
            setUploading(true);
            const res = await uploadDocument(file);
            await loadSessions();
            await loadHistory(res.data.session_id);
        } catch {
            setError("Upload failed.");
        } finally {
            setUploading(false);
        }
    }

    async function handleSend(message: string) {
        if (!selectedSession) {
            alert("Upload a document first.");
            return;
        }

        try {
            setLoading(true);
            setError("");

            setMessages((prev) => [
                ...prev,
                {
                    role: "user",
                    content: message,
                },
            ]);

            const res = await sendMessage(selectedSession, message);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: res.data.answer,
                },
            ]);

            setReferences(res.data.references || []);
        } catch {
            setError("Unable to generate response.");
        } finally {
            setLoading(false);
        }
    }

    async function handleRename(id: string) {
        const title = prompt("Rename chat");
        if (!title) return;

        await renameSession(id, title);
        loadSessions();
    }

    async function handleDelete(id: string) {
        if (!confirm("Delete chat?")) return;

        await deleteSession(id);
        setMessages([]);
        setSelectedSession(null);
        loadSessions();
    }

    async function handleSummary() {
        if (!selectedSession) return;

        const res = await summarizeChat(selectedSession, "short");

        setSummary(res.data.summary);
    }

    return (
        <div className="flex h-full">
            <ChatSidebar
                sessions={sessions}
                selectedSession={selectedSession}
                onSelect={loadHistory}
                onRename={handleRename}
                onDelete={handleDelete}
                onNewChat={() => {
                    alert("Upload a document to create a new chat.");
                }}
            />

            <div className="flex flex-1 overflow-hidden">
                <div className="flex flex-1 flex-col overflow-hidden">
                    <div className="flex items-center justify-between border-b border-slate-800 p-4">
                        <h2 className="text-xl font-semibold">
                            {sessions.find((s) => s.id === selectedSession)?.title ||
                                "AI Chat"}
                        </h2>

                        <div className="flex items-center gap-3">
                            {uploading && <span>Uploading...</span>}

                            <button
                                onClick={handleSummary}
                                className="rounded bg-slate-700 px-4 py-2"
                            >
                                Summary
                            </button>

                            <UploadButton onUpload={handleUpload} />
                        </div>
                    </div>

                    <div className="flex-1 overflow-y-auto space-y-4 p-6">
                        <SummaryPanel summary={summary} />

                        {error && (
                            <div className="m-4 rounded bg-red-800 p-3">{error}</div>
                        )}

                        {!messages.length && !summary && (
                            <div className="mt-40 text-center text-slate-400">
                                Upload a document to begin chatting.
                            </div>
                        )}

                        {messages.map((msg, i) => (
                            <ChatMessage
                                key={i}
                                role={msg.role}
                                content={msg.content}
                            />
                        ))}

                        {loading && <TypingIndicator />}
                        <div ref={bottomRef} />
                    </div>

                    <ChatInput onSend={handleSend} />
                </div>

                <ReferenceSidebar
                    references={references}
                    open={referenceOpen}
                    onToggle={() => setReferenceOpen(!referenceOpen)}
                />
            </div>
        </div>
    );
}