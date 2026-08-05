import { ChevronLeft, ChevronRight, FileText } from "lucide-react";

type Reference = {
    page: number;
    text: string;
};

type ReferenceSidebarProps = {
    references: Reference[];
    open: boolean;
    onToggle: () => void;
};

export default function ReferenceSidebar({
    references,
    open,
    onToggle,
}: ReferenceSidebarProps) {
    if (!open) {
        return (
            <div className="border-l border-slate-800 bg-slate-900/50 p-2">
                <button
                    onClick={onToggle}
                    className="rounded-lg p-2 hover:bg-slate-800 text-slate-400 hover:text-white"
                    title="Open References"
                >
                    <ChevronLeft size={20} />
                </button>
            </div>
        );
    }

    return (
        <aside className="w-80 flex-col border-l border-slate-800 bg-slate-900/50 flex">
            <div className="flex items-center justify-between border-b border-slate-800 p-4">
                <div className="flex items-center gap-2 font-semibold">
                    <FileText size={18} className="text-indigo-400" />
                    <span>References</span>
                </div>
                <button
                    onClick={onToggle}
                    className="rounded-lg p-1.5 hover:bg-slate-800 text-slate-400 hover:text-white"
                    title="Collapse References"
                >
                    <ChevronRight size={18} />
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {!references.length ? (
                    <div className="text-center text-sm text-slate-500 mt-10">
                        No references for this message.
                    </div>
                ) : (
                    references.map((ref, i) => (
                        <div
                            key={i}
                            className="rounded-lg border border-slate-800 bg-slate-900 p-3 space-y-2 text-xs"
                        >
                            <div className="font-semibold text-indigo-400">
                                Page {ref.page}
                            </div>
                            <p className="text-slate-300 leading-relaxed">
                                {ref.text.length > 250
                                    ? `${ref.text.substring(0, 250)}...`
                                    : ref.text}
                            </p>
                        </div>
                    ))
                )}
            </div>
        </aside>
    );
}