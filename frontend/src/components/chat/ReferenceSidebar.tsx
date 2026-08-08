import { ChevronLeft, ChevronRight, FileText, Tag, BookOpen } from "lucide-react";

type Reference = {
    page: number;
    text: string;
};

type Recommendation = {
    id: string;
    title: string;
    authors: string;
    category: string;
    similarity: number;
    update_date: string;
};

interface Props {
    references: Reference[];
    open: boolean;
    onToggle: () => void;

    classification?: {
        code: string;
        name: string;
    } | null;

    recommendations?: Recommendation[];

    webResources?: {
        title: string;
        url: string;
    }[];
}

export default function ReferenceSidebar({
    references,
    open,
    onToggle,
    classification,
    recommendations = [],
    webResources = [],
}: Props) {
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
                {/* Document Insights Block */}
                {classification && (
                    <div className="mb-6 rounded-lg bg-slate-800/80 border border-slate-700/50 p-4 space-y-2">
                        <div className="flex items-center gap-2 font-semibold text-slate-200">
                            <Tag size={16} className="text-indigo-400" />
                            <h3>Document Insights</h3>
                        </div>

                        <div className="text-xs space-y-0.5">
                            <p className="text-slate-400 font-medium">Category</p>
                            <p className="text-sm font-semibold text-slate-100">
                                {classification.name}
                            </p>
                            <p className="text-xs text-indigo-400 font-mono">
                                [{classification.code}]
                            </p>
                        </div>
                    </div>
                )}

                {/* Recommended Papers Block */}
                {recommendations.length > 0 && (
                    <div className="mb-6 space-y-3">
                        <div className="flex items-center gap-2 font-semibold text-slate-200">
                            <BookOpen size={16} className="text-indigo-400" />
                            <h3>Recommended Papers</h3>
                        </div>

                        {recommendations.map((paper) => (
                            <div
                                key={paper.id}
                                className="rounded-lg border border-slate-800 bg-slate-900 p-3 space-y-2"
                            >
                                <h4 className="text-sm font-semibold text-slate-100 leading-snug">
                                    {paper.title}
                                </h4>

                                <p className="text-xs text-slate-400">
                                    {paper.authors}
                                </p>

                                <div className="flex items-center justify-between text-xs font-medium">
                                    <span className="text-indigo-400">
                                        {paper.category}
                                    </span>

                                    <span className="text-emerald-400">
                                        {paper.similarity}% match
                                    </span>
                                </div>

                                <p className="text-xs text-slate-500">
                                    Updated: {paper.update_date}
                                </p>

                                <a
                                    href={`https://arxiv.org/abs/${paper.id}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-block text-xs font-medium text-indigo-400 hover:text-indigo-300 hover:underline"
                                >
                                    View Paper →
                                </a>
                            </div>
                        ))}
                    </div>
                )}

                {/* Web Resources Block */}
                {webResources.length > 0 && (
                    <div className="mb-6 space-y-3">
                        <div className="flex items-center gap-2 font-semibold text-slate-200">
                            <Tag size={16} className="text-indigo-400" />
                            <h3>Web Resources</h3>
                        </div>

                        {webResources.map((resource, index) => (
                            <a
                                key={index}
                                href={resource.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="block rounded-lg border border-slate-800 bg-slate-900 p-3 text-sm text-indigo-400 hover:bg-slate-800"
                            >
                                {resource.title}
                                <span className="ml-1">↗</span>
                            </a>
                        ))}
                    </div>
                )}

                {/* References List */}
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